#!/usr/bin/env python3
"""Pruebas de las cuatro refinaciones. Solo biblioteca estándar.

    python3 agentes/bucles/test_bucles.py

Cada clase prueba una de las cuatro cosas que el Soberano firmó como doctrina.
No prueban que el código corra: prueban que **lo que se prometió es imposible de
romper**. Un append-only que solo existe en un comentario no es append-only.
"""

from __future__ import annotations

import os
import sqlite3
import sys
import tempfile
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import latido as L                                              # noqa: E402
import director as D                                            # noqa: E402
import s0 as S                                                  # noqa: E402


class Casa(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.dir.name, "loops.db")

    def tearDown(self):
        self.dir.cleanup()


class TestElLatidoEsInmutable(Casa):
    """(c) La historia no se reescribe — y lo impone el motor, no la costumbre."""

    def test_un_latido_no_se_puede_editar(self):
        with L.abrir(self.db) as c:
            L.registrar(c, "prueba", "LIGERO", 60)
            L.sale(c, "prueba", "ok")
        with L.abrir(self.db) as c:
            with self.assertRaises(sqlite3.IntegrityError) as caja:
                c.execute("UPDATE latidos SET resultado='fallo' WHERE bucle='prueba'")
            self.assertIn("no se editan", str(caja.exception))

    def test_un_latido_no_se_puede_borrar(self):
        with L.abrir(self.db) as c:
            L.registrar(c, "prueba", "LIGERO", 60)
            L.sale(c, "prueba", "fallo", nota="se rompió")
        with L.abrir(self.db) as c:
            with self.assertRaises(sqlite3.IntegrityError):
                c.execute("DELETE FROM latidos WHERE bucle='prueba'")
            # Y sigue ahí: el fallo incómodo no se puede hacer desaparecer.
            n = c.execute("SELECT COUNT(*) n FROM latidos").fetchone()["n"]
            self.assertEqual(n, 1)

    def test_los_cambios_de_estado_tampoco(self):
        with L.abrir(self.db) as c:
            L.registrar(c, "prueba", "LIGERO", 60)
            L.cambiar_estado(c, "prueba", "muerto", "prueba", ahora=time.time() + 10_000)
        with L.abrir(self.db) as c:
            with self.assertRaises(sqlite3.IntegrityError):
                c.execute("DELETE FROM estados")


class TestLaHisteresis(Casa):
    """(a) Ningún estado cambia por un solo evento."""

    def test_un_estado_recien_puesto_no_se_mueve(self):
        with L.abrir(self.db) as c:
            L.registrar(c, "prueba", "LIGERO", 60)
            cambiado, razon = L.cambiar_estado(c, "prueba", "muerto", "un fallo suelto")
            self.assertFalse(cambiado)
            self.assertIn("histéresis", razon)
            fila = c.execute("SELECT estado FROM bucles WHERE nombre='prueba'").fetchone()
            self.assertEqual(fila["estado"], "vivo")

    def test_pasado_el_descanso_si_se_mueve(self):
        with L.abrir(self.db) as c:
            L.registrar(c, "prueba", "LIGERO", 60)
            luego = time.time() + L.DESCANSO_ESTADO_S + 1
            cambiado, _ = L.cambiar_estado(c, "prueba", "muerto", "sostenido", ahora=luego)
            self.assertTrue(cambiado)

    def test_el_flapping_no_llena_la_bandeja(self):
        """El caso que motiva la regla: carga oscilando alrededor del umbral.

        Diez intentos de cambiar de estado en un minuto tienen que producir
        UN cambio como mucho, no diez. Sin esto, la bandeja de firmas recibe
        diez avisos de lo mismo y acaba ignorada, que es la forma educada de
        apagar la vigilancia.
        """
        with L.abrir(self.db) as c:
            L.registrar(c, "prueba", "LIGERO", 60)
            base = time.time()
            cambios = 0
            for i in range(10):
                destino = "muerto" if i % 2 == 0 else "vivo"
                ok, _ = L.cambiar_estado(c, "prueba", destino, "oscila", ahora=base + i * 6)
                cambios += 1 if ok else 0
            self.assertLessEqual(cambios, 1, "la histéresis dejó pasar el flapping")


