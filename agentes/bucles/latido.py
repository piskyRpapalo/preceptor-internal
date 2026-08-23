#!/usr/bin/env python3
"""L0 · El latido. La infraestructura de la que cuelgan todos los bucles.

**Solo biblioteca estándar.** Un sistema de vigilancia que necesita instalar algo
para arrancar es un sistema que no arranca el día que importa.

TRES DECISIONES QUE NO SON DE ESTILO
------------------------------------

**1 · El latido es append-only, y lo impone la base de datos.**
No «por convención», no «por disciplina del que escribe»: hay dos disparadores
de SQLite que hacen fallar cualquier UPDATE o DELETE sobre la tabla de latidos.
Un latido que se puede sobrescribir pierde la historia del fallo, que es justo
lo que se quiere leer cuando algo lleva tres semanas muriéndose despacio. La
historia no se reescribe.

**2 · Ningún estado cambia por un solo evento (histéresis).**
Un bucle no pasa a muerto porque una ejecución falló, ni vuelve a vivo porque
una salió bien. Hace falta evidencia sostenida **y** que haya pasado un tiempo
mínimo desde el último cambio. Sin esto, con la carga oscilando alrededor del
umbral, un bucle entra y sale de servicio sin llegar a hacer nada — y la bandeja
de firmas se llena de ruido hasta que alguien la apaga.

**3 · Dormir un bucle exige escribir qué lo despierta.**
No se puede marcar `@sleeping` sin condición de despertar. Es un `NOT NULL` en
el esquema, no una recomendación. Una capacidad retirada sin condición escrita
es una capacidad perdida: dentro de seis meses nadie sabrá si ya toca.
"""

from __future__ import annotations

import contextlib
import os
import sqlite3
import time

RUTA_DEFECTO = os.path.expanduser("~/.aurelius/loops.db")

# Cuánto tiene que aguantar un estado antes de poder cambiar. Cinco minutos
# salen de la histéresis del filtro de eficiencia del archivo: es el tiempo que
# ya se midió como suficiente para que el flapping deje de producir ruido.
DESCANSO_ESTADO_S = 300

# Cuántas ventanas seguidas sin latido hacen sospechar. Dos, no una: una
# ventana perdida es un reinicio; dos seguidas es una avería.
VENTANAS_PARA_DUDAR = 2

CLASES = ("LIGERO", "MEDIO", "PESADO")
RESULTADOS = ("ok", "fallo", "pospuesto", "saltado")
ESTADOS = ("vivo", "muerto", "dormido")

ESQUEMA = """
CREATE TABLE IF NOT EXISTS bucles (
  nombre               TEXT PRIMARY KEY,
  clase                TEXT NOT NULL CHECK (clase IN ('LIGERO','MEDIO','PESADO')),
  ventana_s            INTEGER NOT NULL,
  estado               TEXT NOT NULL DEFAULT 'vivo'
                       CHECK (estado IN ('vivo','muerto','dormido')),
  estado_desde         REAL NOT NULL,
  -- Dormir exige decir que despierta. Sin esto, `@sleeping` es un borrado
  -- con mejores modales.
  motivo_sueno         TEXT,
  condicion_despertar  TEXT,
  CHECK (estado <> 'dormido'
         OR (motivo_sueno IS NOT NULL AND condicion_despertar IS NOT NULL))
);

CREATE TABLE IF NOT EXISTS latidos (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  bucle      TEXT NOT NULL,
  momento    REAL NOT NULL,
  evento     TEXT NOT NULL CHECK (evento IN ('entra','sale')),
  resultado  TEXT CHECK (resultado IN ('ok','fallo','pospuesto','saltado')),
  duracion_s REAL,
  nota       TEXT
);
CREATE INDEX IF NOT EXISTS idx_latidos_bucle ON latidos(bucle, momento);

-- El append-only, impuesto por el motor y no por la buena voluntad de quien
-- escriba el proximo bucle a las tres de la manana.
CREATE TRIGGER IF NOT EXISTS latidos_no_se_editan
BEFORE UPDATE ON latidos
BEGIN
  SELECT RAISE(ABORT, 'los latidos no se editan: la historia no se reescribe');
END;

CREATE TRIGGER IF NOT EXISTS latidos_no_se_borran
BEFORE DELETE ON latidos
BEGIN
  SELECT RAISE(ABORT, 'los latidos no se borran: la historia no se reescribe');
END;

-- Los cambios de estado tambien son historia, y por el mismo motivo.
CREATE TABLE IF NOT EXISTS estados (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  bucle    TEXT NOT NULL,
  momento  REAL NOT NULL,
  desde    TEXT NOT NULL,
  hasta    TEXT NOT NULL,
  motivo   TEXT NOT NULL
);
CREATE TRIGGER IF NOT EXISTS estados_no_se_editan
BEFORE UPDATE ON estados
BEGIN
  SELECT RAISE(ABORT, 'los cambios de estado no se editan');
END;
CREATE TRIGGER IF NOT EXISTS estados_no_se_borran
BEFORE DELETE ON estados
BEGIN
  SELECT RAISE(ABORT, 'los cambios de estado no se borran');
END;

-- Lo que produce cada filtro. Sin esto no hay forma de saber que un detector
-- lleva una semana sin detectar porque esta roto (ver s0.py).
CREATE TABLE IF NOT EXISTS hallazgos (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  bucle    TEXT NOT NULL,
  momento  REAL NOT NULL,
  clave    TEXT NOT NULL,
  detalle  TEXT
);
CREATE INDEX IF NOT EXISTS idx_hallazgos_bucle ON hallazgos(bucle, momento);
"""


