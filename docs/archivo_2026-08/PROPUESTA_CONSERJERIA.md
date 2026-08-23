# PROPUESTA DE CONSERJERÍA

**Fecha:** 2026-08-23 · **Fase:** Conserje (equipo de lectura)
**Estado:** PROPUESTA. **No se ha movido, borrado ni editado ningún fichero.**

Dónde debería ir cada cosa. Una fila por destino, no por documento: 316 filas no se firman,
nueve decisiones sí.

---

## 0 · Lo que NO se mueve, y no es negociable

| Qué | Dónde está | Por qué se queda quieto |
|---|---|---|
| `MD 3/HEXELION_LEGION_DEPIN_20260514.md` | `~/pre-bee/p0x/MD 3/` | **Contraseña de servicio en claro, wallets EVM y SOL operativas, cuenta POKT.** No entra en ningún repositorio, ni público ni privado. Si algún día se necesita su contenido, se extrae el texto útil a mano y el original se queda fuera de git |
| `hexelion_m2m_manifest_yaml__1_.txt` | ídem | Publica `hexelion.near` de **mainnet** con `no_human_required: true`. La propia auditoría de mayo ordenó retirarlo |
| `CV_David_Pecero.*`, `Fixed_Term_...pdf` | `~/pre-bee/David/`, `~/pre-bee/p0x/` | Personal, no de proyecto. No se han abierto y no se inventarían |
| Las claves del Faro | `~/pre-bee/hexelion/faro/keys/` | Solo hay `.pub` ahí. **Antes de tocar nada del Faro hay que localizar las privadas**, y esa búsqueda la dirige el carbono |

---

## 1 · Al Segundo Cerebro (`~/p0x/mente/`)

El Soberano apuntó que esto *«podría ser parte del second-brain»*. Estoy de acuerdo, con
una condición: **entra el destilado, no el archivo**. Volcar 316 documentos en `mente/`
convierte el Segundo Cerebro en el mismo montón, solo que versionado.

| Qué | Destino propuesto | Forma |
|---|---|---|
| El audit operativo de sesiones, las Cinco Leyes, la function-call key acotada, «cero claves en la embajada» | `mente/doctrina/` | **Redacción nueva de frontera**, no copia. Es el porqué que le falta a «jamás firmas valor» |
| El gradiente de privilegio (Zona Soberana / Zona de Aprovechamiento) | `mente/doctrina/` | Ídem |
| La membrana, con su prueba falsable, actualizada a Aurelius público | `mente/doctrina/` | Ídem. Renombrar Preceptor → Aurelius antes de escribir |
| La re-especificación de IronClaw (lección arquitectónica ≠ operativa) | `mente/doctrina/` | Ídem. Es el mejor razonamiento de seguridad del archivo |
| El flujo canónico de `hexelion.near` | `mente/doctrina/` | Ídem, bajo CANON-C |
| Los tres ejes del descarte y la métrica anti-teología | `mente/doctrina/` o `mente/necropolis/` | El criterio con el que se emiten los veredictos |
| El Rastro del Soberano | `mente/codice/` — **el Códice, que está vacío** | Sus cuatro capas dicen literalmente `(vacio)`. Este es el material que las llena |
| Los ~40 veredictos motivados del archivo | `mente/necropolis/` + siembra de Qdrant | Corpus de la Necrópolis Vectorial |

**Antes de escribir una sola línea en `mente/`, hay dos cosas que arreglar** (ver §5).

---

## 2 · A `aurelius-internal` (forja, privado)

| Qué | Destino |
|---|---|
| Los cuatro documentos de este equipo de lectura | `docs/archivo_2026-08/` — **ya están ahí** |
| Los 231 resúmenes de la pasada local, en JSON | `docs/archivo_2026-08/resumenes/` cuando cierre |
| El caso trabajado del «Triángulo de la Muerte» y demás trazas de razonamiento | `aurelius-lora/datos/` — **material de entrenamiento, no documentación**. Es CoT en la voz del sistema, escrito a mano, jamás usado |
| El expediente del Faro (qué hay, qué falta, dónde están las claves) | `docs/faro/` |
| El informe de peaq Paso 1, cuando se ejecute | `docs/faro/` |

