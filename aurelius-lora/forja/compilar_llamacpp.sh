#!/usr/bin/env bash
# FASE 0d · compila llama.cpp en el Beelink · DESBLOQUEA LA FASE 4
#
# Se corre ANTES de la Fase 2: sin herramientas de exportación no hay Fase 4, y
# entrenar algo que no se puede llevar al teléfono es entrenar para el cajón.
#
# DESVIACIÓN DECLARADA · `make` ya no existe
# ------------------------------------------
# La orden firmada decía `make`. El Makefile de llama.cpp es hoy una lápida:
# aborta con "Build system changed: The Makefile build has been replaced by
# CMake". Medido sobre el árbol clonado el 2026-08-20. Se usa CMake, que es lo
# que el propio proyecto manda. No es una sustitución silenciosa: es esta nota.
#
# LO QUE SE VERIFICÓ AGUAS ARRIBA, ANTES DE ESCRIBIR ESTO
# -------------------------------------------------------
#   examples/training/finetune.cpp  →  target `llama-finetune`   ✓ existe
#   tools/export-lora               →  target `llama-export-lora` ✓ existe
#   tools/quantize                  →  target `llama-quantize`    ✓ existe
#   convert_lora_to_gguf.py         →  adapter PEFT a GGUF        ✓ existe
#
# El cuarto es el que de verdad desatasca la Fase 4: convierte el adapter que
# produce PEFT, sin pasar por `llama-finetune` en absoluto.
set -uo pipefail

FUENTE="${LLAMA_CPP_SRC:-$HOME/.llama.cpp}"
REPO="https://github.com/ggerganov/llama.cpp"
DESTINO_BIN="${LLAMA_CPP_BIN:-$HOME/.local/bin}"
NUCLEOS="$(nproc)"
EJECUTAR=0
[ "${1:-}" = "--ejecutar" ] && EJECUTAR=1

az() { printf '\033[38;5;141m··\033[0m %s\n' "$1"; }
nota() { printf '\033[38;5;103m   %s\033[0m\n' "$1"; }
muere() { printf '\n✗ %s\n' "$1" >&2; exit 1; }

OBJETIVOS=(llama-finetune llama-export-lora llama-quantize)

printf '\n\033[38;5;141mLLAMA.CPP\033[0m · compilación en la Forja\n\n'
az "Plan"
nota "fuentes   $FUENTE"
nota "objetivos ${OBJETIVOS[*]}"
nota "núcleos   $NUCLEOS"
nota "build     CMake (el Makefile está retirado aguas arriba)"

if [ "$EJECUTAR" -eq 0 ]; then
  printf '\n\033[38;5;103mCERROJO: no se ha clonado ni compilado nada. Añade --ejecutar.\033[0m\n\n'
  exit 0
fi

command -v cmake >/dev/null || muere "cmake no está, y sin sudo no lo instalo. Para."
command -v git   >/dev/null || muere "git no está."

az "1 · Fuentes"
if [ -d "$FUENTE/.git" ]; then
  git -C "$FUENTE" pull --ff-only >/dev/null 2>&1 || nota "sin cambios nuevos"
  nota "ya estaban; actualizadas"
else
  git clone --depth 1 "$REPO" "$FUENTE" >/dev/null 2>&1 || muere "no pude clonar $REPO"
  nota "clonadas en $FUENTE"
fi
nota "commit $(git -C "$FUENTE" rev-parse --short HEAD)"

az "2 · Configuración"
# GGML_NATIVE=OFF a proposito: un binario compilado con -march=native en este
# Ryzen puede no arrancar en otro metal, y esta casa mueve binarios entre
# maquinas. Se pierde algo de velocidad y se gana que el binario sea portable.
cmake -S "$FUENTE" -B "$FUENTE/build" \
      -DCMAKE_BUILD_TYPE=Release \
      -DLLAMA_CURL=OFF \
      -DGGML_NATIVE=OFF \
      -DLLAMA_BUILD_TESTS=OFF \
      -DLLAMA_BUILD_EXAMPLES=ON \
      -DLLAMA_BUILD_TOOLS=ON >/dev/null 2>&1 \
  || muere "cmake no pudo preparar la compilación"
nota "configurado"

az "3 · Compilación · $NUCLEOS núcleos"
for objetivo in "${OBJETIVOS[@]}"; do
  printf '   %-20s ' "$objetivo"
  if cmake --build "$FUENTE/build" --target "$objetivo" -j"$NUCLEOS" >/dev/null 2>&1; then
    printf 'ok\n'
  else
    printf 'FALLO\n'
    muere "no pude compilar $objetivo. No sigo: media forja parece una forja."
  fi
done

az "4 · Verificación · el disco manda, no el log del compilador"
FALTAN=0
mkdir -p "$DESTINO_BIN"
for objetivo in "${OBJETIVOS[@]}"; do
  BIN="$(find "$FUENTE/build" -name "$objetivo" -type f -perm -u+x 2>/dev/null | head -1)"
  if [ -n "$BIN" ]; then
    ln -sf "$BIN" "$DESTINO_BIN/$objetivo"
    nota "SI  $objetivo → $DESTINO_BIN/$objetivo"
  else
    nota "NO  $objetivo · compiló y no encuentro el binario"
    FALTAN=1
  fi
done

CONV="$FUENTE/convert_lora_to_gguf.py"
[ -f "$CONV" ] && nota "SI  convert_lora_to_gguf.py" || { nota "NO  convert_lora_to_gguf.py"; FALTAN=1; }

if [ "$FALTAN" -ne 0 ]; then
  printf '\n✗ Falta alguna herramienta. La FASE 4 sigue bloqueada.\n\n' >&2
  exit 1
fi

printf '\n\033[38;5;141mForja completa.\033[0m FASE 4 desbloqueada.\n'
printf '  La cadena de exportación queda:\n'
printf '    adapter PEFT → convert_lora_to_gguf.py → llama-export-lora → llama-quantize\n\n'
