#!/usr/bin/env python3
"""L4 · El Director. El meta-bucle que reparte la energía y detecta a los muertos.

**Solo biblioteca estándar.**

    python3 agentes/bucles/director.py            # una pasada
    python3 agentes/bucles/director.py --informe  # imprime el estado y sale

QUÉ HACE, Y QUÉ NO
------------------
Lee los latidos, mira la carga y la hora, y **propone** una cola de ventanas.
No ejecuta nada por su cuenta: escribe el plan y las alertas. Lo que toca
producto, memoria o publicación va a la bandeja de firmas.

Marcar a un muerto NO es instantáneo: hacen falta dos ventanas sin latido **y**
que el estado actual lleve puesto el descanso mínimo (`latido.DESCANSO_ESTADO_S`).
Esa doble condición es la histéresis, y existe porque un bucle que oscila entre
vivo y muerto llena la bandeja de firmas de ruido hasta que alguien deja de
mirarla — y entonces el sistema de vigilancia ha dejado de vigilar sin que nadie
lo haya apagado.

EL CERROJO
----------
Un solo PESADO a la vez, con `flock`. Los LIGERO corren siempre. Los MEDIO se
posponen si la carga pasa del umbral, **y la posposición se registra**: un
bucle que se pospone en silencio es indistinguible de uno que no existe.
"""

from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import latido as L                                              # noqa: E402

CERROJO = os.path.expanduser("~/.aurelius/loops.lock")
PLAN = os.path.expanduser("~/.aurelius/plan_ventanas.json")
BANDEJA = os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "docs", "bandeja_firmas.md")

# Un pesado no arranca fuera de esta franja aunque la máquina esté ociosa: el
# Soberano duerme y el 30B hace ruido de ventilador.
VENTANA_PESADOS = (1, 6)
CARGA_MAXIMA = 2.0


def carga():
    """Carga a un minuto. `os.getloadavg` es stdlib y no depende de `uptime`."""
    try:
        return os.getloadavg()[0]
    except OSError:
        return 0.0


def hay_pesado_corriendo():
    """Mira el cerrojo sin quedarse esperando."""
    try:
        fh = open(CERROJO, "a+")
    except OSError:
        return False
    try:
        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.flock(fh, fcntl.LOCK_UN)
        return False
    except BlockingIOError:
        return True
    finally:
        fh.close()


def dentro_de_ventana_pesados(ahora=None):
    h = (dt.datetime.fromtimestamp(ahora) if ahora else dt.datetime.now()).hour
    ini, fin = VENTANA_PESADOS
    return ini <= h < fin


def _sin_latido_desde(c, nombre):
    f = L.ultimo_latido(c, nombre, "sale")
    return None if f is None else time.time() - f["momento"]


def revisar(c, ahora=None):
    """Un veredicto por bucle. NO cambia estados: solo dice qué haría.

    Se separa a propósito de `aplicar`: así la decisión se puede leer, probar y
    discutir sin que nada se mueva. Un meta-bucle que decide y actúa en la misma
    función es un meta-bucle que no se puede auditar.
    """
    ahora = time.time() if ahora is None else ahora
    veredictos = []
    for b in c.execute("SELECT * FROM bucles ORDER BY nombre").fetchall():
        v = {"bucle": b["nombre"], "clase": b["clase"], "estado": b["estado"],
             "accion": "ninguna", "porque": ""}
        if b["estado"] == "dormido":
            v["accion"] = "ninguna"
            v["porque"] = f"dormido: {b['motivo_sueno']} · despierta si: {b['condicion_despertar']}"
            veredictos.append(v)
            continue

        callado = _sin_latido_desde(c, b["nombre"])
        margen = b["ventana_s"] * L.VENTANAS_PARA_DUDAR
        if callado is None:
            v["accion"] = "esperar"
            v["porque"] = "registrado y aún sin ninguna salida"
        elif callado > margen and b["estado"] != "muerto":
            v["accion"] = "marcar_muerto"
            v["porque"] = (f"sin latido desde hace {int(callado)} s, más de "
                           f"{L.VENTANAS_PARA_DUDAR} ventanas de {b['ventana_s']} s")
        elif callado <= b["ventana_s"] and b["estado"] == "muerto":
            v["accion"] = "marcar_vivo"
            v["porque"] = f"volvió a latir hace {int(callado)} s"
        veredictos.append(v)
    return veredictos


def aplicar(c, veredictos, ahora=None):
    """Ejecuta los veredictos pasándolos por la histéresis de `latido`.

    Lo que la histéresis frena NO se pierde: se devuelve como `frenado` para que
    el informe lo enseñe. Un freno invisible se confunde con un fallo.
    """
    hechos, frenados = [], []
    for v in veredictos:
        if v["accion"] == "marcar_muerto":
            ok, razon = L.cambiar_estado(c, v["bucle"], "muerto", v["porque"], ahora)
        elif v["accion"] == "marcar_vivo":
            ok, razon = L.cambiar_estado(c, v["bucle"], "vivo", v["porque"], ahora)
        else:
            continue
        (hechos if ok else frenados).append({**v, "razon": razon})
    return hechos, frenados


