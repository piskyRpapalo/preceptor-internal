# SPRINT · 2026-08-24

**Para el Soberano, con café. 15 minutos de lectura.**
Detalle completo en [`verificacion_cruzada_v31.md`](verificacion_cruzada_v31.md) ·
Enmiendas en [`enmiendas_v32.md`](enmiendas_v32.md)

---

## 1 · Verificación cruzada · lo que hay que saber antes de firmar

**v3.1 es bueno.** Los 25 módulos que declara existentes, existen. `fase()`,
`punto_decision`, `paso0_presentacion()`, M0–M7, los estados sin FALLO: todo comprobado
literal. La disciplina de «cero nombres nuevos» es la correcta y hay que mantenerla.

**Pero lleva tres cosas que no se sostienen contra el disco:**

| # | Qué | Gravedad |
|---|---|---|
| 1 | **La tabla `hilos` SÍ existe** (`memory.py:111`, más `hilos_eventos` en `:117`, con `test_hilos.py` en verde). v3.1 aceptó una crítica falsa y la enmendó *hacia* el error | 🔴 Corrige en dirección contraria |
| 2 | **D-D no existe.** Los siete `.sh` (afinador, guardián, centinela, peregrino, médico, escriba, cronista) no están en el disco. Lo construido es L0/L4/S0. Y cronificar **exige firma**: `ARQ_LOOPS.md` lo condiciona a *«no se crean servicios systemd sin aprobación explícita»* | 🔴 **No ejecutado** |
| 3 | **D7 repite la forma del Índice I_DT**, enterrado en el archivo por *«falsa precisión: un número compuesto que aparenta medir algo que nadie midió»*. Los cuatro ejes (S,X,Z,W) no tienen sensor hoy | 🔴 Condición, no veto |

**Duplicaciones:** ninguna. Buscado `olvido|repaso|espaciad|FSRS|retenci` en los 225
documentos del archivo: cero. D7/D11 son nuevos de verdad.

**Joyas enterradas que deberían entrar:**

- **El Gólem · «CALIBRA TU RADIO»** — mini-juego que etiquetaba dato real sin que el usuario
  supiera que etiquetaba. Antepasado directo de D2+D7, y **la respuesta al hueco de D7**.
- **La Doctrina del Silencio** — cinco criterios sostenidos **14 días** + voto explícito. Es
  el molde de «criterio de éxito / condición de muerte» que v3.1 inventa de cero, y trae la
  ventana temporal que a D8 le falta.
- **La Necrópolis Vectorial** — la-fragua ya corre embeddings + Qdrant. B.1b y C.5 no están
  muertas: están **en el rack**, que es exactamente D3.

**¿Necesita v3.1 enmienda antes del sprint?** Sí. Seis enmiendas, **todas de coste S**. Es
una tarde de café, no una reescritura.

---

## 2 · Verificación de v3.1 contra el código

| Feature v3.1 | ¿Existe tal como se cita? | Notas |
|---|---|---|
| Los 25 módulos | ✅ 25/25 | Comprobados uno a uno |
| `fase()` extensible (D8) | ✅ | `conversacion.py:220`, puro, 2 consumidores |
| M0–M7 | ✅ | `cara.py:175`. Ocho peldaños, ni uno más |
| `punto_decision` | ✅ | `cara.py:265`, derivado de `M2` |
| Tablas `engrams`/`links`/`profile`/`borradores`/`salidas` | ✅ | `memory.py:45/58/72/98/127` |
| Tabla `hilos` | ❌ **v3.1 se equivoca** | Existe en `memory.py:111` |
| `brujula_estado` cabe en `memory.db` (D7) | ✅ técnicamente | El problema es **qué guarda**, no dónde |
| «Solo biblioteca estándar» | ✅ | Única excepción: `PIL` en `laminas/recortar.py`, herramienta |
| B.1a · FTS5 | ✅ **medido en las dos máquinas** | Ver §3 |
| D9 · SVG sin NetworkX | ✅ viable | Pero depende de que haya ejes que dibujar |

---

## 3 · Mediciones hechas esta noche (con su máquina, como manda D79c)

### Las pruebas

