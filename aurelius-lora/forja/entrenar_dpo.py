#!/usr/bin/env python3
"""FASE 2-bis · DPO sobre pares de preferencia · enseñar a NEGARSE.

POR QUÉ EXISTE
--------------
Medido el 2026-08-21: el canon enseña a declarar ausencias y no tiene ni un
ejemplo de negarse a lo que se le pide. Los cinco edge cases que fallan son
justo los que exigen un no; los siete que pasan, los que exigen declarar. Por
eso EC-2.4 aguanta con r=8 y con r=4: no es capacidad, es que nadie se lo
enseñó.

Un paso causal no puede enseñarlo -- aprendería a CONTINUAR el texto malo. La
preferencia sí: se le dan las dos respuestas y se le enseña cuál prefiere.

EL MODELO DE REFERENCIA NO SE CARGA DOS VECES
---------------------------------------------
DPO compara la política contra una referencia congelada. Lo obvio sería cargar
dos modelos de 4B -- 16 GB en bf16. No hace falta: con un adapter, la
referencia **es el mismo modelo con el adapter apagado**. `disable_adapter()`
da exactamente eso, y el pico se queda en ~9 GiB.

CERROJO: `--ejecutar`, y pares COMPLETOS. Ver `revisar_pares`.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATASET = RAIZ / "data" / "lora_dataset.jsonl"
SALIDA = RAIZ / "salida"
BASE_HF = "Qwen/Qwen3-4B-Instruct-2507"

HIPER = {
    "rank": 8, "alpha": 16, "dropout": 0.05,
    "lr": 5e-6,          # DPO va con paso corto: mueve preferencia, no estilo
    "beta": 0.1,         # cuánto se le deja alejarse de la referencia
    "epocas": 1,
    "validacion": 0.20,
    "max_len": 512,
    "objetivo": ["q_proj", "k_proj", "v_proj", "o_proj"],
}

CLASES = ("preferencia", "negativo")


def cargar_pares(ruta):
    """Devuelve (completos, mancos). Un manco es media pieza, y se dice."""
    completos, mancos = [], []
    for linea in ruta.open(encoding="utf-8"):
        linea = linea.strip()
        if not linea:
            continue
        r = json.loads(linea)
        if r.get("clase") not in CLASES:
            continue
        elegido = (r.get("elegido") or "").strip()
        rechazado = (r.get("rechazado") or "").strip()
        prompt = (r.get("prompt") or "").strip()
        if elegido and rechazado and prompt:
            completos.append({"id": r["id"], "idioma": r.get("idioma", "?"),
                              "prompt": prompt, "elegido": elegido,
                              "rechazado": rechazado})
        else:
            falta = [k for k, v in (("prompt", prompt), ("elegido", elegido),
                                    ("rechazado", rechazado)) if not v]
            mancos.append({"id": r["id"], "falta": falta})
    return completos, mancos


def revisar_pares(completos, mancos):
    """DPO sobre medio par no es DPO: es entrenar contra el vacío.

    Se para en vez de rellenar. Escribir aquí la respuesta que 'debería' haber
    dado el modelo sería inventarse la doctrina de otro y llamarlo dato.
    """
    if mancos and not completos:
        return [f"los {len(mancos)} pares de preferencia están MANCOS: "
                f"tienen `rechazado` y no `elegido`. DPO necesita las dos "
                f"mitades y no las escribo yo."]
    if mancos:
        return [f"{len(mancos)} pares mancos de {len(mancos)+len(completos)}: "
                f"se entrenaría con un subconjunto silencioso. Complétalos o "
                f"decláralos fuera."]
    if not completos:
        return ["no hay ni un par de preferencia en el dataset."]
    return []


def partir(pares, fraccion):
    """Mismo corte estratificado por idioma que la Fase 2."""
    val, tren = [], []
    for idioma in ("en", "es"):
        de_ese = [p for p in pares if p["idioma"] == idioma]
        corte = max(1, round(len(de_ese) * fraccion)) if de_ese else 0
        for i, p in enumerate(de_ese):
            (val if i < corte else tren).append(p)
    tren += [p for p in pares if p["idioma"] not in ("en", "es")]
    return tren, val


def main(argv=None):
    ap = argparse.ArgumentParser(description="FASE 2-bis · DPO")
    ap.add_argument("--ejecutar", action="store_true")
    ap.add_argument("--version", default="dpo-v1")
    ap.add_argument("--desde", type=Path,
                    help="adapter de partida; sin esto, DPO desde el base")
    ap.add_argument("--hilos", type=int, default=8)
    a = ap.parse_args(argv)

    if not DATASET.is_file():
        print(f"[dpo] NO_DATA · no existe {DATASET}", file=sys.stderr)
        return 2

    completos, mancos = cargar_pares(DATASET)
    faltas = revisar_pares(completos, mancos)
    print(f"[dpo] pares completos: {len(completos)} · mancos: {len(mancos)}")
    for m in mancos[:4]:
        print(f"    manco {m['id']}  falta: {', '.join(m['falta'])}")
    if len(mancos) > 4:
        print(f"    … y {len(mancos)-4} más")
    for f in faltas:
        print(f"[dpo] BLOQUEADO · {f}")

    if not a.ejecutar:
        print("[dpo] CERROJO: no se entrena. Añade --ejecutar")
        return 0
    if faltas:
        print("[dpo] no entreno con medio par. Paro.", file=sys.stderr)
        return 2

    import torch
    import torch.nn.functional as F
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import (LoraConfig, get_peft_model, PeftModel,
                      get_peft_model_state_dict, set_peft_model_state_dict)
    import copy

    torch.set_num_threads(a.hilos)
    tok = AutoTokenizer.from_pretrained(BASE_HF)
    modelo = AutoModelForCausalLM.from_pretrained(BASE_HF, dtype=torch.bfloat16)
    modelo.config.use_cache = False
    if a.desde:
        modelo = PeftModel.from_pretrained(modelo, str(a.desde),
                                           is_trainable=True)
    else:
        modelo = get_peft_model(modelo, LoraConfig(
            r=HIPER["rank"], lora_alpha=HIPER["alpha"],
            lora_dropout=HIPER["dropout"], bias="none", task_type="CAUSAL_LM",
            target_modules=HIPER["objetivo"]))

    def logp(prompt, respuesta):
        ids_p = tok(prompt, return_tensors="pt")["input_ids"]
        ids_r = tok(respuesta, return_tensors="pt",
                    add_special_tokens=False)["input_ids"]
        ids = torch.cat([ids_p, ids_r], dim=1)[:, :HIPER["max_len"]]
        etq = ids.clone()
        etq[:, :ids_p.shape[1]] = -100
        n = int((etq != -100).sum())
        salida = modelo(input_ids=ids, labels=etq)
        return -salida.loss * max(n, 1)          # log-prob total de la respuesta

    def perdida(par):
        pe = logp(par["prompt"], par["elegido"])
        pr = logp(par["prompt"], par["rechazado"])
        with torch.no_grad(), modelo.disable_adapter():
            re_ = logp(par["prompt"], par["elegido"]).detach()
            rr = logp(par["prompt"], par["rechazado"]).detach()
        margen = (pe - re_) - (pr - rr)
        return -F.logsigmoid(HIPER["beta"] * margen), float(margen)

    tren, val = partir(completos, HIPER["validacion"])
    print(f"[dpo] tren {len(tren)} · validación {len(val)}")
    if len(val) < 6:
        print(f"[dpo] AVISO: {len(val)} pares de validación no sostienen una "
              f"conclusión estadística. El juez de verdad es el tester.")

    opt = torch.optim.AdamW(
        [p for p in modelo.parameters() if p.requires_grad], lr=HIPER["lr"])
    SALIDA.mkdir(parents=True, exist_ok=True)
    bitacora = SALIDA / "dpo_loss.jsonl"
    mejor = {"val": float("inf"), "paso": 0, "pesos": None}
    historial, t0 = [], time.time()

    with bitacora.open("w", encoding="utf-8") as fh:
        for paso, par in enumerate(tren * HIPER["epocas"], 1):
            modelo.train()
            l, m = perdida(par)
            l.backward()
            opt.step()
            opt.zero_grad(set_to_none=True)
            fh.write(json.dumps({"paso": paso, "loss": float(l),
                                 "margen": m}) + "\n")

            if paso % max(1, len(tren) // 4) == 0 or paso == len(tren):
                modelo.eval()
                with torch.no_grad():
                    ls, ms = zip(*(perdida(p) for p in val)) if val else ((0,), (0,))
                vl = sum(float(x) for x in ls) / len(ls)
                acc = sum(1 for x in ms if x > 0) / len(ms)
                historial.append({"paso": paso, "train": float(l),
                                  "val": vl, "acierto_val": acc})
                fh.write(json.dumps({"paso": paso, "loss": float(l),
                                     "val_loss": vl}) + "\n")
                fh.flush()
                if vl < mejor["val"]:
                    mejor.update(val=vl, paso=paso,
                                 pesos=copy.deepcopy(get_peft_model_state_dict(modelo)))
                print(f"  paso {paso:3d} · train {float(l):.4f} · val {vl:.4f} "
                      f"· acierto {acc:.0%}"
                      + ("  ← mejor" if mejor["paso"] == paso else ""), flush=True)

    if mejor["pesos"] is None:
        print("[dpo] ninguna evaluación. Nada que guardar.", file=sys.stderr)
        return 1
    set_peft_model_state_dict(modelo, mejor["pesos"])
    destino = SALIDA / a.version
    destino.mkdir(parents=True, exist_ok=True)
    modelo.save_pretrained(str(destino))
    tok.save_pretrained(str(destino))

    (SALIDA / "dpo.json").write_text(json.dumps({
        "fecha": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "hiper": HIPER, "desde": str(a.desde) if a.desde else "base",
        "tren": len(tren), "validacion": len(val),
        "historial": historial, "mejor_paso": mejor["paso"],
        "segundos": round(time.time() - t0, 1),
        "guardado": "mejor_checkpoint",
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[dpo] guardado el paso {mejor['paso']} · adapter en {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
