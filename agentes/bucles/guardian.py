#!/usr/bin/env python3
"""L1 · EL GUARDIAN · vigila las dependencias del arbol de Aurelius.

QUE VIGILA
----------
Que no entre en el arbol un `import` de algo que no sea la biblioteca estandar
ni un modulo del propio proyecto. El README promete que la stdlib es el unico
requisito, y esa promesa es el producto: el dia que se rompa sin que nadie se
entere, el producto deja de ser lo que dice ser.

LAS TRES CICATRICES QUE LLEVA PUESTAS
-------------------------------------
Este bucle se propuso con tres errores. Los tres estan documentados en
`docs/archivo_2026-08/REVISION_CRUZADA.md` §5.1, y los tres se corrigen aqui:

1. **El `grep` de la propuesta no bajaba por las subcarpetas.** Usaba
   `grep -r "^import" *.py`, que en bash se expande SOLO a la raiz. Medido: la
   raiz da 58 ficheros y el recursivo 60. Los dos que se escapaban eran
   `empaquetado/lanzador.py` y `laminas/recortar.py` -- **y `recortar.py` es el
   unico fichero del arbol que importa algo fuera de la stdlib.** Ese guardian
   habria dado verde todas las noches sin ver lo unico que tenia que ver. Aqui
   se recorre el arbol entero.

2. **La lista blanca no puede ser solo stdlib.** Este arbol tiene decenas de
   modulos propios -- `casa`, `textos`, `memory`, `fusible`, `path`... -- que un
   filtro de stdlib marcaria como intrusos cada noche hasta que alguien lo
   apagara por ruido. Los propios se descubren leyendo el arbol, no de una
   lista escrita a mano que se queda vieja.

3. **Lo conocido se declara, con su motivo.** `PIL` en `laminas/recortar.py` es
   una dependencia real y aceptada: es herramienta de assets, no runtime del
   producto. Si no estuviera declarada aqui, el guardian avisaria de ella todas
   las noches -- y un aviso que sale siempre es un aviso que se deja de leer.
   Declarada con su motivo, cualquier OTRA se ve al instante.

Y NO SE CALLA CUANDO NO ENCUENTRA NADA
--------------------------------------
Registra el recuento de ficheros mirados en la nota del latido, encuentre o no.
S0 sospecha del filtro que lleva siete dias en verde sin hallar nada; con el
recuento en la nota se puede distinguir «no habia nada» de «no miro nada», que
es justo la averia que este bucle no puede permitirse.
"""
from __future__ import annotations

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import latido as L  # noqa: E402

# El arbol vigilado. Se declara por variable de entorno para que la prueba
# pueda apuntarlo a un arbol de mentira sin tocar el de verdad.
#
# El defecto era `~/p0x/aurelius`, que dejo de existir con el renombrado del
# producto. La unidad si se actualizo (`afinador.service:16` ya dice
# `%h/p0x/preceptor`); el defecto del codigo no. Resultado medido el
# 2026-08-30: el guardian corrio a las 04:13 y anoto «0 ficheros mirados»
# despues de anotar 877 la vispera.
ARBOL = os.path.expanduser(os.environ.get("GUARDIAN_ARBOL", "~/p0x/preceptor"))

VENTANA_S = 86400          # una vez al dia basta: las dependencias no cambian solas
CLASE = "LIGERO"           # solo lee ficheros y parsea; no invoca nada

# Dependencias fuera de la stdlib que YA estan aceptadas, con su motivo. Sin
# motivo escrito, dentro de un ano nadie sabra si esto era una excepcion
# pensada o un olvido que se quedo.
CONOCIDAS = {
    "PIL": "herramienta de assets en laminas/recortar.py, no runtime del producto",
}


def _modulos_propios(raiz):
    """Los modulos del propio arbol. Se descubren, no se listan a mano.

    Una lista escrita a mano se queda vieja el dia que alguien anade un modulo,
    y entonces el guardian avisa de un fichero del propio proyecto como si
    fuera un intruso.
    """
    propios = set()
    for base, _dirs, ficheros in os.walk(raiz):
        if os.path.basename(base).startswith("."):
            continue
        for f in ficheros:
            if f.endswith(".py"):
                propios.add(f[:-3])
        # Un paquete tambien es un modulo importable.
        if "__init__.py" in ficheros:
            propios.add(os.path.basename(base))
    return propios


def _es_entorno_virtual(ruta):
    """Un directorio con `pyvenv.cfg` dentro ES un entorno virtual.

    Se comprueba por el FICHERO y no por el nombre a proposito. Los entornos de
    este rack se llaman `venv`, `.venv`, `.venv-dashboard` y `env` segun quien
    los creara; una lista de nombres deja fuera el siguiente que aparezca, y
    este guardian ya se quemo una vez por mirar donde no debia (cicatriz nº1).
    `pyvenv.cfg` lo pone el propio `venv` de la stdlib, siempre.
    """
    return os.path.isfile(os.path.join(ruta, "pyvenv.cfg"))


