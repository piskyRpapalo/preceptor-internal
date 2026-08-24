#!/usr/bin/env python3
"""Pruebas del Afinador. Solo biblioteca estándar.

    python3 agentes/bucles/test_afinador.py

Lo que se prueba no es que la tanda corra —eso lo hace `bin/pruebas` solo— sino
que el bucle vea **las tres formas de romperse que dan VERDE**. Un afinador que
solo distingue verde de rojo no aporta nada sobre un cron.
"""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import afinador as A  # noqa: E402

BASE = {"pruebas": 337, "suites_corridas": 20, "suites_en_arbol": 33}


def claves(hoy, antes=BASE):
    return {h["clave"] for h in A.comparar(hoy, antes)}


class TestLoQueDaVerdeYEstaRoto(unittest.TestCase):

    def test_el_recuento_a_la_baja_se_ve(self):
        """`VERDE 320/320` se lee igual de bien que `VERDE 337/337`. Nadie mira
        el número; se mira el color."""
        self.assertIn("recuento-a-la-baja", claves(dict(BASE, pruebas=320)))

    def test_una_suite_que_cae_del_corredor_se_ve(self):
        self.assertIn("suite-fuera-del-corredor",
                      claves(dict(BASE, suites_corridas=19)))

    def test_una_suite_nueva_sin_corredor_ensancha_el_hueco(self):
        """Deuda S3: una suite que nadie corre no es cobertura, es decoración."""
        self.assertIn("cobertura-mas-estrecha",
                      claves(dict(BASE, suites_en_arbol=35, pruebas=340)))

    def test_crecer_bien_NO_es_un_hallazgo(self):
        """Suite nueva Y metida en el corredor: eso es exactamente lo que se
        quiere. Avisar aquí enseñaría a ignorar los avisos."""
        self.assertEqual(claves({"pruebas": 350, "suites_corridas": 21,
                                 "suites_en_arbol": 34}), set())

    def test_sin_cambios_no_hay_ruido(self):
        self.assertEqual(claves(dict(BASE)), set())

    def test_la_primera_vez_no_inventa_comparacion(self):
        """Sin un `antes` no hay delta, y un delta inventado sería peor que nada."""
        self.assertEqual(A.comparar(dict(BASE), None), [])


