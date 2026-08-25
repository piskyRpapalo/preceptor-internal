#!/usr/bin/env python3
"""L3 · EL CURADOR · higiene de la memoria, sin tocarla nunca.

QUÉ HACE
--------
Busca duplicados y enlaces rotos entre los recuerdos, y **propone**. No borra,
no fusiona, no edita: abre la memoria en **solo lectura** y deja sus hallazgos
en la bandeja de firmas. La regla de cero DELETE de `memory.py` protege lo que
la persona escribió; un bucle nocturno con permiso de escritura sobre eso sería
la forma más rápida de romperla, y encima sin testigos.

LA ESCALADA POR COSTE, QUE AQUÍ NO ES UNA PREFERENCIA
-----------------------------------------------------
`REVISION_CRUZADA.md` §5.1, corrección 3 del Soberano:

> *«El Médico no escala. Clasificar semánticamente mil recuerdos con el 30B en
> un turno es imposible [...] duplicados por cadena exacta en SQLite primero
> (instantáneo), y solo los candidatos supervivientes pasan al 30B, por
> ventanas de ~100 recuerdos activos.»*

Medido el 2026-08-25: el 27B genera a **4,6 tok/s**. Mil recuerdos comparados
con el modelo no son lentos: no terminan. Así que se baja por la escalera del
canon, y cada peldaño solo pasa al siguiente lo que no supo resolver:

    1. Cadena exacta (SQLite)      instantáneo   ·  resuelve los idénticos
    2. FTS5 sobre `engrams`        milisegundos  ·  saca CANDIDATOS parecidos
    3. El 27B, solo si quedan      ~7 s cada uno ·  decide los dudosos

El peldaño 2 es la búsqueda léxica que se construyó hoy (B.1a). Sin ella habría
que comparar todos contra todos: con 1.000 recuerdos son 499.500 parejas.

CERO NO ES LO MISMO QUE LIMPIO
------------------------------
Sobre una memoria vacía, «0 duplicados» no significa nada. El bucle lo
distingue y lo dice — es el mismo modo de fallo que S0 vigila: el filtro que da
verde porque no miró.
"""
from __future__ import annotations

import os
import re
import sqlite3
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cerebro as CE  # noqa: E402
import latido as L  # noqa: E402

MEMORIA = os.path.expanduser(os.environ.get("CURADOR_MEMORIA",
                                            "~/.aurelius/memory.db"))
VENTANA_S = 604800          # semanal: la memoria no se ensucia en un día
CLASE = "MEDIO"             # puede llamar al modelo; no es LIGERO

# Cuántos candidatos como mucho pasan al peldaño 3 en una pasada. A ~7 s cada
# uno, 20 son algo más de dos minutos. Lo que no entre hoy entra la semana que
# viene: la memoria sigue ahí.
TOPE_AL_MODELO = int(os.environ.get("CURADOR_TOPE_MODELO", "20"))
MINIMO_PALABRAS = 4         # por debajo, «parecido» no significa nada


def _normalizar(texto):
    """Para comparar por cadena exacta: sin acentos, sin caja, sin puntuación.

    No se guarda en ningún sitio. Es una lente para mirar, no una edición: lo
    que la persona escribió se queda exactamente como lo escribió.
    """
    t = unicodedata.normalize("NFKD", (texto or "").lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^\w\s]", " ", t).split()


def _clave(texto):
    return " ".join(_normalizar(texto))


