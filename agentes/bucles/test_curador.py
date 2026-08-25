#!/usr/bin/env python3
"""Pruebas del Curador. Solo biblioteca estándar.

    python3 agentes/bucles/test_curador.py

Dos cosas se prueban por encima de todo: que **no toca la memoria** y que la
escalada por coste de verdad ahorra llamadas al modelo. Lo segundo no es una
optimización: a 4,6 tok/s, comparar todo con todo no es lento, no termina.

El modelo no participa en esta suite. Un test que depende de que un LLM acierte
no prueba el código: prueba el humor del modelo esa noche.
"""
from __future__ import annotations

import os
import sqlite3
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.expanduser("~/p0x/aurelius"))
import curador as CU  # noqa: E402

ESQUEMA = """
create table engrams (
    id integer primary key autoincrement,
    what text not null, why text default 'NO_DATA',
    learned text default '', status text default 'activo',
    created_at text default (datetime('now')));
create table links (
    id integer primary key autoincrement,
    from_engram integer, to_engram integer);
"""


def memoria(*textos, enlaces=(), fts=False):
    ruta = os.path.join(tempfile.mkdtemp(prefix="curador_p_"), "m.db")
    con = sqlite3.connect(ruta)
    con.executescript(ESQUEMA)
    for t in textos:
        con.execute("insert into engrams (what) values (?)", (t,))
    for a, b in enlaces:
        con.execute("insert into links (from_engram, to_engram) values (?,?)", (a, b))
    if fts:
        con.execute("create virtual table engrams_fts using fts5("
                    "what, content=engrams, content_rowid=id, "
                    'tokenize="unicode61 remove_diacritics 2")')
        con.execute("insert into engrams_fts(engrams_fts) values('rebuild')")
    con.commit()
    con.close()
    return ruta


class TestNoTocaLaMemoria(unittest.TestCase):
    """La regla de cero DELETE protege lo que la persona escribió. Un bucle
    nocturno con permiso de escritura sobre eso la rompería sin testigos."""

    def test_la_abre_en_SOLO_LECTURA(self):
        ruta = memoria("un recuerdo cualquiera de la persona", fts=True)
        c = CU.abrir_memoria(ruta)
        with self.assertRaises(sqlite3.OperationalError):
            c.execute("delete from engrams")
        with self.assertRaises(sqlite3.OperationalError):
            c.execute("update engrams set what='pisado'")
        c.close()

    def test_una_pasada_entera_deja_la_memoria_byte_a_byte_igual(self):
        import hashlib
        ruta = memoria("aprendi a compilar llama.cpp con Vulkan en el Beelink",
                       "compile llama.cpp usando Vulkan sobre el Beelink",
                       "hoy he comido lentejas con chorizo", fts=True)
        antes = hashlib.sha256(open(ruta, "rb").read()).hexdigest()
        CU.revisar(ruta, usar_modelo=False)
        self.assertEqual(hashlib.sha256(open(ruta, "rb").read()).hexdigest(), antes,
                         "la pasada modificó el fichero de la memoria")


class TestVacioNoEsLimpio(unittest.TestCase):
    """«0 duplicados» sobre una memoria vacía no dice nada. Es el modo de fallo
    que S0 vigila: el filtro que da verde porque no miró."""

    def test_una_memoria_vacia_se_declara(self):
        r, h = CU.revisar(memoria(fts=True), usar_modelo=False)
        self.assertTrue(r["vacia"])
        self.assertIn("memoria-vacia", {x["clave"] for x in h})
        self.assertIn("VACIA", CU.nota(r))

    def test_una_memoria_que_no_existe_tampoco_pasa_por_limpia(self):
        r, h = CU.revisar("/no/existe/memoria.db", usar_modelo=False)
        self.assertIn("error", r)
        self.assertIn("sin-memoria", {x["clave"] for x in h})

    def test_sin_indice_lo_dice_en_vez_de_dar_cero_candidatos(self):
        """Sin FTS5 solo se ven los exactos. Callarlo haría creer que se miró
        todo."""
        r, h = CU.revisar(memoria("un recuerdo largo sobre soberania digital",
                                  "otro recuerdo largo sobre soberania tecnica",
                                  fts=False), usar_modelo=False)
        self.assertFalse(r["indice"])
        self.assertIn("sin-indice-fts5", {x["clave"] for x in h})


