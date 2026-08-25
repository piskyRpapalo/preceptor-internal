# CUARENTENA · VEREDICTOS

**Fecha:** 2026-08-26 · **Alcance de esta tanda:** los cuatro documentos que el Soberano
nombró primero. El inventario mecánico del resto va aparte, en `CUARENTENA_INVENTARIO.md`.

> **Nada se ha borrado, movido ni editado.** «eliminar» aquí significa *propuesto para
> eliminar*, y como toda propuesta la firma el carbono. Es la misma regla que el Curador:
> propone sobre la memoria y no la toca.

Cuatro veredictos posibles: **rescatar** (vale y no está en ningún sitio) · **fusionar**
(su contenido ya vive en otro documento, y lo que falta es la cita) · **`[sleeping]`**
(se retira con condición de despertar escrita) · **eliminar** (propuesto).

---

## 1 · `ENJAMBRE_MEDALLON.txt` — **FUSIONAR**

*9.255 B · 2026-08-09 · permisos `0600` · «Autor: el Preceptor. Canoniza: el Soberano».*

**Qué es.** Corrige un plan de cuatro agentes y dice que no son cuatro agentes sino
**cuatro roles que ocupa el mismo motor en momentos distintos**. Seis secciones: la
corrección de partida, la Medallón como sustrato del traspaso, los cuatro roles y su capa,
el ciclo del prompt del Preceptor al Soberano, la nube dentro de la Medallón, y qué se
construye primero.

**Por qué fusionar y no rescatar.** Es un **antepasado directo de `ARQ_LOOPS.md`**, que se
escribió catorce días después (2026-08-23) y que ya declara —correctamente— que sus cuatro
refinaciones *«salen del archivo del propio Soberano […] se aprendieron pagando entre mayo
y julio»*. La tesis de un motor con varios roles es exactamente lo que hoy son L0–L4 más la
bandeja de firmas, y el «ciclo del prompt» de §4 es la bandeja.

**Acción propuesta:** añadir una fila a la tabla de antepasados de `ARQ_LOOPS.md` citando
este fichero por ruta y fecha, como ya se hace con el Filtro de Eficiencia y el Score S0.
Después, el documento queda como fuente citada, no como material pendiente.

---

## 2 · `capas-aurelius-jardin-v2.md` — **RESCATAR (parcial) + `[sleeping]` el resto**

*12.066 B · Medallón de tres capas para Aurelius Core y Hexelion/Jardín, más «las 11
meditaciones».*

**Medido hoy, y esto decide el veredicto:** la Medallón de Aurelius Core que describe §2
—`data/bronze/`, `proposals_YYYY-MM.jsonl`, `gold_chain.jsonl`— **no existe**. `find` no
encuentra ni `gold_chain*` ni `proposals_*` en todo el árbol, y `bronze/` contiene **un solo
fichero**, que es una predicción de CineK. Es decir: se diseñó y no se construyó.

Pero **una de las once meditaciones sí llegó a producción**: §3.10 *«engrams en SQLite
FTS5»* es literalmente lo que hoy hace `aurelius/memory.py` —18 apariciones de
`engrams_fts`— y sobre lo que se apoya el peldaño 2 del Curador. Y §3.1 (`llamacpp`) es el
motor del producto.

- **Rescatar:** §1 (el motivo — mitigar *write wear* en SD/eMMC de los nodos edge) y las
  meditaciones 3.1 y 3.10, que ya son código y merecen quedar citadas como origen.
- **`[sleeping]`** el resto de §2 y §3. Condición de despertar escrita:
  *«despierta cuando exista una segunda fuente de escritura frecuente en un nodo con eMMC —
  hoy la única memoria que se escribe de verdad es `memory.db`, y está vacía (0 recuerdos
  activos, medido por el Curador)»*.

Una arquitectura de tres capas para amortiguar escrituras sobre una base sin escrituras es
complejidad comprada por adelantado.

---

## 3 · `medallon-dashboards-v2.md` — **FUSIONAR (dos tercios) + ELIMINAR (un tercio)**

*10.030 B · define tres tableros: El Nexo, Le Jardin des Ombres y Dashboard CMP.*

- **§1 El Nexo** y **§2 Le Jardin des Ombres** → **fusionar** con el canon visual vigente
  (`BLUEPRINT_DISENO_SOBERANO.md`, que ya manda en paletas del Nexo y de Le Jardin) y con
  el backlog (`mente/backlog/BACKLOG_UI.md`, BLOQUE 6, «Le Jardin = Fase 4»). Entra directo
  en el tablero de rack de M10: hoy la cámara del rincón verde ya sirve, y es el widget de
  Le Jardin sin más ceremonia.
- **§3 Dashboard CMP** (Compose Multiplatform + Skia) → **eliminar (propuesto)**. Ya tiene
  lápida firmada: `mente/auditorias/RACK_Y_CODICE_2026-08-09.md:94` registra el commit
  `f4a7ad7 docs(canon): Misiones 7-9 (§5.1 ambiente, --nx-green fix, lápida CMP)`. Mantener
  el diseño de algo enterrado hace once meses no conserva una opción: conserva una duda.

**Aviso de coherencia:** el documento habla de «tres tableros». Con CMP enterrado son dos, y
el canon del 2026-07-20 ya separa Hexelion (Nexo y Le Jardin) de PreceptorOS. Al fusionar,
que la cuenta se corrija.

---

## 4 · `Prompt Maestro … Nexo, Le Jardin y Sistema HEXELION.pdf` — **PENDIENTE DE LECTURA**

*660.576 B · PDF · 2026-08-12.*

**No emito veredicto sobre lo que no he leído.** Es un PDF de 645 KiB y esta sesión no lo ha
abierto; decir «fusionar» por el título sería exactamente la avería que denuncia la
sugerencia S5 de `PENDIENTES.md` —*«una crítica entró como enmienda sin comprobarse contra
el código»*— con el sentido invertido.

**Lo que sí se sabe, y acota el trabajo:** por título cubre los mismos tres sistemas que el
documento §3, dos de los cuales quedan fusionados arriba y uno enterrado. Lo probable es que
sea **fusionar**, y por eso mismo hay que leerlo antes de decirlo.

**Siguiente paso concreto:** extraer su texto y clasificarlo por secciones contra los cuatro
veredictos de arriba. Es lectura, cabe en una tanda corta.

---

## Estado de la tanda

| documento | veredicto | ¿toca fichero? |
|---|---|---|
| `ENJAMBRE_MEDALLON.txt` | **fusionar** → cita en `ARQ_LOOPS.md` | no |
| `capas-aurelius-jardin-v2.md` | **rescatar §1/§3.1/§3.10** · `[sleeping]` el resto | no |
| `medallon-dashboards-v2.md` | **fusionar §1/§2** · **eliminar §3 (propuesto)** | no |
| PDF *Prompt Maestro* | **pendiente de lectura** — sin veredicto | no |

Quedan **61 documentos** en la raíz de Cuarentena sin mirar. Inventario mecánico aparte.
