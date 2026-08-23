---
id: grounding-v15
titulo: Verificación de grounding del borrador Blueprint v1.5
tipo: operativo
clase: operativo
version: 1.0.0
dominio: canon-blueprint
estado: PROPUESTA
actualizado: 2026-08-11
---

# GROUNDING · BLUEPRINT v1.5
### Cada afirmación del borrador, con su fuente en disco o su `NO_DATA`. Sin excepción.

**Cláusula que rige** — D9: *"toda afirmación de v1.5 sobre software, rutas o versiones cita fuente (ruta+hash o D-id); sin fuente = NO_DATA."*

**Convención de hash:** `sha256`, prefijo de 16 caracteres. Comando reproducible: `sha256sum <ruta>`. Raíz de todas las rutas relativas: `/home/pisky/p0x/`.

**Fecha de medición:** 2026-08-11 (entorno). El reloj del sandbox devuelve `2026-08-10`; discrepancia no resuelta, declarada también en R00 §6.

---

## §0 · CRÍTICO ANTES DE LEER EL RESTO

### §0.1 · `HASHES_R00.txt` no cubre lo que dice cubrir

`Cuarentena/salida/HASHES_R00.txt` · `ae9d7ab0400276d3` · 64 líneas.

El fichero se generó **sin entrecomillar los nombres con espacios**. Consecuencia medida: el segundo campo de 9 líneas está truncado en el primer espacio, y esas 9 entradas **no son resolubles a un fichero**.

| Medición | Cifra | Comando |
|---|---|---|
| Líneas | 64 | `wc -l < salida/HASHES_R00.txt` |
| Nombres únicos en campo 2 | 62 | `awk '{print $2}' … \| sort -u \| wc -l` |
| Ficheros hoy en primer nivel | 63 | `ls -p \| grep -v / \| wc -l` |
| Entradas truncadas / inservibles | 9 | `comm -23` entre HASHES y disco |
| Ficheros con hash verificable | **54 de 63** | 63 − 9 |

Nombres truncados (aparecen así en el artefacto): `ANEXO_DE_CASOS_COMPLEJOS`, `Architectural`, `De` (×2, colisionan), `Del`, `Hoja` (×2, colisionan), `Plan`, `p0x-repositorios-tecnicas-qwen-v2`.

Ficheros reales sin hash utilizable, por tanto: los 6 informes externos con espacios en el nombre, el PDF de CineK, `ANEXO_DE_CASOS_COMPLEJOS V4.txt` y `p0x-repositorios-tecnicas-qwen-v2 (1).txt`.

**Consecuencia doctrinal:** ninguna afirmación de v1.5 puede apoyarse en el hash de esos 9 ficheros. Se citan por ruta y tamaño, marcados `HASH_NO_DATA`. La línea base anti-deriva de R00 es **parcial**, y quien firme debe saberlo. Esta sugerencia salió de R00; salió mal ejecutada; se corrige antes de usarse como autoridad.

### §0.2 · Verificación de integridad contra la línea base parcial

De los 54 ficheros con hash verificable, **uno** ha cambiado desde R00:

`Cuarentena/03_ESTADO_FIRMADO.md` — hash R00 ≠ hash hoy (`3159e5237398a9f7`, 6803 B).
**Causa identificada y legítima:** incorporación de D9 y D10 (líneas 91–101). No es deriva; es firma. Se declara para que la discrepancia no se lea como corrupción.

Los 53 restantes: sin cambio. Comando: bucle `sha256sum` por entrada contra la línea base.

### §0.3 · El POST_VERIFICACION de R00 sigue declarándose sin firmar

`docs/post_verificacion/POST_VERIFICACION_R00_INVENTARIO.md` · `acf95f6f5bd47af6` · 17497 B.
Su línea 5 dice literalmente `Estado: PENDIENTE_DE_FIRMA`.

Sin embargo D9 y D10 (en `03_ESTADO_FIRMADO.md`) resuelven dos de sus hallazgos, y el documento fue movido de `Cuarentena/salida/` a `docs/post_verificacion/` — el paso 2 de `01_LEEME_PRIMERO.md §6`.

