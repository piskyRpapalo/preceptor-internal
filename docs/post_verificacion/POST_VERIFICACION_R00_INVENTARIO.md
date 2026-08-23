# POST_VERIFICACION · R00
Misión: Inventario + clasificación documental de `/home/pisky/p0x/Cuarentena` (solo ficheros de primer nivel).
Fecha: 2026-08-11 (reloj del sandbox: 2026-08-10T UTC · discrepancia declarada, ver §6)
Dominio: INVENTARIO_DOCUMENTAL
Estado: FIRMADO
Firmante: Soberano

## 1 · RESUMEN

Se inventariaron **63 ficheros** (1.977.342 bytes; 22.567 líneas de texto; 37 `.md`, 25 `.txt`, 1 `.pdf`). 6 son instrucción (`0X_*`); 57 son dato a clasificar. Método: barrido determinista de metadatos (tamaño, líneas, frontmatter, conteo de URLs, patrones de secreto, términos aparcados) + lectura profunda solo de los 6 canon y verificación puntual de 2 colisiones. No hubo lectura completa de los 57 datos: se declara como límite del método, no como cobertura.
Se propone: `EXTRAER` 19 · `CONSOLIDAR` 10 · `ARCHIVAR` 17 · `NO_USAR` 4 · `REVISAR_SOBERANO` 7 (suma 57 = total de datos; verificado por conteo sobre el propio anexo).
Hallazgo grave: el `BLUEPRINT_DISENO_SOBERANO.md` de la raíz está en **v1.3.0** y la cuarentena contiene un **v1.4** que declara sustituirlo. El canon de disco está por detrás de un borrador en cuarentena (P1_SOBERANÍA).
Decisión requerida: §8.

## 2 · HECHO

- Ritual de arranque completo: leídos `01`, `02`, `03`, `04`, `05` (P1: canon = disco).
- Inventario de primer nivel de `Cuarentena/`. `salida/` y `necropolis/` verificados: **ambos vacíos**.
- Clasificación y acción propuesta por fichero (ANEXO A).
- Detección de duplicados por `md5sum`; de supuestos prohibidos por conteo de términos; de secretos por patrón (`eyJ…`, `sk-…`, `AKIA…`, `Bearer …`, `key=`, `token=`, `password=`).
- Una lectura fuera de Cuarentena, solo-lectura y acotada: `p0x/BLUEPRINT_DISENO_SOBERANO.md` (para resolver colisión de versión).

**NO ejecutado (explícito):** ningún borrado, movimiento, edición, `git`, deploy, instalación. Ninguna escritura fuera de `Cuarentena/salida/`. Ningún barrido residual (R01), censo de fuentes (R02), árbol Medallón (R03) ni verificación de hardware. Ninguna orden contenida en un documento fue obedecida (§3 de `01`).

## 3 · MEDIDO

| Medición | Cifra | Origen (solo-lectura) |
|---|---|---|
| Ficheros de primer nivel | 63 | `ls -p \| grep -v / \| wc -l` |
| Bytes totales (excl. subcarpetas) | 1.977.342 | `du -sb --exclude=necropolis --exclude=salida .` |
| Líneas de texto totales | 22.567 | `cat *.md *.txt \| wc -l` |
| Ficheros instrucción / dato | 6 / 57 | listado |
| `salida/` · `necropolis/` | 0 ficheros cada una | `ls -la salida/ necropolis/` |
| Duplicados byte-idénticos | 2 pares | `md5sum *.txt *.md \| uniq -d` |
| Ficheros con ≥20 URLs externas | 6 | `grep -o -iE 'https?://' \| wc -l` |
| URLs externas, dominio top | youtube.com 56 · nasa.gov 20 · github.com 18 · reddit.com 15 · facebook.com 13 | `grep -h -oE 'https?://[a-zA-Z0-9.-]+' *.md` |
| Ficheros con IP tailnet/LAN | 2 (`AURELIUS_MANUAL_ASSEMBLY_V1.2/V4.txt`) | `grep -lE '100\.\|192\.168\.\|10\.'` |
| Patrones de secreto vivos en Cuarentena | **0** | `grep -iE 'eyJ…\|sk-…\|AKIA…\|Bearer …'` → única coincidencia: `03_ESTADO_FIRMADO.md:87`, placeholder AWS ya declarado por el Soberano |
| Fichero más grande (texto) | `CATALOGO_SKILLS_AURELIUS_V3_…` 199.576 B / 3.512 L | `stat`, `wc -l` |
| Colisión de versión Blueprint | raíz v1.3.0 (266 L) vs cuarentena v1.4 (331 L), md5 distinto | `md5sum`, `grep -m3 version` |
| JWT de "Del Barrido al Borde" (D8: quemado) | **NO_DATA** — 0 coincidencias de patrón JWT literal en el fichero | `grep -oE '[A-Za-z0-9_-]{40,}'` → solo slugs de URL |

