# REVISIÓN CRUZADA

**Fecha:** 2026-08-23 · **Fase:** Revisor (equipo de lectura)
**Entrada:** [INVENTARIO](INVENTARIO_MATERIAL_DISPERSO.md) · [CLASIFICACIÓN](CLASIFICACION.md) · [RASTRO](RASTRO_DEL_SOBERANO.md)

Cruce del material del archivo contra el estado real de `aurelius-mvp`, `p0x` y
`aurelius-internal` a 2026-08-23. Esbozo: cubre los 81 documentos leídos con token de
frontera. La pasada local sobre los 231 restantes lo ampliará.

---

## 1 · Ideas descartadas que NO deben resucitarse

Cada una con el motivo por el que murió. **El motivo importa más que el veredicto**: sin
él, la idea vuelve en tres meses con otro nombre.

| Idea | Por qué NO |
|---|---|
| **Protocolo público de 5 tiers** (Gólem, HexelionOS, el Nexo como red, token $SOLARIS, marco legal LDA + MiCA) | Anulado por la Doctrina de Solitud del 24-may, y rematado por la decisión de hoy: un mueble en el jardín no sostiene una red con SLA comercial. Resucitarlo reabre la capa jurídica entera |
| **Omni-Node v6.5 / La Legión DePIN** (~20 protocolos repartidos entre HP1 y HP2) | El hardware no existe: hp-01 inhabilitado desde 2026-08-04, hp-02 medido como Chromebook de 7,6 GB sin GPU. Y `DOCTRINA_P0X_PRODUCTO` CANON-C veta el DePIN con reparto automático de valor |
| **Solver JIT y todo el frame de trading** | Enterrado con ingeniería, no con opinión: latencia MPC de 30 s + riesgo de inventario. El razonamiento está en `2026-05-30_Escalpelo_Necropolis_Trading.md` y sigue siendo correcto |
| **Nexo-Engine** (claves de terceros en RAM) | Custodia. Contradice de frente «jamás firmas valor» y el patrón de clave acotada |
| **Control autónomo del agente energético** | Se guardó solo el pronosticador **propose-only**. El control autónomo es un bucle que actúa: exactamente lo que la lección del 11 de mayo prohíbe |
| **Índice I_DT** | Falsa precisión: un número compuesto que aparenta medir algo que nadie midió |
| **Auto-generación de código ejecutable** | Misma familia: un bucle que produce y ejecuta sin firma |
| **`hexelion_m2m_manifest`** (mainnet, `no_human_required: true`) | La propia auditoría ordenó retirarlo. Declara como activos hardware que nunca llegó y una cuenta de mainnet como identidad M2M. **Además contiene material que no debe salir del disco** |
| **La estrategia de `SINTESIS_hexelion-lab...2026-06-14`** | Formalmente revocada por CANON-A y CANON-C. Es el documento con más potencial de confundir de todo el archivo: leído como vigente, reconstruye una estrategia vetada |

---

## 2 · Ideas abandonadas que SÍ merecen revisitarse

Ordenadas por relación valor/riesgo, no por entusiasmo. **La columna que decide es «por
qué hoy sí»**: casi todas murieron por hardware o software de 2026-05, y ese motivo ha
caducado.

### 2.1 · Encender lo que ya está construido

**El Faro.** Verificado por mí, no por el informe: en `~/pre-bee/hexelion/faro/` hay
`chain_verify.py`, `faro_admin.py`, `faro_anchor.py`, `faro_client.py`, `faro_mcp.py`,
`faro_proof.py`, `faro_verify.py` y más, con pruebas de inclusión Merkle persistidas para
los epochs **13, 19, 23 y 25**. En `faro/keys/` solo hay `anchor_fc.pub` y
`attest_ed25519.pub` — **las privadas no están ahí**, y eso hay que resolverlo antes de dar
nada por vivo. No es un plan: es un oráculo de atestación firmada, pagable por HTTP 402 y
consumible por MCP, apagado desde julio.
*Por qué hoy sí:* hay cliente MCP nativo, que en mayo no existía.

**peaq · Paso 1.** Prompt maestro escrito, **read-only, keyless, cero escritura en cadena**,
jamás lanzado. No hay informe en ningún sitio del disco. Cumple entera la doctrina de hoy
porque no firma nada, y el 30B local puede hacer buena parte.
*Por qué hoy sí:* es la única tarea del archivo que avanza la tesis NEAR sin tocar una
clave. **La mejor relación valor/riesgo que he encontrado.**