**Contradicción declarada.** Ante conflicto manda `03_ESTADO_FIRMADO.md`, y D9/D10 implican que R00 se leyó y se decidió sobre ella. Pero el campo `Estado` del propio entregable no se actualizó. Un documento archivado que se declara sin firmar es una trampa para el agente de la ronda siguiente. No lo corrijo: no es mi fichero y está fuera de mi zona de escritura.

### §0.4 · Existe una tercera copia del Blueprint, y está en la carpeta de doctrina

| Ruta | Versión declarada | Líneas | sha256 (16) |
|---|---|---|---|
| `BLUEPRINT_DISENO_SOBERANO.md` (raíz) | frontmatter `1.3.0`, título `v1.2`, enmienda v1.3 embebida | 266 | `cb767c464cc25631` |
| `mente/doctrina/BLUEPRINT_DISENO_SOBERANO.md` | frontmatter `1.2.0`, título `v1.2` | 271 | `43e73ae74fb28d63` |
| `Cuarentena/blueprint-de-diseno-soberano-v1.4.md` | `v1.4` | 331 | `9349c558829bd678` |

R00 detectó dos copias. Hay **tres**. La que vive en `mente/doctrina/` — el sitio donde la doctrina debería vivir — es la **más antigua** (1.2.0) y tiene **más líneas** que la de la raíz (271 vs 266), luego no es un subconjunto: divergen, no solo se suceden.

D9 declara canon la de la raíz (v1.3.0). La de `mente/doctrina/` no está contemplada por D9 y hoy es un canon fantasma. Se reporta; no se toca.

---

## §1 · IDENTIDAD Y DOCTRINA

| Afirmación de v1.5 | Fuente |
|---|---|
| El suelo operativo es `02_CANON_OPERATIVO.md` §0–§7 | `Cuarentena/02_CANON_OPERATIVO.md` · `1426f37ec8661398` · 7701 B · 117 L |
| Medallón = capas de dato; profundidad documental usa `basico\|medio\|experto` | ídem, §1 y §1.1 |
| El filtro de borde se llama **la Aduana**, no Aurelius | ídem, §2 |
| Taxonomía documental y acciones | ídem, §3 |
| Orden de trabajo innegociable (0→5) | ídem, §4 |
| Supuestos prohibidos | ídem, §5 |
| Higiene y secretos | ídem, §6 |
| Autoridad: silicio propone, carbono firma | `Cuarentena/04_CONTRATO_CLAUDE_CODE.md` · `2ac89e6d7078ca47` · 7039 B · 128 L · §1, §2 |
| Ritual de rondas y regla de procedencia | `Cuarentena/01_LEEME_PRIMERO.md` · `cb244b4f1f551bab` · 3976 B · 75 L · §3, §4 |
| Forma del entregable de ronda | `Cuarentena/05_PLANTILLA_POST_VERIFICACION.md` · `da0cf517a7370598` · 3342 B · 87 L |
| Canon **visual** vigente | `BLUEPRINT_DISENO_SOBERANO.md` · `cb767c464cc25631` · v1.3.0 · **D9** |

## §2 · ARQUITECTURA ACTUAL (medida hoy, no aspirada)

Recuento por directorio de primer nivel — `find <dir> -type f -not -path '*/node_modules/*' | wc -l`:

| Directorio | Ficheros | Lectura honesta |
|---|---|---|
| `mente/` | 104 | El volumen real del proyecto vive aquí. 18 subcarpetas |
| `deploy/` | 48 | Nodos: `fragua`, `soberano`, `vigia`, `torre`, `comun` |
| `skills/` | 8 | Una sola skill: `auditar-p0x` (6 scripts + SKILL.md + runner) |
| `corpus/` | 7 | Transcripciones y `meta.tsv` de 2 ingestas |
| `pipeline/` | 7 | `delta_engine.py`, `ingest_youtube.py`, `observar_*`, `bench_delta` |
| `bin/` | 4 | `cc-local`, `p0x-enqueue`, `p0x-instalar-ganchos`, `prune_backups.py` |
| `voz/` | 3 | `voz_server.py`, `gate0`, `gate0_sintesis.sh` |
| `preceptor/` | 2 | `frontera.py` (jaula wasmtime) |
| `bronze/` | **1** | `bronze/2026-08-10-prediccion-cinek.md` |
| `silver/` | **0** | vacío |
| `gold/` | **0** | vacío |
| `codice/`, `config/`, `monje/`, `propuestas/`, `proxy/`, `registro_tecnicas/`, `verde/` | 1 cada uno | — |
| `docs/` | 1 | solo el POST_VERIFICACION de R00 |