class TestPeldano1Exactos(unittest.TestCase):

    def test_la_caja_y_los_acentos_no_esconden_un_duplicado(self):
        ruta = memoria("aprendi a compilar llama.cpp con Vulkan",
                       "Aprendí a compilar llama.cpp con Vulkan.", fts=True)
        r, h = CU.revisar(ruta, usar_modelo=False)
        self.assertEqual(r["exactos"], 1)
        self.assertTrue(any(x["clave"].startswith("duplicado-exacto")
                            for x in h))

    def test_un_recuerdo_muy_corto_no_cuenta_como_duplicado(self):
        """Dos «ok» no son un duplicado que merezca la firma de nadie."""
        r, _ = CU.revisar(memoria("ok", "ok", "ok", fts=True), usar_modelo=False)
        self.assertEqual(r["exactos"], 0)

    def test_la_propuesta_conserva_el_mas_antiguo(self):
        ruta = memoria("un recuerdo repetido sobre el hardware soberano",
                       "un recuerdo repetido sobre el hardware soberano", fts=True)
        _, h = CU.revisar(ruta, usar_modelo=False)
        detalle = [x for x in h if x["clave"].startswith("duplicado-exacto")][0]["detalle"]
        self.assertIn("id 1", detalle)
        self.assertIn("NO se ha tocado nada", detalle)


class TestElSolape(unittest.TestCase):
    """Se eligió el coeficiente de solape midiendo, no por gusto."""

    A = "aprendi a compilar llama.cpp con Vulkan en el Beelink"
    B = "compile llama.cpp usando Vulkan sobre el Beelink de casa"

    def test_dos_formas_de_decir_lo_mismo_pasan_el_umbral(self):
        self.assertGreaterEqual(CU._solape(self.A, self.B), CU.UMBRAL_SOLAPE)

    def test_jaccard_habria_escondido_ese_caso(self):
        """La razón del cambio, escrita como prueba: Jaccard da 0,33 -- por
        debajo del umbral -- para dos frases que dicen lo mismo."""
        a, b = CU._contenido(self.A), CU._contenido(self.B)
        jaccard = len(a & b) / len(a | b)
        self.assertLess(jaccard, CU.UMBRAL_SOLAPE)
        self.assertGreaterEqual(CU._solape(self.A, self.B), CU.UMBRAL_SOLAPE)

    def test_compartir_una_palabra_no_es_parecerse(self):
        self.assertLess(CU._solape("el Beelink tiene 64 GB de RAM",
                                   "hoy he comido lentejas con chorizo"), 0.5)

    def test_las_palabras_de_relleno_no_inflan_el_parecido(self):
        """Sin filtrar «con», «de», «que», dos recuerdos ajenos se parecen."""
        self.assertNotIn("con", CU._contenido("un texto con cosas de las que hablar"))