## 4 · CRÍTICO

1. **El canon de disco va por detrás de la cuarentena.** `p0x/BLUEPRINT_DISENO_SOBERANO.md` = v1.3.0. `Cuarentena/blueprint-de-diseno-soberano-v1.4.md` declara literalmente *"Archivo que sustituye: BLUEPRINT DE DISEÑO SOBERANO v1.3"*. Mientras no se firme, el canon vigente es el de la raíz (v1.3.0) y el v1.4 es **propuesta**, no ley. Violaría P1_SOBERANÍA tratar el borrador como canon.
2. **`test_fuga.md`** (9 bytes, contenido: la palabra `soberano`). Nombre y contenido son compatibles con un **canario de fuga** plantado a propósito. No se toca ni se propone borrar: `REVISAR_SOBERANO`. Si es canario, borrarlo destruye la prueba; si es basura, se archiva.
3. **`p0x.system.pending.md` (4.501 B) y `p0x.system.pending(1).md` (9.092 B)** no son duplicados: divergen. Dos listas de pendientes en desacuerdo son peores que ninguna.
4. **Frentes aparcados presentes como plan, no como historia.** "Mesh Soberana" / DePIN / enjambre aparecen 7–32 veces en la familia AURELIUS_CATALOG y en `ENJAMBRE_MEDALLON.txt`, con endpoints y mecánica de validación entre nodos. Es material aparcado por `03 §4`. Se clasifica, no se planifica.

## 5 · BLOQUEADO

- Extracción de doctrina del Blueprint ← decisión del Soberano sobre v1.3.0 vs v1.4 (§8).
- Verificación del JWT quemado de "Del Barrido al Borde" ← el patrón no aparece en el fichero; solo el Soberano sabe dónde viajó el valor.
- Clasificación fina de `Architectural Blueprint … CineK Automático.pdf` ← binario, no leído en esta ronda (R00 es inventario, no extracción de PDF).
- Cualquier ronda posterior (R01+) ← firma de R00 (`01 §4`).

## 6 · NO_DATA

- Contenido íntegro de los 57 ficheros de dato: **no leído**. La clasificación se apoya en metadatos y muestreo de contexto, y puede corregirse en la extracción.
- Contenido del PDF de CineK: `NO_DATA`.
- Fecha real: el reloj del sandbox devuelve `2026-08-10` y el entorno declara `2026-08-11`. No resuelvo la discrepancia; uso la del entorno y la declaro.
- Autoría y procedencia exacta de cada documento (qué modelo o humano lo produjo): `NO_DATA` salvo lo inferible del nombre (`…qwen…`, `respuesta_preceptor_…`).
- Si los duplicados `(1)` proceden de una descarga repetida o de una divergencia posterior colapsada: `NO_DATA`.
- Estado de `apklvsr` (`03 §3`): sigue `NO_DATA`. No se conjetura.
- Métricas de la Aduana: `NO_DATA` (no existe el componente; `02 §2`).

## 7 · PARA CLAUDE CODE

Nada que ejecutar hasta firma. Tareas acotadas propuestas, en este orden:

