#!/usr/bin/env python3
"""FASE 0 · el mini-run de verdad · PEFT + transformers sobre torch-CPU.

Responde a UNA pregunta y la escribe con fecha: ¿este metal entrena LoRA sobre
Qwen3-4B, y a qué ritmo? No extrapola desde un modelo pequeño -- una cifra sin
su máquina y sin su modelo es un rumor con decimales.

Deja `salida/loss.jsonl` con una línea por paso, que es justo lo que la Fase 5
sabe leer. El instrumento de medida alimenta al guardián de salud sin adaptador.

Solo se ejecuta con `--ejecutar`.
"""
from __future__ import annotations

import argparse
import json
import os
import resource
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE = "Qwen/Qwen3-4B-Instruct-2507"
SALIDA = RAIZ / "salida"


def formatear(reg):
    """Un registro del dataset a texto plano. Los negativos NO entran aquí.

    Un negativo enseña por preferencia (elegido vs rechazado), no por
    imitación: meterlo en un entrenamiento causal enseñaría exactamente la
    forma que se quiere evitar. Se filtran, y se dice que se filtran.
    """
    if reg.get("clase") != "canon":
        return None
    partes = [m.get("contenido", "") for m in reg.get("mensajes", [])]
    texto = "\n".join(p for p in partes if p).strip()
    return texto or None


def main(argv=None):
    ap = argparse.ArgumentParser(description="FASE 0 · mini-run PEFT/CPU")
    ap.add_argument("--pasos", type=int, default=100)
    ap.add_argument("--max-len", type=int, default=512)
    ap.add_argument("--hilos", type=int, default=8)
    ap.add_argument("--dataset", type=Path, default=RAIZ / "data" / "lora_dataset.jsonl")
    ap.add_argument("--ejecutar", action="store_true")
    a = ap.parse_args(argv)

    if not a.ejecutar:
        print(f"[minirun] CERROJO: {a.pasos} pasos sobre {BASE}. Añade --ejecutar")
        return 0

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model

    torch.set_num_threads(a.hilos)
    t_inicio = time.time()
    print(f"[minirun] torch {torch.__version__} · {a.hilos} hilos · bf16")
    print(f"[minirun] base: {BASE}")

    tok = AutoTokenizer.from_pretrained(BASE)
    t_tok = time.time()
    modelo = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.bfloat16)
    modelo.config.use_cache = False
    t_carga = time.time()
    print(f"[minirun] cargado en {t_carga - t_tok:.1f}s")

    cfg = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, bias="none",
                     task_type="CAUSAL_LM",
                     target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
    modelo = get_peft_model(modelo, cfg)
    entrenables = sum(p.numel() for p in modelo.parameters() if p.requires_grad)
    total = sum(p.numel() for p in modelo.parameters())
    print(f"[minirun] LoRA: {entrenables:,} de {total:,} parámetros "
          f"({100*entrenables/total:.3f} %)")

    textos = []
    descartados = 0
    for linea in a.dataset.open(encoding="utf-8"):
        linea = linea.strip()
        if not linea:
            continue
        t = formatear(json.loads(linea))
        if t:
            textos.append(t)
        else:
            descartados += 1
    print(f"[minirun] {len(textos)} textos · {descartados} no-canon filtrados")
    if not textos:
        print("[minirun] sin textos. Paro.", file=sys.stderr)
        return 2

    opt = torch.optim.AdamW([p for p in modelo.parameters() if p.requires_grad], lr=2e-4)
    modelo.train()
    SALIDA.mkdir(parents=True, exist_ok=True)
    bitacora = SALIDA / "loss.jsonl"
    tiempos, perdidas = [], []

    with bitacora.open("w", encoding="utf-8") as fh:
        for paso in range(1, a.pasos + 1):
            texto = textos[(paso - 1) % len(textos)]
            lote = tok(texto, return_tensors="pt", truncation=True,
                       max_length=a.max_len)
            lote["labels"] = lote["input_ids"].clone()

            t0 = time.time()
            salida = modelo(**lote)
            salida.loss.backward()
            opt.step()
            opt.zero_grad(set_to_none=True)
            dt = time.time() - t0

            perdida = float(salida.loss.item())
            tiempos.append(dt)
            perdidas.append(perdida)
            fh.write(json.dumps({"paso": paso, "loss": perdida,
                                 "segundos": round(dt, 3)}) + "\n")
            fh.flush()
            if paso <= 3 or paso % 10 == 0:
                print(f"  paso {paso:3d}/{a.pasos} · loss {perdida:.4f} · {dt:.2f}s",
                      flush=True)

    pico = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 2)
    medio = sum(tiempos) / len(tiempos)
    veredicto = {
        "fecha": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "entrenador": "peft+transformers/torch-cpu",
        "torch": torch.__version__,
        "base": BASE,
        "metal": "Ryzen 7 255 · 8 núcleos · sin GPU · bf16",
        "pasos": a.pasos,
        "seg_por_paso_medio": round(medio, 3),
        "seg_por_paso_mediana": round(sorted(tiempos)[len(tiempos) // 2], 3),
        "total_entrenamiento_s": round(sum(tiempos), 1),
        "carga_modelo_s": round(t_carga - t_tok, 1),
        "total_pared_s": round(time.time() - t_inicio, 1),
        "loss_primera": round(perdidas[0], 4),
        "loss_ultima": round(perdidas[-1], 4),
        "ram_pico_GiB": round(pico, 2),
        "parametros_entrenables": entrenables,
    }
    (RAIZ / "FASE0_MINIRUN.json").write_text(
        json.dumps(veredicto, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n[minirun] VEREDICTO")
    for k, v in veredicto.items():
        print(f"  {k:24s} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