```
Beelink · Python 3.14.4 · /usr/bin/python3 · TMPDIR=/var/tmp ext4
bin/pruebas          282/282 · 17 suites · 6 corredores · VERDE
sabotajes            test_idioma 4/4 · test_fuga 6/6 detectadas
las 13 de fuera      103 pruebas, todas verdes
                     ───────────────────────
TOTAL REAL           385/385 · 30 suites
```

`bin/pruebas` certifica el **73 %** del árbol. **S3 de `PENDIENTES.md` sigue abierta**: subió
de 241 a 282, y las 13 suites que deja fuera son exactamente las mismas.

### FTS5 · **la incógnita que podía tumbar B.1a queda cerrada**

Aprovechando que el Doogee está conectado por tailnet:

| | Doogee (Termux) | Beelink |
|---|---|---|
| Python | 3.14.6 | 3.14.4 |
| sqlite | **3.53.4** | 3.46.1 |
| FTS5 | **DISPONIBLE** | DISPONIBLE |
| 100 engramas, 20 búsquedas | **0.14 ms** por búsqueda | 0.017 ms |

Criterio de éxito de B.1a: < 50 ms. **Cumplido con 350× de margen en el teléfono, que es la
máquina lenta.** B.1a pasa de «depende de una medición» a **lista para construir**.

### El estado del Doogee

```
memory.db     61.440 bytes (60K)   · 2026-08-23 00:41
RAM           11.792 MB total · 7.078 MB disponibles
servicio      bin/aurelius-pwa vivo (pid 18647)
repo          ~/aurelius en 0fb9784
```

---

## 4 · 🔴 Hallazgo nuevo: D-F es más grande de lo que parecía

El encargo trata `9a25dee` como un problema de GitHub. **El blob de 3,54 MB vive en tres
sitios, y dos son tuyos.**

| Dónde | Estado medido |
|---|---|
| `~/p0x/aurelius` (4f2f64e) | ✅ **Limpio.** `git log --all -- ashly_zhao.md` → vacío |
| `~/p0x/aurelius-mvp` | ❌ Rama local `main` clavada en `0fb9784` (*ahead 60 / behind 60*), alcanza `9a25dee`. `.git` = 36 MB |
| **El Doogee** `~/aurelius` | ❌ HEAD en `0fb9784`. Blob `ashly_zhao.md` de **3.541.100 bytes** en el pack, entrado por `6f7bb5a`. `.git` = 18 MB |
| GitHub | ❌ Commit huérfano, esperando gc o ticket |

**El riesgo concreto:** un `git push` desde el Doogee o desde `aurelius-mvp` **resucita la
línea entera en GitHub** y deja el ticket a Support en papel mojado. La purga remota no sirve
de nada mientras dos clones puedan reponer el objeto.

**Acción propuesta (no ejecutada, es tuya):** antes de abrir el ticket, alinear los dos
clones con `origin/main` (`4f2f64e`) y dejarlos sin la referencia vieja. Es destructivo sobre
historia — **no lo hago sin tu firma.**

---

## 5 · El sprint propuesto

Invierto el orden del encargo, y digo por qué: **la brújula no se puede construir con
honestidad hoy, porque nada mide sus ejes.** Delante va lo que produce dato.

| # | Tarea | Prioridad | Coste | Depende de | Criterio de éxito | Condición de muerte |
|---|---|---|---|---|---|---|
| 1 | **v3.2** · las 6 enmiendas (E1–E6) | P0 | S | Tu firma | Las tres falsedades fuera del documento | — |
| 2 | **Regla de higiene systemd/cron** a `CLAUDE.md` + `mente/` | P0 | S | Tu firma | La regla vive donde se lee, no en el archivo | La rechazas y D-D se desbloquea |
| 3 | **B.1a · FTS5 sobre `engrams`** | P1 | M | — (medido ✅) | Búsqueda < 50 ms en Doogee **y** las 30 suites siguen verdes | Si obliga a tocar el `CHECK` de `engrams` |
| 4 | **A.5 · latencia por turno** en `salidas` | P1 | M | — | 20 turnos con `ms` real en las dos máquinas | Si el registro altera el turno medido |
| 5 | **D2 · Path** en `~/.aurelius/path/` | P2 | M | — | Un path se lee y se lista **sin LLM y sin red** | Si necesita LLM para leerse |
| 6 | **D7a · `brujula_estado`** solo registro crudo | P3 | M | 4+5 | Guarda eventos medidos. **Cero columnas calculadas** | Si aparece un número compuesto |
| 7 | **D10 · rama `NO_DATA`** en la Pizarra | P3 | S | 6 | Sin datos, dice que no los tiene | — |
| — | **D7b** (la ecuación `ln(t)`) | — | — | 30 días de D7a | — | Fuera del sprint |
| — | **D8** (Invariante) | — | — | Rediseño con histéresis | — | Fuera del sprint |
| — | **D9** (SVG del campo) | — | — | D7b | — | Fuera del sprint |

