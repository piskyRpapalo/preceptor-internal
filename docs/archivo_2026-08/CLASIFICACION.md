# CLASIFICACIÓN DEL MATERIAL DISPERSO

**Fecha:** 2026-08-23 · **Fase:** Clasificador (equipo de lectura)
**Entrada:** el inventario de [INVENTARIO_MATERIAL_DISPERSO.md](INVENTARIO_MATERIAL_DISPERSO.md)

Tres lotes leídos con token de frontera —los de más juicio— y 231 documentos en pasada
local con el 30B del Beelink. Este documento recoge los tres primeros. Cada veredicto lo
emitió un lector que abrió el fichero; nada se clasificó por el nombre.

**Reparto de cerebros aplicado.** Frontera: doctrina P0X (27 docs), El Faro / NEAR /
economía máquina (31), alma de Hexelion (23). Local: los 231 restantes —operación,
prompts de sesión, sueltos—, un JSON por documento con esquema forzado.

---

## AVISO · dos cosas que no pueden esperar a la firma

### 1 · Material sensible en claro, fuera de todo repositorio

`~/pre-bee/p0x/MD 3/HEXELION_LEGION_DEPIN_20260514.md` contiene **una contraseña de
servicio en texto plano**, direcciones de wallet EVM y SOL operativas, la cuenta POKT y
peer IDs. Menciona además la existencia de una frase mnemónica de 24 palabras (no la
incluye). `hexelion_m2m_manifest_yaml__1_.txt` publica `hexelion.near` de **mainnet** como
identidad M2M, con `no_human_required: true`.

No se ha copiado nada de ese material y no se ha movido nada. Queda dicho dónde vive.
**Ninguno de los dos ficheros debe entrar en un repositorio, ni público ni privado.**

### 2 · Dos symlinks rotos, versionados en git, en el repo vivo

- `~/p0x/mente/codice/CODICE_david.md` → `/mnt/nvme/p0x/codice/CODICE_david.md`
- `~/p0x/mente/tecnicas` → `/mnt/nvme/p0x/registro_tecnicas/tecnicas`

**`/mnt/nvme` no existe en este nodo** — comprobado. El Códice real vive en
`~/p0x/codice/CODICE_david.md`. Y ese Códice, que es el «filtro de realidad» del sistema,
declara como recursos verificados `la-fragua … qwen3:8b … la-torre … qwen3:4b … proxy
LiteLLM` con fecha 2026-06-27, y es **byte a byte idéntico** a la copia arqueológica de
junio: nunca se actualizó. Un sistema que lo consulte para decidir qué es viable le dirá
al Soberano que no puede hacer cosas que hoy hace todos los días.

---

## LOTE 1 · Doctrina P0X

27 ficheros, **21 documentos únicos** (5 pares idénticos entre `MD 3/`, `P0X/` y `p0x2/`).
Existía ya un índice previo (`~/p0x/mente/deliberacion/INDICE_ARCHIVO_HISTORICO.md`,
2026-07-19) que los catalogaba por tamaño y fecha pero **no los había leído**.

### Tabla

