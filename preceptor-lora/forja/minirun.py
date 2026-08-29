#!/usr/bin/env python3
"""FASE 0 · VEREDICTO DE ENTRENADOR · mide antes de comprometer. Solo stdlib.

Tres candidatos, en el orden en que el plan los nombra:

  1. unsloth  · el que pide el plan. Se construye sobre CUDA/Triton, y este
                nodo tiene una Radeon 780M integrada y ninguna NVIDIA. La
                expectativa razonable es que no importe siquiera. Esto lo
                convierte en un dato con fecha, que es distinto de una opinión.
  2. peft     · PEFT + transformers sobre torch-CPU. Lento y real. Es el que
                el plan no nombra y el que hoy tiene más probabilidad.
  3. llamacpp · el "fallback soberano". Ver verificar_llamacpp.sh: hoy no
                existe como binario en este nodo.

SIN `--ejecutar` solo detecta qué es importable y escribe el veredicto. No
instala, no descarga, no entrena. El mini-run de 100 pasos necesita `--ejecutar`
Y un entorno preparado por forja/preparar_beelink.sh.
"""
from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

VEREDICTO = Path(__file__).resolve().parent.parent / "FASE0_VEREDICTO.json"
PASOS = 100


def _importable(modulo):
    """¿Importa, y con qué versión? Sin instalarlo y sin romperse si no está."""
    orden = [sys.executable, "-c",
             f"import {modulo}; print(getattr({modulo},'__version__','?'))"]
    try:
        r = subprocess.run(orden, capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as e:
        return False, type(e).__name__
    if r.returncode == 0:
        return True, r.stdout.strip()
    ultima = (r.stderr.strip().splitlines() or ["sin salida"])[-1]
    return False, ultima[:160]


def sondear():
    py = platform.python_version()
    torch_ok, torch_nota = _importable("torch")
    filas = []

    ok, nota = _importable("unsloth")
    filas.append({
        "candidato": "unsloth", "importa": ok, "nota": nota,
        "bloqueo": None if ok else "no importable en este entorno",
    })

    peft_ok, peft_nota = _importable("peft")
    filas.append({
        "candidato": "peft", "importa": bool(peft_ok and torch_ok),
        "nota": f"peft={peft_nota} · torch={torch_nota}",
        "bloqueo": None if (peft_ok and torch_ok) else
                   ("torch no importable" if not torch_ok else "peft no importable"),
    })

    binario = shutil.which("llama-finetune")
    filas.append({
        "candidato": "llamacpp", "importa": bool(binario),
        "nota": binario or "llama-finetune no está en PATH",
        "bloqueo": None if binario else "el binario de entrenamiento no existe",
    })

    return {
        "fecha": None,                       # la estampa quien ejecuta, no el guion
        "python_sistema": py,
        "python_soporta_torch": tuple(int(x) for x in py.split(".")[:2]) <= (3, 13),
        "candidatos": filas,
        "elegido": next((f["candidato"] for f in filas if f["importa"]), None),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="FASE 0 · veredicto de entrenador")
    ap.add_argument("--ejecutar", action="store_true",
                    help=f"corre de verdad los {PASOS} pasos del candidato elegido")
    ap.add_argument("--escribir", action="store_true",
                    help="guarda el veredicto en FASE0_VEREDICTO.json")
    a = ap.parse_args(argv)

    v = sondear()
    print(f"[fase0] python del sistema: {v['python_sistema']}"
          f" · ¿lo soporta torch? {'sí' if v['python_soporta_torch'] else 'NO'}")
    if not v["python_soporta_torch"]:
        print("[fase0]   → torch no publica ruedas para este intérprete.")
        print("[fase0]   → la forja necesita su propio entorno (uv, 3.11/3.12).")
    for f in v["candidatos"]:
        estado = "IMPORTA" if f["importa"] else "no"
        print(f"[fase0] {f['candidato']:10s} {estado:8s} {f['nota']}")

    if v["elegido"] is None:
        print("[fase0] VEREDICTO: NO_DATA · ningún candidato disponible todavía.")
        print("[fase0] Nada que medir aún. Prepara el entorno y vuelve a sondear.")
    else:
        print(f"[fase0] candidato disponible: {v['elegido']}")

    if a.escribir:
        VEREDICTO.write_text(json.dumps(v, ensure_ascii=False, indent=2),
                             encoding="utf-8")
        print(f"[fase0] veredicto escrito en {VEREDICTO}")

    if not a.ejecutar:
        print(f"[fase0] CERROJO: el mini-run de {PASOS} pasos necesita --ejecutar")
        return 0

    if v["elegido"] is None:
        print("[fase0] no se ejecuta un mini-run sin candidato. Paro.", file=sys.stderr)
        return 2
    print(f"[fase0] el mini-run de {PASOS} pasos con {v['elegido']} se implementa "
          f"cuando el entorno exista y el Soberano firme el candidato.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
