#!/usr/bin/env python3
"""El cerebro local, para los bucles. **Solo biblioteca estándar.**

Todo bucle de L3 necesita lo mismo: hablar con el 27B sin repetir los tres
errores que este fichero ya lleva resueltos y medidos. Sin esto, cada bucle los
descubre por su cuenta y los descubre tarde — de madrugada, sin nadie mirando.

LOS TRES ERRORES, MEDIDOS EL 2026-08-25
---------------------------------------

**1 · El binario del PATH no tiene GPU.** `~/.local/bin/llama-cli` responde
`(none)` a `--list-devices`: es CPU pura. El que trae Vulkan vive en
`soberano-bench`. Medido con el mismo modelo y la misma herramienta:

    CPU    (-ngl 0)    22,76 tok/s prompt · 2,74 tok/s generación
    Vulkan (-ngl 99)   67,17 tok/s prompt · 4,63 tok/s generación
                       ×2,95              · ×1,69

Un bucle que coja el binario equivocado corre a un tercio de velocidad **sin
decirlo**. Aquí se elige el bueno, y si no está se PARA en vez de degradarse en
silencio: un bucle nocturno que tarda el triple no lo nota nadie hasta que
alguien mira el reloj de pared un mes después.

**2 · El razonamiento viene encendido.** Medido con «responde solo con la
palabra: listo»: **45 tokens de pensamiento interno para decir una palabra**, y
4,7 tok/s. Con `--reasoning off`: cero pensamiento, 6,9 tok/s, respuesta
directa. A 5 tok/s cada token invisible es tiempo de pared. En un bucle eso no
es una ineficiencia: es la diferencia entre terminar antes del amanecer y no
terminar. **Aquí va siempre apagado, y no es configurable.**

**3 · El prompt de sistema se reprocesa entero en cada llamada.** Medido hoy
sobre el 4B de PreceptorOS: con `--prompt-cache`, el primer token pasó de 17,7 s
a 2,4 s en el Beelink y de 337 s a 7,3 s en el teléfono. Un bucle que llama N
veces con las mismas instrucciones delante paga N veces por leerlas. Con caché,
una.

LO QUE ESTE MÓDULO NO HACE
--------------------------
**No abre ningún puerto.** Proceso hijo por entrada y salida estándar, como
`conversacion.motor_llama` en el producto. La razón está escrita allí (D68): *un
puerto local es indistinguible de un túnel*. Levantar `llama-server` para que
los bucles le peguen por HTTP es una decisión aparte, del Soberano, y no se toma
de paso por comodidad de un bucle.

**No decide si merece la pena llamar.** Eso es de quien llama, y es la regla de
oro del nodo: retrieval primero, después determinista, y el modelo **solo si lo
anterior no basta**. Este módulo es el último escalón, no el primero.
"""
from __future__ import annotations

import os
import re
import subprocess
import time

# El build con Vulkan. Se declara por entorno para que una prueba pueda apuntar
# a otro sitio sin tocar el de verdad.
VULKAN = os.path.expanduser(os.environ.get(
    "CEREBRO_VULKAN",
    "~/p0x/soberano-bench/bin/llama-b10068-bin-ubuntu-vulkan-x64/llama-b10068"))
MODELO = os.path.expanduser(os.environ.get(
    "CEREBRO_MODELO",
    "~/ia-models/qwen-uncensored/Qwen3.8-27B-Uncensored-OrcaRouter-Q4_K_M.gguf"))

# Medido: 32K carga y responde con la GPU llena y 50 GB de RAM libres. Por
# encima, NO_DATA -- y este canon exige `num_ctx` demostrado por dato.
CONTEXTO = int(os.environ.get("CEREBRO_CONTEXTO", "32768"))
CAPAS_GPU = 99
HILOS = int(os.environ.get("CEREBRO_HILOS", "8"))     # 8 nucleos fisicos

# A 4,6 tok/s, 512 tokens son casi dos minutos. El tope va bajo a proposito: un
# bucle que necesita mas de esto casi siempre necesita otra cosa -- partir la
# tarea -- y no mas tokens.
TOPE_TOKENS = int(os.environ.get("CEREBRO_TOPE", "512"))
ESPERA_S = int(os.environ.get("CEREBRO_ESPERA", "900"))

RUTA_CACHE = os.path.expanduser(
    os.environ.get("CEREBRO_CACHE", "~/.aurelius/cache_bucles.bin"))


class SinCerebro(RuntimeError):
    """No hay con qué pensar. Es una ausencia declarada, no un fallo mudo."""


class SeAgotoElTiempo(RuntimeError):
    """Estaba trabajando y no le dio tiempo. No es lo mismo que fallar."""


def _binario():
    ruta = os.path.join(VULKAN, "llama-cli")
    return ruta if os.path.isfile(ruta) and os.access(ruta, os.X_OK) else None


def estado():
    """('LISTO'|'NO_DATA', detalle). Lo que hay, sin adornar."""
    if _binario() is None:
        return "NO_DATA", f"no está el binario Vulkan en {VULKAN}"
    if not os.path.isfile(MODELO):
        return "NO_DATA", f"no está el modelo en {MODELO}"
    return "LISTO", f"{os.path.basename(MODELO)} · Vulkan · contexto {CONTEXTO}"


def _tiene_gpu(binario):
    """Que el binario ENUMERE la GPU, no que se llame «vulkan».

    Comprobar el nombre del directorio sería fiarse de una etiqueta. Se le
    pregunta al binario, que es quien lo sabe.
    """
    try:
        r = subprocess.run([binario, "--list-devices"], capture_output=True,
                           text=True, timeout=120, stdin=subprocess.DEVNULL,
                           env=dict(os.environ, LD_LIBRARY_PATH=VULKAN))
    except Exception:
        return False
    return "Vulkan" in (r.stdout + r.stderr)