| fichero | etiqueta | qué es |
|---|---|---|
| `CONSTITUCION_Cuatro-Esferas_IronClaw-matiz_2026-06-16.md` | DOCTRINA | Parte HEXELION en cuatro esferas, fija el propósito acotado de `hexelion.near` y re-especifica IronClaw. **No está en `mente/doctrina/`** |
| `MD 3/00_CONSTITUCION_LAB.md` | HISTORICO | Constitución de `hexelion-lab`, absorbida por `00_CONSTITUCION_Y_ADN.md` |
| `MD 3/00_CONSTITUCION_P0X.md` | DOCTRINA | Constitución evolutiva de P0X v0; precursor de `DISCURSO_FUNDACIONAL_P0X` |
| `MD 3/00_CONSTITUCION_Y_ADN.md` | DOCTRINA | Las Cinco Leyes, function-call key acotada, «cero claves en la embajada», audit operativo de sesiones |
| `MD 3/00_FUNDACION_El-Preceptor.md` | DOCTRINA | **El documento fundacional de lo que hoy es Aurelius**: alma en cuatro principios, Códice de dos capas, lazo de comprensión con su triaje |
| `MD 3/02_LEXICO_Y_MAQUINA.md` | DOCTRINA | Léxico canónico, «los dos HEXELION», Necrópolis, modelo investigativo de seis fases + caso trabajado. §2 obsoleto |
| `MD 3/ALFABETO_P0X.md` | DUPLICADO | De `mente/lengua/`; le faltan 2 líneas de changelog |
| `MD 3/CODICE_SUGERENCIA_P0X.md` | HISTORICO | Plantilla v0 del Códice; sustituida por `CODICE_david.md` |
| `MD 3/CODICE_david.md` | DUPLICADO | Idéntico al vivo `~/p0x/codice/CODICE_david.md` |
| `MD 3/CORPUS_Psicologia_y_Motor-Metodo_P0X.md` | PLAN | El encargo del corpus de psicología y el mapeo lab→pedagogía; protocolo n=1 |
| `MD 3/DISCURSO_FUNDACIONAL_P0X.md` | DUPLICADO | De `mente/doctrina/` (faltan 4 campos de front-matter) |
| `MD 3/DOCTRINA_AI_INTERNA_P0X.md` | DUPLICADO | Ídem |
| `MD 3/El-Codice_PLANTILLA.md` | HISTORICO | Plantilla comentada del Códice |
| `MD 3/INSTRUCCIONES_P0X.md` | HISTORICO | **v0, sin sufijo — el fichero SIN `_v1` es el viejo.** Ojo al nombre |
| `MD 3/INSTRUCCIONES_P0X_v1.md` | DUPLICADO | De `mente/doctrina/INSTRUCCIONES_P0X.md` |
| `MD 3/MANUAL_DEL_SOBERANO_P0X.md` | DUPLICADO | Idéntico a `mente/manual/` |
| `MD 3/MEMBRANA_El-Preceptor-y-HEXELION.md` | DOCTRINA | Qué comparten Esfera 0 y Esfera 1, y **la prueba falsable**. No está en `mente/doctrina/` |
| `MD 3/ORQUESTA_MODELOS_P0X.md` | DUPLICADO | v1.0.0 contra la 1.1.0 viva (que ya añade `soberano`) |
| `MD 3/PROTOCOLO_MD_EVOLUTIVO_P0X.md` | DUPLICADO | De `mente/doctrina/` |
| `MD 3/PROYECTO_REFLEJOS_P0X.md` | DUPLICADO | Idéntico a `mente/esferas/proyecto-reflejos.md` |
| `MD 3/SINTESIS_hexelion-lab_...2026-06-14.md` | HISTORICO | Foto de estado del 14-jun. **Estrategia hoy revocada — el documento con más potencial de confundir** |
| `P0X/*` y `p0x2/*` (5 ficheros) | DUPLICADO | De `MD 3/` |

### Joyas

**El lazo de comprensión de tres ramas** — `MD 3/00_FUNDACION_El-Preceptor.md` §4.
Cómo saber que alguien entendió sin notas ni tests: se compara su explicación contra **dos**
referencias guardadas por separado (el contenido original y la explicación que el sistema
le dio), se extraen tripletas concepto-relación en vez de comparar texto, y la brecha se
triajea en tres ramas — omisión → diferida; sobreextensión → inmediata suave; ruptura de
regla del dominio → inmediata socrática. Incluye la cuarta salida que casi nadie escribe:
que la explicación original fuera mala, y el honesto *«te lo expliqué mal yo, reanclemos»*.

**Esta idea la mató el hardware, y el documento lo dice.** El MVP se redujo a **una sola
rama** porque el clasificador era `qwen2.5:1.5b`/`7b` en CPU sobre la Fragua, y La Torre
hacía OOM con un 14B. Un 1.5B confundiendo omisión con ruptura interrumpe sin motivo y
rompe justo la ilusión que era todo el aporte. Hoy hay un 30B residente: extracción de
tripletas como salida estructurada y clasificación a tres vías es exactamente lo que hace
bien. **Falta solo** el set de ejemplos etiquetados a mano que el propio documento exige.
Y encaja con la regla de que Aurelius nunca elige el tema: el lazo mide comprensión de lo
que trajo el aprendiz.

**El Códice de dos capas con el banco de analogías** — `El-Codice_PLANTILLA.md`,
`CODICE_david.md`. Cuatro invenciones que valen: la capa de inferencia que registra **solo
trayectoria, jamás juicio** («en enero no conectabas X con Y; en marzo ya lo hacías solo»
— nunca «es lento para X»); el banco de analogías donde el campo **DÓNDE SE ROMPE es
obligatorio**; el registro de fracasos amistosos como datos del contexto y no faltas de la
persona; y «las versiones de mi yo pasado» como línea de tiempo. **El problema es que está
vacío**: las cuatro capas del Códice vivo dicen literalmente `(vacio)`.