---

## 3 · Al repositorio público (`aurelius`) — **nada por ahora**

Ni un documento de este archivo va al público sin pasar antes por la frontera. El archivo
está lleno de nombres de nodos, IPs, VLANs, MACs y estrategia comercial. Lo que sí puede
salir algún día es **producto derivado** del destilado —el lazo de comprensión de tres
ramas, por ejemplo— y eso se escribe de cero, no se copia.

---

## 4 · A la papelera — con motivo firmado

Solo lo que es basura demostrable, no lo que es viejo.

| Qué | Cuánto | Motivo |
|---|---|---|
| **18 copias byte a byte idénticas** | 18 ficheros | Medido por sha256. Se conserva una de cada grupo, la de la ruta más estable. El listado está en el scratchpad de la sesión y se anexará |
| **Copias truncadas** (`2026-05-29_Plan_Servicios_Datos.md` a 8192 B, `HEXELION_LEGION_DEPIN` a 8192 B, `HEXELION_VISION_CREATIVA` a 16384 B, todas en `pre-bee/p0x/` raíz) | 3+ ficheros | Cortadas a mitad de palabra por una copia fallida. El completo está en `MD 3/` |
| Artefactos de compilación y `site-packages` que la red del Localizador pescó | — | Nunca fueron material |

**Lo que NO se borra aunque lo parezca:** las **29 familias de versiones** (`v1 → v2 → v3`,
`BRIEFING → BRIEFING_v2`). Ahí es donde se ve cómo cambió de opinión, y esa información no
existe en ningún otro sitio. El archivo pesa 13,7 MB: no hay ningún motivo de espacio para
tocarlas.

---

## 5 · Dos reparaciones previas, en el repo vivo

Esto no es conserjería del archivo: es que **el destino está roto**. Si se escribe en
`mente/` antes de arreglarlo, se escribe sobre arena.

**5.1 · Dos symlinks rotos, versionados en git.**

```
~/p0x/mente/codice/CODICE_david.md -> /mnt/nvme/p0x/codice/CODICE_david.md
~/p0x/mente/tecnicas               -> /mnt/nvme/p0x/registro_tecnicas/tecnicas
```

`/mnt/nvme` no existe en este nodo — comprobado. El Códice real vive en
`~/p0x/codice/CODICE_david.md`. Propuesta: rehacer los enlaces a rutas relativas dentro del
repo, o sustituirlos por el fichero real. **Decisión del Soberano**, porque toca la
estructura del Segundo Cerebro.

**5.2 · El Códice miente sobre la máquina.**

Línea 40: *«Recursos reales (verificado 2026-06-27): la-fragua … qwen3:8b … la-torre …
qwen3:4b … proxy LiteLLM enruta · El Oráculo para lo pesado (a mano)»*. Es el «filtro de
realidad» del sistema y es **byte a byte idéntico** a la copia arqueológica de junio: nunca
se actualizó. Hoy el cómputo pesado vive en el Beelink con un 30B residente y 64 GB. Un
sistema que consulte ese Códice para decidir qué es viable **le dirá al Soberano que no
puede hacer lo que ya hace todos los días**.

Propuesta: actualizar la línea de recursos con lo medido, y fechar la actualización. Es
una línea, pero es la línea que gobierna qué se considera posible.

---

## 6 · Orden propuesto

1. **Reparar el destino** (§5). Sin esto, lo demás se escribe sobre arena.
2. **Firmar la papelera** (§4) — 21 ficheros, todos con motivo medido.
3. **Redactar la doctrina ausente** (§1). Frontera, no local: es escritura de canon.
4. **Poblar el Códice** con el Rastro. Local, bajo supervisión.
5. **Sembrar la Necrópolis Vectorial** con los veredictos. Local.
6. Solo entonces, mover ficheros.

Nada de esto ocurre sin firma. El equipo de lectura ha terminado su parte: **hay un mapa
donde había un montón.**
