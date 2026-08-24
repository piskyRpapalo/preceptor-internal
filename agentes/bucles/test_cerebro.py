#!/usr/bin/env python3
"""Pruebas del cerebro local. Solo biblioteca estándar.

    python3 agentes/bucles/test_cerebro.py

No prueban que el modelo acierte —eso no se prueba en una suite— sino que el
bucle **no se trague el banner como si fuera la respuesta**. Un recorte que
falla no revienta: devuelve texto plausible, y el bucle actúa sobre él.
"""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cerebro as C  # noqa: E402


# La salida REAL de `llama-cli` de este build, con su banner y su pie.
SALIDA_REAL = """Loading model... |\x08-\x08\\\x08
build      : b10068-571d0d540
model      : /home/x/modelo.gguf
ftype      : Q4_K - Medium

available commands:
  /exit or Ctrl+C     stop or exit

> Responde solo con la palabra: listo
listo

[ Prompt: 15,2 t/s | Generation: 6,9 t/s ]


Exiting..."""


class TestRecorte(unittest.TestCase):

    def test_devuelve_la_respuesta_y_no_el_banner(self):
        texto, _ = C._limpiar(SALIDA_REAL, "Responde solo con la palabra: listo")
        self.assertEqual(texto, "listo")

    def test_el_banner_no_se_cuela(self):
        texto, _ = C._limpiar(SALIDA_REAL, "Responde solo con la palabra: listo")
        for basura in ("build", "ftype", "/exit", "Loading model", "Exiting"):
            self.assertNotIn(basura, texto, f"se coló «{basura}» en la respuesta")

    def test_saca_los_tok_s_del_propio_motor(self):
        """Mejor la medida del motor que mi cuenta de palabras."""
        _, m = C._limpiar(SALIDA_REAL, "Responde solo con la palabra: listo")
        self.assertAlmostEqual(m["tok_s_prompt"], 15.2)
        self.assertAlmostEqual(m["tok_s_generacion"], 6.9)

    def test_la_coma_decimal_no_rompe_el_numero(self):
        """El binario imprime «6,9» en esta locale. `float("6,9")` revienta."""
        self.assertEqual(C._numero("6,9"), 6.9)
        self.assertEqual(C._numero("15.2"), 15.2)
        self.assertIsNone(C._numero("no es un numero"))

    def test_una_respuesta_de_varias_lineas_llega_entera(self):
        salida = ("banner\n> dime tres cosas\nuna\ndos\ntres\n\n"
                  "[ Prompt: 10,0 t/s | Generation: 5,0 t/s ]\nExiting...")
        texto, _ = C._limpiar(salida, "dime tres cosas")
        self.assertEqual(texto, "una\ndos\ntres")

    def test_sin_pie_de_metricas_no_inventa_medidas(self):
        texto, m = C._limpiar("banner\n> hola\nadios", "hola")
        self.assertEqual(texto, "adios")
        self.assertEqual(m, {}, "inventó métricas que el motor no dio")

    def test_un_prompt_que_contiene_la_marca_no_confunde_el_corte(self):
        """Si el prompt lleva «> » dentro, se toma el ÚLTIMO eco, no el primero."""
        prompt = "traduce esto: > hola"
        salida = f"banner\n> {prompt}\nla traduccion\n\n[ Prompt: 1,0 t/s | Generation: 1,0 t/s ]"
        texto, _ = C._limpiar(salida, prompt)
        self.assertEqual(texto, "la traduccion")

    def test_salida_vacia_no_revienta(self):
        self.assertEqual(C._limpiar("", "hola"), ("", {}))
        self.assertEqual(C._limpiar(None, "hola"), ("", {}))


class TestGuardas(unittest.TestCase):

    def test_sin_binario_se_declara_en_vez_de_caer_a_CPU(self):
        """Degradarse a CPU en silencio triplica el tiempo sin que nadie lo note
        hasta que mira el reloj de pared un mes después."""
        with tempfile.TemporaryDirectory() as d, \
             mock.patch.object(C, "VULKAN", d):
            est, detalle = C.estado()
            self.assertEqual(est, "NO_DATA")
            self.assertIn("Vulkan", detalle)
            with self.assertRaises(C.SinCerebro):
                C.pensar("lo que sea")

    def test_sin_modelo_tambien_se_declara(self):
        with tempfile.TemporaryDirectory() as d:
            binario = os.path.join(d, "llama-cli")
            open(binario, "w").close()
            os.chmod(binario, 0o755)
            with mock.patch.object(C, "VULKAN", d), \
                 mock.patch.object(C, "MODELO", "/no/existe.gguf"):
                self.assertEqual(C.estado()[0], "NO_DATA")

    def test_el_razonamiento_va_apagado_y_no_es_negociable(self):
        """A 5 tok/s cada token de pensamiento invisible es tiempo de pared.
        Medido: 45 tokens para decir «listo»."""
        vistas = []

        class Falsa:
            returncode = 0
            stdout = "> hola\nlisto\n"
            stderr = ""

        with tempfile.TemporaryDirectory() as d:
            binario = os.path.join(d, "llama-cli")
            open(binario, "w").close()
            os.chmod(binario, 0o755)
            modelo = os.path.join(d, "m.gguf")
            open(modelo, "w").close()
            with mock.patch.object(C, "VULKAN", d), \
                 mock.patch.object(C, "MODELO", modelo), \
                 mock.patch.object(C.subprocess, "run",
                                   lambda o, **k: (vistas.append(o), Falsa())[1]):
                C.pensar("hola")
        orden = vistas[0]
        self.assertIn("--reasoning", orden)
        self.assertEqual(orden[orden.index("--reasoning") + 1], "off")

    def test_JAMAS_prompt_cache_all(self):
        """`-all` guardaría también lo que se le manda y lo que contesta, en un
        fichero grande y sin cifrar. Esto es un acelerador, no un registro."""
        vistas = []

        class Falsa:
            returncode = 0
            stdout = "> hola\nlisto\n"
            stderr = ""

        with tempfile.TemporaryDirectory() as d:
            binario = os.path.join(d, "llama-cli")
            open(binario, "w").close()
            os.chmod(binario, 0o755)
            modelo = os.path.join(d, "m.gguf")
            open(modelo, "w").close()
            with mock.patch.object(C, "VULKAN", d), \
                 mock.patch.object(C, "MODELO", modelo), \
                 mock.patch.object(C.subprocess, "run",
                                   lambda o, **k: (vistas.append(o), Falsa())[1]):
                C.pensar("hola")
        self.assertNotIn("--prompt-cache-all", vistas[0])
        self.assertIn("--prompt-cache", vistas[0])


class TestNoAbrePuertos(unittest.TestCase):
    """D68: un puerto local es indistinguible de un túnel. Levantar
    `llama-server` es una decisión del Soberano, no la comodidad de un bucle."""

    def test_el_modulo_no_habla_por_red(self):
        import ast
        from pathlib import Path
        fuente = Path(__file__).parent / "cerebro.py"
        arbol = ast.parse(fuente.read_text(encoding="utf-8"))
        importados = set()
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.Import):
                importados.update(a.name.split(".")[0] for a in nodo.names)
            elif isinstance(nodo, ast.ImportFrom) and nodo.module:
                importados.add(nodo.module.split(".")[0])
        prohibidos = {"socket", "http", "urllib", "requests", "asyncio", "ssl"}
        self.assertEqual(importados & prohibidos, set(),
                         "el cerebro de los bucles abrió una puerta de red")


if __name__ == "__main__":
    unittest.main(verbosity=2)