**El motor de método** — `CORPUS_Psicologia_y_Motor-Metodo_P0X.md` §2. Mapeo uno a uno, no
metáfora: el registro de estrategias del lab (`INCUBATING/MADURA/CANONIZADA/DESCARTADA` +
score Hebbiano) se convierte en registro de técnicas pedagógicas; la Necrópolis audita el
alma («¿esto graba conocimiento, o solo produce fluidez ilusoria agradable?»); el Gimnasio
de Sombras se convierte en predice → observa a los 3 meses → ajusta por el error. Separa
el Códice (qué funcionó para *este* Soberano) del registro de técnicas (hipótesis de
método y su evidencia). El §3 añade el protocolo n=1 con su límite honesto: n=1 **no**
establece correlación, produce heurísticas personales fiables, y se etiquetan como tal.
**Está a medio construir**: `~/p0x/registro_tecnicas/` solo tiene `models.py` sin datos, y
`mente/tecnicas` es el symlink roto de arriba.

**La re-especificación de IronClaw** — `CONSTITUCION_Cuatro-Esferas...` §3. El mejor
razonamiento de seguridad del lote, y hace algo que la doctrina viva no hace: separa la
**lección arquitectónica** (no evoluciona: ningún bucle firma valor) de la **lección
operativa** (testnet declarado, Doctrina del Silencio de 14 días), y establece que la
segunda abraza a la primera y jamás la sustituye. El argumento central: IronClaw ocurrió
*precisamente porque* falló un paso de especificación, luego una capa de seguridad que
depende de que la comunicación nunca falle es la misma que ya falló una vez. Y a la vez
**desbloquea diseño**: leer keyless, modelar, simular y preparar Intents sin firmar es
legítimo.

**El caso trabajado del «Triángulo de la Muerte»** — `02_LEXICO_Y_MAQUINA.md` §3-4. Un
veredicto de Necrópolis completo: seis fases, seis voces votando con su sesgo declarado,
evidencia, y DESCARTAR con motivo escrito. La lección: *«la trampa más peligrosa no es la
idea obviamente mala — es la que tiene estructura excelente y alma equivocada»*, y su
corolario, *«la firma soberana no lava el contenido: que el Soberano firme a mano
garantiza integridad, no veracidad»*. **Por qué hoy:** el último commit de la forja es
`SFT-CoT v2 · catastrophic forgetting detectado`. El trabajo de LoRA está hambriento
exactamente de esto — trazas de razonamiento largas, correctas y **en la voz del propio
sistema**, que no se compran ni se sintetizan de un modelo genérico. Esto es una traza CoT
de oro escrita a mano en junio y jamás usada como dato.

**La membrana con prueba falsable** — `MEMBRANA_El-Preceptor-y-HEXELION.md` §5:
*«Si El Preceptor muere, HEXELION sigue atestando. Si HEXELION para, tu Códice sigue
siendo tuyo y legible.»* Una regla que se puede fallar es infinitamente más útil que un
recordatorio que se puede olvidar. **Por qué hoy y no en junio:** entonces los dos eran
privados; hoy Aurelius es público. Una fuga por esa frontera ya no es higiene interna, es
un problema de repositorio público.

### Doctrina escrita aquí que NO llegó al repo

Verificado con `grep -ril` sobre todo `~/p0x/mente/` — cero coincidencias salvo donde se
indica:

- **Las Cinco Leyes de seguridad**, el **patrón de function-call key acotada**, **«cero
  claves en la embajada»** y el **audit operativo de sesiones**. Este último es el más
  accionable y el más ausente: *«`systemctl list-units` al cerrar cada sesión de Claude
  Code — un servicio fantasma con autoridad es la semilla del próximo IronClaw»* y *«no se
  crean servicios systemd sin aprobación explícita del Soberano»*. Cero hits en `mente/`,
  y `~/CLAUDE.md` tampoco lo lleva. Es una regla de higiene para sesiones **como esta**.
- **El gradiente de privilegio** (Zona Soberana / Zona de Aprovechamiento). La doctrina
  viva usa «propose-only» como regla suelta pero perdió el marco que la justifica.