def _ficheros(raiz):
    """Todos los .py del arbol, subcarpetas incluidas. La cicatriz nº1.

    Los entornos virtuales quedan FUERA, y no es una comodidad: es lo que hace
    que este bucle signifique algo. Medido el 2026-08-30 sobre la base de
    latidos: de los ultimos 224 hallazgos, **222 venian de dentro de un venv**
    -- paquetes de terceros que el guardian denunciaba una y otra vez, 111 cada
    noche desde el 28 de agosto.

    Ciento once hallazgos permanentes son cero hallazgos. A la tercera noche
    nadie mira la lista, y el dia que entre una dependencia de verdad en el
    codigo del producto se pierde entre el ruido. Lo que este bucle vigila es
    lo que ESCRIBIMOS, no lo que instalamos.
    """
    for base, dirs, ficheros in os.walk(raiz):
        dirs[:] = [d for d in dirs
                   if not d.startswith(".")
                   and d not in ("__pycache__", "build")
                   and not _es_entorno_virtual(os.path.join(base, d))]
        for f in sorted(ficheros):
            if f.endswith(".py"):
                yield os.path.join(base, f)


def _importados(ruta):
    """Los modulos de primer nivel que importa un fichero.

    Con `ast` y no con `grep`: `grep "^import"` no ve un import dentro de una
    funcion ni de un `try`, y este arbol tiene los dos.
    """
    try:
        with open(ruta, encoding="utf-8") as f:
            arbol = ast.parse(f.read())
    except (SyntaxError, OSError, UnicodeDecodeError) as e:
        return None, f"{type(e).__name__}: {e}"
    fuera = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            fuera.update(a.name.split(".")[0] for a in nodo.names)
        elif isinstance(nodo, ast.ImportFrom):
            if nodo.level:          # `from . import x` es del propio paquete
                continue
            if nodo.module:
                fuera.add(nodo.module.split(".")[0])
    return fuera, None


def revisar(raiz=None):
    """Devuelve (hallazgos, mirados). Un hallazgo es un import no permitido."""
    raiz = raiz or ARBOL
    if not os.path.isdir(raiz):
        return ([{"clave": "arbol-ausente",
                  "detalle": f"no existe el arbol vigilado: {raiz}"}], 0)

    permitidos = set(sys.stdlib_module_names) | _modulos_propios(raiz) \
        | set(CONOCIDAS) | {"__future__"}
    hallazgos = []
    mirados = 0
    for ruta in _ficheros(raiz):
        mirados += 1
        modulos, error = _importados(ruta)
        if error is not None:
            hallazgos.append({
                "clave": f"ilegible:{os.path.relpath(ruta, raiz)}",
                "detalle": f"no se pudo analizar: {error}"})
            continue
        for m in sorted(modulos - permitidos):
            hallazgos.append({
                "clave": f"{m}:{os.path.relpath(ruta, raiz)}",
                "detalle": (f"`{m}` no es stdlib, no es un modulo de este arbol "
                            f"y no esta declarado en CONOCIDAS")})
    return hallazgos, mirados


def main():
    if "--informe" in sys.argv[1:]:
        hallazgos, mirados = revisar()
        print(f"guardian · {mirados} ficheros mirados · {len(hallazgos)} hallazgos")
        for h in hallazgos:
            print(f"  {h['clave']}\n    {h['detalle']}")
        if CONOCIDAS:
            print("\n  declaradas y por tanto no avisadas:")
            for k, v in sorted(CONOCIDAS.items()):
                print(f"    {k}: {v}")
        return 0

    with L.turno("guardian", CLASE, VENTANA_S) as caja:
        hallazgos, mirados = revisar()
        with L.abrir() as c:
            for h in hallazgos:
                L.hallazgo(c, "guardian", h["clave"], h["detalle"])
        # El recuento va SIEMPRE, encuentre o no. Es lo que deja distinguir
        # "no habia nada" de "no miro nada".
        caja["nota"] = f"{mirados} ficheros mirados · {len(hallazgos)} hallazgos"
        # Y si no miro NADA, el turno es un fallo, no un ok.
        #
        # Hasta el 2026-08-30 esto devolvia `ok` con el arbol ausente. El
        # recuento en la nota permitia darse cuenta -- si alguien la leia --
        # pero `systemctl` y cualquier panel que mirase el resultado veian
        # verde. Es literalmente el modo de fallo que S0 existe para cazar:
        # «el detector se rompe y todo se queda verde». Un vigilante que no
        # mira ningun fichero no esta sano: esta ciego.
        if mirados == 0:
            caja["resultado"] = "fallo"
            caja["nota"] += " · CIEGO: no se miro ni un fichero"
    return 0


if __name__ == "__main__":
    sys.exit(main())