@contextlib.contextmanager
def abrir(ruta=RUTA_DEFECTO):
    """Conexión con diario WAL y disparadores vivos."""
    os.makedirs(os.path.dirname(os.path.abspath(ruta)), exist_ok=True)
    c = sqlite3.connect(ruta, timeout=30)
    c.row_factory = sqlite3.Row
    try:
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("PRAGMA foreign_keys=ON")
        c.executescript(ESQUEMA)
        yield c
        c.commit()
    finally:
        c.close()


def registrar(c, nombre, clase, ventana_s):
    """Da de alta un bucle, o actualiza su clase y ventana. Nunca su estado.

    El estado lo mueve `cambiar_estado`, que es quien aplica la histéresis. Si
    esta función pudiera tocarlo, cualquier arranque de bucle resucitaría al
    muerto y el Director no se enteraría nunca.
    """
    if clase not in CLASES:
        raise ValueError(f"clase desconocida: {clase}")
    c.execute(
        "INSERT INTO bucles (nombre, clase, ventana_s, estado, estado_desde) "
        "VALUES (?,?,?,'vivo',?) "
        "ON CONFLICT(nombre) DO UPDATE SET clase=excluded.clase, "
        "ventana_s=excluded.ventana_s",
        (nombre, clase, int(ventana_s), time.time()))


def entra(c, nombre, nota=None):
    """Latido de entrada. Se escribe ANTES de trabajar."""
    c.execute("INSERT INTO latidos (bucle, momento, evento, nota) VALUES (?,?,'entra',?)",
              (nombre, time.time(), nota))


def sale(c, nombre, resultado, duracion_s=None, nota=None):
    """Latido de salida. Sin esto, la ejecución no cuenta."""
    if resultado not in RESULTADOS:
        raise ValueError(f"resultado desconocido: {resultado}")
    c.execute("INSERT INTO latidos (bucle, momento, evento, resultado, duracion_s, nota) "
              "VALUES (?,?,'sale',?,?,?)",
              (nombre, time.time(), resultado, duracion_s, nota))


def hallazgo(c, nombre, clave, detalle=None):
    """Algo que el bucle encontró. Es el alimento del monitor de fallo silencioso."""
    c.execute("INSERT INTO hallazgos (bucle, momento, clave, detalle) VALUES (?,?,?,?)",
              (nombre, time.time(), clave, detalle))


def ultimo_latido(c, nombre, evento="sale"):
    f = c.execute("SELECT * FROM latidos WHERE bucle=? AND evento=? "
                  "ORDER BY momento DESC LIMIT 1", (nombre, evento)).fetchone()
    return f