def pensar(prompt, tope_tokens=None, espera=None, cache=True, temperatura=0.2):
    """Una llamada al modelo local. Devuelve (texto, medidas).

    `medidas` trae `ms`, `palabras` y `palabras_por_s`. Se devuelven SIEMPRE,
    porque un bucle que no sabe lo que costó su propia llamada no puede decidir
    mañana si merecía la pena — y esa decisión es la regla de oro del nodo.

    `temperatura` baja por defecto: un bucle quiere la misma respuesta ante la
    misma entrada. La creatividad es para el chat.
    """
    binario = _binario()
    if binario is None or not os.path.isfile(MODELO):
        _, detalle = estado()
        raise SinCerebro(detalle)

    orden = [
        binario, "-m", MODELO,
        "-ngl", str(CAPAS_GPU),
        "-c", str(CONTEXTO),
        "-n", str(tope_tokens or TOPE_TOKENS),
        "-t", str(HILOS),
        "--temp", str(temperatura),
        "-st", "--no-warmup", "--no-display-prompt",
        # No configurable, y a proposito. Ver el error nº2 del docstring.
        "--reasoning", "off",
        "-p", prompt,
    ]
    if cache:
        # NUNCA `--prompt-cache-all`: esa variante guardaria tambien lo que se
        # le manda y lo que contesta, en un fichero grande y sin cifrar. Esto
        # es un acelerador, no un registro.
        orden += ["--prompt-cache", RUTA_CACHE]

    entorno = dict(os.environ, LD_LIBRARY_PATH=VULKAN)
    t0 = time.perf_counter()
    try:
        r = subprocess.run(orden, capture_output=True, text=True,
                           timeout=espera or ESPERA_S,
                           stdin=subprocess.DEVNULL, env=entorno)
    except subprocess.TimeoutExpired:
        raise SeAgotoElTiempo(
            f"el modelo pasó de {espera or ESPERA_S} s. A ~5 tok/s eso es "
            f"normal si la tarea era grande: pártela en vez de esperar más.")
    ms = (time.perf_counter() - t0) * 1000

    if r.returncode != 0 and cache:
        # El caché es una optimización: si estorba, se tira y se reintenta sin
        # él. Falla ABIERTO el acelerador; la respuesta sigue fallando cerrado.
        try:
            os.remove(RUTA_CACHE)
        except OSError:
            pass
        return pensar(prompt, tope_tokens, espera, cache=False,
                      temperatura=temperatura)
    if r.returncode != 0:
        raise SinCerebro(f"el modelo salió con código {r.returncode}")

    texto, motor = _limpiar(r.stdout, prompt)
    palabras = len(texto.split())
    medidas = {
        "ms": round(ms, 1),
        "palabras": palabras,
        "palabras_por_s": round(palabras / max(ms / 1000, 0.001), 2),
    }
    medidas.update(motor)      # tok/s del propio motor, si los imprimio
    return texto, medidas


# `llama-cli` escribe su banner, el eco del prompt y un pie de metricas por la
# MISMA salida que la respuesta. `--no-display-prompt` no calla el banner. Se
# recorta aqui y no en cada bucle: un recorte copiado en cinco sitios se corrige
# en cuatro.
#
# Se usa `llama-cli` y no `llama-completion` aunque este ultimo dé la salida
# limpia, porque `llama-completion` de este build NO tiene `--reasoning off` y
# piensa igual -- y el pensamiento no es ruido en la salida, es tiempo de pared
# a 5 tok/s. Mejor limpiar texto que pagar minutos.
_PIE = re.compile(r"\[\s*Prompt:\s*([\d,.]+)\s*t/s\s*\|\s*Generation:\s*([\d,.]+)\s*t/s\s*\]")


def _numero(s):
    try:
        return float(s.replace(",", "."))
    except (ValueError, AttributeError):
        return None


def _limpiar(crudo, prompt):
    """(respuesta, medidas_del_motor). Lo que dijo, sin lo que se dice a si mismo."""
    salida = crudo or ""
    motor = {}
    pie = _PIE.search(salida)
    if pie:
        motor = {"tok_s_prompt": _numero(pie.group(1)),
                 "tok_s_generacion": _numero(pie.group(2))}
        salida = salida[:pie.start()]

    # El eco del prompt marca donde empieza lo suyo. Se busca el ULTIMO, por si
    # el propio prompt contiene la marca.
    marca = "> " + (prompt or "").strip().split("\n")[0]
    corte = salida.rfind(marca)
    if corte >= 0:
        salida = salida[corte + len(marca):]
    elif prompt:
        corte = salida.rfind(prompt.strip().split("\n")[-1])
        if corte >= 0:
            salida = salida[corte + len(prompt.strip().split("\n")[-1]):]

    for basura in ("Exiting...", "Loading model"):
        salida = salida.replace(basura, "")
    return salida.strip(), motor


def main():
    import sys
    est, detalle = estado()
    print(f"cerebro · {est} · {detalle}")
    if est != "LISTO":
        return 1
    binario = _binario()
    print(f"  enumera GPU: {'sí' if _tiene_gpu(binario) else 'NO -- correría en CPU'}")
    if "--probar" in sys.argv[1:]:
        texto, m = pensar("Responde solo con la palabra: listo")
        print(f"  respuesta: {texto!r}")
        print(f"  {m['ms']:.0f} ms · {m['palabras']} palabras · "
              f"{m['palabras_por_s']} pal/s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