Sin cambio y fuera del sprint: **A.1–A.3** (voz — las mides tú en casa), B.2, B.4, B.5, C.4.

---

## 6 · Mediciones que quedan

| Qué medir | Quién | Cuándo | Para qué |
|---|---|---|---|
| ~~FTS5 en Termux~~ | ~~Preceptor~~ | ✅ hecho | ~~B.1a~~ |
| Latencia de turno: Doogee vs Beelink, 4B vs 30B | Soberano (voces) + Preceptor | Prueba de voces | A.5 y los criterios de A.1–A.3 |
| `memory.db` tras 100 turnos (hoy: 60K sin llegar) | Preceptor | Con A.5 | B.2 |
| RAM con el 30B cargado — **`ollama ps` primero, backend anotado** | Preceptor | Antes de D7a | D7a / L3 |

---

## 7 · Deudas heredadas · estado real

| Deuda | Estado medido | Acción del Soberano |
|---|---|---|
| **D-A** rotar contraseña | ABIERTA · fichero fuera de todo git, nunca publicado | **Rotar, despierto.** Esta sesión no ha tocado credenciales |
| **D-B** leer El Rastro | Pendiente | Leer y decidir qué entra al Lore |
| **D-C** firmar Lore Hexelion | PROPUESTA, no canon | Firmar o devolver |
| **D-D** cronificar bucles | ❌ **No existe + requiere firma. NO EJECUTADO.** `crontab -l` → sin crontab | Decidir: ¿se firma la regla de higiene y se escriben los bucles, o se aparca? |
| **D-E** identidad del Faro | Confirmada, y son **dos** campos: `hexelion.near` vs testnet **y** vs `hexelion-beato-01` | Diff propuesto en `p0x/propuestas/`. **Propose-only**: lo aplicas tú en la-fragua |
| **D-F** purga de `9a25dee` | Más grande: el blob vive también en el Doogee y en `aurelius-mvp` | Alinear los dos clones **antes** del ticket a Support |
| **S3** (`PENDIENTES.md`) | Sigue abierta: 282 de 385 certificadas | Candidata a P1 del sprint siguiente |

---

## 8 · Commits de esta sesión

En `aurelius-internal` (privado):

- `docs: verificacion cruzada de v3.1 · tres hechos que no se sostienen`
- `docs: enmiendas v3.2 · seis, todas de coste S`
- `docs: sprint del 24-ago · dato primero, brujula despues`

En `p0x` (forja): la propuesta del Faro, sin aplicar.

**Nada empujado al repo público. Ningún crontab creado. Ninguna credencial tocada. Ningún
comando ejecutado en la-fragua** (solo dos `GET` de lectura al Faro).

---

## 9 · La pregunta

**D-D no se puede ejecutar** —los siete bucles no existen, y cronificar exige una firma que
no está dada—, y v3.1 lleva dos hechos falsos dentro: la tabla `hilos` sí existe, y ninguna
de las cifras que circulan es la de hoy (son **385/385 en 30 suites**, de las que el corredor
certifica 282).

> **¿Firmas v3.2 con las seis enmiendas y el sprint en este orden — dato primero (FTS5,
> latencia, Path), brújula después y solo como registro crudo — o prefieres la brújula
> delante aun sin sensores que la alimenten?**

Y una segunda, que ha aparecido esta noche y no puede esperar al sprint siguiente:

> **¿Alineo el Doogee y `aurelius-mvp` con `origin/main` antes de que abras el ticket a
> Support?** Mientras esos dos clones puedan hacer `push`, la purga remota es reversible.