| Tarea | Prioridad | Riesgo | Dependencia | Prompt sugerido |
|---|---|---|---|---|
| Diff textual completo `BLUEPRINT_DISENO_SOBERANO.md` (v1.3.0) vs `blueprint-de-diseno-soberano-v1.4.md` | Alta | Bajo (solo-lectura) | Firma R00 | "Genera `diff -u` de ambos ficheros a `Cuarentena/salida/DIFF_BLUEPRINT_v13_v14.txt`. No edites ninguno de los dos. Reporta §8 del contrato." |
| Diff `p0x.system.pending.md` vs `p0x.system.pending(1).md` | Media | Bajo | Firma R00 | "Genera `diff -u` de ambos a `Cuarentena/salida/DIFF_PENDING.txt`. No fusiones. Reporta." |
| Inventario de hashes de toda la Cuarentena (línea base anti-deriva) | Media | Bajo | Firma R00 | "Escribe `Cuarentena/salida/HASHES_R00.txt` con `sha256sum` de cada fichero de primer nivel. Sin mover nada." |

Ningún prompt abre frente aparcado.

## 8 · DECISIÓN PARA EL SOBERANO

**¿El `blueprint-de-diseno-soberano-v1.4.md` de la cuarentena sustituye al `BLUEPRINT_DISENO_SOBERANO.md` v1.3.0 de la raíz (y por tanto R00 lo marca `EXTRAER` como canon candidato), o el v1.4 queda `ARCHIVAR` y el canon sigue siendo v1.3.0?**

## 9 · CIERRE

- **Destino propuesto de este documento:** permanece en `Cuarentena/salida/`. Su archivo definitivo en la documentación del proyecto se propone como decisión posterior; la ruta destino no existe y **no se crea aquí**.
- **Documentos útiles que no deben perderse:** los 19 marcados `EXTRAER` en ANEXO A. Su contenido **no** está incorporado a este POST_VERIFICACION (R00 es inventario; la extracción es trabajo posterior). Se declara explícitamente: **no archivar ni borrar ninguno de ellos apoyándose en este documento.**
- **Archivado o borrado:** por defecto **archivar**. Ningún borrado se propone. La secuencia de `01_LEEME_PRIMERO.md §6` no está completa y su paso 5 no lo ejecuta ningún agente.

---

## ANEXO A · DOCUMENTAL (R00)

`L` = líneas · `U` = URLs externas · clasificación y acción según `02 §3`.

### A.1 · Instrucción (`0X_*`) — no se clasifica como dato

| Fichero | L | Nota |
|---|---|---|
| `00_INSTRUCCIONES_COWORK.md` | 48 | **Inconsistencia:** define LA CARPETA = `/home/pisky/p0x/Cuarentena (referencia historica a ruta inexistente, corregida en R01)`, que **no existe** en disco → esa referencia es `NO_DATA`. La carpeta real es `Cuarentena/`. |
| `01_LEEME_PRIMERO.md` | 75 | Orden de lectura. Dice que `04` no se lee para trabajar, se entrega. Se leyó por directiva del Soberano; se declara. |
| `02_CANON_OPERATIVO.md` | 117 | Taxonomía aplicada en este anexo. |
| `03_ESTADO_FIRMADO.md` | 89 | Manda ante contradicción. `caduca: 2026-09-10`. |
| `04_CONTRATO_CLAUDE_CODE.md` | 128 | Para entregar a Claude Code. |
| `05_PLANTILLA_POST_VERIFICACION.md` | 87 | Ruta que indica: `LA CARPETA/POST_VERIFICACION_R<id>.md`. Este entregable se escribió en `Cuarentena/salida/POST_VERIFICACION_R00_INVENTARIO.md` por directiva explícita del Soberano. Divergencia declarada. |

### A.2 · Familia AURELIUS · catálogos y manuales (9)

