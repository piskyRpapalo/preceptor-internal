# VERIFICACIÓN CRUZADA DE v3.1

**Fecha:** noche del 2026-08-23 → 24 · **Sesión:** frontera (`P0X_BRAIN` sin poner)
**Entrada:** v3.0 + v3.1 (documento del Soberano), las deudas D-A…D-F, el archivo
clasificado del 2026-08 y el árbol vivo de `aurelius`, `aurelius-mvp` y `aurelius-internal`.

> Todo lo que sigue está medido contra el disco esta noche. Cuando digo «no existe», lo he
> buscado; cuando doy una cifra, la he corrido. El comando va al lado para que no haya que
> creerme.

---

## 0 · Veredicto en tres líneas

El documento v3.1 es bueno y su disciplina —«cero nombres nuevos», mapeo contra módulos
reales— es la correcta. **Pero lleva dentro dos hechos falsos y una decisión que repite un
descarte ya firmado**, y la tarea que el encargo declara «puramente mecánica» (D-D) **no se
puede ejecutar**: los ficheros que manda cronificar no existen, y cronificar exige una firma
que no está dada.

No he tocado el crontab. No he tocado la-fragua. No he tocado ninguna credencial.

---

## 1 · Verificación contra el código actual

### 1.1 · Los 25 módulos: 25/25 existen

Comprobado uno a uno en `~/p0x/aurelius`. Todos los que v3.1 declara existentes, existen,
y con el papel que les asigna:

| Pieza que v3.1 cita | Dónde está de verdad |
|---|---|
| `fase()` · el punto de decisión | `conversacion.py:220` · puro, 15 líneas |
| `FASES` | `conversacion.py:119` · `("nucleo","decision","side_quest","proyecto")` |
| `punto_decision` | `cara.py:265` · se deriva de `M2 == "hecho"` |
| El Camino M0–M7 | `cara.py:175` · ocho peldaños, ni uno más |
| `paso0_presentacion()` | `aurelius.py:273` · solo corre si el perfil tiene huecos |
| `progreso_camino()` | `cara.py:201` |
| `cruzar_frontera()` | `memory.py:707` |
| `respaldar()` / `restaurar()` | `memory.py:561` / `memory.py:600` |
| `promover_a_engrama()` | `memory.py:833` |
| `importar()` | `memory.py:895` |

Los consumidores de `fase()` son dos —`aurelius.py:647` y `conversacion.py:344`— más las
pruebas. **D8 es extensible sin cirugía**; el problema de D8 es otro (§2.4).

### 1.2 · Las tablas de `memory.db`

```bash
grep -n "create table\|CREATE TABLE" ~/p0x/aurelius/memory.py
```

| Tabla | Línea | v3.1 acierta |
|---|---|---|
| `engrams` | `memory.py:45` | Sí |
| `links` | `memory.py:58` | Sí |
| `profile` | `memory.py:72` (`ESQUEMA_PERFIL`, aparte a propósito) | Sí |
| `borradores` | `memory.py:98` | Sí |
| **`hilos`** | **`memory.py:111`** | **NO — ver §2.2** |
| **`hilos_eventos`** | **`memory.py:117`** | **NO — ver §2.2** |
| `salidas` | `memory.py:127` | Sí |

### 1.3 · «Solo biblioteca estándar»: cierto, con una excepción conocida

```bash
find ~/p0x/aurelius -name "*.py" -not -path "*/.*" -exec grep -H "^import\|^from" {} +
```

Una sola dependencia fuera de la stdlib en todo el árbol: **`PIL` en
`laminas/recortar.py:19`**. Es herramienta de assets, no runtime del producto. La promesa
del README se sostiene — y por eso partir B.1 fue la enmienda correcta.

### 1.4 · FTS5: disponible aquí, sin medir allí

```
Python 3.14.4 · sqlite 3.46.1 · FTS5: DISPONIBLE
```

Medido en el Beelink. **En el Doogee (Termux) no está medido**, y es la única incógnita que
puede tumbar B.1a. Va a la lista de mediciones.

