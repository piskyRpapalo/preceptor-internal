#!/usr/bin/env bash
# init_doogee.sh · el campo de pruebas, desde cero
#
# STAGING PRIVADO. No forma parte de aurelius y no viaja al clon publico:
# esto inicializa UNA maquina concreta, y una ruta de maquina en un repo
# publicable es justo lo que la guardia de higiene rechaza.
#
# ESTADO DECLARADO · 2026-08-21
# -----------------------------
# El Doogee S110 se reseteo a fabrica. Todo lo que este guion daba por hecho
# en la sesion anterior -- Termux, el clon, el cerebro de 2,3 GiB, la voz, la
# memoria con un recuerdo -- es NO_DATA: no esta y no se recupera. Se construye
# de nuevo, y esta vez con el guion delante en vez de a mano.
#
# LO QUE NO HACE, Y ES LA MITAD DE SU VALOR
# ------------------------------------------
# * No instala nada sin `--ejecutar`. Sin la bandera dice lo que haria.
# * No toca ajustes de Android, no concede permisos y no activa nada por ti.
#   Depuracion USB y red las pone el carbono, a mano, mirando la pantalla.
# * No descarga el cerebro ni la voz: eso lo ofrece el producto, con su
#   licencia y su huella delante, y lo acepta la persona. Aqui se prepara la
#   casa; quien entra lo decide quien vive en ella.
# * No compila llama.cpp: para eso ya existe `bin/instalar-android` dentro del
#   propio repo, con sus dos puertas. Reimplementarlo aqui seria tener dos
#   verdades sobre como se instala el motor.
set -uo pipefail

EJECUTAR=0
[ "${1:-}" = "--ejecutar" ] && EJECUTAR=1

TERMUX_VER="${TERMUX_VER:-0.118.3}"
TERMUX_APK="termux-app_v${TERMUX_VER}+github-debug_universal.apk"
TERMUX_URL="https://github.com/termux/termux-app/releases/download/v${TERMUX_VER}/${TERMUX_APK}"
DESCARGAS="${DESCARGAS:-$HOME/.cache/doogee}"
REPO="${AURELIUS_REPO:-https://github.com/piskyRpapalo/PreceptorOS}"
PAQUETES="git python clang cmake make"

az()   { printf '\033[38;5;141m··\033[0m %s\n' "$1"; }
nota() { printf '\033[38;5;103m   %s\033[0m\n' "$1"; }
muere(){ printf '\n✗ %s\n' "$1" >&2; exit 1; }

tel() { adb shell "$@"; }
en_termux() { adb shell "am start -n com.termux/.HomeActivity" >/dev/null 2>&1; }

printf '\n\033[38;5;141mDOOGEE S110\033[0m · inicializacion del campo de pruebas\n\n'

# --- 0 · lo que el carbono tiene que haber hecho antes ---------------------
# Tras un reset de fabrica la depuracion USB vuelve a estar APAGADA. Medido el
# 2026-08-21: `adb devices` no lista nada. Ningun guion enciende eso por ti, y
# el que lo intentara estaria tocando ajustes de seguridad del telefono.
az "0 · Requisitos que pone el carbono, a mano"
nota "a) Ajustes → Acerca del telefono → pulsar 7 veces en 'Numero de compilacion'"
nota "b) Opciones de desarrollador → Depuracion USB → activar"
nota "c) Aceptar la huella RSA que sale al conectar el cable"
nota "d) RED en el telefono (WiFi o datos): sin ella 'pkg install' no puede bajar nada"

if ! adb get-state >/dev/null 2>&1; then
  printf '\n\033[38;5;103mNo veo el telefono por adb.\033[0m Haz (a), (b) y (c) y vuelve.\n\n'
  [ "$EJECUTAR" -eq 1 ] && exit 1 || exit 0
fi
nota "telefono visible: $(adb devices | awk 'NR==2{print $1}')"

az "Plan"
nota "1  Termux $TERMUX_VER desde las releases oficiales de GitHub"
nota "2  paquetes base: $PAQUETES"
nota "3  clonar el producto desde $REPO"
nota "4  el motor, delegado a bin/instalar-android del propio repo"
nota "5  verificacion de hardware: CPU, RAM, Vulkan"