**Estado del Medallón:** existe como **tres carpetas**, no como arquitectura. Un único fichero en bronze, ninguno en silver ni gold. Regla de paso, esquemas y validación: `NO_DATA` (no hay artefacto que los implemente).
Fuente del contenido de bronze: `bronze/2026-08-10-prediccion-cinek.md`, primera línea `PREDICCION 2026-08-10 · Soberano`. Es una predicción firmada, no telemetría.

**La Aduana:** `find . -iname '*aduana*'` → **cero resultados**. Confirma `02 §2`: el componente no existe. `NO_DATA`.

**Ganchos de higiene (sí existen, y bloquean):** `deploy/comun/hooks/` contiene `guardia_higiene.py`, `pre-commit`, `pre-push`, `test_guardia.py`, `VERIFICACION.md`. Es el único mecanismo de control de admisión verificado en disco hoy — pero opera sobre commits, no sobre datos de sensor. No es la Aduana.

**Git:** rama `master`; último commit `9a0baf6` (2026-08-10) `docs(mcp): declara fragilidad del pin mcp<2`.
**Árbol sucio — 12 entradas.** 9 borrados en `mente/` (`ENJAMBRE_MEDALLON.txt`, `EQUIPO_AI_LOOP.md`, `MAPA_EVOLUTIVO_P0X.md`, `PAQUETE_NOTEBOOKLM_NIVEL3.txt`, `PROMPT_CARAS_PUBLICAS.txt`, `RESPUESTAS_INTERROGATORIO.txt`, `SEGURIDAD_Y_FRENOS.md`, `TAREAS_CARAS_PUBLICAS.txt`, `test_fuga.md`) y 3 sin seguimiento (`Cuarentena/`, `bronze/`, `docs/`).

**Hallazgo derivado, relevante para R02+:** la cuarentena se llenó **moviendo** ficheros desde `mente/`, no copiándolos. Esos 9 documentos ya no existen en su ruta original y `Cuarentena/` no está bajo seguimiento de git. Archivar o borrar en cuarentena sin restaurarlos primero a una ruta versionada los pierde salvo por el historial. `03 §2` es *(informado)* y no cubre este movimiento.

**Dependencias Python declaradas** — `requirements.txt`: `psutil>=7.1` (monje/genesis.py), `requests>=2.32` (latido de Ollama local), `wasmtime>=46.0` (preceptor/frontera.py, jaula G3). Entorno declarado en el propio fichero: venv de usuario con `uv`. **Versiones realmente instaladas: `NO_DATA`** — no se ejecutó `pip freeze`, y el sandbox de esta sesión no es la máquina `soberano`.

## §3 · DECISIONES D1–D10

Fuente única para las diez: `Cuarentena/03_ESTADO_FIRMADO.md` · `3159e5237398a9f7` · 6803 B · 101 L. **Caduca `2026-09-10`**: pasada esa fecha todo su contenido pasa a `NO_DATA` (regla de caducidad del propio documento).

