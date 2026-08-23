#!/usr/bin/env python3
"""Fase 1a · construye el dataset desde el canon del producto. Solo stdlib.

P1: primario = canon del producto. P3: bilingüe en pares paralelos.
P4: nada sale de esta máquina — este guion no abre un socket.

CERROJO: sin `--ejecutar` no escribe nada. Cuenta y calla.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

PRODUCTO = Path(os.environ.get(
    "AURELIUS_REPO_LOCAL", Path.home() / "p0x" / "aurelius-mvp"))
SALIDA_DEFECTO = Path(__file__).resolve().parent.parent / "data" / "lora_dataset.jsonl"


def huella(texto: str) -> str:
    norm = re.sub(r"\s+", " ", texto.strip()).lower()
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:16]


def commit_del_producto() -> str:
    """El origen lleva su commit, o dice que no lo sabe. No se inventa."""
    cabeza = PRODUCTO / ".git" / "HEAD"
    try:
        ref = cabeza.read_text().strip()
        if ref.startswith("ref: "):
            destino = PRODUCTO / ".git" / ref[5:]
            return destino.read_text().strip()[:7]
        return ref[:7]
    except OSError:
        return "NO_DATA"


def _pares_de_textos(commit: str):
    """Cada clave de TEXTOS produce dos registros que se declaran pareja."""
    sys.path.insert(0, str(PRODUCTO))
    try:
        import textos as T
    except ImportError as e:
        print(f"[dataset] no puedo leer el canon del producto: {e}", file=sys.stderr)
        return
    finally:
        sys.path.pop(0)

    en, es = T.TEXTOS.get("en", {}), T.TEXTOS.get("es", {})
    for clave in sorted(set(en) & set(es)):
        for idioma, tabla in (("en", en), ("es", es)):
            valor = tabla[clave]
            if not isinstance(valor, str) or not valor.strip():
                continue
            otro = "es" if idioma == "en" else "en"
            yield {
                "id": f"textos/{idioma}/{clave}",
                "clase": "canon",
                "idioma": idioma,
                "origen": f"aurelius@{commit}:textos.py",
                "huella": huella(valor),
                "peso": 1.0,
                "mensajes": [{"rol": "aurelius", "contenido": valor}],
                "par": f"textos/{otro}/{clave}",
            }


def _piezas_del_lore(commit: str):
    """LORE.md ya viene en pares EN/ES: dos citas seguidas por pieza."""
    ruta = PRODUCTO / "LORE.md"
    try:
        cuerpo = ruta.read_text(encoding="utf-8")
    except OSError:
        return
    bloques = re.findall(r"\*\*(.+?)\*\*\n((?:>.*\n|\n(?=>))+)", cuerpo)
    for titulo, crudo in bloques:
        citas = [c.strip() for c in re.split(r"\n\s*\n", crudo) if c.strip()]
        textos = [" ".join(l.lstrip("> ").strip() for l in c.splitlines())
                  for c in citas]
        if len(textos) != 2:
            continue                      # sin pareja no entra: lo dice el §P3
        clave = re.sub(r"[^a-z0-9]+", "-", titulo.lower()).strip("-")
        for idioma, texto in (("en", textos[0]), ("es", textos[1])):
            otro = "es" if idioma == "en" else "en"
            yield {
                "id": f"lore/{idioma}/{clave}",
                "clase": "canon",
                "idioma": idioma,
                "origen": f"aurelius@{commit}:LORE.md",
                "huella": huella(texto),
                "peso": 1.0,
                "mensajes": [{"rol": "aurelius", "contenido": texto}],
                "par": f"lore/{otro}/{clave}",
            }


def _negativos():
    """Las tres familias, FIRMADAS por el Soberano el 2026-08-20.

    El contenido vive en `datos/negativos.json`, no aqui: una familia se
    corrige editando datos, sin tocar codigo ni volver a leer este fichero.
    Cada caso sale en los dos idiomas (P3) para no romper el equilibrio.
    """
    ruta = Path(__file__).resolve().parent / "negativos.json"
    try:
        familias = json.loads(ruta.read_text(encoding="utf-8"))["familias"]
    except (OSError, json.JSONDecodeError, KeyError) as e:
        print(f"[dataset] NO_DATA · negativos ilegibles: {e}", file=sys.stderr)
        return []

    fuera = []
    for fam in familias:
        for caso in fam["casos"]:
            for idioma in ("en", "es"):
                rechazado = caso["rechazado"][idioma]
                elegido = caso.get("elegido", {}).get(idioma, "")
                fuera.append({
                    "id": f"negativo/{idioma}/{fam['id']}-{caso['clave']}",
                    "clase": "negativo",
                    "idioma": idioma,
                    "origen": f"sprint 2026-08-20 · familia {fam['id']} {fam['nombre']}",
                    "huella": huella(rechazado),
                    "peso": 2.0,
                    "prompt": caso["prompt"][idioma],
                    "elegido": elegido,
                    "rechazado": rechazado,
                    "motivo": caso["motivo"],
                })
    return fuera


def construir():
    commit = commit_del_producto()
    registros = list(_pares_de_textos(commit)) + list(_piezas_del_lore(commit))
    registros += _negativos()
    return registros, commit


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fase 1a · construir el dataset")
    ap.add_argument("--ejecutar", action="store_true",
                    help="sin esto no se escribe nada")
    ap.add_argument("--salida", type=Path, default=SALIDA_DEFECTO)
    a = ap.parse_args(argv)

    registros, commit = construir()
    por_idioma = {}
    for r in registros:
        por_idioma[r["idioma"]] = por_idioma.get(r["idioma"], 0) + 1
    peso = sum(len(json.dumps(r, ensure_ascii=False)) for r in registros)

    print(f"[dataset] producto: aurelius@{commit}")
    print(f"[dataset] registros: {len(registros)} · " +
          " · ".join(f"{k}={v}" for k, v in sorted(por_idioma.items())))
    print(f"[dataset] peso crudo: {peso/1024:.1f} KiB")
    negs = [r for r in registros if r["clase"] == "negativo"]
    familias = sorted({r["origen"].split("familia ")[-1] for r in negs})
    print(f"[dataset] negativos: {len(negs)} · " + " · ".join(familias))

    if not a.ejecutar:
        print(f"[dataset] CERROJO: no se escribe. Añade --ejecutar para {a.salida}")
        return 0

    a.salida.parent.mkdir(parents=True, exist_ok=True)
    with open(a.salida, "w", encoding="utf-8") as fh:
        for r in registros:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[dataset] escrito: {a.salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