class TestLecturaDeLaTanda(unittest.TestCase):
    """El bucle lee la salida del corredor. Si el formato cambia y el bucle
    deja de encontrar el número, tiene que DECIRLO en vez de dar verde."""

    def _corredor(self, cuerpo):
        d = tempfile.mkdtemp(prefix="afinador_")
        os.makedirs(os.path.join(d, "bin"))
        p = Path(d) / "bin" / "pruebas"
        p.write_text("#!/usr/bin/env bash\n" + cuerpo, encoding="utf-8")
        p.chmod(0o755)
        # Un `test_*.py` suelto, para que el recuento del árbol no sea cero.
        (Path(d) / "test_algo.py").write_text("", encoding="utf-8")
        return d

    def test_lee_recuento_veredicto_y_sabotajes(self):
        d = self._corredor(
            'echo "  337 pruebas · 20 suites · 6 corredores"\n'
            'echo "  ok    test_idioma.py --sabotaje       4/4 detectadas"\n'
            'echo "VERDE · 337/337"\n')
        hoy = A.correr(d)
        self.assertTrue(hoy["verde"])
        self.assertEqual(hoy["pruebas"], 337)
        self.assertEqual(hoy["suites_corridas"], 20)
        self.assertEqual(hoy["sabotajes"][0], {"suite": "test_idioma.py",
                                               "detectadas": 4, "total": 4})

    def test_un_sabotaje_ciego_es_un_hallazgo(self):
        """Un sabotaje que ya no sabotea significa que ese test no vale: el
        código cambió debajo del ancla. Pasó de verdad con `test_memory`."""
        d = self._corredor(
            'echo "  337 pruebas · 20 suites · 6 corredores"\n'
            'echo "  FALLO test_idioma.py --sabotaje       0/4 detectadas"\n'
            'echo "VERDE · 337/337"\n')
        _, hallazgos = A.revisar(d)
        self.assertTrue(any(h["clave"].startswith("sabotaje-ciego")
                            for h in hallazgos), hallazgos)

    def test_una_tanda_en_rojo_es_un_hallazgo(self):
        d = self._corredor(
            'echo "  337 pruebas · 20 suites · 6 corredores"\n'
            'echo "ROJO · 1 corredor(es) en fallo"\nexit 1\n')
        hoy, hallazgos = A.revisar(d)
        self.assertFalse(hoy["verde"])
        self.assertIn("tanda-en-rojo", {h["clave"] for h in hallazgos})

    def test_codigo_cero_pero_veredicto_ROJO_no_pasa_por_verde(self):
        """Hacen falta las dos cosas. Si divergen, una de las dos miente."""
        d = self._corredor(
            'echo "  337 pruebas · 20 suites"\necho "ROJO · algo"\nexit 0\n')
        self.assertFalse(A.correr(d)["verde"])

    def test_sin_recuento_lo_dice_en_vez_de_callarse(self):
        """Sin número no hay con qué comparar mañana, y el bucle se queda ciego
        sin dejar de dar verde."""
        d = self._corredor('echo "todo bien, confía en mí"\necho "VERDE"\n')
        _, hallazgos = A.revisar(d)
        self.assertIn("sin-recuento", {h["clave"] for h in hallazgos})

    def test_un_arbol_que_no_existe_no_pasa_por_bueno(self):
        hoy, hallazgos = A.revisar("/no/existe/este/arbol")
        self.assertIn("error", hoy)
        self.assertIn("tanda-no-corrio", {h["clave"] for h in hallazgos})

    def test_sin_corredor_tampoco(self):
        d = tempfile.mkdtemp(prefix="afinador_vacio_")
        _, hallazgos = A.revisar(d)
        self.assertIn("tanda-no-corrio", {h["clave"] for h in hallazgos})

    def test_una_tanda_colgada_termina_en_hallazgo_y_no_en_espera(self):
        """Un bucle que espera indefinidamente no deja latido de salida y es
        indistinguible de uno que nunca arrancó."""
        d = self._corredor("sleep 60\n")
        antes = A.ESPERA_S
        A.ESPERA_S = 1
        try:
            hoy, hallazgos = A.revisar(d)
        finally:
            A.ESPERA_S = antes
        self.assertIn("error", hoy)
        self.assertIn("tanda-no-corrio", {h["clave"] for h in hallazgos})


class TestLaNota(unittest.TestCase):
    """La nota del latido es de donde sale el «antes» de mañana. Si no se puede
    volver a leer, la comparación no existe."""

    def test_la_nota_se_puede_volver_a_leer(self):
        hoy = dict(BASE, verde=True)
        leido = A._NOTA.search(A.nota(hoy))
        self.assertIsNotNone(leido, "la nota que escribe no la sabe leer")
        self.assertEqual(int(leido.group(1)), 337)
        self.assertEqual(int(leido.group(3)), 20)
        self.assertEqual(int(leido.group(4)), 33)

    def test_la_nota_dice_el_color_y_la_cobertura(self):
        texto = A.nota(dict(BASE, verde=True))
        self.assertIn("VERDE", texto)
        self.assertIn("20 de 33", texto)

    def test_sin_recuento_la_nota_no_finge_uno(self):
        self.assertNotIn("pruebas ·", A.nota({"error": "no corrio"}))


class TestLaClase(unittest.TestCase):

    def test_es_MEDIO_porque_cuesta(self):
        """138 s medidos. LIGERO sería mentir sobre lo que cuesta; PESADO le
        haría competir por el cerrojo con trabajos que sí lo necesitan."""
        self.assertEqual(A.CLASE, "MEDIO")

    def test_la_espera_es_mayor_que_lo_que_tarda(self):
        self.assertGreater(A.ESPERA_S, 138 * 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
