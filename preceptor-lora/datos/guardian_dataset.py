#!/usr/bin/env python3
"""FASE 1 · DATASET GUARDIAN · valida data/lora_dataset.jsonl. Solo stdlib.

No arregla nada. Mide, dice qué falla y con qué regla, y sale distinto de 0.
Un guardián que corrige en silencio es un guardián que oculta.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path

PRODUCTO = Path(os.environ.get(
    "AURELIUS_REPO_LOCAL", Path.home() / "p0x" / "preceptor-mvp"))
DESEQUILIBRIO_MAX = 0.05          # P3: 5 %
LARGO_MAX = 4000
# Suelo de longitud. PROXY DECLARADO: el guardian es stdlib y no tiene
# tokenizador, asi que mide caracteres. ~4 tokens son ~12 caracteres en
# estos dos idiomas. Sirve para AVISAR, no para decidir: quien decide es
# el entrenador, que si tokeniza.
LARGO_MIN_CANON = 12

# Vocabulario de control del rack. LORE.md §1: no viaja. La lista es corta a
# propósito -- una lista larga da falsa seguridad y esto es una red, no un muro.
CASA = ("soberano", "la-fragua", "la-torre", "el-vigia", "el-vigía",
        "musculo-hp", "hexelion", "beelink", "jetson", "tailnet", "p0x")


def cargar_redactor():
    """El guardrails del producto, si está. Si no está, se dice."""
    sys.path.insert(0, str(PRODUCTO))
    try:
        import guardrails
        return guardrails
    except ImportError:
        return None
    finally:
        sys.path.pop(0)


def texto_de(reg):
    partes = [m.get("contenido", "") for m in reg.get("mensajes", [])]
    partes += [reg.get(k, "") for k in ("prompt", "elegido", "rechazado")]
    return "\n".join(p for p in partes if p)


def validar(registros):
    """Devuelve (fallos, avisos, resumen).

    Un fallo para la tanda; un aviso solo se dice. La diferencia importa: si
    todo fuera fallo, este dataset nunca estaria verde por culpa de entradas
    legitimas de `textos.py`, y un guardian que jamas puede estar verde ensena
    a ignorarlo. Eso es peor que no tenerlo.
    """
    fallos, avisos = [], []
    def mal(regla, id_, detalle):
        fallos.append({"regla": regla, "id": id_, "detalle": detalle})

    def avisa(regla, id_, detalle):
        avisos.append({"regla": regla, "id": id_, "detalle": detalle})

    ids = Counter(r.get("id") for r in registros)
    for id_, n in ids.items():
        if n > 1:
            mal("R1 id duplicado", id_, f"{n} veces")

    por_huella = {}
    for r in registros:
        por_huella.setdefault(r.get("huella"), []).append(r.get("id"))
    def sin_idioma(id_):
        """El id menos su segmento de idioma: `x/es/y` y `x/en/y` son el mismo caso."""
        trozos = (id_ or "").split("/")
        return "/".join(t for i, t in enumerate(trozos) if not (i == 1 and t in ("en", "es")))

    for h, lista in por_huella.items():
        distintos = set(lista)
        if len(lista) > 1 and len(distintos) > 1:
            # Dos idiomas del MISMO caso pueden compartir contenido a proposito:
            # la pregunta del idioma se dice en los dos a la vez, porque se hace
            # antes de saber en cual hablar (textos.py). La regla existe para
            # cazar duplicados accidentales, no cadenas bilingues deliberadas.
            if len({sin_idioma(i) for i in distintos}) == 1:
                continue
            mal("R1 huella repetida con id distinto", ",".join(sorted(distintos)), h)

    presentes = set(ids)
    for r in registros:
        if r.get("clase") != "canon":
            continue
        par = r.get("par")
        if not par:
            mal("R2 canon sin par", r.get("id"), "P3 exige pareja")
        elif par not in presentes:
            mal("R2 par inexistente", r.get("id"), par)

    cuenta = Counter(r.get("idioma") for r in registros)
    en, es = cuenta.get("en", 0), cuenta.get("es", 0)
    if en + es:
        desv = abs(en - es) / max(en, es, 1)
        if desv > DESEQUILIBRIO_MAX:
            mal("R3 desequilibrio EN/ES", "-", f"en={en} es={es} ({desv:.1%})")

    red = cargar_redactor()
    for r in registros:
        cuerpo = texto_de(r)
        if not cuerpo.strip():
            mal("R6 contenido vacio", r.get("id"), "-")
            continue
        # R8 · media pieza no es un par. Un registro de preferencia con
        # `rechazado` y sin `elegido` no puede entrenar DPO: se le ensenaria
        # que evitar sin ensenarle que hacer en su lugar. Es FALLO y no aviso,
        # porque a diferencia de una cadena corta -- que el entrenador
        # descarta solo -- esto no se descarta: bloquea la pasada entera.
        if r.get("clase") in ("preferencia", "negativo"):
            faltan = [k for k in ("prompt", "elegido", "rechazado")
                      if not (r.get(k) or "").strip()]
            if faltan:
                mal("R8 par manco", r.get("id"), "falta: " + ", ".join(faltan))

        if r.get("clase") == "canon" and len(cuerpo) < LARGO_MIN_CANON:
            avisa("R7 corta para entrenar", r.get("id"),
                f"{len(cuerpo)} car. · un causal no aprende de esto")
        if len(cuerpo) > LARGO_MAX:
            mal("R6 demasiado largo", r.get("id"), f"{len(cuerpo)} car.")
        if red is not None:
            try:
                _, hallazgos = red.redactar_salida(cuerpo)
                if hallazgos:
                    mal("R4 dato privado", r.get("id"),
                        ", ".join(sorted({h.get("policy", "?") for h in hallazgos})))
            except Exception as e:
                mal("R4 no verificable", r.get("id"), type(e).__name__)
        bajo = cuerpo.lower()
        for palabra in CASA:
            if palabra in bajo:
                mal("R5 vocabulario de la casa", r.get("id"), palabra)
                break
    return fallos, avisos, {"total": len(registros), "en": en, "es": es,
                            "redactor": red is not None}


def main(argv=None):
    ap = argparse.ArgumentParser(description="FASE 1 · dataset guardian")
    ap.add_argument("--dataset", type=Path,
                    default=Path(__file__).resolve().parent.parent / "data" / "lora_dataset.jsonl")
    a = ap.parse_args(argv)

    if not a.dataset.is_file():
        print(f"[guardian-1] NO_DATA · no existe {a.dataset}")
        print("[guardian-1] constrúyelo con datos/construir_dataset.py --ejecutar")
        return 2

    registros, rotas = [], 0
    for n, linea in enumerate(a.dataset.open(encoding="utf-8"), 1):
        linea = linea.strip()
        if not linea:
            continue
        try:
            registros.append(json.loads(linea))
        except json.JSONDecodeError:
            rotas += 1
            print(f"[guardian-1] linea {n}: JSON invalido")

    fallos, avisos, resumen = validar(registros)
    print(f"[guardian-1] {resumen['total']} registros · "
          f"en={resumen['en']} es={resumen['es']}")
    if not resumen["redactor"]:
        print("[guardian-1] AVISO: guardrails.py no importable · R4 NO VERIFICADA")
    for f in fallos[:40]:
        print(f"  FALLO  {f['regla']:32s} {f['id']}  ·  {f['detalle']}")
    if len(fallos) > 40:
        print(f"  … y {len(fallos)-40} más")

    if avisos:
        print(f"[guardian-1] {len(avisos)} avisos · el entrenador los descarta, "
              f"no bloquean:")
        for v in avisos[:3]:
            print(f"  aviso  {v['regla']:28s} {v['id']}  ·  {v['detalle']}")
        if len(avisos) > 3:
            print(f"  … y {len(avisos)-3} más de la misma clase")

    if fallos or rotas:
        print(f"[guardian-1] ROJO · {len(fallos)} fallos, {rotas} lineas rotas")
        return 1
    print("[guardian-1] VERDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