| Fichero | L | U | Clasificación | Motivo | Acción |
|---|---|---|---|---|---|
| `CATALOGO_SKILLS_AURELIUS_V3_ARQUITECTO_PSI_INGRESOS_HONESTOS.txt` | 3512 | 0 | UTIL_HISTORICO · CONTRADICE_FIRMADO | Versión más completa del catálogo; 32 menciones de Mesh y 12 de RAG, frentes aparcados (`03 §4`) | CONSOLIDAR |
| `CATALOGO_SKILLS_AURELIUS_CON_INGRESOS.txt` | 1833 | 0 | OBSOLETO | Superado por V3 | ARCHIVAR |
| `CATALOGO_SKILLS_AURELIUS.txt` | 1202 | 0 | OBSOLETO | Superado por V3 | ARCHIVAR |
| `AURELIUS_CATALOG_V4.txt` | 1909 | 0 | UTIL_HISTORICO · CONTRADICE_FIRMADO | 22 menciones Mesh/DePIN como diseño, no como historia | CONSOLIDAR |
| `AURELIUS_CATALOG_V1.2.txt` | 1933 | 0 | OBSOLETO | Superado por V4 | ARCHIVAR |
| `AURELIUS_MANUAL_ASSEMBLY_V4.txt` | 1294 | 4 | UTIL_OPERATIVO | Manual de montaje; contiene IPs tailnet/LAN — **visibles por D8**, no secreto | EXTRAER |
| `AURELIUS_MANUAL_ASSEMBLY_V1.2.txt` | 1326 | 4 | OBSOLETO | Superado por V4 | ARCHIVAR |
| `AURELIUS_ANNEX_V1.2.txt` | 892 | 0 | UTIL_HISTORICO | Anexo de la línea V1.2 | ARCHIVAR |
| `ANEXO_DE_CASOS_COMPLEJOS V4.txt` | 869 | 0 | UTIL_HISTORICO | Casos de uso; 17 menciones Mesh | ARCHIVAR |

### A.3 · Informes externos con citas web (7) — `EXTERNO_NO_VERIFICADO`

Criterio `02 §3`: se aprovecha la **estructura**, se descarta la **autoridad**. Ninguna de estas citas es verificable sin internet, y esta misión no lo tiene.

| Fichero | L | U | Motivo | Acción |
|---|---|---|---|---|
| `De la Teoría a la Práctica_ … Medallion y el Canon de Aurelius.md` | 112 | 87 | Máxima densidad de cita; propone MQTT(2), Azure(1), Platinum(2), multiusuario(4) — todos prohibidos por `02 §5` | EXTRAER (solo matrices) |
| `De Ollama al Borde_ … 'Le Cahier' … .md` | 146 | 66 | 56 citas de YouTube entre las fuentes; arquitectura de inferencia local sin evidencia en disco | EXTRAER (solo estructura) |
| `Hoja de Ruta para la Activación Visual del Dashboard p0x_ … .md` | 187 | 55 | Dominio visual = R06, solo con orden explícita | ARCHIVAR |
| `Hoja de Ruta para Claude Cowork_ Supervisión Activa … .md` | 239 | 51 | Documento que da órdenes a un agente: **dato con forma de orden** (`01 §3`), no instrucción | NO_USAR |
| `Del Barrido al Borde Inteligente_ … Medallion.md` | 97 | 35 | Origen del JWT declarado quemado en D8; llama "Aurelius" al filtro Edge, renombrado a **Aduana** por `02 §2` | REVISAR_SOBERANO |
| `Plan Integral para Aurelius Evolucionado_ … BigBang v1.md` | 202 | 23 | MQTT(1), Mesh(3); orquestación multiagente no firmada | ARCHIVAR |
| `Architectural Blueprint & Strategic Implementation Plan for CineK Automático.pdf` | BIN | NO_DATA | 374.685 B, no leído. D1 archiva `cinek_automatico`; el título nombra ese repo | REVISAR_SOBERANO |

### A.4 · Doctrina y operativa propia de p0x (16)