| D | Contenido (resumen fiel) | Verificación en disco hoy |
|---|---|---|
| D1 | `CineK_Studio` repo oficial; `cinek_automatico` archivado | **NO_DATA.** `find -maxdepth 2 -iname '*cinek*'` → solo `bronze/2026-08-10-prediccion-cinek.md` y el PDF en cuarentena. Ningún repo con ese nombre bajo `p0x/` |
| D2 | Corrección hacia adelante en `config.py`; sin reescribir historia | **NO_DATA** en cuanto a la ruta: no se localizó `config.py` en esta pasada. Sí verificado el pre-check VERDE de claves (03, VERIFICACIÓN RAÍZ) |
| D3 | Dashboard v2 en `hexelion/dashboard`, `localhost:5173/ui/`; `:8001` descartado | **NO_DATA.** `ls -d hexelion` falla (stderr en Anexo A.1) y `find -type d -iname '*dashboard*\|*hexelion*\|ui'` → cero. Vive fuera de `p0x/`, fuera de mi alcance de lectura. Un agente documental no puede verificar un puerto |
| D4 | Push de `35b2553` autorizado, nunca forzado | **NO_DATA.** No verifiqué la existencia del objeto; `git log` sin `--all` no lo mostró. Verificable con `git cat-file -e 35b2553` |
| D5 | `planta_brote.webp` placeholder provisional | **NO_DATA.** No localizado en esta pasada |
| D6 | K firma Gold en Herbier cuando entienda que firma | Coherente con `gold/` **vacío** (0 ficheros). No hay Gold que firmar. Consistente |
| D7 | Anclaje pospuesto hasta dashboard MVP funcional | Consistente con D3 `NO_DATA` |
| D8 | IPs tailnet/LAN visibles; keys secreto; JWT de "Del Barrido" quemado | Aplicado en R00 y aquí. Patrones de secreto vivos en cuarentena: **0**. El JWT literal no aparece en el fichero: `NO_DATA` (R00 §3) |
| D9 | v1.3.0 canon hasta firma de v1.5; v1.4 borrador sin autoridad; cláusula de grounding | Verificado: los tres ficheros existen y divergen (§0.4). **Cumplido por este documento** |
| D10 | `test_fuga.md` = canario antiguo; enterrado en `necropolis/` con motivo; original eliminado | **VERIFICADO.** `Cuarentena/necropolis/` contiene `test_fuga.md` (9 B) y `test_fuga.tumba` (124 B). `ls Cuarentena/test_fuga.md` falla (stderr en Anexo A.2). Ejecución correcta y completa |

D10 es la única decisión de las diez **verificable de punta a punta en disco hoy**. Se dice porque es información, no reproche: el resto describe superficies que un agente documental no alcanza.

## §4 · PRODUCTOS

| Producto | Afirmación admisible | Fuente |
|---|---|---|
| **Aurelius** | Preceptor local del Soberano; producto pedagógico con repo, modelo y doctrina propios. **No es el portero de datos** | `02 §2` · `1426f37ec8661398` |
| **Le Jardin / Herbier / Le Cahier / La Sentinelle** | Superficies definidas en el canon visual v1.3.0 §4 | `BLUEPRINT_DISENO_SOBERANO.md` · `cb767c464cc25631` |
| **El Nexo** | Cara brutalista; celda hexagonal; estados NO DATA en interfaz | ídem, §0 y §3 |
| **CineK** | `CineK_Studio` es el repo oficial (D1). Estado del código: `NO_DATA` (no está bajo `p0x/`). Existe una predicción firmada del Soberano sobre su objetivo | D1 · `bronze/2026-08-10-prediccion-cinek.md` |
| **Hexelion / dashboard v2** | Oficial por D3. Existencia en disco: `NO_DATA` | D3 |
| **skill `auditar-p0x`** | Existe y es la única skill en `skills/`: 6 scripts (`audit_frontmatter`, `audit_git`, `audit_report`, `audit_telemetria`, `audit_grafo`, `audit_lib`) + `SKILL.md` + `run_audit.sh` | `skills/auditar-p0x/` |
| **`monje/genesis.py`** | Sensores honestos del nodo + latido de Ollama local, según `requirements.txt` | `requirements.txt`, `monje/genesis.py` |
| **`preceptor/frontera.py`** | Jaula wasmtime para código propuesto (G3) | `requirements.txt`, `preceptor/frontera.py` |
| **`pipeline/`** | Motor delta, ingesta de YouTube, runner de observación. Salida medida: `pipeline/out/bench_delta.json` | `pipeline/` (7 ficheros) |
| **`voz/`** | `voz_server.py` + gate0 | `voz/` (3 ficheros) |
| **`proxy/litellm_config.yaml`** | Configuración de proxy de modelos. Contenido no leído: `NO_DATA` | ruta verificada |

## §5 · HARDWARE

`03 §3` fija la forma de la verificación: cinco campos por fuente. `03 §2` es *(informado)* y **no** medición. Un agente documental no ve un sensor; ve su rastro en disco.