class TestDormirExigeLaLlave(Casa):
    """(b) Retirar sin borrar — pero solo si se escribe qué lo despierta."""

    def test_no_se_puede_dormir_sin_condicion(self):
        with L.abrir(self.db) as c:
            L.registrar(c, "prueba", "LIGERO", 60)
            with self.assertRaises(ValueError):
                L.dormir(c, "prueba", "ya no aplica", "")
            with self.assertRaises(ValueError):
                L.dormir(c, "prueba", "", "cuando haya hierro")

    def test_dormido_guarda_motivo_y_llave(self):
        with L.abrir(self.db) as c:
            L.registrar(c, "prueba", "PESADO", 60)
            ok, _ = L.dormir(c, "prueba", "el hardware no existe",
                             "cuando musculo-hp-01 vuelva a la tailnet")
            self.assertTrue(ok)
            f = c.execute("SELECT * FROM bucles WHERE nombre='prueba'").fetchone()
            self.assertEqual(f["estado"], "dormido")
            self.assertIn("hp-01", f["condicion_despertar"])

    def test_el_dormido_no_entra_en_la_cola(self):
        with L.abrir(self.db) as c:
            L.registrar(c, "despierto", "LIGERO", 60)
            L.registrar(c, "dormido", "LIGERO", 60)
            L.dormir(c, "dormido", "sin hardware", "cuando haya hierro")
            plan = D.planificar(c)
            self.assertIn("despierto", plan["cola"])
            self.assertNotIn("dormido", plan["cola"])

    def test_el_dormido_no_se_marca_muerto(self):
        """Dormido no es muerto. Confundirlos genera una alerta cada noche."""
        with L.abrir(self.db) as c:
            L.registrar(c, "dormido", "LIGERO", 60)
            L.dormir(c, "dormido", "sin hardware", "cuando haya hierro")
            veredictos = D.revisar(c, ahora=time.time() + 10_000)
            v = next(x for x in veredictos if x["bucle"] == "dormido")
            self.assertEqual(v["accion"], "ninguna")
            self.assertIn("despierta si", v["porque"])


class TestElMonitorDeFalloSilencioso(Casa):
    """(d) Todo verde porque el detector está roto es el peor verde."""

    def test_un_filtro_que_corre_y_nunca_halla_es_sospechoso(self):
        with L.abrir(self.db) as c:
            L.registrar(c, "guardian", "LIGERO", 86400)
            for i in range(8):
                L.sale(c, "guardian", "ok")
            sos = S.silencios(c)
        self.assertEqual(len(sos), 1)
        self.assertEqual(sos[0]["bucle"], "guardian")
        self.assertTrue(sos[0]["nunca_hallo"])

    def test_un_filtro_que_halla_no_es_sospechoso(self):
        with L.abrir(self.db) as c:
            L.registrar(c, "guardian", "LIGERO", 86400)
            L.sale(c, "guardian", "ok")
            L.hallazgo(c, "guardian", "import_nuevo", "PIL en laminas/recortar.py")
            sos = S.silencios(c)
        self.assertEqual(sos, [])

    def test_un_bucle_parado_no_cuenta_como_callado(self):
        """Parado y callado son averías distintas y las avisa gente distinta.

        De un bucle que no corre ya avisa el Director. Si S0 avisara también,
        habría dos alertas de lo mismo y ninguna diría la verdad.
        """
        with L.abrir(self.db) as c:
            L.registrar(c, "parado", "LIGERO", 86400)
            sos = S.silencios(c)
        self.assertEqual(sos, [])

    def test_s0_se_vigila_a_si_mismo(self):
        """Si S0 se rompe, el siguiente S0 sospecha de S0."""
        with L.abrir(self.db) as c:
            L.registrar(c, "guardian", "LIGERO", 86400)
            L.sale(c, "guardian", "ok")
        S.pasada(self.db)
        with L.abrir(self.db) as c:
            n = c.execute("SELECT COUNT(*) n FROM hallazgos WHERE bucle='s0'").fetchone()["n"]
        self.assertGreater(n, 0, "S0 no registró lo que encontró y no podrá ser vigilado")


class TestElDirector(Casa):
    def test_un_pesado_no_arranca_fuera_de_ventana(self):
        with L.abrir(self.db) as c:
            L.registrar(c, "medico", "PESADO", 86400)
            plan = D.planificar(c, ahora=time.mktime(
                time.strptime("2026-08-23 14:00", "%Y-%m-%d %H:%M")))
        self.assertNotIn("medico", plan["cola"])
        self.assertTrue(any(p["bucle"] == "medico" for p in plan["pospuestos"]))

    def test_la_posposicion_se_registra(self):
        """Un bucle que se pospone en silencio no se distingue de uno que no existe."""
        with L.abrir(self.db) as c:
            L.registrar(c, "medico", "PESADO", 86400)
        D.pasada(self.db, ahora=time.mktime(
            time.strptime("2026-08-23 14:00", "%Y-%m-%d %H:%M")))
        with L.abrir(self.db) as c:
            f = c.execute("SELECT * FROM latidos WHERE bucle='medico' "
                          "AND resultado='pospuesto'").fetchall()
        self.assertGreater(len(f), 0)

    def test_el_turno_deja_latido_aunque_reviente(self):
        with self.assertRaises(RuntimeError):
            with L.turno("frágil", "LIGERO", 60, self.db):
                raise RuntimeError("me rompí")
        with L.abrir(self.db) as c:
            f = c.execute("SELECT * FROM latidos WHERE bucle='frágil' "
                          "AND evento='sale'").fetchone()
        self.assertEqual(f["resultado"], "fallo")
        self.assertIn("me rompí", f["nota"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