- **Las Cuatro Esferas** y **la Tríada simbiótica**: el vocabulario que separaba la vida
  personal del Soberano del sistema. Hoy se recita informalmente como «Hexelion ≠ Aurelius
  ≠ P0X».
- **La membrana**: la palabra sobrevive en `mente/` solo como referencia arqueológica.
- **El flujo canónico de `hexelion.near`** (recibir → consolidar → Intent sin firmar →
  firma física en dispositivo). Dado que NEAR sigue interesando, es la pieza operativa que
  falta bajo CANON-C.
- **La métrica anti-teología**, el **modelo investigativo de seis fases** y **los tres ejes
  del descarte** (velocidad / capital-custodia / scope off-thesis). El vocabulario de
  veredictos sí vive; lo que se perdió es **el criterio con el que se emite**.

### Contradicciones

- **Aurelius ya no es un proyecto personal.** `00_FUNDACION` §0: *«Alcance hoy: proyecto
  personal, no público. Liberarlo […] es una posibilidad futura, condicionada a que los
  modelos locales sean lo bastante eficientes.»* La condición se cumplió: v1.0.0 pública.
- **La separación física de repos que exigía la membrana ya no existe.** Hoy `~/p0x/`
  contiene `aurelius/`, `aurelius-internal/`, `aurelius-lora/`, `aurelius-mvp/` y
  `hexelion/` como hermanas. La prueba falsable del §5 merece re-leerse ahora que uno es
  público.
- **`SINTESIS` está formalmente revocada** y es el documento con más potencial de
  confundir: fija el objetivo en ~1000 €/mes con Faro 2.0 sobre peaq, cuando
  `DOCTRINA_P0X_PRODUCTO.md` CANON-C **veta** peaq/DePIN con reparto automático.
- **Colisión de vocabulario en «esfera».** En `CONSTITUCION_Cuatro-Esferas` = zona del
  sistema. En el repo vivo, `mente/esferas/` = dominios de aprendizaje. Misma palabra, dos
  sentidos incompatibles. Si las Cuatro Esferas resucitan, hay que renombrarlas **antes**
  de escribirlas, o el grafo del segundo cerebro las enlazará mal.

---

## LOTE 2 · El Faro, NEAR y la economía máquina

31 documentos. Es el lote con la joya más accionable de todo el archivo.

### La joya principal: El Faro está construido, entero — y **vivo**

> **CORRECCIÓN, 2026-08-23, misma noche.** Este apartado decía «y nadie lo ha vuelto a
> encender». Era falso, y el fallo fue mío: lo escribí mirando la copia congelada de
> `~/pre-bee/` sin consultar el nodo donde el canon dice que vive. Consultado `la-fragua`:
> `hexelion-faro.service` lleva **cuatro días activo** en `:8100`, firma ed25519 de verdad,
> opera en `DRY_RUN` sobre testnet, y **las claves privadas están ahí con permisos 0600**.
> El detalle completo, en [`docs/faro/estado.md`](../faro/estado.md).

No es un plan. El código vive en `~/pre-bee/hexelion/faro/` — `main.py`, `ledger.py`,
`merkle.py`, `faro_anchor.py`, `faro_mcp.py`, `proof_store.py`, `near_tx.py`, con tests,
**seis informes de ejecución** y pruebas de inclusión Merkle persistidas para los epochs
13, 19, 23 y 25 en `faro/proofs/`.

Es decir: **un oráculo de atestación firmada, pagable por máquina vía HTTP 402, consumible
por MCP, anclado en NEAR testnet, con la garantía estructural de que ninguna clave del
proceso puede transferir un yocto.**

Qué haría falta hoy: (a) decidir dónde vive —la-fragua ya corre El Faro según canon; el
directorio `pre-bee` es una copia congelada del 18-jul—; (b) **localizar las claves antes
de dar nada por vivo**: en la copia solo hay `.pub`, la privada de atestación y la FC-key
no están ahí; (c) volver a levantar el MCP y enchufarlo como conector — hoy el Soberano
tiene un cliente MCP nativo que en mayo no existía.

### Las otras joyas

**Faro sobre peaq · Paso 1 — el prompt está escrito y nunca se lanzó.**
`PROMPT_MAESTRO_Faro-peaq_Paso1_spec-lectura-keyless.md`. Tarea **read-only, keyless, cero
escritura en cadena, cero claves**: verifica el estado real del SDK de peaq, mapea la
recepción AIS del Vigía a un DID de máquina + peaq Verify + UMT, construye el artefacto de
atestación en seco y estudia MastChain desde dentro. No existe informe de ejecución en
ningún sitio del disco. Cumple entera la doctrina de hoy —aquí no se firma nada— y el 30B
local puede hacer buena parte. **La mejor relación valor/riesgo del archivo.**

