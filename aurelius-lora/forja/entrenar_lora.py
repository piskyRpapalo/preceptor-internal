#!/usr/bin/env python3
"""FASE 2 · TRAINER GUARDIAN · LoRA en CPU sobre Qwen3-4B-Instruct.

Hiperparámetros FIRMADOS por el Soberano el 2026-08-20, tras la Fase 0:
    rango 8 · 1 época · corte de validación del 10 %
La razón está medida: 11,8 M de parámetros entrenables contra ~4 000 tokens de
datos memorizaban en vez de aprender. Con r=8 son 5,9 M, y una época no le da
tiempo a recitar.

NO es QLoRA. La Q es el NF4 de bitsandbytes y ese kernel es CUDA; aquí no hay
NVIDIA. Esto es LoRA en bf16, que en este metal va a 45-60 tok/s (Fase 0).

CERROJO DOBLE: `--ejecutar`, y un veredicto de Fase 0 que nombre entrenador.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VEREDICTO = RAIZ / "FASE0_VEREDICTO.json"
DATASET = RAIZ / "data" / "lora_dataset.jsonl"
SALIDA = RAIZ / "salida"

BASE_HF = "Qwen/Qwen3-4B-Instruct-2507"     # los pesos sin cuantizar, no el GGUF

HIPER = {
    "rank": 8,                # FIRMADO. Era 16; memorizaba.
    "alpha": 16,              # 2x el rango, como estaba la proporción en r=16
    "dropout": 0.05,
    "lr": 2e-4,
    "epocas": 1,              # FIRMADO. Eran 3.
    "validacion": 0.20,       # FIRMADO v2. Era 0,10: 17 muestras eran poca
                              # evidencia para un umbral que aborta una corrida.
    "subidas_para_abortar": 2,  # FIRMADO v2. Era 1 (implicito).
    "max_len": 512,
    "cada_cuantos_evalua": 20,
    "min_tokens": 4,           # ver `descartar_degeneradas`

    "objetivo": ["q_proj", "k_proj", "v_proj", "o_proj"],
}


def veredicto():
    try:
        return json.loads(VEREDICTO.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def revisar(exportacion=True):
    """Todo lo que falta, de una vez. No para en el primer hueco."""
    faltas = []
    v = veredicto()
    if v is None:
        faltas.append(f"no existe {VEREDICTO.name}: corre forja/minirun.py --escribir")
    elif not v.get("elegido"):
        faltas.append("el veredicto de la Fase 0 no nombra entrenador elegido")
    if not DATASET.is_file():
        faltas.append(f"no existe {DATASET}: datos/construir_dataset.py --ejecutar")
    if exportacion:
        for h in ("llama-export-lora", "llama-quantize"):
            if not shutil.which(h):
                faltas.append(f"{h} no está: corre forja/compilar_llamacpp.sh --ejecutar")
    return faltas, v


def cargar(ruta):
    """Separa lo que entrena de lo que no, y dice por qué.

    Los negativos NO entran en el paso causal. Un entrenamiento causal aprende
    a CONTINUAR el texto que se le da: meterle el campo `rechazado` le enseña
    exactamente la forma que las tres familias existen para evitar. Sirven como
    pares de preferencia (una pasada DPO futura) y como aserciones del tester
    de la Fase 3, que es donde ya se usan.
    """
    entrenables, negativos = [], 0
    for linea in ruta.open(encoding="utf-8"):
        linea = linea.strip()
        if not linea:
            continue
        r = json.loads(linea)
        if r.get("clase") != "canon":
            negativos += 1
            continue
        texto = "\n".join(m.get("contenido", "")
                          for m in r.get("mensajes", [])).strip()
        if texto:
            entrenables.append({"texto": texto, "idioma": r.get("idioma", "?")})
    return entrenables, negativos


def partir(muestras, fraccion):
    """Corte de validación estratificado por idioma.

    Sin estratificar, un corte del 10 % sobre 208 puede llevarse 21 muestras
    del mismo idioma y dejar la validación midiendo media promesa. P3 no es
    solo del dataset: es también de cómo se mide.
    """
    val, tren = [], []
    for idioma in ("en", "es"):
        de_ese = [m for m in muestras if m["idioma"] == idioma]
        corte = max(1, round(len(de_ese) * fraccion))
        # Determinista: cada n-ésima. Sin barajar, para que dos corridas del
        # mismo dataset partan igual y sus pérdidas se puedan comparar.
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
    ap = argparse.ArgumentParser(description="FASE 2 · trainer guardian")
    ap.add_argument("--ejecutar", action="store_true")
    ap.add_argument("--version", default="v1")
    ap.add_argument("--hilos", type=int, default=8)
    # El rango se puede mover POR BANDERA, no editando HIPER. Los valores
    # firmados siguen siendo los del diccionario; un experimento que cambia
    # la constante deja el fichero mintiendo sobre lo que se firmo.
    ap.add_argument("--rango", type=int, default=HIPER["rank"])
    ap.add_argument("--alpha", type=int, default=HIPER["alpha"])
    ap.add_argument("--sin-exportacion", action="store_true",
                    help="entrena aunque falten las herramientas de la Fase 4")
    a = ap.parse_args(argv)

    faltas, v = revisar(exportacion=not a.sin_exportacion)
    print(f"[guardian-2] base: {BASE_HF} (pesos sin cuantizar, bf16)")
    print(f"[guardian-2] LoRA r={a.rango} alpha={a.alpha} "
          f"lr={HIPER['lr']} · {HIPER['epocas']} época · "
          f"validación {HIPER['validacion']:.0%}")
    print(f"[guardian-2] entrenador: {(v or {}).get('elegido') or 'NO_DATA'}")

    if DATASET.is_file():
        muestras, negativos = cargar(DATASET)
        tren, val = partir(muestras, HIPER["validacion"])
        print(f"[guardian-2] {len(muestras)} entrenables · "
              f"tren {len(tren)} · validación {len(val)} "
              f"(en={sum(1 for m in val if m['idioma']=='en')} "
              f"es={sum(1 for m in val if m['idioma']=='es')})")
        print(f"[guardian-2] {negativos} negativos FUERA del paso causal "
              f"(ver docstring de cargar)")
    else:
        tren = val = []

    if faltas:
        print("[guardian-2] BLOQUEADO · falta:")
        for f in faltas:
            print(f"    · {f}")
    if not a.ejecutar:
        print("[guardian-2] CERROJO: no se entrena. Añade --ejecutar")
        return 0
    if faltas:
        print("[guardian-2] no entreno con huecos. Paro.", file=sys.stderr)
        return 2

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import (LoraConfig, get_peft_model,
                      get_peft_model_state_dict,
                      set_peft_model_state_dict)
    import copy

    torch.set_num_threads(a.hilos)
    tok = AutoTokenizer.from_pretrained(BASE_HF)
    modelo = AutoModelForCausalLM.from_pretrained(BASE_HF, dtype=torch.bfloat16)
    modelo.config.use_cache = False
    modelo = get_peft_model(modelo, LoraConfig(
        r=a.rango, lora_alpha=a.alpha, lora_dropout=HIPER["dropout"],
        bias="none", task_type="CAUSAL_LM", target_modules=HIPER["objetivo"]))
    entrenables = sum(p.numel() for p in modelo.parameters() if p.requires_grad)
    print(f"[guardian-2] parámetros entrenables: {entrenables:,}")

    def descartar_degeneradas(muestras):
        """Fuera lo que no tiene con qué entrenar.

        Un modelo causal predice el token siguiente: tras desplazar etiquetas,
        una muestra de UN token deja cero posiciones objetivo y su pérdida es
        una media sobre el vacío -- `nan`. Y un `nan` en el gradiente no se
        queda en su paso: envenena los pesos del adapter para siempre.

        Medido el 2026-08-20: el mini-run de Fase 0 dio nan en los pasos 37, 38
        y 85. La causa son 14 entradas de `textos.py` de <=2 tokens -- 'o',
        'yes', 'lista', 'ready'. Son cadenas legítimas del producto y no son
        texto entrenable: de la palabra "o" no se aprende una voz.
        """
        buenas, fuera = [], []
        for m in muestras:
            n = len(tok(m["texto"])["input_ids"])
            (buenas if n >= HIPER["min_tokens"] else fuera).append(m)
        return buenas, fuera

    tren, fuera_tren = descartar_degeneradas(tren)
    val, fuera_val = descartar_degeneradas(val)
    if fuera_tren or fuera_val:
        print(f"[guardian-2] descartadas por cortas "
              f"(<{HIPER['min_tokens']} tokens): "
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
    bitacora = SALIDA / "loss.jsonl"

    ventana, historial = [], []
    abortado = None
    # PARADA TEMPRANA DE VERDAD. No basta con dejar de entrenar: hay que
    # QUEDARSE CON EL MEJOR y tirar el resto. La v2 termino su epoca entera,
    # no aborto, y guardo el paso 140 -- un 28,8 % peor en validacion que el
    # paso 80, por el que ya habia pasado. Guardar el ultimo es guardar el que
    # mas ha memorizado.
    #
    # El adapter son 5,9 M de parametros: una copia en RAM cuesta ~23 MiB y
    # ahorra reescribir el disco en cada mejora.
    mejor = {"val": float("inf"), "paso": 0, "train": None, "pesos": None}
    t0 = time.time()

    with bitacora.open("w", encoding="utf-8") as fh:
        for paso, m in enumerate(tren * HIPER["epocas"], 1):
            salida = modelo(**lote_de(m))
            salida.loss.backward()
            opt.step()
            opt.zero_grad(set_to_none=True)
            perdida = float(salida.loss.item())
            ventana.append(perdida)
            fh.write(json.dumps({"paso": paso, "loss": perdida}) + "\n")

            if paso % HIPER["cada_cuantos_evalua"] == 0:
                tren_medio = sum(ventana) / len(ventana)
                val_medio = perdida_validacion()
                ventana = []
                historial.append({"paso": paso, "train": tren_medio, "val": val_medio})
                if val_medio < mejor["val"]:
                    mejor.update(val=val_medio, paso=paso, train=tren_medio,
                                 pesos=copy.deepcopy(
                                     get_peft_model_state_dict(modelo)))
                fh.write(json.dumps({"paso": paso, "loss": tren_medio,
                                     "val_loss": val_medio}) + "\n")
                fh.flush()
                print(f"  paso {paso:4d} · train {tren_medio:.4f} · "
                      f"val {val_medio:.4f}"
                      + ("  ← mejor" if mejor["paso"] == paso else ""),
                      flush=True)

                # SOBREAJUSTE. Dos exigencias, y las dos vienen de una cicatriz.
                #
                # 1) Que la validación suba MIENTRAS el tren baja. Una
                #    validación que sube sola puede ser ruido, y abortar por
                #    ruido enseña a desconfiar del guardián.
                # 2) Que pase DOS evaluaciones seguidas. La v1 abortó en el
                #    paso 120 con una sola subida sobre 17 muestras: la regla
                #    era correcta y la evidencia, delgada. Dos subidas cuestan
                #    veinte segundos y separan el giro de la curva del ruido.
                n = HIPER["subidas_para_abortar"]
                if len(historial) >= n + 1:
                    tramos = historial[-(n + 1):]
                    seguidas = all(
                        b["val"] > a["val"] and b["train"] < a["train"]
                        for a, b in zip(tramos, tramos[1:]))
                    if seguidas:
                        detalle = " · ".join(
                            f"{a['val']:.4f}→{b['val']:.4f}"
                            for a, b in zip(tramos, tramos[1:]))
                        abortado = (f"sobreajuste en el paso {paso}: "
                                    f"{n} subidas seguidas de validación "
                                    f"({detalle}) con el tren bajando")
                        break

    informe = {
        "fecha": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version": a.version,
        "hiper": {**HIPER, "rank": a.rango, "alpha": a.alpha},
        "tren": len(tren), "validacion": len(val),
        "pasos": len(historial) * HIPER["cada_cuantos_evalua"],
        "historial": historial,
        "segundos": round(time.time() - t0, 1),
        "abortado": abortado,
        "mejor_paso": mejor["paso"],
        "mejor_val": None if mejor["pesos"] is None else round(mejor["val"], 4),
        "guardado": "mejor_checkpoint",
    }
    (SALIDA / "entrenamiento.json").write_text(
        json.dumps(informe, ensure_ascii=False, indent=2), encoding="utf-8")

    if abortado:
        print(f"\n[guardian-2] ABORTA · {abortado}")

    if mejor["pesos"] is None:
        print("[guardian-2] no hubo ni una evaluación: nada que guardar.",
              file=sys.stderr)
        return 1

    # Se guarda el MEJOR, incluso cuando la corrida abortó. Un aborto dice
    # "deja de entrenar", no "tira lo que ya habías ganado": el mejor
    # checkpoint es anterior al giro y no lleva dentro el sobreajuste que
    # disparó el aborto.
    set_peft_model_state_dict(modelo, mejor["pesos"])
    destino.mkdir(parents=True, exist_ok=True)
    modelo.save_pretrained(str(destino))
    tok.save_pretrained(str(destino))

    ultimo = historial[-1]
    print(f"\n[guardian-2] guardado el paso {mejor['paso']} "
          f"(val {mejor['val']:.4f}), no el {ultimo['paso']} "
          f"(val {ultimo['val']:.4f})")
    print(f"[guardian-2] {'ABORTADA pero con adapter' if abortado else 'VERDE'}"
          f" · adapter en {destino}")
    print(f"[guardian-2] siguiente: convert_lora_to_gguf.py → "
          f"llama-export-lora → llama-quantize")
    return 1 if abortado else 0


if __name__ == "__main__":
    sys.exit(main())
