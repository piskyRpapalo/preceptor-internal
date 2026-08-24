#!/usr/bin/env python3
"""L1 · EL AFINADOR · corre la tanda de pruebas y vigila que siga midiendo.

QUE VIGILA, Y POR QUE NO BASTA CON «VERDE O ROJO»
-------------------------------------------------
Lo obvio: si la tanda se pone en rojo, deja hallazgo. Eso lo hace cualquier
cron.

Lo que este bucle anade son **tres formas de romperse que dan VERDE**, y las
tres estan documentadas en el archivo del Soberano como cosas que ya pasaron:

1. **El recuento BAJA y sigue diciendo verde.** Si una suite desaparece del
   arbol, o alguien la quita del corredor, el total baja y `VERDE 320/320`
   se lee igual de bien que `VERDE 337/337`. Nadie mira el numero; se mira el
   color. `ARQ_LOOPS` lo dice del corredor: *«si manana una suite desaparece
   del arbol, un total agregado baja sin que nadie sepa cual falta»*.

2. **La cobertura se ENSANCHA.** `bin/pruebas` declara sus suites a mano. Una
   suite nueva escrita fuera de esa lista no la corre nadie, y el verde del
   corredor pasa a cubrir una fraccion menor del arbol sin que el numero lo
   diga. Es la deuda S3 de `PENDIENTES.md`, abierta desde el 2026-08-21: el
   corredor subio de 241 a 282 pruebas y seguia dejando 13 suites fuera.

3. **Los sabotajes dejan de sabotear.** Si un ancla de sabotaje se queda
   obsoleta -- porque el codigo cambio debajo --, el sabotaje ya no rompe nada
   y se reporta como detectado... o como no detectado, segun la suite. Paso de
   verdad: el sabotaje de durabilidad de `test_memory` llevaba semanas sin
   sabotear nada porque D11 anadio una columna al insert, y nadie lo veia
   porque `bin/pruebas` no corre el modo sabotaje de esa suite.

CLASE: MEDIO, y por medicion
----------------------------
`bin/pruebas` tarda **138 s** en este nodo (medido 2026-08-25) y come CPU de
verdad. LIGERO seria mentir sobre lo que cuesta. PESADO sobra: no carga un
modelo de 18 GB ni necesita el cerrojo de los pesados, y ponerlo ahi lo dejaria
compitiendo por un cerrojo con trabajos que si lo necesitan.

DE DONDE SALE EL «ANTES»
------------------------
De su propio latido anterior, no de un fichero de estado nuevo. El latido ya es
append-only y ya se respalda con la memoria; un segundo sitio donde guardar el
recuento seria un segundo sitio que se puede desincronizar del primero.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import latido as L  # noqa: E402

ARBOL = os.path.expanduser(os.environ.get("AFINADOR_ARBOL", "~/p0x/aurelius"))
CORREDOR = "bin/pruebas"

VENTANA_S = 86400
CLASE = "MEDIO"

# 138 s medidos, por siete. Si un dia tarda mas de veinte minutos es que algo
# se colgo, y colgado es un resultado -- no una espera indefinida que deja el
# bucle sin latido de salida hasta que alguien lo mate a mano.
ESPERA_S = 1200

_RECUENTO = re.compile(r"(\d+)\s+pruebas\s+·\s+(\d+)\s+suites")
_VEREDICTO = re.compile(r"^(VERDE|ROJO)", re.M)
_SABOTAJE = re.compile(r"(\S+)\s+--sabotaje\s+(\d+)/(\d+)\s+detectadas")
_NOTA = re.compile(r"(\d+)/(\d+) pruebas · (\d+) de (\d+) suites")


def suites_en_el_arbol(raiz):
    """Cuantos `test_*.py` hay, mire o no el corredor."""
    return len([f for f in os.listdir(raiz)
                if f.startswith("test_") and f.endswith(".py")])


def correr(raiz=None):
    """Corre la tanda y devuelve lo que se puede medir de ella."""
    raiz = raiz or ARBOL
    if not os.path.isdir(raiz):
        return {"error": f"no existe el arbol: {raiz}"}
    corredor = os.path.join(raiz, CORREDOR)
    if not os.path.isfile(corredor):
        return {"error": f"no existe el corredor: {corredor}"}
    try:
        r = subprocess.run(["bash", corredor], cwd=raiz, capture_output=True,
                           text=True, timeout=ESPERA_S, stdin=subprocess.DEVNULL)
        salida = r.stdout + r.stderr
        codigo = r.returncode
    except subprocess.TimeoutExpired:
        # Colgado ES un resultado. Un bucle que espera indefinidamente no deja
        # latido de salida y es indistinguible de uno que nunca arranco.
        return {"error": f"la tanda no termino en {ESPERA_S} s"}

    recuento = _RECUENTO.search(salida)
    veredicto = _VEREDICTO.search(salida)
    sabotajes = [{"suite": s, "detectadas": int(d), "total": int(t)}
                 for s, d, t in _SABOTAJE.findall(salida)]
    return {
        "codigo": codigo,
        "verde": codigo == 0 and bool(veredicto) and veredicto.group(1) == "VERDE",
        "pruebas": int(recuento.group(1)) if recuento else None,
        "suites_corridas": int(recuento.group(2)) if recuento else None,
        "suites_en_arbol": suites_en_el_arbol(raiz),
        "sabotajes": sabotajes,
        "cola": "\n".join(salida.strip().split("\n")[-25:]),
    }


def _anterior(c):
    """El recuento del latido anterior, leido de su nota. None si es el primero."""
    for fila in L.salidas_recientes(c, "afinador", cuantas=5):
        m = _NOTA.search(fila["nota"] or "")
        if m:
            return {"pruebas": int(m.group(1)),
                    "suites_corridas": int(m.group(3)),
                    "suites_en_arbol": int(m.group(4))}
    return None


def comparar(hoy, antes):
    """Los hallazgos que solo se ven mirando el ANTES. Aqui esta el valor."""
    hallazgos = []
    if antes is None or hoy.get("pruebas") is None:
        return hallazgos

    if hoy["pruebas"] < antes["pruebas"]:
        hallazgos.append({
            "clave": "recuento-a-la-baja",
            "detalle": (f"la tanda paso de {antes['pruebas']} a {hoy['pruebas']} "
                        f"pruebas. Menos pruebas y sigue en verde: o se borro "
                        f"una suite, o se cayo del corredor. El color no lo "
                        f"dice; el numero si.")})

    if hoy["suites_corridas"] < antes["suites_corridas"]:
        hallazgos.append({
            "clave": "suite-fuera-del-corredor",
            "detalle": (f"el corredor declaraba {antes['suites_corridas']} suites "
                        f"y ahora declara {hoy['suites_corridas']}.")})

    hueco_hoy = hoy["suites_en_arbol"] - hoy["suites_corridas"]
    hueco_antes = antes["suites_en_arbol"] - antes["suites_corridas"]
    if hueco_hoy > hueco_antes:
        hallazgos.append({
            "clave": "cobertura-mas-estrecha",
            "detalle": (f"suites en el arbol que el corredor NO declara: "
                        f"{hueco_antes} -> {hueco_hoy}. Una suite nueva que "
                        f"nadie corre no es cobertura, es decoracion. "
                        f"(Deuda S3 de PENDIENTES.md)")})
    return hallazgos


def revisar(raiz=None, antes=None):
    hoy = correr(raiz)
    hallazgos = []
    if "error" in hoy:
        return hoy, [{"clave": "tanda-no-corrio", "detalle": hoy["error"]}]

    if not hoy["verde"]:
        hallazgos.append({
            "clave": "tanda-en-rojo",
            "detalle": "la tanda no dio verde:\n" + hoy["cola"]})

    for s in hoy["sabotajes"]:
        if s["detectadas"] < s["total"]:
            hallazgos.append({
                "clave": f"sabotaje-ciego:{s['suite']}",
                "detalle": (f"{s['detectadas']}/{s['total']} roturas detectadas. "
                            f"Un sabotaje que ya no sabotea significa que ese "
                            f"test no vale: el codigo cambio debajo del ancla.")})

    if hoy["pruebas"] is None:
        hallazgos.append({
            "clave": "sin-recuento",
            "detalle": ("la tanda no imprimio su recuento. Sin numero no hay "
                        "con que comparar manana, y el bucle se queda ciego "
                        "sin dejar de dar verde.")})

    hallazgos.extend(comparar(hoy, antes))
    return hoy, hallazgos


def nota(hoy):
    if "error" in hoy or hoy.get("pruebas") is None:
        return hoy.get("error", "sin recuento")
    return (f"{hoy['pruebas']}/{hoy['pruebas']} pruebas · "
            f"{hoy['suites_corridas']} de {hoy['suites_en_arbol']} suites "
            f"certificadas · {'VERDE' if hoy['verde'] else 'ROJO'}")


def main():
    if "--informe" in sys.argv[1:]:
        hoy, hallazgos = revisar()
        print(f"afinador · {nota(hoy)}")
        for h in hallazgos:
            print(f"  {h['clave']}\n    {h['detalle'].splitlines()[0]}")
        if not hallazgos:
            print("  sin hallazgos")
        return 0

    with L.abrir() as c:
        antes = _anterior(c)

    with L.turno("afinador", CLASE, VENTANA_S) as caja:
        hoy, hallazgos = revisar(antes=antes)
        with L.abrir() as c:
            for h in hallazgos:
                L.hallazgo(c, "afinador", h["clave"], h["detalle"])
        caja["nota"] = nota(hoy)
        if hallazgos:
            caja["resultado"] = "fallo"
    return 0


if __name__ == "__main__":
    sys.exit(main())