| Fuente declarada | existe | visible por la Aduana | esquema | última medición real | estado |
|---|---|---|---|---|---|
| `bme680` | NO_DATA | No (la Aduana no existe) | NO_DATA | NO_DATA | `NO_DATA` |
| `axl345` → probablemente ADXL345 | NO_DATA | No | NO_DATA | NO_DATA | `PENDIENTE_CONFIRMACION` |
| `apklvsr` | NO_DATA | No | NO_DATA | NO_DATA | **`NO_DATA` — BLOQUEA** |
| `camara` (nodo Vigía) | NO_DATA | No | NO_DATA | NO_DATA | `NO_DATA` |
| ESP32 | NO_DATA | No | NO_DATA | NO_DATA | `NO_DATA` |

**Rastro documental encontrado** (menciona los dispositivos; **no** es telemetría): `mente/reflejos/reflejo-vibracion.md`, `mente/reflejos/reflejo-termico-m5.md`, `mente/feedback/PENDIENTES.md`, `mente/reportes/DOS_PIELES_soberano_2026-07-19.md`, `mente/auditorias/INVENTARIO_WIDGETS_2026-07-13.md`, `mente/doctrina/DISCURSO_FUNDACIONAL_P0X.md`. Comando: `grep -rl -iE 'esp32|bme680|adxl345|axl345'` excluyendo `Cuarentena/` y `node_modules`.

**`mente/telemetria/` contiene 9 ficheros**, y ninguno es telemetría de sensor: son *benchmarks y evaluaciones de modelos* (`cerebro_local.jsonl`, `cerebro_local_bench.json`, `duelo_harness_g1.json`, `eval_grounding_g1r_retest.json`, `eval_grounding_g2.json`, `scraper_bambu_g1.json`, `soberano_bench_g0.json`, `PLAYWRIGHT_DOS_PIELES.md`, `README.md`). La carpeta se llama telemetría y mide siliconas, no jardín. Se declara porque un agente futuro buscará ahí el rastro de los sensores y no lo encontrará.

**Conclusión de §5, sin adornos:** cero mediciones de sensor en disco. `03 §2` afirma "ESP32 con sensores funcionando" y "cámara en el Vigía funcional" — ambas son **declaraciones del Soberano**, citables como tales y **no** como hecho medido. `deploy/vigia/firmware/` existe como ruta; su contenido no se leyó en esta ronda.

## §6 · LO QUE v1.5 NO AFIRMA (y por qué)

- Ninguna cifra de rendimiento, ahorro o latencia. Sin contador → `NO_DATA` (`02 §2`).
- Ningún estado de puerto, servicio o URL. No hay `curl` en una ronda documental (`04 §5`).
- Ninguna versión de paquete instalada. Solo lo declarado en `requirements.txt`.
- Ningún frente aparcado de `03 §4`, ni como próximo paso ni como mención de futuro.
- Ninguna reescritura del canon visual: es R06 y exige orden explícita. v1.5 lo **referencia por hash**, no lo sustituye. Ver §8.
- Nada procedente de v1.4: usado solo como esqueleto de secciones (D9).

## §7 · FUENTES EXCLUIDAS DELIBERADAMENTE

Los 57 documentos de dato de la cuarentena **no** son fuente de v1.5. R00 los clasificó; 19 quedaron `EXTRAER`, y la extracción no ha ocurrido. Citarlos hoy como autoridad convertiría material en cuarentena en canon por la puerta de atrás, contra `01 §1`. Los 7 informes con citas web son `EXTERNO_NO_VERIFICADO` y además 6 de ellos carecen de hash utilizable (§0.1).

## §8 · LA OBJECIÓN QUE DEBE RESOLVER EL SOBERANO

v1.3.0 y v1.4 son, de principio a fin, **biblias visuales**: switcher de tres caras, tipografías, paletas Nexo y Jardin, z-index, anatomía de celda hexagonal, micro-interacciones, reglas de emergencia de interfaz.

El contenido mínimo que la misión fija para v1.5 —identidad, arquitectura, D1–D10, productos, hardware, punteros a `02_`— es un documento **de sistema**, no de interfaz. No hay solapamiento real entre ambos.

