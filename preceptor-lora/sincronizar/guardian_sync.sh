#!/usr/bin/env bash
# FASE 4 · SYNC GUARDIAN · el afinado viaja al Doogee, se gana el sitio o vuelve.
#
# ORDEN, Y EL PORQUÉ DEL ORDEN
#   1. copia de seguridad ANTES de tocar nada
#   2. empujar el GGUF a un nombre NUEVO -- jamás encima del cerebro base
#   3. declararlo con su huella MEDIDA en el destino, no en el origen
#   4. pasarle la suite EN EL TELÉFONO
#   5. si falla, rollback; si pasa, se queda
#
# El paso 3 es el que no se puede saltar: una huella calculada en la Forja
# certifica el fichero de la Forja. Lo que hay que certificar es lo que llegó.
# Ya hay cicatriz en esta casa: "nada conserva su verdad al cambiar de sitio".
#
# El paso 2 tampoco: `descarga.presente()` compara el sha256 del cerebro contra
# el catálogo firmado. Sobrescribirlo rompe la integridad que el producto
# promete. Ver README §3.
#
# CERROJO: sin --ejecutar solo dice lo que haría.
set -uo pipefail

GGUF="${1:-}"; VERSION="${2:-v1}"; EJECUTAR=0
[ "${3:-}" = "--ejecutar" ] && EJECUTAR=1

# La casa del teléfono NO se incrusta aquí. Un repo que lleva dentro la ruta
# de una máquina concreta deja de ser publicable, y además miente el día que
# esa máquina cambie. La declara quien opera:
#     export AURELIUS_TERMUX_HOME=...   (la home de Termux en el teléfono)
TEL_HOME="${AURELIUS_TERMUX_HOME:?declara AURELIUS_TERMUX_HOME antes de sincronizar}"
CASA_TEL="$TEL_HOME/.aurelius"
REPO_TEL="$TEL_HOME/aurelius"
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

az() { printf '\033[38;5;141m··\033[0m %s\n' "$1"; }
nota() { printf '\033[38;5;103m   %s\033[0m\n' "$1"; }
muere() { printf '\n✗ %s\n' "$1" >&2; exit 1; }

printf '\n\033[38;5;141mSYNC GUARDIAN\033[0m · Forja → Doogee\n\n'

[ -n "$GGUF" ] || muere "uso: guardian_sync.sh RUTA.gguf [version] [--ejecutar]"
[ -f "$GGUF" ] || muere "no existe $GGUF"
command -v adb >/dev/null || muere "adb no está"
adb get-state >/dev/null 2>&1 || muere "no hay teléfono conectado"

SELLO_ORIGEN="$(sha256sum "$GGUF" | cut -d' ' -f1)"
DESTINO="modelos/afinado-${VERSION}.gguf"

az "Plan"
nota "origen   $GGUF"
nota "sello    ${SELLO_ORIGEN:0:16}…  (en la Forja)"
nota "destino  $CASA_TEL/$DESTINO"
nota "el cerebro base NO se toca"

if [ "$EJECUTAR" -eq 0 ]; then
  printf '\n\033[38;5;103mCERROJO: nada se ha copiado. Añade --ejecutar.\033[0m\n\n'
  exit 0
fi

az "1 · Copia de seguridad del registro"
adb shell "run-as com.termux cp $CASA_TEL/cerebro.json $CASA_TEL/cerebro.json.bak" \
  2>/dev/null || nota "no había registro previo (primera vez)"

az "2 · Empujando el GGUF"
adb push "$GGUF" "/data/local/tmp/afinado-${VERSION}.gguf" >/dev/null \
  || muere "adb push falló"
adb shell "mkdir -p $CASA_TEL/modelos && cp /data/local/tmp/afinado-${VERSION}.gguf $CASA_TEL/$DESTINO && rm /data/local/tmp/afinado-${VERSION}.gguf" \
  || muere "no pude colocarlo en la casa del producto"
nota "colocado"

az "3 · Huella MEDIDA en el destino"
SELLO_DESTINO="$(adb shell "sha256sum $CASA_TEL/$DESTINO" | cut -d' ' -f1 | tr -d '\r')"
nota "destino  ${SELLO_DESTINO:0:16}…"
[ "$SELLO_ORIGEN" = "$SELLO_DESTINO" ] \
  || muere "la huella cambió al viajar. No declaro lo que no llegó entero."

adb shell "cd $REPO_TEL && python3 -c \"
import sys; sys.path.insert(0,'$AQUI/integracion')
import motor_afinado as M
M.promover('$CASA_TEL', '$CASA_TEL/$DESTINO', '$VERSION', 'sync $(date -u +%FT%TZ)')
print('declarado')\"" || muere "no pude declarar el afinado"

az "4 · La suite, en el teléfono"
if adb shell "cd $REPO_TEL && python3 $AQUI/pruebas/guardian_tester.py \
     --modelo $CASA_TEL/$DESTINO --test-no-data --test-fusible --ejecutar \
     --informe $CASA_TEL/tester.json"; then
  az "5 · Verde · el afinado se queda"
  nota "el turno siguiente ya lo usa: el motor es un hijo por turno, sin reinicio"
  exit 0
fi

az "5 · ROJO · rollback"
adb shell "cd $REPO_TEL && python3 -c \"
import sys; sys.path.insert(0,'$AQUI/integracion')
import motor_afinado as M
M.rollback('$CASA_TEL', 'tester supero el umbral')
print('vuelto al base')\""
nota "el afinado NO se ha borrado: un rollback no destruye pruebas"
exit 1
