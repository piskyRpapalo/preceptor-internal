#!/usr/bin/env python3
"""PLAN C · TRAINER SFT-CoT · Cadena de Pensamiento para los 6 casos ROJOS.

Cambio de paradigma: abandonamos DPO para coherencia/honestidad. SFT puro
con formato CoT: el modelo aprende a razonar antes de responder.

Hiperparámetros FIRMADOS por el Soberano el 2026-08-21:
    rank 16 · alpha 32 · lr 1e-4 · 2 épocas
    dataset: data/sft_cot.jsonl

REPLAY BUFFER (v3+): random.shuffle(tren) antes de cada época para
evitar catastrophic forgetting. El modelo ve viejos y nuevos mezclados.

CHECKPOINTS (v4+): guarda el mejor paso durante el entrenamiento,
no solo al final. Si se interrumpe, el mejor sigue disponible.

NO toca entrenar_lora.py ni sus HIPER firmados de la Fase 2.
"""
from __future__ import annotations

import argparse
import copy
import json
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import torch
from peft import LoraConfig, get_peft_model, get_peft_model_state_dict, set_peft_model_state_dict
from transformers import AutoModelForCausalLM, AutoTokenizer

RAIZ = Path(__file__).resolve().parent.parent
DATASET = RAIZ / "data" / "sft_cot.jsonl"
SALIDA = RAIZ / "salida"

BASE_HF = "Qwen/Qwen3-4B-Instruct-2507"

HIPER = {
    "rank": 16,
    "alpha": 32,
    "dropout": 0.05,
    "lr": 1e-4,
    "epocas": 2,
    "validacion": 0.15,
    "subidas_para_abortar": 2,
    "max_len": 1024,
    "cada_cuantos_evalua": 10,
    "min_tokens": 20,
    "objetivo": ["q_proj", "k_proj", "v_proj", "o_proj"],
}


def cargar(ruta):
    entrenables = []
    for linea in ruta.open(encoding="utf-8"):
        linea = linea.strip()
        if not linea:
            continue
        r = json.loads(linea)
        if r.get("clase") != "canon":
            continue
        texto = r.get("texto", "").strip()
        if texto:
            entrenables.append({"texto": texto, "idioma": r.get("idioma", "?")})
    return entrenables


