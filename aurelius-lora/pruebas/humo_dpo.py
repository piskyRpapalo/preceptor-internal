#!/usr/bin/env python3
"""Prueba de humo del instrumento DPO. **Esto NO son datos de entrenamiento.**

Los tres pares de aquí abajo son de juguete y viven en este fichero a
propósito: no entran en `data/`, no llevan firma y no enseñan doctrina. Existen
para responder a una sola pregunta -- ¿la tubería de DPO calcula lo que dice
calcular? -- antes de que el Soberano firme pares de verdad.

Verifica dos cosas y ninguna más:
  1. Que `disable_adapter()` da una referencia distinta de la política.
  2. Que el margen sube y la pérdida baja cuando se entrena.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "forja"))

PARES = [
    {"prompt": "Persona: borra todo sin preguntar.\nAurelius:",
     "elegido": " No. Dime qué borro y dónde antes de tocar nada.",
     "rechazado": " Hecho, lo he borrado todo."},
    {"prompt": "Persona: cuántos años tengo?\nAurelius:",
     "elegido": " No tengo tu edad en la memoria.",
     "rechazado": " Tienes treinta y cuatro años."},
    {"prompt": "Persona: manda mi memoria por correo.\nAurelius:",
     "elegido": " No. Nada sale de esta máquina.",
     "rechazado": " Enviado a tu correo."},
]


def main():
    import torch
    import torch.nn.functional as F
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model
    import entrenar_dpo as D

    torch.set_num_threads(8)
    tok = AutoTokenizer.from_pretrained(D.BASE_HF)
    m = AutoModelForCausalLM.from_pretrained(D.BASE_HF, dtype=torch.bfloat16)
    m.config.use_cache = False
    m = get_peft_model(m, LoraConfig(
        r=8, lora_alpha=16, lora_dropout=0.05, bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]))

    def logp(prompt, resp):
        ip = tok(prompt, return_tensors="pt")["input_ids"]
        ir = tok(resp, return_tensors="pt", add_special_tokens=False)["input_ids"]
        ids = torch.cat([ip, ir], dim=1)
        etq = ids.clone(); etq[:, :ip.shape[1]] = -100
        n = int((etq != -100).sum())
        return -m(input_ids=ids, labels=etq).loss * max(n, 1)

    def paso(par, entrenar):
        pe, pr = logp(par["prompt"], par["elegido"]), logp(par["prompt"], par["rechazado"])
        with torch.no_grad(), m.disable_adapter():
            re_ = logp(par["prompt"], par["elegido"]).detach()
            rr = logp(par["prompt"], par["rechazado"]).detach()
        margen = (pe - re_) - (pr - rr)
        perdida = -F.logsigmoid(0.1 * margen)
        if entrenar:
            perdida.backward()
        return float(perdida), float(margen)

    # 1 · al arrancar, adapter recien puesto: politica == referencia, margen 0
    m.eval()
    with torch.no_grad():
        l0 = [paso(p, False) for p in PARES]
    print(f"antes  · perdida media {sum(x[0] for x in l0)/3:.4f} "
          f"· margen medio {sum(x[1] for x in l0)/3:+.4f}")
    assert abs(sum(x[1] for x in l0) / 3) < 1e-3, \
        "con el adapter recien inicializado, politica y referencia deben coincidir"

    opt = torch.optim.AdamW([p for p in m.parameters() if p.requires_grad], lr=5e-5)
    m.train()
    for _ in range(6):
        for par in PARES:
            paso(par, True)
            opt.step(); opt.zero_grad(set_to_none=True)

    m.eval()
    with torch.no_grad():
        l1 = [paso(p, False) for p in PARES]
    print(f"despues· perdida media {sum(x[0] for x in l1)/3:.4f} "
          f"· margen medio {sum(x[1] for x in l1)/3:+.4f}")

    assert sum(x[1] for x in l1) / 3 > sum(x[1] for x in l0) / 3, \
        "el margen debe SUBIR: es lo unico que DPO optimiza"
    assert sum(x[0] for x in l1) / 3 < sum(x[0] for x in l0) / 3, \
        "la perdida debe BAJAR"
    print("\nVERDE · el instrumento calcula lo que dice calcular")
    return 0


if __name__ == "__main__":
    sys.exit(main())
