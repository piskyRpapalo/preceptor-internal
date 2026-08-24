#!/usr/bin/env python3
"""Pruebas del Guardián de dependencias. Solo biblioteca estándar.

    python3 agentes/bucles/test_guardian.py

No prueban que corra: prueban que **encuentra**. Un guardián que no falla nunca
es indistinguible de un guardián averiado, y ese es exactamente el modo de fallo
que S0 existe para sospechar. Cada cicatriz documentada en REVISION_CRUZADA §5.1
tiene aquí su prueba, con un intruso puesto a propósito para verlo cazarlo.
"""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guardian as G  # noqa: E402


def arbol(**ficheros):
    """Crea un árbol de mentira. Las claves con `/` crean subcarpetas."""
    d = tempfile.mkdtemp(prefix="guardian_prueba_")
    for nombre, cuerpo in ficheros.items():
        ruta = Path(d) / nombre
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(cuerpo, encoding="utf-8")
    return d


class TestCazaDeVerdad(unittest.TestCase):
    """Cicatriz nº1: el grep de la propuesta no bajaba por las subcarpetas."""

    def test_un_intruso_escondido_hondo_no_se_escapa(self):
        d = arbol(**{"limpio.py": "import os\n",
                     "sub/mas/hondo/colado.py": "import requests\n"})
        hallazgos, mirados = G.revisar(d)
        self.assertEqual(mirados, 2, "no miró el árbol entero")
        claves = [h["clave"] for h in hallazgos]
        self.assertEqual(len(claves), 1, claves)
        self.assertIn("requests", claves[0])
        self.assertIn("sub/mas/hondo/colado.py", claves[0])

    def test_un_import_dentro_de_una_funcion_tampoco(self):
        """`grep "^import"` no ve esto. Por eso se usa `ast` y no `grep`."""
        d = arbol(**{"tardio.py": "def f():\n    import numpy\n    return numpy\n"})
        claves = [h["clave"] for h in G.revisar(d)[0]]
        self.assertTrue(any("numpy" in k for k in claves), claves)

    def test_un_import_dentro_de_un_try_tampoco(self):
        d = arbol(**{"opcional.py":
                     "try:\n    import scipy\nexcept ImportError:\n    scipy = None\n"})
        claves = [h["clave"] for h in G.revisar(d)[0]]
        self.assertTrue(any("scipy" in k for k in claves), claves)

    def test_from_x_import_y_tambien_cuenta(self):
        d = arbol(**{"desde.py": "from yaml import safe_load\n"})
        claves = [h["clave"] for h in G.revisar(d)[0]]
        self.assertTrue(any("yaml" in k for k in claves), claves)


class TestNoDaFalsosPositivos(unittest.TestCase):
    """Cicatriz nº2: una lista blanca de solo stdlib avisa cada noche de los
    módulos del propio proyecto, hasta que alguien apaga el guardián por ruido."""

    def test_la_stdlib_no_es_un_intruso(self):
        d = arbol(**{"a.py": "import os, sys, json, sqlite3, pathlib\n"
                             "from datetime import datetime\n"})
        self.assertEqual(G.revisar(d)[0], [])

    def test_los_modulos_del_propio_arbol_no_son_intrusos(self):
        d = arbol(**{"casa.py": "NOMBRE = '.aurelius'\n",
                     "textos.py": "DEFECTO = 'es'\n",
                     "usa.py": "import casa\nimport textos\n"})
        self.assertEqual(G.revisar(d)[0], [])

    def test_un_modulo_de_una_subcarpeta_tampoco(self):
        d = arbol(**{"paquete/__init__.py": "", "paquete/dentro.py": "x = 1\n",
                     "usa.py": "import paquete\n"})
        self.assertEqual(G.revisar(d)[0], [])

    def test_los_relativos_no_cuentan(self):
        d = arbol(**{"p/__init__.py": "", "p/a.py": "from . import b\n",
                     "p/b.py": "x = 1\n"})
        self.assertEqual(G.revisar(d)[0], [])

    def test_from_future_no_es_un_intruso(self):
        d = arbol(**{"a.py": "from __future__ import annotations\n"})
        self.assertEqual(G.revisar(d)[0], [])