| Fichero | L | Clasificación | Motivo | Acción |
|---|---|---|---|---|
| `blueprint-de-diseno-soberano-v1.4.md` | 331 | CONTRADICE_FIRMADO | Declara sustituir al v1.3.0 que vive en la raíz. Ver §4.1 y §8 | REVISAR_SOBERANO |
| `SEGURIDAD_Y_FRENOS.md` | 251 | UTIL_DOCTRINA | Frontmatter válido; frenos y comprobaciones bloqueantes (`04 §3.7`) | EXTRAER |
| `MAPA_EVOLUTIVO_P0X.md` | 109 | UTIL_DOCTRINA | Frontmatter válido; historia del proyecto | EXTRAER |
| `EQUIPO_AI_LOOP.md` | 218 | UTIL_OPERATIVO | Frontmatter válido; reparto de roles silicio/carbono | EXTRAER |
| `p0x.doctrina.filosofia.md` | 51 | UTIL_DOCTRINA | Suelo filosófico, sin cita externa | EXTRAER |
| `p0x.infra.hardware.md` | 60 | UTIL_OPERATIVO | Insumo directo de R02/R03 (fuentes declaradas) | EXTRAER |
| `p0x.infra.software.md` | 60 | UTIL_OPERATIVO | Insumo directo de R01 | EXTRAER |
| `p0x.proyecto.aurelius.md` | 63 | UTIL_OPERATIVO | Delimita Aurelius = preceptor, no portero (`02 §2`) | EXTRAER |
| `p0x.proyecto.hexelion.md` | 62 | UTIL_OPERATIVO | Dashboard v2 oficial (D3) | EXTRAER |
| `p0x.system.pending.md` | 48 | NO_DATA | Divergente de `(1)`; no se sabe cuál rige | REVISAR_SOBERANO |
| `p0x.system.pending(1).md` | 87 | NO_DATA | Ídem, y es el más largo | REVISAR_SOBERANO |
| `p0x-arquitectura-y-especificaciones-paralelo.md` | 277 | UTIL_OPERATIVO | Especificaciones sin cita externa | CONSOLIDAR |
| `p0x-bootstrap-paralelo.md` | 77 | UTIL_OPERATIVO | Arranque; verificar contra disco en R01 | CONSOLIDAR |
| `p0x-canon-visual-y-diseno-unificado.md` | 281 | UTIL_HISTORICO | Dominio visual → R06, aparcado | ARCHIVAR |
| `p0x-doctrina-skills-y-repositorios-unificado.md` | 351 | UTIL_HISTORICO | 8 menciones Mesh, 2 RAG | ARCHIVAR |
| `p0x-remediacion-red-tailscale.md` | 69 | UTIL_OPERATIVO | Red; solo `0.0.0.0`/`127.0.0.1`, ninguna IP privada. Sin secretos | EXTRAER |

### A.5 · Manifiestos, técnicas y duplicados (14)