def salidas_recientes(c, nombre, cuantas=3):
    return c.execute("SELECT * FROM latidos WHERE bucle=? AND evento='sale' "
                     "ORDER BY momento DESC LIMIT ?", (nombre, cuantas)).fetchall()


def cambiar_estado(c, nombre, nuevo, motivo, ahora=None, descanso_s=DESCANSO_ESTADO_S):
    """El único camino para mover un estado. Aplica la histéresis.

    Devuelve (cambiado, motivo_de_la_decisión). No cambia y lo dice cuando el
    estado actual lleva menos de `descanso_s` puesto: un bucle que oscila entre
    vivo y muerto cada dos minutos no informa de nada, solo hace ruido en la
    bandeja de firmas hasta que alguien deja de mirarla.

    El sueño es la excepción: dormir y despertar son decisiones del carbono, no
    lecturas de un sensor, así que no esperan.
    """
    if nuevo not in ESTADOS:
        raise ValueError(f"estado desconocido: {nuevo}")
    ahora = time.time() if ahora is None else ahora
    fila = c.execute("SELECT estado, estado_desde FROM bucles WHERE nombre=?",
                     (nombre,)).fetchone()
    if fila is None:
        raise KeyError(f"bucle no registrado: {nombre}")
    actual, desde = fila["estado"], fila["estado_desde"]
    if actual == nuevo:
        return False, "ya estaba en ese estado"

    decision_humana = "dormido" in (actual, nuevo)
    if not decision_humana and (ahora - desde) < descanso_s:
        faltan = int(descanso_s - (ahora - desde))
        return False, (f"histéresis: {actual} lleva puesto menos de "
                       f"{descanso_s} s, faltan {faltan} s")

    c.execute("UPDATE bucles SET estado=?, estado_desde=? WHERE nombre=?",
              (nuevo, ahora, nombre))
    c.execute("INSERT INTO estados (bucle, momento, desde, hasta, motivo) "
              "VALUES (?,?,?,?,?)", (nombre, ahora, actual, nuevo, motivo))
    return True, f"{actual} → {nuevo}"


def dormir(c, nombre, motivo, condicion_despertar):
    """`@sleeping`: retirar sin borrar. Exige la condición de despertar.

    «El organismo no rompe con su pasado. Lo pone en pausa, y guarda la llave.»
    La llave es la condición: sin ella, dentro de seis meses nadie sabrá si ya
    toca despertarlo, y un bucle dormido para siempre es un bucle borrado con
    mejores modales.
    """
    if not (motivo and motivo.strip()):
        raise ValueError("dormir un bucle exige motivo")
    if not (condicion_despertar and condicion_despertar.strip()):
        raise ValueError("dormir un bucle exige escribir qué lo despierta")
    c.execute("UPDATE bucles SET motivo_sueno=?, condicion_despertar=? WHERE nombre=?",
              (motivo.strip(), condicion_despertar.strip(), nombre))
    return cambiar_estado(c, nombre, "dormido", f"dormido: {motivo.strip()}")


def despertar(c, nombre, motivo):
    cambiado, razon = cambiar_estado(c, nombre, "vivo", f"despertado: {motivo}")
    if cambiado:
        c.execute("UPDATE bucles SET motivo_sueno=NULL, condicion_despertar=NULL "
                  "WHERE nombre=?", (nombre,))
    return cambiado, razon


@contextlib.contextmanager
def turno(nombre, clase, ventana_s, ruta=RUTA_DEFECTO):
    """Envoltorio para un bucle entero: late al entrar y al salir, pase lo que pase.

    Un bucle que revienta a mitad deja su latido de fallo escrito. Sin esto, una
    excepción no controlada es indistinguible de un bucle que nunca arrancó.
    """
    inicio = time.time()
    with abrir(ruta) as c:
        registrar(c, nombre, clase, ventana_s)
        entra(c, nombre)
    caja = {"resultado": "ok", "nota": None}
    try:
        yield caja
    except BaseException as e:
        caja["resultado"] = "fallo"
        caja["nota"] = f"{type(e).__name__}: {e}"[:400]
        raise
    finally:
        with abrir(ruta) as c:
            sale(c, nombre, caja["resultado"], time.time() - inicio, caja["nota"])