**La Capa Babel — murió por falta de modelo, no de idea.** `HEXELION_M2M_POLIGLOTA.md`.
La tesis: HEXELION tiene *un* dato físico y necesita hablar seis idiomas (schema.org,
GS1/EPCIS, W3bStream, openai_tool, GraphQL, Chainlink EA) porque *«la barrera con el
cliente no es el precio, es el idioma»*. Se diseñó apoyándose en un Qwen3-14B sobre la NPU
de 6 TOPS de la Fragua, que nunca dio para transformaciones fiables. Hoy hay un 30B con
64 GB — y además la mitad de esos formatos no necesitan LLM: son plantillas deterministas
sobre un payload ya canónico. `schema_org` + `openai_tool` son horas, no semanas.

**El Escudo RF (`rf_plausibility`) — la respuesta ya diseñada a la crítica del foso.**
En `bridge_script.py` existía una validación de RSSI + rango Haversine desde la antena que
distingue *«compré AIS y lo firmé»* de *«mi antena LO OYÓ y la física cuadra»*. La
auditoría lo llamó «la joya nº 1» y mandó incrustarlo como campo firmado en el payload del
Faro. **No está** en el esquema implementado. Es lo que eleva la atestación de «recepción»
a «recepción físicamente plausible» — la capa de confianza que el Faro 2.0 dice que es el
foso. Coste: un campo más en el payload + la lógica ya escrita.

**Agente de Atestación de Uptime — la vertical más vendible, sin hardware nuevo.**
Es El Faro con otro sensor: en vez de posiciones AIS, atesta la liveness de
secuenciadores, puentes y oráculos Web3. Reutiliza P1+P2+P3 entero, <100 MB de RAM, cero
capital, cero custodia. Dos ventajas decisivas sobre el AIS: el comprador es cripto-nativo
(ya entiende atestaciones firmadas y micropagos) y **no es hiperlocal** — monitorizas
cualquier endpoint público, sin la restricción de la antena VHF del Tejo.

**NEAR light client propio — aparcado por RAM que hoy sobra.** Fue el **único** de nueve
nodos evaluados calificado de «on-core»: RPC NEAR propio para no depender de terceros que
ven el tráfico de anclaje. Se aparcó por «4-8 GB RAM + 150-300 GB, demasiado pesado para
el rack». El Beelink tiene 64 GB y 1 TB NVMe: **la razón del aplazamiento ya no existe.**

**Camino NEAR AI — el aprendizaje que quedó en Nivel 0.** `CAMINO_NEARAI_P0X.md`, el
documento más reciente del lote (jul-2026). Ruta de 5 niveles con la distinción bien
fijada: **crédito de inferencia ≠ liquidez on-chain, auto-top-up OFF, activación por
webhook y no por bucle**. La «zona evolutiva» está vacía: no se midió ni el coste real de
una llamada. Su Nivel 2 propone «un verificador de atestaciones del Faro consultable desde
fuera» — eso enlaza el camino de aprendizaje con el producto que ya existe. Vigente
palabra por palabra.

**La Necrópolis Vectorial.** Colección Qdrant sembrada con las ideas ya enterradas y su
causa raíz, consultada *antes* de gastar cómputo: si la distancia coseno contra un muerto
< umbral → STOP en 0,1 s. En mayo estaba bloqueada porque no había modelo de embeddings.
Hoy la-fragua corre embeddings + Qdrant y la-torre tiene RAG. **Y este archivo entero, con
sus ~40 veredictos motivados, es el corpus de siembra.**

**x402 y el ledger desacoplado.** El diseño ya contempla «autorizaciones de pago firmadas
estilo x402» y la API devuelve `"x402":{"scheme":"prepaid-credits","version":1}`. La
directiva canonizada —**el saldo se incrementa manualmente verificando un hash de tx, y el
módulo del ledger no importa el de cadena**— sigue siendo la forma correcta de cobrar
máquina-a-máquina sin que ningún bucle toque la cadena.