### 2.2 · Lo que murió por falta de modelo

**El lazo de comprensión de tres ramas.** El documento fundacional de Aurelius lo reduce a
**una sola rama** y dice por qué: el clasificador era un 1.5B en CPU y confundía omisión
con ruptura. Hoy hay un 30B con salida estructurada verificada.
*Falta:* el set de ejemplos etiquetados a mano que el propio documento exige. Nada más.

**La Capa Babel.** Traducir un payload canónico a seis idiomas de máquina. Se diseñó sobre
una NPU de 6 TOPS que nunca dio para transformaciones fiables. Hoy: la mitad ni necesita
LLM —son plantillas deterministas— y la otra mitad la hace el 30B.

**La Necrópolis Vectorial.** Consultar las ideas ya enterradas *antes* de gastar cómputo en
evaluar una nueva. Bloqueada en mayo porque no había modelo de embeddings. Hoy la-fragua
corre embeddings + Qdrant. **Y el corpus de siembra es este mismo archivo**, con sus ~40
veredictos motivados.

**El fingerprint de identidad, 12 pruebas.** Suite de regresión de identidad evaluada por
embeddings contra un baseline, con escalera de severidad. En mayo no había hardware.
*Falta:* el baseline T0 y ~100 líneas de coseno.

**NEAR light client propio.** El único de nueve nodos calificado «on-core», aparcado por
«4-8 GB RAM + 150-300 GB, demasiado pesado». El Beelink tiene 64 GB y 1 TB.
*La razón del aplazamiento ya no existe.*

### 2.3 · Lo que nunca necesitó hardware

**El Escudo RF.** Un campo firmado que distingue «compré AIS y lo firmé» de «mi antena lo
oyó y la física cuadra». La lógica estaba escrita; nunca se incrustó en el payload. Es la
capa de confianza que el propio pitch dice que es el foso.

**El Agente de Atestación de Uptime.** El Faro con otro sensor. Reutiliza todo, no
necesita hardware nuevo, y su comprador es cripto-nativo y no hiperlocal.

**El Puente B2B.** Cinco a diez conversaciones con consignatarios y abogados marítimos de
Lisboa. Cuesta unas horas. Todos los documentos posteriores repiten que el cuello de
botella ya no es técnico sino de demanda; este es el único que dice qué hacer.

### 2.4 · Lo que tiene más ADN de Aurelius y nunca pasó del papel

**El Gólem y «CALIBRA TU RADIO».** Un mini-juego que entrenaba el clasificador de señal
**sin que el usuario supiera que estaba etiquetando**. Es la idea con más parentesco con
Aurelius de todo el archivo — misiones jugables que producen dato real — y no pasó del
documento.

---

## 3 · Doctrina en papel que nunca llegó al repo

Comprobado con `grep -ril` sobre todo `~/p0x/mente/`: cero coincidencias.

| Qué falta | Por qué duele hoy |
|---|---|
| **El audit operativo de sesiones**: *«`systemctl list-units` al cerrar cada sesión de Claude Code — un servicio fantasma con autoridad es la semilla del próximo IronClaw»* y *«no se crean servicios systemd sin aprobación explícita»* | Es una regla de higiene **para sesiones como esta**, y no está ni en `mente/` ni en `CLAUDE.md`. Con loops 24/7 en el horizonte, su ausencia pasa de incómoda a peligrosa |
| **Las Cinco Leyes**, la **function-call key acotada**, **«cero claves en la embajada»** | Es el razonamiento que hay **debajo** de «jamás firmas valor». Hoy la regla existe sin su porqué, y una regla sin porqué se negocia |
| **El gradiente de privilegio** (Zona Soberana / Zona de Aprovechamiento) | «Propose-only» sobrevive como regla suelta; el marco que la justifica y que clasifica cualquier herramienta nueva sin deliberar, no |
| **La membrana con su prueba falsable**: *«Si El Preceptor muere, HEXELION sigue atestando. Si HEXELION para, tu Códice sigue siendo tuyo y legible»* | Entonces los dos eran privados. **Hoy Aurelius es público**: una fuga por esa frontera ya no es higiene interna |
| **El flujo canónico de `hexelion.near`** (recibir → consolidar → Intent sin firmar → firma física) | NEAR sigue interesando. Es la pieza operativa que falta bajo CANON-C |
| **Los tres ejes del descarte** (velocidad / capital-custodia / scope off-thesis) y la **métrica anti-teología** | El vocabulario de veredictos vive; **el criterio con el que se emiten**, no |
| **La re-especificación de IronClaw**: lección arquitectónica ≠ lección operativa | El mejor razonamiento de seguridad del archivo, y desbloquea diseño en vez de solo prohibir |