class TestLoConocidoSeDeclara(unittest.TestCase):
    """Cicatriz nº3: un aviso que sale todas las noches se deja de leer."""

    def test_una_dependencia_declarada_no_avisa(self):
        d = arbol(**{"laminas/recortar.py": "from PIL import Image\n"})
        self.assertEqual(G.revisar(d)[0], [],
                         "PIL está declarada en CONOCIDAS y aun así avisó")

    def test_pero_cualquier_otra_si(self):
        """El valor de declarar lo conocido es que lo NUEVO se ve al instante."""
        d = arbol(**{"laminas/recortar.py": "from PIL import Image\n",
                     "otro.py": "import cv2\n"})
        claves = [h["clave"] for h in G.revisar(d)[0]]
        self.assertEqual(len(claves), 1, claves)
        self.assertIn("cv2", claves[0])

    def test_cada_conocida_trae_su_motivo_escrito(self):
        """Sin motivo, dentro de un año nadie sabrá si fue decisión u olvido."""
        for nombre, motivo in G.CONOCIDAS.items():
            self.assertTrue(motivo and motivo.strip() != "",
                            f"`{nombre}` está declarada sin motivo")
            self.assertGreater(len(motivo), 20,
                               f"el motivo de `{nombre}` no explica nada")


class TestNoSeCallaNunca(unittest.TestCase):
    """S0 sospecha del filtro que lleva días en verde sin hallar nada. El
    recuento es lo que deja distinguir «no había nada» de «no miró nada»."""

    def test_cuenta_los_ficheros_mirados_aunque_no_halle_nada(self):
        d = arbol(**{"a.py": "import os\n", "b.py": "import sys\n",
                     "sub/c.py": "import json\n"})
        hallazgos, mirados = G.revisar(d)
        self.assertEqual(hallazgos, [])
        self.assertEqual(mirados, 3, "un cero de hallazgos sin recuento no dice nada")

    def test_un_fichero_ilegible_es_un_hallazgo_y_no_un_silencio(self):
        d = arbol(**{"roto.py": "def (((\n"})
        claves = [h["clave"] for h in G.revisar(d)[0]]
        self.assertTrue(any(k.startswith("ilegible:") for k in claves), claves)

    def test_un_arbol_que_no_existe_se_declara_en_vez_de_dar_verde(self):
        """Apuntar a una ruta que no está daría 0 hallazgos y 0 ficheros: verde
        perfecto por avería total."""
        hallazgos, mirados = G.revisar("/no/existe/este/arbol")
        self.assertEqual(mirados, 0)
        self.assertTrue(any(h["clave"] == "arbol-ausente" for h in hallazgos),
                        "un árbol ausente pasó por bueno")

    def test_no_mira_dentro_de_pycache_ni_de_ocultos(self):
        d = arbol(**{"a.py": "import os\n",
                     "__pycache__/viejo.py": "import requests\n",
                     ".git/hook.py": "import requests\n"})
        hallazgos, mirados = G.revisar(d)
        self.assertEqual(mirados, 1, "miró donde no debía")
        self.assertEqual(hallazgos, [])


class TestElArbolDeVerdad(unittest.TestCase):

    def test_el_arbol_real_esta_limpio_o_lo_dice(self):
        """Si algún día entra una dependencia, que lo diga esta suite y no la
        persona que instala el producto y descubre que le falta algo."""
        if not os.path.isdir(G.ARBOL):
            self.skipTest(f"no está el árbol vigilado: {G.ARBOL}")
        hallazgos, mirados = G.revisar()
        self.assertGreater(mirados, 20, "miró sospechosamente pocos ficheros")
        self.assertEqual(hallazgos, [],
                         f"el árbol tiene dependencias no declaradas: {hallazgos}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