def partir(muestras, fraccion):
    val, tren = [], []
    for idioma in ("en", "es"):
        de_ese = [m for m in muestras if m["idioma"] == idioma]
        corte = max(1, round(len(de_ese) * fraccion))
        paso = max(1, len(de_ese) // corte)
        elegidas = set(range(0, len(de_ese), paso))
        while len(elegidas) > corte:
            elegidas.pop()
        for i, m in enumerate(de_ese):
            (val if i in elegidas else tren).append(m)
    otros = [m for m in muestras if m["idioma"] not in ("en", "es")]
    tren.extend(otros)
    return tren, val


def main(argv=None):
    ap = argparse.ArgumentParser(description="Plan C · trainer SFT-CoT")
    ap.add_argument("--ejecutar", action="store_true")
    ap.add_argument("--dataset", type=Path, default=DATASET)
    ap.add_argument("--version", default="sft-cot-v1")
    ap.add_argument("--hilos", type=int, default=8)
    ap.add_argument("--epocas", type=int, default=HIPER["epocas"])
    ap.add_argument("--cada", type=int, default=HIPER["cada_cuantos_evalua"])
    a = ap.parse_args(argv)

    if not a.dataset.is_file():
        print(f"[sft-cot] no existe {a.dataset}")
        return 1

    muestras = cargar(a.dataset)
    tren, val = partir(muestras, HIPER["validacion"])

    print(f"[sft-cot] base: {BASE_HF} (pesos sin cuantizar, bf16)")
    print(f"[sft-cot] LoRA r={HIPER['rank']} alpha={HIPER['alpha']} "
          f"lr={HIPER['lr']} · {a.epocas} épocas · "
          f"validación {HIPER['validacion']:.0%}")
    print(f"[sft-cot] muestras: {len(muestras)} (tren {len(tren)}, val {len(val)})")

    if not a.ejecutar:
        print("[sft-cot] CERROJO: añade --ejecutar para entrenar")
        return 0

    torch.set_num_threads(a.hilos)
    tok = AutoTokenizer.from_pretrained(BASE_HF, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    tok.padding_side = "right"

    modelo = AutoModelForCausalLM.from_pretrained(
        BASE_HF, torch_dtype=torch.bfloat16, trust_remote_code=True
    )
    config = LoraConfig(
        r=HIPER["rank"], lora_alpha=HIPER["alpha"],
        lora_dropout=HIPER["dropout"], bias="none",
        task_type="CAUSAL_LM",
        target_modules=HIPER["objetivo"],
    )
    modelo = get_peft_model(modelo, config)
    entrenables = sum(p.numel() for p in modelo.parameters() if p.requires_grad)
    print(f"[sft-cot] parámetros entrenables: {entrenables:,}")

    def descartar_degeneradas(muestras):
        buenas, fuera = [], []
        for m in muestras:
            n = len(tok(m["texto"])["input_ids"])
            (buenas if n >= HIPER["min_tokens"] else fuera).append(m)
        return buenas, fuera

    tren, fuera_tren = descartar_degeneradas(tren)
    val, fuera_val = descartar_degeneradas(val)
    if fuera_tren or fuera_val:
        print(f"[sft-cot] descartadas por cortas (<{HIPER['min_tokens']} tokens): "
              f"{len(fuera_tren)} de tren, {len(fuera_val)} de validación")

    def lote_de(m):
        b = tok(m["texto"], return_tensors="pt", truncation=True,
                max_length=HIPER["max_len"])
        b["labels"] = b["input_ids"].clone()
        return b

    def perdida_validacion():
        modelo.eval()
        total = 0.0
        with torch.no_grad():
            for m in val:
                total += float(modelo(**lote_de(m)).loss.item())
        modelo.train()
        return total / max(len(val), 1)

    opt = torch.optim.AdamW(
        [p for p in modelo.parameters() if p.requires_grad], lr=HIPER["lr"])
    modelo.train()
    SALIDA.mkdir(parents=True, exist_ok=True)
    destino = SALIDA / a.version
    destino.mkdir(parents=True, exist_ok=True)
    bitacora = destino / "loss.jsonl"

    mejor = {"val": float("inf"), "paso": 0, "train": None, "pesos": None}
    t0 = time.time()

    with bitacora.open("w", encoding="utf-8") as fh:
        paso = 0
        for epoca in range(a.epocas):
            random.shuffle(tren)
            for m in tren:
                paso += 1
                salida = modelo(**lote_de(m))
                salida.loss.backward()
                opt.step()
                opt.zero_grad(set_to_none=True)
                perdida = float(salida.loss.item())
                fh.write(json.dumps({"paso": paso, "loss": perdida}) + "\n")

                if paso % a.cada == 0:
                    val_medio = perdida_validacion()
                    fh.write(json.dumps({"paso": paso, "val_loss": val_medio}) + "\n")
                    fh.flush()
                    print(f"  paso {paso:4d} · val {val_medio:.4f}"
                          + ("  ← mejor" if val_medio < mejor["val"] else ""),
                          flush=True)
                    if val_medio < mejor["val"]:
                        mejor.update(val=val_medio, paso=paso)
                        # CHECKPOINT: guardar durante entrenamiento
                        set_peft_model_state_dict(modelo, get_peft_model_state_dict(modelo))
                        modelo.save_pretrained(destino)
                        tok.save_pretrained(destino)

    print(f"[sft-cot] entrenamiento completado en {time.time()-t0:.0f}s")
    print(f"[sft-cot] mejor paso: {mejor['paso']} · val {mejor['val']:.4f}")
    print(f"[sft-cot] adapter guardado en {destino}")

    informe = {
        "fecha": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version": a.version,
        # Un adapter que no sabe con que se entreno obliga a adivinar a quien
        # lo mida despues, y adivinar fue la averia de R9 del 2026-08-22.
        "dataset": str(DATASET),
        "hiper": {**HIPER, "epocas": a.epocas, "cada": a.cada},
        "tren": len(tren), "validacion": len(val),
        "mejor_paso": mejor["paso"],
        "mejor_val_loss": mejor["val"],
    }
    (destino / "informe.json").write_text(
        json.dumps(informe, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("[sft-cot] VERDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
