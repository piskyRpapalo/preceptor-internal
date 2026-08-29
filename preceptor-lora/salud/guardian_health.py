#!/usr/bin/env python3
"""FASE 5 · HEALTH GUARDIAN · lee la bitácora y avisa si no converge. Stdlib.

No entrena, no toca modelos. Lee lo que dejaron las fases 2 y 3 y responde a
una sola pregunta: ¿esto va a algún sitio?

«No converge» se define aquí y se mide, en vez de dejarse a la vista de quien
mire la gráfica: la pérdida de la última ventana no mejora la de la anterior
en al menos `MEJORA_MIN`.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VENTANA = 20
MEJORA_MIN = 0.01


def leer_perdidas(ruta, vals=None):
    valores = []
    vals = [] if vals is None else vals
    try:
        for linea in ruta.open(encoding="utf-8"):
            linea = linea.strip()
            if not linea:
                continue
            try:
                d = json.loads(linea)
            except json.JSONDecodeError:
                continue
            if isinstance(d.get("loss"), (int, float)):
                valores.append(float(d["loss"]))
            if isinstance(d.get("val_loss"), (int, float)):
                vals.append(float(d["val_loss"]))
    except OSError:
        return None
    return valores


def converge(v):
    if len(v) < VENTANA * 2:
        return None, f"solo {len(v)} pasos · hacen falta {VENTANA*2}"
    antes = sum(v[-VENTANA*2:-VENTANA]) / VENTANA
    ahora = sum(v[-VENTANA:]) / VENTANA
    mejora = antes - ahora
    return mejora >= MEJORA_MIN, f"{antes:.4f} → {ahora:.4f} (mejora {mejora:+.4f})"


def main(argv=None):
    ap = argparse.ArgumentParser(description="FASE 5 · health guardian")
    ap.add_argument("--perdidas", type=Path, default=RAIZ / "salida" / "loss.jsonl")
    ap.add_argument("--informe", type=Path, default=RAIZ / "salida" / "tester.json")
    a = ap.parse_args(argv)

    alerta = False
    medido = False

    v = leer_perdidas(a.perdidas)
    if v is None:
        print(f"[guardian-5] NO_DATA · no existe {a.perdidas}")
    else:
        medido = True
        ok, detalle = converge(v)
        if ok is None:
            print(f"[guardian-5] pérdida: aún no medible · {detalle}")
        elif ok:
            print(f"[guardian-5] pérdida de ENTRENAMIENTO: converge · {detalle}")
            print("[guardian-5]   (esto no dice nada de la validación · ver abajo)")
        else:
            print(f"[guardian-5] ALERTA · la pérdida de entrenamiento no baja · {detalle}")
            alerta = True

    # El informe del entrenador manda sobre la bitacora: si la Fase 2 ya
    # aborto por sobreajuste, decirlo es mas util que reinterpretar las cifras.
    try:
        ent = json.loads((RAIZ / "salida" / "entrenamiento.json").read_text(encoding="utf-8"))
        medido = True
        if ent.get("abortado"):
            print(f"[guardian-5] ALERTA · la Fase 2 aborto: {ent['abortado']}")
            alerta = True
        else:
            h = ent.get("historial") or []
            if h:
                print(f"[guardian-5] entrenamiento: {len(h)} evaluaciones · "
                      f"val {h[0]['val']:.4f} -> {h[-1]['val']:.4f}")
                # No basta con mirar el principio y el final. Un modelo puede
                # acabar mejor que como empezo y aun asi haber pasado hace
                # rato por su mejor momento -- y lo que se guarda es el ULTIMO
                # paso, no el mejor. Medido en v2: la validacion toco fondo en
                # el paso 80 y termino un 29 % peor, y este guardian decia
                # "sin alertas". Un sensor que calla eso no es honesto.
                mejor = min(h, key=lambda e: e["val"])
                # QUE se guardo lo dice el entrenador, no lo supone este
                # guardian. La primera version de esto asumia que lo guardado
                # era el ultimo paso; el dia que el entrenador aprendio a
                # guardar el mejor, el sensor empezo a mentir sin que nadie
                # tocara el sensor. Una suposicion sobre otro modulo caduca
                # cuando ese modulo cambia -- y no avisa.
                guardado_paso = ent.get("mejor_paso")
                if ent.get("guardado") != "mejor_checkpoint" or not guardado_paso:
                    guardado_paso = h[-1]["paso"]
                guardado = next((e for e in h if e["paso"] == guardado_paso), h[-1])

                if guardado["paso"] != mejor["paso"]:
                    peor = (guardado["val"] - mejor["val"]) / mejor["val"]
                    print(f"[guardian-5] el mejor momento fue el paso "
                          f"{mejor['paso']} (val {mejor['val']:.4f}); "
                          f"el adapter guardado es del paso {guardado['paso']} "
                          f"(val {guardado['val']:.4f}, {peor:+.1%})")
                    if peor > 0.10:
                        print("[guardian-5] ALERTA · se guardo un adapter "
                              "medida peor que el mejor que hubo")
                        alerta = True
                else:
                    print(f"[guardian-5] parada temprana correcta · se guardo "
                          f"el paso {mejor['paso']} (val {mejor['val']:.4f}), "
                          f"que es el mejor de los {len(h)}")
    except (OSError, json.JSONDecodeError):
        print("[guardian-5] NO_DATA · sin informe de entrenamiento")

    try:
        inf = json.loads(a.informe.read_text(encoding="utf-8"))
        tasa, umbral = inf.get("tasa", 0.0), inf.get("umbral", 0.10)
        medido = True
        print(f"[guardian-5] tests: fallo {tasa:.0%} (umbral {umbral:.0%})")
        if tasa > umbral:
            print("[guardian-5] ALERTA · el afinado no pasa la suite")
            alerta = True
    except (OSError, json.JSONDecodeError):
        print(f"[guardian-5] NO_DATA · no existe {a.informe}")

    if alerta:
        print("[guardian-5] ROJO · hay algo que mirar antes de promover")
        return 1
    if not medido:
        # Sin dato no se dice "sano": eso seria fabricar un sensor deshonesto
        # encima de uno honesto. NO_DATA es una respuesta, "verde" no lo es.
        print("[guardian-5] NO_DATA · no hay nada medido todavia. No digo sano.")
        return 2
    print("[guardian-5] sin alertas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