def abrir_memoria(ruta=None):
    """Solo lectura, y a propósito. Ni un `UPDATE` puede salir de aquí."""
    ruta = ruta or MEMORIA
    if not os.path.isfile(ruta):
        return None
    con = sqlite3.connect(f"file:{ruta}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return con


def _engramas(c):
    return [dict(f) for f in c.execute(
        "select id, what, why, learned, created_at from engrams "
        "where status='activo' order by id")]


# --- peldaño 1 · cadena exacta · instantáneo -------------------------------

def duplicados_exactos(engramas):
    """Los que dicen literalmente lo mismo. Sin modelo y sin dudas."""
    por_clave = {}
    for e in engramas:
        k = _clave(e["what"])
        if len(k.split()) < MINIMO_PALABRAS:
            continue
        por_clave.setdefault(k, []).append(e)
    return [v for v in por_clave.values() if len(v) > 1]


# --- peldaño 2 · FTS5 · milisegundos ---------------------------------------

def hay_indice(c):
    return c.execute(
        "select 1 from sqlite_master where name='engrams_fts'").fetchone() is not None


def candidatos_parecidos(c, engramas, ya_vistos):
    """Parejas que comparten palabras. NO son duplicados: son sospechas.

    Se usa el índice FTS5 en vez de comparar todos contra todos: con 1.000
    recuerdos eso serían 499.500 parejas, y la mayoría no comparten ni una
    palabra rara.
    """
    if not hay_indice(c):
        return None            # ausencia declarada, no lista vacía
    parejas = {}
    for e in engramas:
        if e["id"] in ya_vistos:
            continue
        palabras = [p for p in _normalizar(e["what"]) if len(p) > 4]
        if len(palabras) < MINIMO_PALABRAS:
            continue
        consulta = " OR ".join(f'"{p}"' for p in palabras[:8])
        try:
            filas = c.execute(
                "select e.id, e.what from engrams_fts "
                "join engrams e on e.id = engrams_fts.rowid "
                "where engrams_fts match ? and e.status='activo' and e.id != ? "
                "order by rank limit 3", (consulta, e["id"])).fetchall()
        except sqlite3.OperationalError:
            continue
        for f in filas:
            par = tuple(sorted((e["id"], f["id"])))
            if par in parejas or par[0] in ya_vistos or par[1] in ya_vistos:
                continue
            solape = _solape(e["what"], f["what"])
            if solape >= UMBRAL_SOLAPE:
                parejas[par] = {"a": e, "b": dict(f), "solape": round(solape, 2)}
    return list(parejas.values())


# Coeficiente de SOLAPE, no Jaccard, y esto se midió antes de elegirlo.
#
# Con Jaccard, «aprendi a compilar llama.cpp con Vulkan en el Beelink» y
# «compile llama.cpp usando Vulkan sobre el Beelink de casa» dan **0,33**: la
# unión crece con cada palabra distinta, así que decir lo mismo con otro fraseo
# BAJA la nota. Es exactamente el caso que hay que cazar, y Jaccard lo esconde.
#
# El solape divide por el conjunto pequeño, así que mide «¿cuánto de lo que dice
# el corto está también en el largo?». Los mismos dos recuerdos dan **0,60**.
#
# Y sobre palabras de más de tres letras: sin eso, «a», «con», «en», «el», «de»
# inflan el parecido entre dos recuerdos que no tienen nada que ver.
UMBRAL_SOLAPE = float(os.environ.get("CURADOR_UMBRAL", "0.5"))


def _contenido(texto):
    return {p for p in _normalizar(texto) if len(p) > 3}


def _solape(uno, otro):
    """Cuánto de lo que dice el más corto está también en el otro. 0 a 1."""
    a, b = _contenido(uno), _contenido(otro)
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


# --- peldaño 3 · el modelo, solo sobre lo que sobrevivió -------------------

INSTRUCCIONES = (
    "Eres un curador de memoria. Te doy dos recuerdos escritos por la misma "
    "persona. Responde SOLO con una palabra:\n"
    "DUPLICADO  si dicen lo mismo con otras palabras\n"
    "DISTINTO   si son cosas diferentes aunque compartan tema\n"
    "No expliques. Una palabra."
)


def preguntar_al_modelo(par):
    """Devuelve ('DUPLICADO'|'DISTINTO'|'NO_DATA', medidas).

    Las INSTRUCCIONES van primero y los recuerdos después, a propósito: el
    caché de prompt guarda el prefijo común, así que se cachea la parte fija y
    NO los recuerdos de la persona, que cambian en cada pareja.
    """
    prompt = (f"{INSTRUCCIONES}\n\n"
              f"Recuerdo A: {par['a']['what']}\n"
              f"Recuerdo B: {par['b']['what']}\n\n"
              f"Una palabra:")
    try:
        texto, medidas = CE.pensar(prompt, tope_tokens=8)
    except (CE.SinCerebro, CE.SeAgotoElTiempo) as e:
        return "NO_DATA", {"motivo": str(e)}
    arriba = texto.upper()
    if "DUPLICADO" in arriba:
        return "DUPLICADO", medidas
    if "DISTINTO" in arriba:
        return "DISTINTO", medidas
    # Ni una cosa ni la otra: se declara. Adivinar por «lo que parece» es
    # meter una opinión del bucle en el registro como si fuera del modelo.
    return "NO_DATA", dict(medidas, respuesta=texto[:80])


# --- enlaces rotos · gratis ------------------------------------------------

def enlaces_rotos(c):
    return [dict(f) for f in c.execute(
        "select l.id, l.from_engram, l.to_engram from links l "
        "left join engrams a on a.id = l.from_engram "
        "left join engrams b on b.id = l.to_engram "
        "where a.id is null or b.id is null")]


# --- la pasada -------------------------------------------------------------

def revisar(ruta=None, usar_modelo=True):
    c = abrir_memoria(ruta)
    if c is None:
        return {"error": f"no hay memoria en {ruta or MEMORIA}"}, [
            {"clave": "sin-memoria",
             "detalle": f"no existe {ruta or MEMORIA}. Nada que curar, y no es "
                        f"lo mismo que estar limpia."}]
    try:
        engramas = _engramas(c)
        resumen = {"engramas": len(engramas), "exactos": 0, "candidatos": 0,
                   "al_modelo": 0, "confirmados": 0, "enlaces_rotos": 0,
                   "indice": hay_indice(c), "ms_modelo": 0.0}
        hallazgos = []

        if not engramas:
            # Cero no es limpio. Es el modo de fallo que S0 vigila.
            resumen["vacia"] = True
            return resumen, [{
                "clave": "memoria-vacia",
                "detalle": "0 recuerdos activos. «0 duplicados» sobre una "
                           "memoria vacía no dice nada: no se ha mirado nada."}]

        # 1 · exactos
        ya = set()
        for grupo in duplicados_exactos(engramas):
            resumen["exactos"] += 1
            ids = [e["id"] for e in grupo]
            ya.update(ids)
            hallazgos.append({
                "clave": f"duplicado-exacto:{'+'.join(map(str, ids))}",
                "detalle": (f"{len(grupo)} recuerdos dicen literalmente lo "
                            f"mismo: {grupo[0]['what'][:90]!r}. "
                            f"Propuesta: conservar el más antiguo (id {ids[0]}) "
                            f"y archivar el resto. NO se ha tocado nada.")})

        # 2 · parecidos por FTS5
        candidatos = candidatos_parecidos(c, engramas, ya)
        if candidatos is None:
            hallazgos.append({
                "clave": "sin-indice-fts5",
                "detalle": ("esta memoria no tiene el índice de búsqueda, así "
                            "que solo se han mirado los duplicados EXACTOS. "
                            "Se crea solo al abrirla con una versión reciente.")})
            candidatos = []
        resumen["candidatos"] = len(candidatos)

        # 3 · el modelo, solo sobre los que sobrevivieron
        if usar_modelo and candidatos:
            est, detalle = CE.estado()
            if est != "LISTO":
                hallazgos.append({
                    "clave": "sin-cerebro",
                    "detalle": f"{len(candidatos)} parejas dudosas sin revisar: "
                               f"{detalle}"})
            else:
                for par in candidatos[:TOPE_AL_MODELO]:
                    resumen["al_modelo"] += 1
                    veredicto, medidas = preguntar_al_modelo(par)
                    resumen["ms_modelo"] += medidas.get("ms", 0)
                    if veredicto == "DUPLICADO":
                        resumen["confirmados"] += 1
                        hallazgos.append({
                            "clave": f"duplicado-probable:{par['a']['id']}+{par['b']['id']}",
                            "detalle": (f"solape {par['solape']} y el modelo dice "
                                        f"DUPLICADO.\n  A: {par['a']['what'][:80]!r}"
                                        f"\n  B: {par['b']['what'][:80]!r}\n"
                                        f"  Propuesta: mirarlos. NO se ha tocado nada.")})
                if len(candidatos) > TOPE_AL_MODELO:
                    hallazgos.append({
                        "clave": "cola-pendiente",
                        "detalle": (f"{len(candidatos) - TOPE_AL_MODELO} parejas "
                                    f"quedan para la próxima pasada. No se han "
                                    f"perdido: la memoria sigue ahí.")})

        # enlaces rotos · gratis
        for l in enlaces_rotos(c):
            resumen["enlaces_rotos"] += 1
            hallazgos.append({
                "clave": f"enlace-roto:{l['id']}",
                "detalle": (f"el enlace {l['id']} apunta de {l['from_engram']} "
                            f"a {l['to_engram']} y uno de los dos no existe.")})
        return resumen, hallazgos
    finally:
        c.close()


def nota(r):
    if "error" in r:
        return r["error"]
    if r.get("vacia"):
        return "memoria VACIA · 0 recuerdos activos · nada que mirar"
    return (f"{r['engramas']} recuerdos · {r['exactos']} duplicados exactos · "
            f"{r['confirmados']}/{r['al_modelo']} confirmados por el modelo · "
            f"{r['enlaces_rotos']} enlaces rotos · "
            f"{r['ms_modelo'] / 1000:.0f} s de modelo")


def main():
    sin_modelo = "--sin-modelo" in sys.argv[1:]
    if "--informe" in sys.argv[1:]:
        r, hallazgos = revisar(usar_modelo=not sin_modelo)
        print(f"curador · {nota(r)}")
        for h in hallazgos:
            print(f"  {h['clave']}\n    {h['detalle'].splitlines()[0]}")
        if not hallazgos:
            print("  sin hallazgos")
        return 0

    with L.turno("curador", CLASE, VENTANA_S) as caja:
        r, hallazgos = revisar(usar_modelo=not sin_modelo)
        with L.abrir() as c:
            for h in hallazgos:
                L.hallazgo(c, "curador", h["clave"], h["detalle"])
        caja["nota"] = nota(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
