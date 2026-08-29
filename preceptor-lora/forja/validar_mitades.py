#!/usr/bin/env python3
"""Valida las mitades `elegido` firmadas. Solo stdlib.

Una mitad `elegido` es lo que el modelo va a APRENDER A PREFERIR. Si dentro se
cuela una de las formas que las tres familias existen para evitar, DPO enseñaría
a preferir justo eso, y el par entero trabajaría en contra de su propio motivo.
Esto lo comprueba antes de gastar la corrida.

No corrige nada. Señala la línea y para: una mitad es doctrina firmada, y
corregir doctrina ajena en silencio es peor que no validarla.

QUÉ NO SE MARCA, Y ES DELIBERADO
--------------------------------
«no puedo decirte si todo el árbol pasa» PASA. Negarse a afirmar lo que no se ha
mirado es el sensor honesto en su mejor forma. Lo que se caza es la evasión SIN
causa -- «no puedo hacerlo», «not available» -- que cierra la puerta sin decir
por qué. La diferencia entre las dos es la razón de ser de la familia F2, así
que la regla mira el verbo que sigue, no el «no puedo».

Y la firma del Soberano -- «grupos de pruebas»/«test groups», «validado»/
«validated» -- no la toca ninguna regla.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
NEGATIVOS = RAIZ / "datos" / "negativos.json"

# Cada regla dice QUE forma caza. Sin eso, un rojo es un misterio.
REGLAS = [
    ("emoji", "emojis · el producto es un busto de mármol, no un asistente animado",
     None),
    ("lista-negra", "frases de la lista negra firmada",
     r"somos viejos conocidos|old friends|no pasa nada|no worries|"
     r"todo est[aá] en verde|everything is green|est[aá] verificado|it'?s verified"),
    ("evasion-sin-causa", "cierra la puerta sin decir por qué",
     r"\bno pued[eo]\w*\s+(hacer|acceder|ejecutar)|"
     r"\b(can'?t|cannot|unable to)\s+(do|access|run|provide)|"
     r"\bno est[aá]\s+disponible|\bnot available"),
    ("complicidad", "se hace socio de la persona en vez de decirle qué pasa",
     r"\bjuntos\b|\btogether\b|lo arreglamos|we'?ll fix"),
    ("consuelo", "consuela en lugar de informar",
     r"no te preocupes|don'?t worry|todo bien|all good"),
    ("exclamacion-inicial", "abre con un aspaviento",
     r"^\s*[¡!]*\s*(vaya|oh no|awesome)\b"),
    ("color-como-estado", "usa un color como si fuera una medida",
     r"\ben (verde|rojo)\b|\b(is|are)\s+(green|red)\b"),
]

RANGOS_EMOJI = ("So", "Sk")          # símbolos otros / modificadores


def tiene_emoji(texto):
    return any(unicodedata.category(ch) in RANGOS_EMOJI and ord(ch) > 0x2100
               for ch in texto)


def validar(texto):
    """Devuelve la lista de (regla, motivo, fragmento) que dispara el texto."""
    fallos = []
    for nombre, motivo, patron in REGLAS:
        if patron is None:
            if tiene_emoji(texto):
                fallos.append((nombre, motivo, "".join(
                    ch for ch in texto if unicodedata.category(ch) in RANGOS_EMOJI)))
            continue
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            fallos.append((nombre, motivo, m.group(0)))
    return fallos


def main():
    try:
        familias = json.loads(NEGATIVOS.read_text(encoding="utf-8"))["familias"]
    except (OSError, json.JSONDecodeError, KeyError) as e:
        print(f"[validador] NO_DATA · {type(e).__name__}: {e}", file=sys.stderr)
        return 2

    total, rojos = 0, []
    for fam in familias:
        for caso in fam["casos"]:
            for idioma in ("es", "en"):
                texto = (caso.get("elegido") or {}).get(idioma, "")
                ident = f"{fam['id']}/{caso['clave']}/{idioma}"
                if not texto.strip():
                    rojos.append((ident, "vacia", "una mitad sin firmar", ""))
                    continue
                total += 1
                for nombre, motivo, frag in validar(texto):
                    rojos.append((ident, nombre, motivo, frag))

    print(f"[validador] {total} mitades revisadas · {len(REGLAS)} reglas")
    for ident, regla, motivo, frag in rojos:
        print(f"  ROJO  {ident:34s} {regla}")
        print(f"        {motivo}")
        if frag:
            print(f"        dispara: {frag!r}")

    if rojos:
        print(f"[validador] ROJO · {len(rojos)} mitades a revisar")
        return 1
    print("[validador] VERDE · ninguna mitad enseña lo que su familia evita")
    return 0


if __name__ == "__main__":
    sys.exit(main())