---

## 4 · Planes a medio ejecutar que merecen cierre honesto

No «terminarlos»: **cerrarlos con una línea que diga qué pasó**, para que no vuelvan como
zombis.

- **El Ciclo Dorado** — la puerta de la que colgaba todo lo demás. Nunca ocurrió, luego
  nada de lo que dependía de él existe. Cerrar la puerta explícitamente.
- **Los dos drills** (Reencarnación y Resiliencia). El registro dice `[pendiente]`.
  **Que hoy hp-01 sea «no recuperable por vía remota» es exactamente el precio de ese
  hueco.** Merece un párrafo, no un borrado.
- **El Guardián / backups.** Marcado URGENTE el 29-mayo; el 30 la auditoría anotó *«cero
  backups… irónico para un nodo de certidumbre física»*. Comprobar si sigue siendo cierto
  antes de escribir nada.
- **Protocolo de Primera Luz.** Los €30 nunca entraron; la tabla de seguimiento está vacía.
- **El Ritual del Primer Día.** Copia mensual al USB, día 1 a las 09:00. Sin registro de
  ninguna copia.
- **Levantar el Silencio.** Ningún reporte de promoción. Visto desde hoy, **es la decisión
  correcta tomada por omisión** — y eso merece decirse, no callarse.
- **El Camino NEAR AI.** La zona evolutiva está vacía: no se midió ni el coste de una
  llamada. Es el documento más reciente del archivo y sigue vigente palabra por palabra.

### Y dos cosas que están rotas ahora mismo en el repo vivo

1. **Dos symlinks rotos versionados en git**, apuntando a `/mnt/nvme`, que no existe en
   este nodo: `mente/codice/CODICE_david.md` y `mente/tecnicas`. Verificado por mí.
2. **El Códice vivo miente sobre la máquina.** `~/p0x/codice/CODICE_david.md` línea 40
   declara «verificado 2026-06-27»: `la-fragua … qwen3:8b`, `la-torre … qwen3:4b`, `proxy
   LiteLLM enruta`, «El Oráculo para lo pesado». Sus cuatro capas están literalmente
   `(vacio)`. Es el «filtro de realidad» del sistema, y le diría al Soberano que no puede
   hacer lo que hoy hace todos los días.

---

## 5 · La arquitectura de loops, cruzada contra el archivo

El Soberano trajo una propuesta de loops anidados (DOS, agosto 2026) y preguntó si aporta
valor real. **Sí, y es buena.** Pero el cruce da el hallazgo que justifica todo este
trabajo de lectura: **su propio archivo ya contiene cuatro refinamientos que esa propuesta
no tiene**, y los aprendió pagando.

| Pieza de DOS | Antepasado en el archivo | Qué añade el antepasado |
|---|---|---|
| Clases LIGERO / MEDIO / PESADO | **El Score S0** (`CODICE_2026_14` §VI) | Un portero de 80 MB en CPU, <50 ms, con **umbrales ajustables sin tocar código** y **tres bandas** en vez de dos. La escalada por coste ya implementada |
| `load>2 → posponer` | **El Filtro de Eficiencia** (`DOCTRINA_SOL_SINCRONO`) | **Histéresis de 5 minutos contra el flapping.** La propuesta de DOS pospone y reintenta sin histéresis: con carga oscilando alrededor del umbral, un loop entra y sale sin hacer nada. Ya le pasó |
| Bandeja de firmas | **La Doctrina del Silencio** §II | No es solo «el carbono firma»: son **cinco criterios cuantitativos sostenidos 14 días MÁS voto explícito** — *«sin voto no se promueve, aunque los números cuadren»* — y un **circuit breaker de degradación inversa** |
| Heartbeats en `loops.db` | **El registro de drills append-only** | Las filas **nunca se editan**. Un latido que se sobrescribe pierde la historia del fallo, que es justo lo que quieres cuando algo lleva semanas muriendo |
| *(no está en DOS)* | **El monitor de fallo silencioso** del Score S0 | *«Si nada supera el filtro en 7 días, sospecha del filtro.»* Es el modo de fallo más traicionero de un sistema de loops: todo verde porque el detector está roto. **A la propuesta de DOS le falta entero** |
| *(no está en DOS)* | **El patrón `@sleeping`** | Cómo retirar un loop sin borrarlo: marcado dormido, con motivo y referencia al documento, detrás de **un solo flag**, con la doctrina reducida como fallback |
| Cola de ventanas | **`~/p0x/bin/p0x-enqueue`** | Ya existe. No hace falta inventar la cola |

