#!/usr/bin/env bash
# FASE 0c · ¿existe de verdad el "fallback soberano"? Comprueba, no compila.
#
# El plan lo llama "mismo stack que la inferencia". Medido el 2026-08-20 en
# este nodo: llama.cpp build 10488 trae `llama-cli` y `llama-completion`, y
# ningún binario de entrenamiento. Eso no lo hace imposible: lo hace no
# verificado, que es otra cosa y se dice distinto.
set -uo pipefail

az() { printf '\033[38;5;141m··\033[0m %s\n' "$1"; }
nota() { printf '\033[38;5;103m   %s\033[0m\n' "$1"; }

printf '\n\033[38;5;141mFALLBACK SOBERANO\033[0m · llama.cpp\n\n'

az "Binarios en PATH"
for b in llama-cli llama-completion llama-finetune llama-export-lora llama-quantize; do
  if command -v "$b" >/dev/null 2>&1; then nota "SI  $b"; else nota "--  $b"; fi
done

az "Versión de lo que hay"
command -v llama-cli >/dev/null && llama-cli --version 2>&1 | head -2 | sed 's/^/   /'

az "Fuentes"
FUENTE="${LLAMA_CPP_SRC:-$HOME/.llama.cpp}"
if [ -d "$FUENTE/.git" ]; then
  nota "árbol en $FUENTE"
  if [ -d "$FUENTE/examples/finetune" ] || [ -d "$FUENTE/tools/finetune" ]; then
    nota "el ejemplo de entrenamiento EXISTE aguas arriba"
  else
    nota "NO encuentro el ejemplo de entrenamiento en este árbol"
  fi
else
  nota "NO_DATA · no hay árbol de fuentes en $FUENTE"
  nota "sin fuentes no se puede afirmar que el fallback exista"
fi

printf '\n\033[38;5;103mNo se ha compilado nada. Esto solo mira.\033[0m\n\n'