def planificar(c, ahora=None):
    """La cola de la próxima ventana. Ligeros siempre; pesados con permiso."""
    ahora = time.time() if ahora is None else ahora
    c_actual = carga()
    ventana_ok = dentro_de_ventana_pesados(ahora)
    ocupado = hay_pesado_corriendo()
    cola, pospuestos = [], []
    for b in c.execute("SELECT * FROM bucles WHERE estado <> 'dormido' "
                       "ORDER BY nombre").fetchall():
        if b["clase"] == "LIGERO":
            cola.append(b["nombre"])
            continue
        if b["clase"] == "MEDIO":
            if c_actual > CARGA_MAXIMA:
                pospuestos.append({"bucle": b["nombre"],
                                   "porque": f"carga {c_actual:.2f} > {CARGA_MAXIMA}"})
            else:
                cola.append(b["nombre"])
            continue
        # PESADO
        if not ventana_ok:
            pospuestos.append({"bucle": b["nombre"],
                               "porque": f"fuera de la ventana {VENTANA_PESADOS}"})
        elif ocupado:
            pospuestos.append({"bucle": b["nombre"], "porque": "otro pesado tiene el cerrojo"})
        elif c_actual > CARGA_MAXIMA:
            pospuestos.append({"bucle": b["nombre"],
                               "porque": f"carga {c_actual:.2f} > {CARGA_MAXIMA}"})
        else:
            cola.append(b["nombre"])
    return {"momento": ahora, "carga": c_actual, "ventana_pesados": ventana_ok,
            "cerrojo_ocupado": ocupado, "cola": cola, "pospuestos": pospuestos}


def a_bandeja(entradas):
    """Escribe propuestas en la bandeja de firmas. Nunca las ejecuta.

    Lo rechazado se memoriza en el propio fichero: si una propuesta ya está ahí
    con estado RECHAZADA, no se vuelve a añadir. Sin eso, el mismo aviso
    reaparece cada noche y la bandeja se vuelve ilegible — que es la forma
    educada de apagarla.
    """
    if not entradas:
        return 0
    os.makedirs(os.path.dirname(BANDEJA), exist_ok=True)
    previo = ""
    if os.path.exists(BANDEJA):
        with open(BANDEJA, encoding="utf-8") as fh:
            previo = fh.read()
    else:
        previo = ("# BANDEJA DE FIRMAS\n\n"
                  "El silicio propone; el carbono firma. Lo RECHAZADO no se vuelve a "
                  "proponer: el bucle que lo propuso lee este fichero antes de escribir.\n\n"
                  "| fecha | bucle | propuesta | severidad | estado |\n"
                  "|---|---|---|---|---|\n")
    hoy = dt.date.today().isoformat()
    nuevas = 0
    lineas = []
    for e in entradas:
        firma = f"| {e['bucle']} | {e['propuesta']} |"
        if firma in previo:
            continue
        lineas.append(f"| {hoy} | {e['bucle']} | {e['propuesta']} | "
                      f"{e.get('severidad','media')} | PENDIENTE |")
        nuevas += 1
    if nuevas:
        with open(BANDEJA, "w", encoding="utf-8") as fh:
            fh.write(previo.rstrip("\n") + "\n" + "\n".join(lineas) + "\n")
    return nuevas


def pasada(ruta=L.RUTA_DEFECTO, ahora=None):
    with L.turno("director", "LIGERO", 900, ruta) as caja:
        with L.abrir(ruta) as c:
            veredictos = revisar(c, ahora)
            hechos, frenados = aplicar(c, veredictos, ahora)
            plan = planificar(c, ahora)
            for p in plan["pospuestos"]:
                L.sale(c, p["bucle"], "pospuesto", None, p["porque"])
            muertos = [h for h in hechos if h["accion"] == "marcar_muerto"]
            puestas = a_bandeja([
                {"bucle": m["bucle"], "severidad": "alta",
                 "propuesta": f"bucle muerto: {m['porque']}"} for m in muertos])
        os.makedirs(os.path.dirname(PLAN), exist_ok=True)
        with open(PLAN, "w", encoding="utf-8") as fh:
            json.dump(plan, fh, indent=2, ensure_ascii=False)
        caja["nota"] = (f"cola={len(plan['cola'])} pospuestos={len(plan['pospuestos'])} "
                        f"muertos={len(muertos)} frenados_por_histeresis={len(frenados)} "
                        f"a_bandeja={puestas}")
        return {"plan": plan, "hechos": hechos, "frenados": frenados,
                "a_bandeja": puestas}


def informe(ruta=L.RUTA_DEFECTO):
    with L.abrir(ruta) as c:
        filas = c.execute("SELECT * FROM bucles ORDER BY clase, nombre").fetchall()
        if not filas:
            return "No hay ningún bucle registrado todavía."
        out = [f"carga {carga():.2f} · ventana de pesados "
               f"{'abierta' if dentro_de_ventana_pesados() else 'cerrada'} · "
               f"cerrojo {'ocupado' if hay_pesado_corriendo() else 'libre'}", ""]
        for b in filas:
            callado = _sin_latido_desde(c, b["nombre"])
            cuando = "nunca" if callado is None else f"hace {int(callado)} s"
            linea = f"  {b['estado']:8} {b['clase']:7} {b['nombre']:16} último latido: {cuando}"
            if b["estado"] == "dormido":
                linea += f"\n           despierta si: {b['condicion_despertar']}"
            out.append(linea)
        return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="El Director · meta-bucle")
    ap.add_argument("--informe", action="store_true", help="enseña el estado y sale")
    ap.add_argument("--db", default=L.RUTA_DEFECTO)
    a = ap.parse_args(argv)
    if a.informe:
        print(informe(a.db))
        return 0
    r = pasada(a.db)
    print(json.dumps(r, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