class TestEscaladaPorCoste(unittest.TestCase):
    """A 4,6 tok/s, comparar todo con todo no es lento: no termina."""

    def test_los_exactos_NO_llegan_al_modelo(self):
        """Ya están resueltos por cadena. Preguntarle al modelo sería pagar
        siete segundos por algo que SQLite dio instantáneo."""
        llamadas = []
        ruta = memoria("un recuerdo repetido sobre el hardware soberano",
                       "un recuerdo repetido sobre el hardware soberano", fts=True)
        with mock.patch.object(CU, "preguntar_al_modelo",
                               lambda p: (llamadas.append(p), ("DUPLICADO", {}))[1]):
            r, _ = CU.revisar(ruta, usar_modelo=True)
        self.assertEqual(r["exactos"], 1)
        self.assertEqual(llamadas, [], "un duplicado exacto llegó al modelo")

    def test_los_que_no_se_parecen_NO_llegan_al_modelo(self):
        llamadas = []
        ruta = memoria("aprendi a compilar llama.cpp con Vulkan en el Beelink",
                       "hoy he comido lentejas con chorizo y morcilla",
                       "la luna estaba llena sobre el tejado de casa", fts=True)
        with mock.patch.object(CU, "preguntar_al_modelo",
                               lambda p: (llamadas.append(p), ("DISTINTO", {}))[1]):
            CU.revisar(ruta, usar_modelo=True)
        self.assertEqual(llamadas, [], "el modelo miró recuerdos que no se parecen")

    def test_hay_tope_de_llamadas_por_pasada_y_se_dice_lo_que_queda(self):
        """Lo que no entra hoy entra la semana que viene. Callarlo haría creer
        que se revisó todo."""
        parejas = [{"a": {"id": i, "what": "x"}, "b": {"id": i + 100, "what": "y"},
                    "solape": 0.9} for i in range(1, 31)]
        ruta = memoria("un recuerdo cualquiera con bastantes palabras dentro",
                       fts=True)
        with mock.patch.object(CU, "candidatos_parecidos", lambda *a: parejas), \
             mock.patch.object(CU, "preguntar_al_modelo", lambda p: ("DISTINTO", {})), \
             mock.patch.object(CU.CE, "estado", lambda: ("LISTO", "de mentira")):
            r, h = CU.revisar(ruta, usar_modelo=True)
        self.assertEqual(r["al_modelo"], CU.TOPE_AL_MODELO)
        self.assertIn("cola-pendiente", {x["clave"] for x in h})

    def test_sin_cerebro_los_dudosos_quedan_declarados_no_perdidos(self):
        parejas = [{"a": {"id": 1, "what": "x"}, "b": {"id": 2, "what": "y"},
                    "solape": 0.9}]
        ruta = memoria("un recuerdo cualquiera con bastantes palabras dentro",
                       fts=True)
        with mock.patch.object(CU, "candidatos_parecidos", lambda *a: parejas), \
             mock.patch.object(CU.CE, "estado", lambda: ("NO_DATA", "no hay modelo")):
            _, h = CU.revisar(ruta, usar_modelo=True)
        self.assertIn("sin-cerebro", {x["clave"] for x in h})


class TestVeredictoDelModelo(unittest.TestCase):

    def _con_respuesta(self, texto):
        with mock.patch.object(CU.CE, "pensar", lambda *a, **k: (texto, {"ms": 1})):
            return CU.preguntar_al_modelo(
                {"a": {"what": "uno"}, "b": {"what": "otro"}})[0]

    def test_lee_las_dos_palabras(self):
        self.assertEqual(self._con_respuesta("DUPLICADO"), "DUPLICADO")
        self.assertEqual(self._con_respuesta("distinto"), "DISTINTO")

    def test_una_respuesta_rara_es_NO_DATA_y_no_una_adivinanza(self):
        """Adivinar por «lo que parece» mete una opinión del bucle en el
        registro como si fuera del modelo."""
        for raro in ("no estoy seguro", "", "quizás sí", "42"):
            self.assertEqual(self._con_respuesta(raro), "NO_DATA", f"con {raro!r}")

    def test_si_el_modelo_falla_se_declara_en_vez_de_reventar(self):
        with mock.patch.object(CU.CE, "pensar",
                               mock.Mock(side_effect=CU.CE.SinCerebro("no hay"))):
            v, m = CU.preguntar_al_modelo({"a": {"what": "x"}, "b": {"what": "y"}})
        self.assertEqual(v, "NO_DATA")
        self.assertIn("motivo", m)

    def test_las_instrucciones_van_ANTES_de_los_recuerdos(self):
        """El caché de prompt guarda el prefijo común: así se cachea la parte
        fija y NO los recuerdos de la persona."""
        visto = {}
        with mock.patch.object(CU.CE, "pensar",
                               lambda p, **k: (visto.setdefault("p", p), ("DISTINTO", {}))[1]):
            CU.preguntar_al_modelo({"a": {"what": "AAA"}, "b": {"what": "BBB"}})
        self.assertLess(visto["p"].index("curador de memoria"), visto["p"].index("AAA"))


class TestEnlacesRotos(unittest.TestCase):

    def test_un_enlace_a_la_nada_se_ve(self):
        ruta = memoria("un recuerdo cualquiera con palabras suficientes",
                       enlaces=[(1, 999)], fts=True)
        r, h = CU.revisar(ruta, usar_modelo=False)
        self.assertEqual(r["enlaces_rotos"], 1)
        self.assertTrue(any(x["clave"].startswith("enlace-roto") for x in h))

    def test_un_enlace_sano_no_molesta(self):
        ruta = memoria("un recuerdo cualquiera con palabras suficientes",
                       "otro recuerdo distinto del anterior por completo",
                       enlaces=[(1, 2)], fts=True)
        r, _ = CU.revisar(ruta, usar_modelo=False)
        self.assertEqual(r["enlaces_rotos"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