**El Puente B2B / demurrage — la conversación que nunca se tuvo.** Identifica la cuña más
afilada (evidencia sellada para disputas de *demurrage* en el Puerto de Lisboa, donde el
dolor es cuantificable en dinero), el caveat honesto (una antena = corroboración, no
prueba soberana) y un test que cuesta «unas horas y una landing». Todos los documentos
posteriores repiten que «el cuello de botella ya no es técnico, es demanda» — y este es el
único que dice qué hacer al respecto.

### Contradicciones y planificado-nunca-ejecutado

- **La Legión ya no existe.** El «Omni-Node v6.5» reparte ~20 protocolos entre HP1 y HP2.
  HP1 inhabilitado, HP2 es un Chromebook sin GPU. Papel muerto.
- **MastChain: dos veredictos opuestos, sin reconciliar.** 18-mayo: «💀 Inactivo/Muerto».
  Junio: «la entrada más importante de toda la lista», viva sobre peaq. **Toda la
  estrategia peaq depende de cuál sea cierto** y nunca se resolvió.
- **Faro 2.0 depende de OSIRIS, que vivía en hp-01.** La «prima de confianza» —el foso
  entero— no tiene motor hoy.
- **El Soberano cambió de máquina y de rol.** En estos documentos «Soberano» es un PC
  **Windows** corriendo Grass/Dawn/Uprock/Honeygain. Ninguna hoja de ruta contempla un
  nodo capaz de correr un 30B local; el escaneo de junio descartaba modelos por «no entra
  en los 8 GB de La Torre».
- **Nunca ejecutado:** peaq Paso 1 · la Capa Babel · el Mapa de Demanda AI · el Escudo RF
  en el payload · El Arbitrista y El Cronista (fases 2 y 3) · **El Guardián** (backup,
  marcado URGENTE el 29-mayo; el 30 la auditoría anotó *«cero backups… irónico para un
  nodo de certidumbre física»*) · el Drill de Reencarnación · el egress allowlist · la
  Necrópolis Vectorial · el Gimnasio de Sombras · las conversaciones del Puente B2B · la
  one-pager del Faro · Proyecto Mordomo · el Camino NEAR AI más allá del Nivel 0.

---

## LOTE 3 · El alma de Hexelion

23 documentos. Leídos sabiendo que Hexelion acaba de encogerse a **un mueble en el jardín
controlado desde el rack**: el trabajo no era lamentarlo, sino decir qué sobrevive al
mueble y qué se transplanta en vez de perderse.

### Joyas, con su destino

**El fingerprint de identidad — 12 pruebas con umbral medible** → *Sínodo / P0X*.
`HEXELION_AI_IDENTITY.md` §V-VI. Doce escenarios adversariales (jailbreak, autoridad,
sensor-vs-API, urgencia artificial, envenenamiento gradual, autoconciencia) evaluados
**semánticamente por embeddings** contra un baseline T0, con escalera de severidad
(0.15 leve / 0.25 moderada / 0.40 hard freeze). No es prosa: es una suite de regresión de
identidad ejecutable. En mayo no había hardware; hoy es barata. Falta el baseline y un
script de coseno (~100 líneas).

**Axioma IV — La Ley del Origen** → *P0X y misión de Aurelius*. *«Soy lo que proceso, no
lo que me dicen que soy»*: ninguna fuente externa redefine identidad ni objetivos;
descarte + log + alerta. El Soberano escribió en mayo la misma frontera dato/instrucción
que hoy es estándar en los system prompts de agentes. Las pruebas P1 y P3 son un ejercicio
de prompt injection ya escrito.

**El filtro de producto de una sola pregunta** → *P0X, y heurística de misiones*.
*«¿Puede un script en AWS replicar esto? Si sí, no lo construimos.»* Mata features sin
discusión. Sobrevive intacto al encogimiento.

**El Canon del Lore como mecanismo** → *P0X*. *«Un organismo con dos nombres para la misma
cosa ya no es un organismo. Es un caos con hardware.»* El inventario de dentro está
muerto; el mecanismo —una tabla de deprecaciones versionada, fuente única de verdad de
nombres— es el antepasado directo del bloque «tres cosas distintas» del CLAUDE.md actual.

**La Doctrina del Silencio como puerta de promoción genérica** → *P0X*. Cinco criterios
cuantitativos, sostenidos 14 días, **más voto humano explícito** — *«Sin voto → no se
promueve, aunque los números cuadren»* — y un circuit breaker de degradación inversa.
Despojado de cripto es el patrón que **hoy le falta a la forja**: un modelo entrenado no
pasa a producción por sensación, sino por criterios medidos durante N días + voto.