Por tanto: si v1.5 se firma como *sucesor* de v1.3.0, la firma **retira del canon** el sistema de tokens, las dos paletas y las reglas visuales de NO DATA, que hoy son lo único que impide que la interfaz mienta. Eso sería una pérdida de canon ejecutada por un acto que parece una mejora — y tocaría el dominio visual (R06) sin la orden explícita que R06 exige.

El borrador resuelve la tensión de la única forma que no destruye nada: **v1.5 no sucede a v1.3.0, lo envuelve.** El canon visual sigue siendo v1.3.0, vigente e íntegro, citado por ruta y hash desde v1.5. La decisión de si eso es lo que el Soberano quería es suya, y está formulada en el borrador §7.

---

## ANEXO A · COMANDOS FALLIDOS (stderr literal, sin parafrasear)

**A.1 — verificación de D3:**

`ls -d hexelion`
`ls: cannot access 'hexelion': No such file or directory`

**A.2 — verificación de D10 (fallo esperado y correcto):**

`ls Cuarentena/test_fuga.md`
`ls: cannot access 'Cuarentena/test_fuga.md': No such file or directory`

**A.3 — estado de git sobre montaje de solo lectura:**

`git status --porcelain`
`warning: unable to unlink '/sessions/<sandbox>/mnt/p0x/.git/index.lock': Operation not permitted`  <!-- guardia:permitir mensaje-de-error-verbatim-de-git-en-sandbox -->

El comando devolvió las 12 entradas pese al aviso. El aviso es del montaje del sandbox, no del repositorio: git intentó refrescar su índice y no pudo escribir. **No se modificó nada en `.git/`.** La ruta del sandbox se ofusca aquí por higiene (`02 §6`).

**A.4 — ruta citada por la misión que no existe:**

Se buscó `Cuarentena/salida/POST_VERIFICACION_R00_INVENTARIO.md`. Mi script imprimió `FALTA` (no es stderr: la comprobación fue `[ -f ]`, que no emite error).
Causa: el fichero fue **movido** por el Soberano a `docs/post_verificacion/`, donde sí existe (`acf95f6f5bd47af6`). No es un fallo; es el paso 2 de `01 §6` ya ejecutado.

**A.5 — sin errores:** `sha256sum`, `wc`, `find`, `grep`, `comm`, `awk`, `du`, `stat` sobre las rutas citadas.

---

## ANEXO B · TABLA DE HASHES USADOS EN v1.5

| Ruta | sha256 (16) | Bytes | Líneas |
|---|---|---|---|
| `Cuarentena/01_LEEME_PRIMERO.md` | `cb244b4f1f551bab` | 3976 | 75 |
| `Cuarentena/02_CANON_OPERATIVO.md` | `1426f37ec8661398` | 7701 | 117 |
| `Cuarentena/03_ESTADO_FIRMADO.md` | `3159e5237398a9f7` | 6803 | 101 |
| `Cuarentena/04_CONTRATO_CLAUDE_CODE.md` | `2ac89e6d7078ca47` | 7039 | 128 |
| `Cuarentena/05_PLANTILLA_POST_VERIFICACION.md` | `da0cf517a7370598` | 3342 | 87 |
| `BLUEPRINT_DISENO_SOBERANO.md` (canon visual, D9) | `cb767c464cc25631` | 30153 | 266 |
| `mente/doctrina/BLUEPRINT_DISENO_SOBERANO.md` (copia fantasma v1.2.0) | `43e73ae74fb28d63` | NO_DATA | 271 |
| `Cuarentena/blueprint-de-diseno-soberano-v1.4.md` (borrador, sin autoridad) | `9349c558829bd678` | 36195 | 331 |
| `Cuarentena/salida/HASHES_R00.txt` (parcial, §0.1) | `ae9d7ab0400276d3` | 6838 | 64 |
| `docs/post_verificacion/POST_VERIFICACION_R00_INVENTARIO.md` | `acf95f6f5bd47af6` | 17497 | NO_DATA |

Los 9 ficheros de cuarentena con nombre con espacios: **`HASH_NO_DATA`** (§0.1).

---

Pendiente de firma del Soberano para cierre de Ronda 1.
FIRMADO por el Soberano el 20260811.