### 1.5 · ¿Cabe la brújula (D7) en `memory.db`?

Técnicamente sí: una tabla más en el mismo fichero, con la misma regla de cero `DELETE`, no
rompe nada del esquema actual. La corrección 4 (no reintroducir `system_state.db`) está bien
aplicada. **El problema de D7 no es dónde vive: es qué guarda** (§2.3).

---

## 2 · Lo que no se sostiene

### 2.1 · 🔴 D-D no existe — y aunque existiera, está vetado

**Los siete bucles que D-D manda cronificar no existen en ningún sitio del disco.**

```bash
for n in afinador guardian centinela peregrino medico escriba cronista; do
  find ~ -maxdepth 6 -name "*${n}*.sh" -not -path '*/.git/*'; done
```

Resultado: cero coincidencias para `afinador`, `peregrino`, `medico`, `cronista`. Las de
`guardian` y `escriba` son otras cosas (`guardian_sync.sh` de la LoRA, `mente/voces/escriba.md`).
`centinela` solo aparece como `centinela_termico.py` en `~/pre-bee`, de otro proyecto.

Lo que sí está construido en `agentes/bucles/` es **otra cosa y con otros nombres**:

| Fichero | Qué es |
|---|---|
| `latido.py` | L0 · loops.db, estados, `@sleeping`, histéresis |
| `director.py` | L4 · el meta-bucle |
| `s0.py` | S0 · el monitor de fallo silencioso |
| `test_bucles.py` | 17 pruebas de las cuatro refinaciones |

Los siete nombres de D-D son **los bucles de L1 y L3 que `ARQ_LOOPS.md` marca
`[pendiente]`**. No están escritos. D-D confundió el mapa con el territorio.

**Y cronificar no es mecánico.** `agentes/ARQ_LOOPS.md`, §«Lo que falta», dice literalmente
que cronificar el Director **requiere aprobación explícita**, y cita la regla de higiene que
`docs/archivo_2026-08/REVISION_CRUZADA.md` §3 pone la primera de toda la doctrina que nunca
llegó al repo:

> *«no se crean servicios systemd sin aprobación explícita del Soberano»*
> *«`systemctl list-units` al cerrar cada sesión de Claude Code — un servicio fantasma con
> autoridad es la semilla del próximo IronClaw»*

El encargo autorizaba D-D «porque es mecánico y no toca doctrina». **Toca doctrina de
frente**, y es la doctrina escrita para sesiones exactamente como esta.

Estado al cerrar, verificado:

```
crontab -l                      → no crontab for pisky
systemctl --user list-timers    → 3 timers, todos de Ubuntu (launchpadlib, ubuntu-insights ×2)
```

**No he creado nada. Queda tal cual.**

### 2.2 · 🔴 La tabla `hilos` sí existe — v3.1 corrigió hacia el error

v3.1 aceptó esta crítica: *«hilos.py existe; la tabla hilos no. Los hilos son engramas con
tipo='hilo', no tabla separada»*. **Es falso, y la crítica original también lo era.**

`memory.py:110-124`:

```sql
CREATE TABLE IF NOT EXISTS hilos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    origen_dispositivo TEXT NOT NULL DEFAULT 'NO_DATA',
    creado_en TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS hilos_eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hilo_id INTEGER NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('abierto','tocado','cerrado','reabierto')),
    momento TEXT NOT NULL,
    FOREIGN KEY (hilo_id) REFERENCES hilos(id)
);
```

Comentario en el propio fichero: *«D14: Esquema de Hilos y Eventos (Event Sourcing)»*. Y
`test_hilos.py` corre 11 pruebas verdes contra ellas.

**Consecuencia si se ejecuta v3.1 tal cual:** C.3 («extensión de `importar()`») y M5 se
reescribirían contra engramas `tipo='hilo'` — una columna que no existe en `engrams`, cuyo
`CHECK` de `origin` solo admite `persona|intencion|importado`. Rompería una tabla viva para
sustituirla por una peor.

