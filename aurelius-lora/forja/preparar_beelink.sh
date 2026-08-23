#!/usr/bin/env bash
# FASE 0b · prepara la forja en el Beelink. Idempotente y con cerrojo.
#
# NO usa sudo: en este nodo no hay contraseña cacheada, y un guion que la pide
# a mitad se queda colgado esperando a nadie. Todo por `uv`, en el home.
#
# Por qué un entorno aparte: el intérprete del sistema es 3.14 y torch no
# publica ruedas para él. Y porque la forja tiene dependencias pesadas que el
# producto no debe ver jamás -- aurelius es biblioteca estándar y se queda así.
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${AURELIUS_LORA_VENV:-$HOME/.venvs/aurelius-forja}"
PYVER="3.12"
EJECUTAR=0
[ "${1:-}" = "--ejecutar" ] && EJECUTAR=1

az() { printf '\033[38;5;141m··\033[0m %s\n' "$1"; }
nota() { printf '\033[38;5;103m   %s\033[0m\n' "$1"; }
muere() { printf '\n✗ %s\n' "$1" >&2; exit 1; }

printf '\n\033[38;5;141mAURELIUS · LA FORJA\033[0m · preparación del Beelink\n\n'

az "Lo que hay"
command -v uv >/dev/null || muere "uv no está. Sin él no monto nada a mano."
nota "uv     $(uv --version 2>&1 | head -1)"
nota "python $(python3 --version 2>&1) (del sistema · no se toca)"
nota "libre  $(df -h "$HOME" | awk 'NR==2{print $4}') en $HOME"
nota "RAM    $(free -g | awk 'NR==2{print $7}') GiB disponibles"

az "Lo que haría"
nota "crear  $VENV con python $PYVER"
nota "poner  torch (CPU), transformers, peft, datasets, trl, accelerate"
nota "NO pone bitsandbytes: su NF4 es CUDA y aquí no hay NVIDIA (ver README §2 B1)"
nota "NO pone unsloth por defecto: ver README §2 B2 y forja/minirun.py"

if [ "$EJECUTAR" -eq 0 ]; then
  printf '\n\033[38;5;103mCERROJO: no se ha instalado nada. Añade --ejecutar.\033[0m\n\n'
  exit 0
fi

az "Entorno"
if [ -d "$VENV" ]; then
  nota "ya existía: $VENV"
else
  uv venv --python "$PYVER" "$VENV" || muere "uv no pudo crear el entorno"
  nota "creado: $VENV"
fi

az "Dependencias de la forja"
# El índice de CPU es explícito: sin él, pip trae la rueda con CUDA -- cientos
# de MB de kernels para una GPU que este nodo no tiene.
VIRTUAL_ENV="$VENV" uv pip install --python "$VENV/bin/python" \
    --index-url https://download.pytorch.org/whl/cpu torch \
    || muere "no pude instalar torch-CPU"
VIRTUAL_ENV="$VENV" uv pip install --python "$VENV/bin/python" \
    -r "$AQUI/forja/requisitos.txt" \
    || muere "no pude instalar el resto"
nota "listo"

az "Sonda"
"$VENV/bin/python" "$AQUI/forja/minirun.py" --escribir || true

printf '\n\033[38;5;141mForja preparada.\033[0m Nada se ha entrenado.\n'
printf '  Siguiente:  %s/bin/python %s/forja/minirun.py --ejecutar\n\n' "$VENV" "$AQUI"