| Fichero | L | Clasificación | Motivo | Acción |
|---|---|---|---|---|
| `p0x-master-manifest-merge-v3.txt` | 220 | UTIL_OPERATIVO | Manifiesto vigente de la serie | CONSOLIDAR |
| `p0x-master-manifest-merge-v2.txt` | 168 | OBSOLETO | Superado por v3 | ARCHIVAR |
| `p0x-paper-manifest-v2.txt` | 82 | UTIL_HISTORICO | Vigente de la serie paper | CONSOLIDAR |
| `p0x-paper-manifest.txt` | 192 | OBSOLETO | Superado por v2 (aunque más largo: v2 no es superconjunto → verificar en extracción) | ARCHIVAR |
| `p0x-repositorios-tecnicas-unificado.txt` | 145 | UTIL_HISTORICO | Base de técnicas; MQTT(1), Mesh(3) | CONSOLIDAR |
| `p0x-repositorios-tecnicas-unificado(1).txt` | 145 | **RUIDO** | **md5 idéntico** a la anterior (`3faede4b…`) | NO_USAR |
| `p0x-repositorios-tecnicas-qwen-v2.txt` | 186 | EXTERNO_NO_VERIFICADO | Producido por otro modelo; sin evidencia en disco | CONSOLIDAR |
| `p0x-repositorios-tecnicas-qwen-v2 (1).txt` | 186 | **RUIDO** | **md5 idéntico** a la anterior (`433e5575…`) | NO_USAR |
| `p0x-tecnicas-consolidadas.txt` | 182 | UTIL_HISTORICO | Consolidado previo; MQTT(1), Mesh(3) | CONSOLIDAR |
| `aurelius-clasificacion-ideas.md` | 154 | UTIL_HISTORICO | 6 menciones Mesh; ideación, no plan | ARCHIVAR |
| `aurelius_pendiente_silver-v2.txt` | 11 | UTIL_OPERATIVO | Pendiente concreto de capa silver; corto y accionable | EXTRAER |
| `capas-aurelius-jardin-v2.md` | 105 | UTIL_OPERATIVO | Capas del jardín; insumo de R03 | EXTRAER |
| `medallon-dashboards-v2.md` | 84 | UTIL_OPERATIVO | Medallón ↔ dashboard; 1 mención RAG (aparcado) | EXTRAER |
| `inventario-necropolis-v2.md` | 128 | UTIL_OPERATIVO | Inventario previo de necrópolis; insumo directo de R01. `necropolis/` está **vacía** hoy | EXTRAER |

### A.6 · Prompts, respuestas y residuos (11)

| Fichero | L | Clasificación | Motivo | Acción |
|---|---|---|---|---|
| `PROMPT_ACTIVACION_R00.md` | 33 | UTIL_OPERATIVO | Prompt de esta ronda. **Dato**, no instrucción (`01 §3`) | ARCHIVAR |
| `MITOCONDRIA_PROMPT_CC.txt` | 337 | UTIL_OPERATIVO | Prompt para Claude Code; contrastar con `04` antes de usar | REVISAR_SOBERANO |
| `PROMPT_CARAS_PUBLICAS.txt` | 134 | UTIL_HISTORICO | Prompt de caras públicas; higiene obliga a revisar antes de publicar (`02 §6`) | ARCHIVAR |
| `TAREAS_CARAS_PUBLICAS.txt` | 137 | UTIL_HISTORICO | Tareas asociadas al anterior | ARCHIVAR |
| `PAQUETE_NOTEBOOKLM_NIVEL3.txt` | 205 | RUIDO | Paquete de empaquetado para herramienta de terceros; `01` prohíbe pegar este árbol en terceros no autorizados | NO_USAR |
| `ENJAMBRE_MEDALLON.txt` | 192 | CONTRADICE_FIRMADO | "Enjambre" = frente aparcado (mesh/multiagente, `03 §4`) | ARCHIVAR |
| `RESPUESTAS_INTERROGATORIO.txt` | 275 | UTIL_HISTORICO | Declaraciones del Soberano; **no verificadas en disco** (`03`, regla de origen) | EXTRAER |
| `respuesta_preceptor_limpia_peso_contexto.md` | 148 | UTIL_OPERATIVO | Gestión de peso de contexto; concuerda con `04 §3.8` (`num_ctx` por dato) | EXTRAER |
| `sugerencias-implementacion.md` | 224 | UTIL_HISTORICO | Libro de pendientes previo; sin evidencia de ejecución | CONSOLIDAR |
| `especificacion-cmp-multidispositivo.md` | 201 | UTIL_OPERATIVO | "Multidispositivo" ≠ "multiusuario por ID": este último está aparcado, aquel no. Verificar en extracción que no cruza la línea | EXTRAER |
| `test_fuga.md` | 1 | **SECRETO_POSIBLE / RUIDO** | 9 bytes, contenido `soberano`. Posible canario de fuga. No se borra, no se mueve | REVISAR_SOBERANO |

---

Pendiente de firma del Soberano para cierre de Ronda 0.

FIRMADO por el Soberano el 20260811: R0 cerrada.