**Mi lectura, en una frase:** la arquitectura de DOS es correcta y merece construirse, pero
construirla **sin** el monitor de fallo silencioso y **sin** la histéresis sería repetir dos
errores que este archivo ya documenta. Eso es exactamente el valor de haber leído antes de
construir, y es la razón por la que el Soberano puso el equipo de lectura en Prioridad 0.

**No he construido nada de esto.** El orden de la Palabra del Soberano es Prioridad 0
primero, y sigue abierta hasta que cierre la pasada local.

### 5.1 · Tres correcciones del Soberano, y una se confirma con ironía

El Soberano revisó la propuesta y devolvió tres correcciones técnicas. Las tres son
correctas; la primera la comprobé y es peor de lo que parecía.

**1 · El `grep` del Guardián está roto.** La propuesta usa `grep -r "^import\|^from" *.py`,
que en bash se expande **solo a la raíz**. Medido en `aurelius-mvp`: la raíz da 58 ficheros,
el recursivo da 60. Los dos que se escapan son `empaquetado/lanzador.py` y
`laminas/recortar.py` — **y `recortar.py` es el único fichero del árbol que importa PIL**,
es decir, la única dependencia fuera de la biblioteca estándar que existe en el proyecto.
Un Guardián con ese `grep` habría dado verde todos los días sin ver lo único que tenía que
ver. La forma correcta es la que él da:

```
find . -name "*.py" -not -path "./.*" -exec grep -H "^import\|^from" {} +
```

Y su segundo punto es igual de necesario: la lista blanca no puede ser solo stdlib. Este
árbol tiene **27 módulos propios** (`casa`, `textos`, `memory`, `guardrails`, `fusible`,
`narrador`…) que un filtro stdlib marcaría como intrusos cada noche hasta que alguien lo
apagara por ruido.

**2 · El Centinela necesita una línea base.** «Superficie nueva» no significa nada sin un
antes. Un `docs/seguridad/baseline_YYYY-MM-DD.json` generado la primera vez, y diffs
después.

**3 · El Médico no escala.** Clasificar semánticamente mil recuerdos con el 30B en un turno
es imposible — y coincide con lo medido hoy: el 30B tarda ~36 s por documento y **recarga
18,5 GB en cada invocación** porque en este nodo no hay `llama-server`, solo
`llama-completion`. Su solución es la correcta y además barata: duplicados por cadena
exacta en SQLite primero (instantáneo), y solo los candidatos supervivientes pasan al 30B,
por ventanas de ~100 recuerdos activos.

**Los dos auxiliares y el tercero opcional** quedan registrados: vigilancia técnica
semanal con veredicto `VIABLE / NO_DATA` y sin FOMO; verificación de backups que **abre el
backup y cuenta filas** en vez de mirar que el fichero exista —*«"one file you can carry"
incluye que el fichero funcione cuando lo necesites»*—; y la recolección de tendencias sin
juicio editorial, que cuesta `curl` y cero tokens.

---

## 5.2 · Encargo abierto: el Lore de Hexelion se rehace

Palabra del Soberano, 2026-08-23. El Lore actual describe un organismo, un protocolo de
cinco tiers y una red de nodos. Hexelion es ahora **un mueble en el jardín controlado desde
el rack**. El archivo ya contiene el patrón para hacerlo sin perder nada: `@sleeping` —la
capacidad no se borra, se marca dormida con motivo y referencia, detrás de un solo flag, con
la doctrina reducida como fallback— y la tabla de deprecaciones del Canon del Lore, que es
el mecanismo, no el contenido.

Preparo el esqueleto como propuesta; **el Lore lo firma el carbono**, no lo escribe una
sesión por iniciativa propia.

---

## 6 · Lo que falta para cerrar la Revisión

- La destilación de los **231 documentos** de la pasada local (11/231 al escribir esto).
- La cronología real, reconstruida desde nombres y contenido: **las fechas del sistema de
  ficheros son falsas**.
- El cuarto agente del equipo: la **Propuesta de Conserjería** — dónde va cada documento
  vigente. Nada se moverá sin firma.
