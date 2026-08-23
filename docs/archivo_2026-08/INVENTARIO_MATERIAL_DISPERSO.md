# INVENTARIO DEL MATERIAL DISPERSO

**Fecha:** 2026-08-23 · **Nodo:** soberano (Beelink) · **Fase:** Localizador (equipo de lectura)

Meses de trabajo previo viven fuera de los repositorios. Esto es lo que hay, medido —
no lo que se recuerda que hay.

---

## 1 · Método

Barrido de `~` con dos redes: por nombre (`aurelius`, `lore`, `arquetipo`, `doctrina`,
`manifiesto`, `plan`, `fase`, `lora`, `mvp`, `p0x`, `hexelion`, `preceptor`, `camino`) y
por carpeta declarada por el Soberano. Cada hallazgo se cruzó contra **los 18 repositorios
git del disco** para separar lo ya versionado de lo suelto.

**Lo que NO se miró, y por qué.** `~/.ssh`, `~/.gnupg`, `~/.near-credentials`, `~/.pki`,
`~/.config`, `~/.local`, y los almacenes de tokens. El encargo es inventariar trabajo, no
material criptográfico: si una clave apareciera en este inventario, ya se habría leído de más.

**Lo que se excluyó por ser personal.** Tres documentos (CV y un contrato laboral). No son
material de proyecto y no se han abierto.

**Una corrección durante el propio barrido.** La primera pasada cortó la lista de
repositorios con un `head -12` y marcó como sueltos ficheros que sí están versionados
dentro de `pre-bee/hexelion`. Se rehízo entera. El número que vale es el segundo.

---

## 2 · Lo que hay

| Carpeta | Docs | Peso | Qué es |
|---|---:|---:|---|
| `~/pre-bee/p0x/MD 3` | 201 | 2011 kB | El archivo grande. Doctrina, códices Hexelion, prompts de sesión |
| `~/pre-bee/p0x` | 32 | 276 kB | Copia parcial del anterior + material suelto |
| `~/Downloads` | 26 | 9646 kB | Informes largos de IAs externas, sin clasificar |
| `~/privado_p0x/cuarentena_originales_20260810` | 17 | 311 kB | Cuarentena del 10 de agosto, originales |
| `~/p0x/Cuarentena/salida` | 10 | 117 kB | Salida de la cuarentena, ya procesada |
| `~/p0x/Cuarentena` | 8 | 1258 kB | Cuarentena en el repo, sin versionar |
| `~/pre-bee/p0x/P0X` | 4 | 28 kB | Subcopia dentro de la copia |
| `~/pre-bee/p0x-soberano/docs` | 2 | 19 kB | Documentos del nodo soberano, anteriores a este PC |
| `~` | 1 | 70 kB | — |
| `~/p0x/aurelius-mvp/docs` | 1 | 22 kB | — |

**Total: 316 documentos, 13951 kB.**

### Reparto por estado

| Estado | Ficheros |
|---|---:|
| Ya versionado en algún repositorio | 339 |
| Dentro de un repositorio pero **sin versionar** | 83 |
| **Fuera de todo repositorio** | 415 |

De esos, **316 son documentos** (`.md`, `.txt`, `.odt`, `.pdf`, `.docx`) — el resto son
imágenes, comprimidos y artefactos de compilación que no entran en la lectura.

---

## 3 · Los tres hallazgos del Localizador

### 3.1 · `pre-bee/p0x/MD 3` es el archivo, y casi nada de él llegó al repo

201 documentos. Se comprobó **nombre a nombre** contra `~/p0x`:

> **188 de 202 existen solo aquí. 12 están también en el repositorio.**

Ahí dentro está el núcleo doctrinal (`00_CONSTITUCION_*`, `DOCTRINA_AI_INTERNA_P0X`,
`INSTRUCCIONES_P0X`, `MANUAL_DEL_SOBERANO_P0X`, `ORQUESTA_MODELOS_P0X`,
`PROTOCOLO_MD_EVOLUTIVO_P0X`, `ALFABETO_P0X`) — que es exactamente la lista de la que
`CLAUDE.md` dice haberse destilado. Nueve de esos títulos sí viven hoy en
`~/p0x/mente/doctrina/`. El resto del archivo, no.