Esto es lo más serio del cruce, porque **no es un hueco: es una corrección que va en
dirección contraria**. Un documento que corrige hacia el error es peor que uno que calla.

### 2.3 · 🔴 D7 repite la forma del Índice I_DT, ya enterrado

`docs/archivo_2026-08/REVISION_CRUZADA.md:24`, tabla «Ideas descartadas que NO deben
resucitarse»:

| Idea | Por qué NO |
|---|---|
| **Índice I_DT** | Falsa precisión: un número compuesto que aparenta medir algo que nadie midió |

D7 compone cuatro ejes (S estabilidad, X recuperación, Z dificultad, W desarrollo) en una
dirección de progresión. **Hoy ninguno de los cuatro tiene sensor.** Buscado en el árbol:
no hay nada que registre dificultad percibida, ni recuperación, ni dominio, ni por turno ni
por ejercicio. `salidas` guarda cruces de frontera; `engrams`, recuerdos. Ni una de las
cuatro magnitudes se mide en ningún sitio.

`R = dS/dt = ln(t)` en stdlib puro es cierto y no rompe F1. **La objeción no es la
implementación: es que la ecuación llega antes que el dato.** Un campo vectorial calculado
sobre cuatro variables que nadie mide es exactamente el I_DT con otro nombre y mejor
tipografía.

**No es veto. Es condición:** primero el sensor, después la ecuación. En §3 del sprint eso
se traduce en `brujula_estado` como **registro crudo de eventos medidos**, sin índice
compuesto y sin dirección, hasta que haya con qué calcularla.

Y el archivo ya dice de dónde puede salir el dato — ver §4.1, El Gólem.

### 2.4 · 🟡 D8 no lleva histéresis, y eso ya se pagó

D8 dispara con umbral seco: *«bloquear avance si `dS/dt < -0.5` y `W >= 4`»*.

El archivo documenta este error con nombre y cicatriz. `REVISION_CRUZADA.md` §5, fila
«`load>2 → posponer`»:

> **Histéresis de 5 minutos contra el flapping.** […] con carga oscilando alrededor del
> umbral, un loop entra y sale sin hacer nada. **Ya le pasó.**

Y el rack ya lo tiene resuelto en código: `latido.cambiar_estado()` exige **dos ventanas de
evidencia sostenida Y un descanso mínimo de 300 s**, y es el único camino para mover un
estado — `registrar()` no puede tocarlo.

Un invariante pedagógico que bloquea y desbloquea al oscilar `dS/dt` alrededor de −0.5 es un
invariante que la persona aprende a ignorar en dos días. **D8 necesita rediseño con
histéresis antes de que se escriba una línea**, y el molde está a un `import` de distancia.

### 2.5 · 🟡 Las cifras: ninguna de las que circulan es la de hoy

Corrido entero esta noche:

```bash
cd ~/p0x/aurelius && bin/pruebas
```

```
Python 3.14.4 · /usr/bin/python3 · TMPDIR=/var/tmp · ext4 · 516G libres
282 pruebas · 17 suites · 6 corredores
SABOTAJES · test_idioma.py 4/4 · test_fuga.py 6/6 detectadas
VERDE · 282/282
```

Pero en el árbol hay **30 ficheros `test_*.py`**, y `bin/pruebas:140-142` solo declara 17
(12 `UNITTEST` + 5 `PROPIAS`). Corridas a mano las 13 que quedan fuera:

| suite | pruebas | | suite | pruebas |
|---|---|---|---|---|
| `andamio` | 3 | | `narrador` | 7 |
| `borradores` | 6 | | `puente` | 6 |
| `conversacion` | 30 | | `puerta` | 7 |
| `costura` | 6 | | `recuperacion` | 4 |
| `frontera` | 4 | | `traza` | 7 |
| `fusible` | 9 | | | |
| `hilos` | 11 | | **suma** | **103** |
| `identidad` | 3 | | | |

Todas verdes.

> **La cifra real de esta noche: 385/385 · 30 suites.**
> De ellas, `bin/pruebas` certifica **282 · 17 suites**.