if [ "$EJECUTAR" -eq 0 ]; then
  printf '\n\033[38;5;103mCERROJO: no se ha instalado nada. Anade --ejecutar.\033[0m\n\n'
  exit 0
fi

# --- 1 · Termux ------------------------------------------------------------
# Termux se retiro de Google Play; la via oficial es F-Droid o las releases del
# proyecto. Se usa GitHub porque se puede verificar el fichero antes de
# instalarlo, y F-Droid obligaria a instalar primero otra tienda.
az "1 · Termux"
if tel pm list packages 2>/dev/null | grep -q com.termux; then
  nota "ya estaba instalado"
else
  mkdir -p "$DESCARGAS"
  if [ ! -s "$DESCARGAS/$TERMUX_APK" ]; then
    command -v curl >/dev/null || muere "curl no esta"
    curl -fsSL -o "$DESCARGAS/$TERMUX_APK" "$TERMUX_URL" \
      || muere "no pude bajar Termux de $TERMUX_URL"
  fi
  # La huella se ANOTA, no se compara contra nada: este proyecto no tiene una
  # firma de Termux con la que cotejar, y decir "verificado" sin tener contra
  # que seria fabricar una comprobacion. Se deja escrita para que la proxima
  # instalacion pueda compararse con esta.
  nota "sha256 $(sha256sum "$DESCARGAS/$TERMUX_APK" | cut -c1-16)… (anotado, SIN VERIFICAR contra firma oficial)"
  nota "$(du -h "$DESCARGAS/$TERMUX_APK" | cut -f1)"
  adb install -r "$DESCARGAS/$TERMUX_APK" >/dev/null 2>&1 \
    || muere "adb install fallo. Mira la pantalla: puede pedir confirmacion."
  nota "instalado"
fi

en_termux; sleep 6
nota "Termux abierto. Los pasos siguientes se TECLEAN en el, no por adb shell:"
nota "adb shell no ve el disco de Termux (no es depurable), asi que la unica"
nota "via es el teclado virtual. Verifica el prompt libre ANTES de teclear."

# --- 2 · red, antes de pedir paquetes -------------------------------------
az "2 · Red en el telefono"
if tel "ping -c1 -W2 1.1.1.1" >/dev/null 2>&1; then
  nota "hay salida a internet"
else
  muere "el telefono no tiene red. 'pkg install' no puede bajar nada. Pon WiFi y vuelve."
fi

# --- 3, 4 y 5 · dentro de Termux ------------------------------------------
# Se imprimen para teclear. No se envian con `input text`: el escapado de
# comillas de `input text` ya abrio un selector de ficheros del sistema una vez
# (2026-08-21), y un guion no debe reproducir una trampa conocida.
az "3-5 · Lo que se teclea EN Termux, en este orden"
cat <<'ORDENES'
   termux-change-repo        # elegir un espejo cercano si pkg va lento
   pkg update -y && pkg upgrade -y
   pkg install -y git python clang cmake make
   git clone --depth 1 https://github.com/piskyRpapalo/PreceptorOS ~/aurelius
   cd ~/aurelius && bash bin/instalar-android
   python3 aurelius.py               # crear la memoria, si la persona quiere
ORDENES

az "5 · Verificacion de hardware · lo que se anota antes de prometer nada"
cat <<'MEDIDAS'
   nproc                                   # nucleos
   free -h                                 # RAM real
   cat /proc/cpuinfo | grep -m1 'model name\|Hardware'
   getprop ro.product.model                # el modelo, de boca del sistema
   llama-cli --version                     # backend y build, tras instalar
MEDIDAS
nota "Vulkan: el paquete llama-cpp-backend-vulkan instala y CARGA en este"
nota "telefono, y aun asi dice 'ggml_vulkan: No devices found' (medido"
nota "2026-08-19). La etiqueta del bench es del backend, no de un dispositivo."
nota "Si vuelve a salir, la cifra honesta sigue siendo CPU."

printf '\n\033[38;5;141mCasa preparada.\033[0m El cerebro y la voz los ofrece el producto.\n\n'