### 3.2 · La duplicación no es basura: es el rastro del refinamiento

Comparados por hash, hay **302 documentos distintos** y solo **18 copias exactas**
sobrantes. Lo que se siente como duplicación son **29 familias de versiones** — la misma
idea escrita dos, tres y cuatro veces:

- `CLAUDE_CODE_PROMPT_dashboard_v2 → v3 → v4`
- `HEXELION_BRIEFING_MAESTRO_20260524 → _v2`
- `HEXELION_VISION_PITCH → _v2`
- `INSTRUCCIONES_P0X → _v1`
- `HEXELION_SESION_20260502 → 0510 → 0511`

Eso no se borra: **es donde se ve cómo cambió de opinión.** Las copias exactas sí
sobran, y son solo 18.

### 3.3 · Las fechas del sistema de ficheros no sirven

Los 262 ficheros de `MD 3` tienen la misma fecha de modificación (2026-07-11): la de la
copia, no la de la escritura. La cronología real está **en los nombres**
(`2026-05-28_...`, `_20260524`) y dentro de los documentos. Cualquier orden cronológico
que se construya con `mtime` será falso.

---

## 4 · Duplicación entre carpetas

Pares que se repiten, medidos por contenido idéntico:

| Copias | Entre |
|---:|---|
| 5 | `pre-bee/p0x` ↔ `pre-bee/p0x/MD 3` |
| 4 | `pre-bee/p0x/MD 3` ↔ `pre-bee/p0x/P0X` |
| 3 | `Downloads` ↔ `p0x/Cuarentena` |
| 1 | `pre-bee/p0x/MD 3` ↔ `pre-bee/p0x/p0x2` |

`MD 3` es superconjunto de `pre-bee/p0x` en lo que solapan. `Downloads` contiene los
informes largos de IAs externas, y tres de ellos ya se habían movido a `Cuarentena`.

---

## 5 · Lo más pesado (donde puede estar lo más denso)

| Peso | Documento |
|---:|---|
| 7,5 MB | `~/Downloads/Aurelius_Sovereign_Preceptor.pdf` |
| 645 kB | `Prompt Maestro · Ronda de Agentes AI-AI: Nexo, Le Jardin, HEXELION` (dos copias) |
| 579 kB | `~/Downloads/piskyrpapalo-aurelius-8a5edab282632443.txt` |
| 457 kB | `Plan Integral · Entrenamiento Local del LoRA de Aurelius` |
| 366 kB | `Architectural Blueprint · CineK Automático` |
| 72 kB | `De Ollama al Borde · arquitectura para 'Le Cahier'` (dos copias) |
| 70 kB | `~/Aurelius,plan.odt` |
| 59 kB | `HEXELION_CODICE_2026_14_MAESTRO.md` |
| 56 kB | `Estudio Final · Objetivos y Alcance del Producto Aurelius-MVP.md` |

---

## 6 · Cómo se está leyendo (Regla de oro aplicada)

El volumen es de 13,7 MB. Leerlo entero con token de frontera sería quemarlo en trabajo
mecánico, así que el reparto es:

- **Frontera** — los tres lotes de más juicio: doctrina P0X, El Faro / NEAR / economía
  máquina, y el alma de Hexelion. 81 documentos.
- **AI local (Qwen3-Coder-30B en este mismo PC)** — resumen estructurado de los 231
  restantes: operación de Hexelion, prompts de sesión y los sueltos. Un JSON por
  documento, con esquema forzado por `--json-schema`, que es la capacidad que se verificó
  esta misma mañana. Medido: 36 s por documento.

La pasada local es **reanudable**: si se corta, retoma donde estaba.

---

## 7 · Lo que este inventario NO dice

No dice qué vale y qué no — eso es del Clasificador y del Revisor. No dice dónde debe ir
cada cosa — eso es del Conserje. Y no se ha movido, borrado ni editado **nada**.
