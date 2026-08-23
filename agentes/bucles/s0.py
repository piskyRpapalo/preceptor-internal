#!/usr/bin/env python3
"""S0 · El monitor de fallo silencioso. El bucle que sospecha de los demás.

**Solo biblioteca estándar.**

    python3 agentes/bucles/s0.py            # una pasada semanal
    python3 agentes/bucles/s0.py --informe

POR QUÉ EXISTE
--------------
Es el único bucle que no vigila el sistema: vigila **a los vigilantes**.

Un sistema de bucles tiene un modo de fallo que ninguna alerta detecta, porque
no produce ninguna alerta: **el detector se rompe y todo se queda verde.** El
afinador que dejó de leer la salida real de las pruebas, el guardián cuyo `grep`
solo mira la raíz del árbol, el centinela cuya línea base se quedó vacía. Todos
laten. Todos dicen `ok`. Ninguno encuentra nada, y eso se lee como buenas
noticias durante meses.

La regla viene del archivo del Soberano, del Score S0 de mayo de 2026:

    «Si nada supera el filtro en 7 días, sospecha del filtro.»

No dice «da la alarma»: dice **sospecha**. La salida de este bucle no es un
veredicto, es una propuesta a la bandeja de firmas — porque un filtro callado
también puede significar, simplemente, que no hay nada roto. Distinguir las dos
cosas es trabajo del carbono.

UN CASO REAL, MEDIDO HOY
------------------------
El guardián de dependencias propuesto usaba `grep "^import" *.py`, que en bash
se expande solo a la raíz del árbol. Medido en `aurelius-mvp`: 58 ficheros
frente a los 60 que hay. Los dos que se escapaban eran `empaquetado/lanzador.py`
y `laminas/recortar.py` — **el único fichero del proyecto que importa algo fuera
de la biblioteca estándar**. Ese guardián habría dado verde todas las noches sin
ver lo único que tenía que ver, y solo este monitor lo habría notado.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import latido as L                                              # noqa: E402
import director as D                                            # noqa: E402

SIETE_DIAS_S = 7 * 24 * 3600


def silencios(c, ventana_s=SIETE_DIAS_S, ahora=None):
    """Filtros que llevan la ventana entera sin encontrar nada.

    Se exige que el bucle **haya corrido** en la ventana: uno que no ha corrido
    no está callado, está parado, y de eso ya avisa el Director. Confundir las
    dos cosas haría que un bucle muerto generara dos alertas distintas y que
    ninguna de las dos dijera la verdad.
    """
    ahora = time.time() if ahora is None else ahora
    desde = ahora - ventana_s
    sospechosos = []
    for b in c.execute("SELECT * FROM bucles WHERE estado='vivo' "
                       "ORDER BY nombre").fetchall():
        corridas = c.execute(
            "SELECT COUNT(*) n FROM latidos WHERE bucle=? AND evento='sale' "
            "AND resultado='ok' AND momento>=?", (b["nombre"], desde)).fetchone()["n"]
        if corridas == 0:
            continue
        encontrados = c.execute(
            "SELECT COUNT(*) n FROM hallazgos WHERE bucle=? AND momento>=?",
            (b["nombre"], desde)).fetchone()["n"]
        if encontrados == 0:
            ultimo = c.execute(
                "SELECT momento FROM hallazgos WHERE bucle=? "
                "ORDER BY momento DESC LIMIT 1", (b["nombre"],)).fetchone()
            sospechosos.append({
                "bucle": b["nombre"],
                "corridas_ok": corridas,
                "dias_sin_hallar": (int((ahora - ultimo["momento"]) / 86400)
                                    if ultimo else None),
                "nunca_hallo": ultimo is None,
            })
    return sospechosos


def pasada(ruta=L.RUTA_DEFECTO, ventana_s=SIETE_DIAS_S, ahora=None):
    with L.turno("s0", "LIGERO", 7 * 24 * 3600, ruta) as caja:
        with L.abrir(ruta) as c:
            sos = silencios(c, ventana_s, ahora)
            entradas = []
            for s in sos:
                cuanto = ("nunca ha encontrado nada"
                          if s["nunca_hallo"]
                          else f"{s['dias_sin_hallar']} días sin encontrar nada")
                entradas.append({
                    "bucle": "s0",
                    "severidad": "media",
                    "propuesta": (f"sospecha del filtro «{s['bucle']}»: corrió "
                                  f"{s['corridas_ok']} veces con éxito y {cuanto}. "
                                  f"¿está roto el detector o de verdad no hay nada?"),
                })
            puestas = D.a_bandeja(entradas)
            # El propio S0 registra lo que encuentra: así, si S0 se rompe, el
            # siguiente S0 sospecha de S0. La vigilancia se cierra sobre sí misma.
            for s in sos:
                L.hallazgo(c, "s0", f"silencio:{s['bucle']}", json.dumps(s))
        caja["nota"] = f"sospechosos={len(sos)} a_bandeja={puestas}"
        return {"sospechosos": sos, "a_bandeja": puestas}


def main(argv=None):
    ap = argparse.ArgumentParser(description="S0 · monitor de fallo silencioso")
    ap.add_argument("--informe", action="store_true")
    ap.add_argument("--dias", type=int, default=7)
    ap.add_argument("--db", default=L.RUTA_DEFECTO)
    a = ap.parse_args(argv)
    if a.informe:
        with L.abrir(a.db) as c:
            sos = silencios(c, a.dias * 24 * 3600)
        if not sos:
            print(f"Ningún filtro lleva {a.dias} días callado.")
        else:
            print(f"Filtros bajo sospecha ({a.dias} días):")
            for s in sos:
                print(f"  {s['bucle']}: {s['corridas_ok']} corridas ok, "
                      f"{'nunca halló nada' if s['nunca_hallo'] else str(s['dias_sin_hallar']) + ' días sin hallar'}")
        return 0
    print(json.dumps(pasada(a.db, a.dias * 24 * 3600), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