Ninguna de las cuatro que circulaban (20+, 254/19, 333/26, «30 ficheros») es la de hoy. Y
las 13 de fuera son **exactamente** las que `~/p0x/mente/feedback/PENDIENTES.md` S3 enumeró:
la deuda no ha cambiado de fondo, solo de numerador (241 → 282). Sigue cantando verde sobre
el 73 % del árbol.

### 2.6 · 🟡 El estado de los repos no es el que dice el encargo

| El encargo dice | Medido |
|---|---|
| aurelius (público) → `0fb9784`, tag v1.0.0 | `origin/main` = **`4f2f64e`** · tag `v1.0.0` = **`3e21952`** · ninguno es `0fb9784` |
| — | `aurelius-mvp` tiene la rama local `main` clavada en `0fb9784`, **ahead 60 / behind 60**: la línea previa a la reescritura, viva en el disco |
| `9a25dee` sigue en GitHub | **Y aquí**: `git cat-file -t 9a25dee` → `commit`, en el clon local de `aurelius-mvp` |
| aurelius-internal → `fac92e5` | Correcto |

Dos árboles de trabajo (`p0x/aurelius` y `p0x/aurelius-mvp`) apuntan al mismo remoto con
HEAD y ramas distintas. Y **`aurelius-internal/` figura como `??` sin seguimiento dentro de
`p0x`** — el mismo pie que ya produjo el commit `9368dc8 chore: sacar el gitlink accidental
de aurelius/`. Merece decisión explícita: `.gitignore` o submódulo, pero no silencio.

### 2.7 · 🟡 D-E son dos incoherencias, no una

Leído en vivo, solo `GET`, sin tocar la-fragua:

```
/.well-known/hexelion-attestation.json → "node": "hexelion.near"
/health                                → "network": "testnet", "node": "hexelion-beato-01"
```

`ESTADO_FINAL.md` declara una incoherencia (mainnet vs testnet). **Son dos**: el nombre
tampoco es el mismo nodo. Un `sed` sobre un solo campo dejaría la mitad del error puesto.

Y vive en la-fragua → **propose-only**. Sale como diff en `p0x/propuestas/`, no por SSH desde
aquí.

---

## 3 · Verificación 1 · Duplicaciones

Cruzadas las 19 features de v3.1 contra `CLASIFICACION.md`, `ANEXO_PASADA_LOCAL.md` (225
documentos) y `REVISION_CRUZADA.md`.

**Duplicación crítica: ninguna.** Ninguna feature de v3.1 aparece en el archivo con otro
nombre y otro veredicto. Buscado explícitamente `olvido|repaso|espaciad|FSRS|retenci` en el
archivo clasificado: **cero coincidencias**. D7/D11 son genuinamente nuevos, no un zombi.

Dos solapamientos que no son duplicación pero conviene declarar:

- **B.1b / C.5 (embeddings, RAG) ↔ «La Necrópolis Vectorial»** (`REVISION_CRUZADA.md` §2.2).
  v3.1 las aparca por romper stdlib, y hace bien. Pero omite que **la capacidad ya existe un
  nodo más allá**: la-fragua corre embeddings + Qdrant. No están muertas: están **en el
  rack**, que es exactamente lo que dice D3. Decirlo evita que vuelvan a proponerse desde
  cero en tres meses.
- **A.7 (hardware-aware) ↔ el Score S0** (`CODICE_2026_14` §VI, vía §5 de la revisión): ya
  hay un patrón de tres bandas con umbrales ajustables sin tocar código. A.7 no necesita
  inventar su escalera.

---

## 4 · Verificación 2 · Joyas enterradas que v3.1 no cita

### 4.1 · El Gólem · «CALIBRA TU RADIO» — la que resuelve el hueco de D7

`REVISION_CRUZADA.md` §2.4:

> Un mini-juego que entrenaba el clasificador de señal **sin que el usuario supiera que
> estaba etiquetando**. Es la idea con más parentesco con Aurelius de todo el archivo
> —misiones jugables que producen dato real— y no pasó del documento.

