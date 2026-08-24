#!/usr/bin/env bash
# Dashboard de estado de bucles 24/7
#
# Regla de este fichero: NUNCA dar por callado lo que esta roto. Un panel que
# dice "(ninguno)" tanto si no hay bucles como si el panel no sabe mirarlos es
# peor que no tener panel, porque da permiso para no mirar. Cada seccion
# distingue las tres cosas: no existe / existe y esta vacio / existe y esto hay.
#
# Cicatriz que lo motiva (2026-08-24): la version anterior consultaba
# `loops.db` con el binario `sqlite3` -- que NO esta instalado en este nodo --
# y con una columna `timestamp` que no existe (la real es `momento`). El error
# caia en `2>/dev/null` y el panel imprimia "(tabla latidos no existe)"
# mientras la tabla existia, con dos latidos dentro y el Director vivo.
# Dos averias distintas, un solo mensaje, y el mensaje señalaba a la unica de
# las tres cosas que NO pasaba.
set -uo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
LOOPS_DB="${LOOPS_DB:-$HOME/.aurelius/loops.db}"

# Los ocho del mapa de ARQ_LOOPS. `director` y `s0` estan construidos; los
# otros seis son L1/L3 y siguen [pendiente]. El panel lo dice en vez de
# enseñarlos vacios como si estuvieran parados.
CONSTRUIDOS="director s0 guardian"
PENDIENTES="afinador centinela peregrino medico escriba cronista vigia"

echo "═══════════════════════════════════════════════════════════════"
echo "ESTADO DE BUCLES 24/7 · $(date '+%Y-%m-%d %H:%M')"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "▸ QUE EXISTE (codigo en agentes/bucles/)"
for b in $CONSTRUIDOS; do
  if [ -f "$DIR/bucles/${b}.py" ]; then
    echo "    ✔ ${b}.py"
  else
    echo "    ✘ ${b}.py · DECLARADO CONSTRUIDO Y NO ESTA"
  fi
done
faltan=0
for b in $PENDIENTES; do
  [ -f "$DIR/bucles/${b}.py" ] || faltan=$((faltan + 1))
done
echo "    · ${faltan} de L1/L3 sin escribir todavia: ${PENDIENTES}"
if [ "$faltan" != "$(echo $PENDIENTES | wc -w)" ]; then
  echo "    ! el recuento y la lista no cuadran · mueve el bucle de columna en este fichero"
fi

echo ""
echo "▸ TIMERS ACTIVOS"
encontrados="$(systemctl --user list-timers --all --no-pager 2>/dev/null \
  | grep -E "bucle|director|s0|afinador|guardian|centinela|peregrino|medico|escriba|cronista|vigia" || true)"
if [ -n "$encontrados" ]; then
  echo "$encontrados" | sed 's/^/    /'
else
  echo "    (ninguno · ningun bucle esta cronificado en este nodo)"
fi

echo ""
echo "▸ UNIDADES INSTALADAS"
hay_unidad=0
for b in $CONSTRUIDOS $PENDIENTES; do
  if systemctl --user list-unit-files "${b}.service" --no-pager 2>/dev/null | grep -q "^${b}.service"; then
    hay_unidad=1
    printf '    %-12s ' "$b"
    systemctl --user is-enabled "${b}.service" 2>/dev/null | tr -d '\n'
    echo " · $(systemctl --user is-active "${b}.service" 2>/dev/null)"
  fi
done
[ "$hay_unidad" = "0" ] && echo "    (ninguna)"

echo ""
echo "▸ LATIDOS (${LOOPS_DB})"
# python3, no el binario `sqlite3`: la biblioteca estandar viene con el
# interprete y el binario hay que instalarlo aparte. Aqui NO esta instalado, y
# esa fue justo la averia que este panel escondia.
LOOPS_DB="$LOOPS_DB" python3 - <<'PY' 2>&1 | sed 's/^/    /'
import os, sqlite3, sys

ruta = os.environ["LOOPS_DB"]
if not os.path.exists(ruta):
    print("(el fichero no existe · ningun bucle ha latido nunca en este nodo)")
    sys.exit(0)
try:
    c = sqlite3.connect(f"file:{ruta}?mode=ro", uri=True)
    tablas = {t[0] for t in c.execute(
        "select name from sqlite_master where type='table'")}
    if "latidos" not in tablas:
        print(f"(el fichero existe pero no tiene tabla `latidos` · tablas: {sorted(tablas)})")
        sys.exit(0)
    n = c.execute("select count(*) from latidos").fetchone()[0]
    if n == 0:
        print("(la tabla existe y esta VACIA · no es lo mismo que no existir)")
        sys.exit(0)
    print(f"{n} latidos registrados. Los ultimos:")
    for b, cuando, ev, res, dur in c.execute(
            "select bucle, datetime(momento,'unixepoch','localtime'), evento,"
            " coalesce(resultado,'—'), coalesce(round(duracion_s,2),'—')"
            " from latidos order by momento desc limit 10"):
        print(f"  {cuando}  {b:<10} {ev:<6} {res:<10} {dur}s")
    print("")
    print("Bucles registrados:")
    for nombre, clase, estado, motivo in c.execute(
            "select nombre, clase, estado, coalesce(motivo_sueno,'—') from bucles"):
        print(f"  {nombre:<10} {clase:<8} {estado:<8} {motivo}")
    pend = c.execute("select count(*) from hallazgos").fetchone()[0]
    print("")
    print(f"Hallazgos registrados: {pend}")
except Exception as e:
    # Ruidoso a proposito. Un panel que se calla cuando no sabe leer su propia
    # base es el modo de fallo que este fichero existe para no repetir.
    print(f"AVERIA DEL PANEL · no se pudo leer la base: {type(e).__name__}: {e}")
    sys.exit(1)
PY

echo ""
echo "▸ BANDEJA DE FIRMAS"
BANDEJA="$DIR/../docs/bandeja_firmas.md"
if [ -f "$BANDEJA" ]; then
  pendientes="$(grep -c "PENDIENTE" "$BANDEJA" 2>/dev/null || echo 0)"
  echo "    ${pendientes} propuesta(s) esperando firma · $BANDEJA"
  grep "PENDIENTE" "$BANDEJA" 2>/dev/null | cut -c1-100 | sed 's/^/      /'
else
  echo "    (no existe: $BANDEJA)"
fi

echo ""
echo "▸ LOGS RECIENTES"
hay_log=0
for b in $CONSTRUIDOS $PENDIENTES; do
  log="$DIR/logs/${b}.log"
  if [ -f "$log" ]; then
    hay_log=1
    echo "    $b:"
    tail -5 "$log" | sed 's/^/      /'
  fi
done
[ "$hay_log" = "0" ] && echo "    (ninguno · ningun bucle ha escrito log todavia)"

echo ""
echo "═══════════════════════════════════════════════════════════════"