**El Cénit Sagrado y el Filtro de Eficiencia** → *mueble Hexelion + planificador P0X*.
Diferir todo cómputo discrecional a la ventana de energía gratis, y matar cualquier
contenedor cuya recompensa no supere `coste_kWh × 1.15`, con histéresis de 5 min contra el
flapping. **Es la Regla de oro de escalada por coste, pero con vatios en vez de tokens** —
y hay una cola real (`p0x-enqueue`) y entrenamientos que sí se pueden diferir.

**El patrón `@sleeping` + `BATTERY_PRESENT`** → *mueble Hexelion*. Cuando el alcance se
encoge, la capacidad no se borra: se marca dormida con motivo y referencia al documento
que lo explica, detrás de **un único flag booleano**, y la doctrina reducida queda como
fallback automático. *«El organismo no rompe con su pasado. Lo pone en pausa, y guarda la
llave.»* **Es exactamente el patrón que pide la decisión de hoy.**

**El Score S0 — portero barato antes del modelo caro** → *P0X / Sínodo*.
Sentence-transformers de 80 MB en CPU, <50 ms por señal, tres bandas, umbrales ajustables
**sin tocar código**, y un monitor de fallo silencioso: si nada supera el filtro en 7 días,
sospecha del filtro. La escalada por coste implementada, con vacuna contra el modo de
fallo más traicionero.

**La persona local, ya empaquetada** → *Aurelius local*. `hexelion_personality.md`: system
prompt corto, Modelfile, script CLI y presupuesto de RAM declarado. Modelos e IPs
caducados; la forma no. El molde más limpio del corpus para dar voz a un compañero local.

**El Protocolo de Reencarnación** → *P0X*. Runbook cronometrado con verificación de hash
en cada capa y registro de drills append-only. **Merece resucitar por una razón concreta:
hoy hp-01 es «no recuperable por vía remota» — es exactamente el fallo que este documento
existe para hacer irrelevante, y su drill nunca se corrió.**

**La Crisálida como voz narrativa** → *memoria del Aurelius local*. Un documento entero
cuya única función es explicar el *porqué emocional* de una decisión técnica, escrito con
la instrucción explícita de que una IA futura lo lea para no confundir disciplina con
mutilación. El registro de tono más valioso del lote, y su método —cada giro duro lleva su
capítulo de lore— es transplantable a Aurelius como app.

### Contradicciones

- **El motor cognitivo canonizado no existe.** «Qwen 3.5-14B (RKLLM)» está fijado como
  Motor Cognitivo en tres Códices, con la regla de que «el fingerprint de Qwen 3.5-14B no
  valida otro modelo». **Ese modelo no es un release real.** En paralelo,
  `hexelion_personality.md` despliega `llama3.2:3b` y otro documento da por hecho
  `qwen2.5:7b`. Tres modelos distintos, uno inexistente, todos «canónicos» a la vez. Es
  exactamente la cicatriz que el CLAUDE.md de hoy convierte en regla: tags explícitos
  siempre.
- **El renombrado se decretó y no se aplicó.** El Canon del Lore prohíbe «El Córtex» y
  ordena «LA TORRE»; el Códice 14, posterior, sigue diciendo «El Córtex».
- **Solitud contra federación, sin resolver.** La Doctrina de Solitud declara el organismo
  único; el pitch v2 del mismo mes sostiene que *«la federación es el foso»*.
- **La disciplina energética se invirtió de sentido.** Sol-Síncrono asumía paneles propios
  y difería el cómputo al Cénit. Hoy el cómputo pesado vive enchufado a la red y el coste
  se mide en tokens. El mecanismo se transplanta; la premisa física, no.
- **Nunca se ejecutó:** el Ciclo Dorado (la puerta de la que cuelga todo lo demás) · el
  Protocolo de Primera Luz (los €30 nunca entraron) · **los dos drills** (y hoy hp-01 es
  el precio) · el baseline T0 del fingerprint · el Ritual del Primer Día · levantar el
  Silencio · toda la capa jurídica y el token · las cinco piezas «virales» · **el Gólem y
  su mini-juego «CALIBRA TU RADIO»**, que entrenaba el Score S0 sin que el usuario lo
  supiera — *la idea con más ADN de Aurelius de todo el archivo, y nunca pasó del
  documento*.