**Es el antepasado directo de D2 + D7**, y responde justo a la objeción de §2.3: de dónde
salen las medidas de los cuatro ejes sin convertir el Camino en un formulario. Debe entrar
en v3.2 como genealogía de D2, igual que FSRS entra como genealogía de D7 (D11).

### 4.2 · El lazo de comprensión de tres ramas

`REVISION_CRUZADA.md` §2.2: reducido a **una sola rama** porque el clasificador era un 1.5B
en CPU y confundía omisión con ruptura. Hoy hay 30B con salida estructurada verificada.
*Lo que falta es el set de ejemplos etiquetados a mano que el propio documento exige.*

Mismo hueco que D7, y la misma respuesta: el dato antes que el modelo.

### 4.3 · La Doctrina del Silencio — el molde de «criterio de éxito»

`REVISION_CRUZADA.md` §5: no es «el carbono firma», son **cinco criterios cuantitativos
sostenidos 14 días MÁS voto explícito** — *«sin voto no se promueve, aunque los números
cuadren»* — con circuit breaker de degradación inversa.

v3.1 inventa de cero sus columnas «criterio de éxito / condición de muerte». **El molde ya
existe, y trae la ventana temporal que a D8 le falta.**

### 4.4 · Los tres ejes del descarte y la métrica anti-teología

`REVISION_CRUZADA.md` §3: *«El vocabulario de veredictos vive; el criterio con el que se
emiten, no.»* v3.1 usa F1/F2/F3 como criterio. Merece decirse si F1/F2/F3 **son** esos tres
ejes con otro nombre o algo distinto — si son lo mismo, sobra uno de los dos vocabularios.

### 4.5 · La regla de higiene systemd — la que bloquea D-D

Ya tratada en §2.1. Es la joya más urgente porque **no está ni en `mente/` ni en
`CLAUDE.md`**, y con bucles 24/7 en el horizonte su ausencia deja de ser incómoda.

---

## 5 · Verificación 3 · Contradicciones

| Plan viejo | v3.1 | Resolución |
|---|---|---|
| Crítica del Preceptor: «la tabla `hilos` no existe» | Aceptada como enmienda | **Manda el código.** Existe (`memory.py:111`). Se revierte |
| Índice I_DT: descartado por falsa precisión | D7 compone 4 ejes sin sensores | **Manda el descarte, con condición.** D7 entra como registro crudo; el índice, cuando haya dato |
| Filtro de Eficiencia: histéresis obligatoria | D8 con umbral seco | **Manda el archivo.** D8 se rediseña o no entra |
| `ARQ_LOOPS.md`: cronificar requiere firma | Encargo: «D-D es mecánico, ejecútalo» | **Manda la doctrina.** Parado |
| DePIN / multi-tenant / reparto automático (vetado por CANON-C) | D5: «cada hermano su propio Aurelius, sin multi-tenant» | **Coherente.** No hay contradicción: v3.1 confirma el veto |
| Doctrina de Solitud: nada de red con SLA | D4: asíncrono por defecto, Tailscale como infra del Soberano | **Coherente.** Infra propia ≠ protocolo público |

**Contradicciones abiertas que hereda el Soberano: ninguna nueva.** Las cuatro primeras se
resuelven en v3.2 con las enmiendas de `docs/enmiendas_v32.md`.

---

## 6 · ¿Necesita v3.1 una enmienda antes del sprint?

**Sí, y es barata: tres correcciones y una condición.** Están redactadas en
[`enmiendas_v32.md`](enmiendas_v32.md). Sin ellas, el sprint arrancaría reescribiendo una
tabla viva (§2.2) y construyendo un índice sin sensores (§2.3).

Lo que **no** hay que cambiar de v3.1: el descarte de C.5, la partición de B.1 en FTS5 +
embeddings, la corrección del título y de §6.6, las correcciones 4 y 5 (nada de
`system_state.db`, nada de NetworkX), y D1–D6, D9–D11. Todo eso está bien y está verificado.
