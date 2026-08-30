#!/usr/bin/env python3
"""La memoria entre sesiones. SQLite, stdlib, y un bootstrap que se GENERA.

POR QUE EXISTE
--------------
Cada sesion de IA empieza sin contexto y lo reconstruye leyendo ficheros que
alguien escribio a mano hace dias. Eso funciona hasta que los ficheros
envejecen -- y envejecen siempre, en silencio.

Hoy mismo se midio el coste: la Orden Maestra daba por pendientes seis tareas
que ya estaban hechas (playground.html en tres idiomas, la paridad i18n, la
limpieza de console.log...) y por rotos cuatro servicios que estaban sanos. Una
sesion entera puede irse en perseguir problemas que no existen porque el
documento de arranque decia que existian.

De ahi la decision de diseño que gobierna este fichero: **`bootstrap_continuidad.md`
NO se escribe a mano. Se genera desde esta base.** Un prompt de arranque
redactado a mano miente en cuanto el rack cambia, y un arranque que miente es
peor que no tener arranque. Generado, no puede divergir de lo que la base sabe.

QUE GUARDA Y QUE NO
-------------------
Guarda lo que NO se puede deducir mirando el repo: decisiones y su motivo,
falsos rojos ya desmentidos, cadencias, el estado del rack en cada cierre.

No guarda lo que el codigo ya dice. Duplicar el repo aqui seria crear la
segunda verdad que todo este proyecto existe para evitar.
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DB = AQUI / "continuidad.db"
BOOTSTRAP = AQUI / "bootstrap_continuidad.md"
ESTADO = Path.home() / "p0x" / "Alejandria" / "estado.json"

# Las trece tablas del Anexo B, mas `deltas`. Cada una con su motivo escrito:
# una tabla sin proposito declarado se llena de cualquier cosa en tres sesiones.
ESQUEMA = {
    "hardware": """
        -- Los nodos del rack y lo que se ha MEDIDO de ellos, no lo que se
        -- supone. `medido_en` importa tanto como el dato.
        nodo TEXT PRIMARY KEY, rol TEXT, detalle TEXT,
        medido_en TEXT, fuente TEXT""",
    "servicios": """
        -- Que corre, en que manager y con que cadencia. La columna `gestor`
        -- existe porque preguntarle a `systemctl --user` por una unidad de
        -- sistema devuelve «no existe» -- cierto, y sin significado.
        nombre TEXT PRIMARY KEY, gestor TEXT, cadencia TEXT,
        estado TEXT, nota TEXT, medido_en TEXT""",
    "doctrina": """
        -- Reglas firmadas, con su alcance. `alcance` no es adorno: la regla de
        -- los 10 KB es del Agora y no de la app, y confundirlo cuesta un
        -- refactor entero.
        id TEXT PRIMARY KEY, regla TEXT NOT NULL, alcance TEXT,
        firmada_en TEXT, motivo TEXT""",
    "decisiones": """
        -- El porque. Es la tabla mas valiosa: el codigo cuenta el QUE y el git
        -- el CUANDO, pero el motivo de una decision no vive en ningun sitio
        -- salvo aqui.
        id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, asunto TEXT,
        decision TEXT, motivo TEXT, firmada_por TEXT""",
    "fases": """
        nombre TEXT PRIMARY KEY, estado TEXT, entrega TEXT, nota TEXT,
        actualizada_en TEXT""",
    "estado": """
        -- Instantaneas del rack al cerrar sesion. El JSON entero, para poder
        -- calcular deltas de verdad y no de memoria.
        id INTEGER PRIMARY KEY AUTOINCREMENT, sesion TEXT, generado TEXT,
        modo TEXT, rojos INTEGER, json TEXT""",
    "glosario": """
        -- Que significa cada palabra de la casa. Sin esto, «Hexelion»,
        -- «Aurelius» y «P0X» se confunden en cada sesion nueva.
        termino TEXT PRIMARY KEY, definicion TEXT, no_confundir_con TEXT""",
    "necropolis": """
        -- Lo que se intento y se enterro, con la causa. Sin esta tabla se
        -- reintenta lo mismo cada tres meses.
        id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, que TEXT,
        causa_muerte TEXT, resucitable TEXT""",
    "monetizacion": """
        id INTEGER PRIMARY KEY AUTOINCREMENT, via TEXT, estado TEXT, nota TEXT""",
    "escalabilidad": """
        -- Cuellos de botella CON umbral y accion. Un cuello sin metrica es una
        -- opinion, y sobre opiniones no se actua.
        id INTEGER PRIMARY KEY AUTOINCREMENT, componente TEXT, metrica TEXT,
        umbral TEXT, accion TEXT, medido_en TEXT""",
    "loras": """
        nombre TEXT PRIMARY KEY, base TEXT, dataset TEXT, val_loss TEXT,
        estado TEXT, entrenado_en TEXT, nota TEXT""",
    "sesiones_ia": """
        -- Quien trabajo, cuanto, y que dejo a medias. `pendiente` es lo
        -- primero que lee la sesion siguiente.
        id TEXT PRIMARY KEY, inicio TEXT, fin TEXT, cerebro TEXT,
        resumen TEXT, pendiente TEXT""",
    "deltas": """
        -- Que CAMBIO. La pieza anti-perdida-de-linea: una sesion nueva lee los
        -- deltas antes que el snapshot, porque «que ha cambiado desde que te
        -- fuiste» es la pregunta util, no «como esta todo».
        id INTEGER PRIMARY KEY AUTOINCREMENT, sesion TEXT, fecha TEXT,
        area TEXT, cambio TEXT, evidencia TEXT""",
}


def abrir(ruta=None):
    con = sqlite3.connect(str(ruta or DB), timeout=10)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA foreign_keys=ON")
    return con


def init(con):
    for tabla, cols in ESQUEMA.items():
        con.execute(f"CREATE TABLE IF NOT EXISTS {tabla} ({cols})")
    con.commit()
    return sorted(ESQUEMA)


def _upsert(con, tabla, clave, fila):
    cols = ", ".join(fila)
    marcas = ", ".join("?" * len(fila))
    upd = ", ".join(f"{k}=excluded.{k}" for k in fila if k != clave)
    con.execute(f"INSERT INTO {tabla} ({cols}) VALUES ({marcas}) "
                f"ON CONFLICT({clave}) DO UPDATE SET {upd}",
                tuple(fila.values()))


def absorber_estado(con, sesion, ruta=None):
    """Mete el estado.json del recolector en la base y devuelve el delta.

    El delta se calcula contra la instantanea ANTERIOR de la propia base, no
    contra lo que alguien recuerde. Es lo unico que convierte «todo bien» en
    «esto ha cambiado desde que te fuiste».
    """
    ruta = Path(ruta or ESTADO)
    if not ruta.exists():
        return None, [f"NO_DATA: no existe {ruta}. "
                      f"Remedio: python3 ~/p0x/Alejandria/recolector.py --completo"]
    d = json.loads(ruta.read_text(encoding="utf-8"))
    comp = d.get("componentes", {})

    previo = con.execute(
        "SELECT json FROM estado ORDER BY id DESC LIMIT 1").fetchone()
    antes = json.loads(previo[0]).get("componentes", {}) if previo else {}

    cambios = []
    for clave in sorted(set(comp) | set(antes)):
        a = antes.get(clave)
        b = comp.get(clave)
        if clave == "enjambre":
            for agente in sorted(set(a or {}) | set(b or {})):
                ea = ((a or {}).get(agente) or {}).get("estado")
                eb = ((b or {}).get(agente) or {}).get("estado")
                if ea != eb:
                    cambios.append(("enjambre", f"{agente}: {ea or '—'} → {eb or '—'}",
                                    ((b or {}).get(agente) or {}).get("causa", "")))
            continue
        ea = (a or {}).get("estado") if isinstance(a, dict) else None
        eb = (b or {}).get("estado") if isinstance(b, dict) else None
        if ea != eb:
            cambios.append((clave, f"{ea or '—'} → {eb or '—'}",
                            (b or {}).get("causa", "") if isinstance(b, dict) else ""))

    rojos = sum(1 for v in comp.values()
                if isinstance(v, dict) and v.get("estado") == "RED")
    con.execute("INSERT INTO estado (sesion, generado, modo, rojos, json) "
                "VALUES (?,?,?,?,?)",
                (sesion, d.get("generado"), d.get("modo"), rojos,
                 json.dumps(d, ensure_ascii=False)))

    hoy = datetime.now().isoformat(timespec="seconds")
    for area, cambio, evid in cambios:
        con.execute("INSERT INTO deltas (sesion, fecha, area, cambio, evidencia) "
                    "VALUES (?,?,?,?,?)", (sesion, hoy, area, cambio, evid))

    # Los servicios se refrescan desde la medida, no desde la memoria.
    for agente, b in (comp.get("enjambre") or {}).items():
        _upsert(con, "servicios", "nombre", {
            "nombre": agente, "gestor": "user", "cadencia": b.get("cadencia"),
            "estado": b.get("estado"), "nota": b.get("nota") or b.get("causa"),
            "medido_en": d.get("generado")})
    g = comp.get("api_guia") or {}
    if g:
        _upsert(con, "servicios", "nombre", {
            "nombre": "api-guia", "gestor": g.get("gestor"), "cadencia": "continua",
            "estado": g.get("estado"), "nota": g.get("causa") or "unidad de sistema",
            "medido_en": d.get("generado")})
    con.commit()
    return d, cambios


def escribir_delta(con, sesion, area, cambio, evidencia=""):
    con.execute("INSERT INTO deltas (sesion, fecha, area, cambio, evidencia) "
                "VALUES (?,?,?,?,?)",
                (sesion, datetime.now().isoformat(timespec="seconds"),
                 area, cambio, evidencia))
    con.commit()


def bootstrap(con):
    """Genera el prompt de arranque DESDE la base. Nunca a mano."""
    q = lambda s, *a: con.execute(s, a).fetchall()
    L = []
    A = L.append

    ult = q("SELECT sesion, generado, modo, rojos FROM estado ORDER BY id DESC LIMIT 1")
    A("# 🏛️ Arranque de continuidad · Proyecto Alejandría")
    A("")
    A("> **Este fichero se GENERA desde `continuidad.db`. No lo edites a mano.**")
    A("> Un prompt de arranque escrito a mano envejece en silencio, y un arranque")
    A("> que miente cuesta una sesión entera persiguiendo problemas que no existen.")
    A("> Para regenerarlo: `python3 continuidad.py bootstrap`")
    A("")
    if ult:
        s, gen, modo, rojos = ult[0]
        try:
            edad = int(time.time() - datetime.fromisoformat(gen).timestamp())
            frase = (f"hace {edad//3600} h" if edad > 5400
                     else f"hace {max(edad//60,0)} min")
        except (ValueError, TypeError):
            frase = "antigüedad NO_DATA"
        A(f"**Última medida:** `{gen}` ({frase}) · modo `{modo}` · "
          f"**{rojos} componente(s) en rojo** · sesión `{s}`")
    else:
        A("**Última medida:** NO_DATA — nadie ha cerrado sesión todavía.")
    A("")
    A("---")
    A("")

    A("## 0 · Antes de planificar: lee El Acta")
    A("")
    A("Los mensajes de coordinación con `para` que te incluya, y las acciones")
    A("pendientes que dejaron. **Se lee antes que nada:** el delta dice qué")
    A("cambió; el Acta dice qué se te pidió y quién lo espera.")
    A("")
    A("```bash")
    A("python3 -c \"import sys;sys.path.insert(0,'$HOME/p0x/Alejandria/mensajes');"
      "import mensajes as M;[print(m['ts'][:16],m['de'],'→',m['para'],':',"
      "m['humano'][:120]) for m in M.leer()[-5:]]\"")
    A("```")
    A("")
    A("La cadena de hash se verifica sola al abrir el Ojo. Si sale rota, **para**:")
    A("alguien editó un mensaje pasado y el registro dejó de ser un registro.")
    A("")
    A("## 1 · Lee esto antes que nada: qué cambió")
    A("")
    d = q("SELECT fecha, area, cambio, evidencia FROM deltas ORDER BY id DESC LIMIT 15")
    if d:
        A("| Fecha | Área | Cambio | Evidencia |")
        A("|---|---|---|---|")
        for f, a, c, e in d:
            A(f"| {f} | `{a}` | {c} | {(e or '')[:90]} |")
    else:
        A("*Sin deltas registrados.*")
    A("")

    A("## 2 · Falsos rojos ya desmentidos — NO los persigas")
    A("")
    fr = q("SELECT asunto, decision, motivo FROM decisiones "
           "WHERE asunto LIKE 'falso rojo%' ORDER BY id")
    if fr:
        for asunto, dec, mot in fr:
            A(f"- **{asunto.replace('falso rojo · ', '')}** — {dec}")
            A(f"  - *por qué se creía lo contrario:* {mot}")
    else:
        A("*Ninguno registrado.*")
    A("")

    A("## 3 · Doctrina firmada")
    A("")
    for i, regla, alcance, fecha, motivo in q(
            "SELECT id, regla, alcance, firmada_en, motivo FROM doctrina ORDER BY id"):
        A(f"- **{i}** — {regla}" + (f" · *alcance:* {alcance}" if alcance else ""))
        if motivo:
            A(f"  - {motivo}")
    A("")

    A("## 4 · Decisiones y su motivo")
    A("")
    for fecha, asunto, dec, mot, quien in q(
            "SELECT fecha, asunto, decision, motivo, firmada_por FROM decisiones "
            "WHERE asunto NOT LIKE 'falso rojo%' ORDER BY id DESC LIMIT 20"):
        A(f"- **{asunto}** ({fecha}, firmó *{quien}*) — {dec}")
        if mot:
            A(f"  - *motivo:* {mot}")
    A("")

    A("## 5 · Servicios, con su cadencia")
    A("")
    A("*Los `oneshot` están `inactive` entre disparos: **ese es el estado sano**.*")
    A("")
    A("| Servicio | Manager | Cadencia | Estado | Nota |")
    A("|---|---|---|---|---|")
    for n, ges, cad, est, nota, _ in q(
            "SELECT nombre, gestor, cadencia, estado, nota, medido_en "
            "FROM servicios ORDER BY nombre"):
        A(f"| `{n}` | {ges or '?'} | {cad or '?'} | {est or '?'} | {(nota or '')[:70]} |")
    A("")

    A("## 6 · Glosario — no confundir")
    A("")
    for t, d_, nc in q("SELECT termino, definicion, no_confundir_con FROM glosario "
                       "ORDER BY termino"):
        A(f"- **{t}** — {d_}" + (f" · ⚠️ no confundir con {nc}" if nc else ""))
    A("")

    A("## 7 · Fases")
    A("")
    A("| Fase | Estado | Entrega |")
    A("|---|---|---|")
    for n, est, ent, _, _ in q("SELECT nombre, estado, entrega, nota, "
                               "actualizada_en FROM fases ORDER BY nombre"):
        A(f"| {n} | {est} | {ent or ''} |")
    A("")

    A("## 8 · Qué quedó pendiente")
    A("")
    ses = q("SELECT id, fin, cerebro, resumen, pendiente FROM sesiones_ia "
            "ORDER BY inicio DESC LIMIT 5")
    for i, fin, cer, res, pend in ses:
        A(f"- **{i}** ({fin or 'sin cerrar'}, {cer}) — {res}")
        if pend:
            A(f"  - ⏳ **pendiente:** {pend}")
    if not ses:
        A("*Ninguna sesión cerrada todavía.*")
    A("")

    nec = q("SELECT fecha, que, causa_muerte, resucitable FROM necropolis ORDER BY id DESC LIMIT 10")
    if nec:
        A("## 9 · Necrópolis — ya se intentó, no lo repitas")
        A("")
        for f, que, causa, res in nec:
            A(f"- **{que}** ({f}) — murió por: {causa}. Resucitable: {res or 'NO_DATA'}")
        A("")

    esc = q("SELECT componente, metrica, umbral, accion FROM escalabilidad ORDER BY id")
    if esc:
        A("## 10 · Cuellos de botella, con umbral")
        A("")
        A("*Un cuello sin métrica es una opinión, y sobre opiniones no se actúa.*")
        A("")
        A("| Componente | Métrica | Umbral | Acción |")
        A("|---|---|---|---|")
        for c, m, u, ac in esc:
            A(f"| {c} | {m} | {u} | {ac} |")
        A("")

    A("---")
    A("")
    A("*Generado por `continuidad.py bootstrap` desde `continuidad.db`.*")
    texto = "\n".join(L) + "\n"
    BOOTSTRAP.write_text(texto, encoding="utf-8")
    return texto


# --------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="orden", required=True)
    sub.add_parser("init", help="crea el esquema (idempotente)")
    p = sub.add_parser("absorber", help="mete estado.json y calcula el delta")
    p.add_argument("--sesion", required=True)
    p.add_argument("--estado", default=str(ESTADO))
    p = sub.add_parser("delta", help="escribe un delta a mano")
    p.add_argument("--sesion", required=True)
    p.add_argument("--area", required=True)
    p.add_argument("--cambio", required=True)
    p.add_argument("--evidencia", default="")
    sub.add_parser("bootstrap", help="regenera bootstrap_continuidad.md desde la base")
    sub.add_parser("resumen", help="cuenta filas por tabla")
    a = ap.parse_args(argv)

    con = abrir()
    init(con)

    if a.orden == "init":
        print(f"esquema listo · {len(ESQUEMA)} tablas: {', '.join(sorted(ESQUEMA))}")
    elif a.orden == "absorber":
        d, cambios = absorber_estado(con, a.sesion, a.estado)
        if d is None:
            print(cambios[0], file=sys.stderr)
            return 1
        print(f"estado absorbido · {len(cambios)} cambio(s) desde la instantánea anterior")
        for area, cambio, _ in cambios:
            print(f"  · {area}: {cambio}")
    elif a.orden == "delta":
        escribir_delta(con, a.sesion, a.area, a.cambio, a.evidencia)
        print("delta escrito")
    elif a.orden == "bootstrap":
        bootstrap(con)
        print(f"bootstrap regenerado en {BOOTSTRAP}")
    elif a.orden == "resumen":
        for t in sorted(ESQUEMA):
            n = con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
            print(f"  {t:16} {n}")
    con.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
