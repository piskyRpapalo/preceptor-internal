---
id: matriz-auditoria-r02
titulo: Matriz de auditoría de software residual
tipo: operativo
clase: operativo
version: 1.0.0
dominio: barrido-residual
modo: NOCTURNO_SOLO_LECTURA
estado: PROPUESTA
actualizado: 2026-08-11
---

# MATRIZ DE AUDITORÍA · R02
### Barrido residual. Todo es propuesta. Cero ejecución.

**Modo nocturno respetado:** escritura únicamente en este fichero. Sin `git add/commit/push`, sin editar código productivo, sin tocar `.git/`, sin deploy, sin instalar, sin borrar, sin mover. Un solo dominio, una sola ronda.

---

## §0 · RESULTADO DE `sha256sum -c` (lo primero, como se pidió)

Comando: `cd Cuarentena && sha256sum -c salida/HASHES_R00.txt` · stderr visible (D16) · **EXIT=1**.

| Resultado | Cifra |
|---|---|
| Líneas en la base | 63 |
| `OK` | **60** |
| `FAILED` (contenido cambiado) | 2 |
| `FAILED open or read` (ausente) | 1 |
| Ficheros hoy en primer nivel | 62 |

Los tres que no pasan:

1. **`03_ESTADO_FIRMADO.md` — `FAILED`.** Causa identificada y **legítima**: incorporación de D11–D16. Es firma, no deriva.
2. **`Del Barrido al Borde Inteligente_ … Medallion.md` — ausente.** `find` en todo el árbol: cero resultados. No está en `necropolis/`. `git status` lo muestra como borrado sin confirmar. **Ninguna decisión D1–D16 declara este borrado.** Recuperable desde `bdf2595` (D13 funcionando). Es el fichero que R00 marcó `REVISAR_SOBERANO` y que D8 vincula al JWT quemado.
3. **`p0x-paper-manifest-v2.txt` — `FAILED`.** 13661 B, mtime `2026-08-11 01:22`, posterior al commit de R01. Contenido modificado **sin decisión que lo declare**.

### §0.1 · RECTIFICACIÓN: la línea base nunca estuvo rota. El error fue mío.

D11 dejó abierta la discrepancia «Cowork(9) vs test(5), no resuelta». Queda resuelta, y no a mi favor.

En R01 afirmé que `HASHES_R00.txt` era inservible para 9 ficheros por no entrecomillar nombres con espacios. **Esa conclusión era falsa.** `sha256sum -c` no parte el campo por el primer espacio: parte por el doble espacio que él mismo escribe. El formato era correcto desde el principio.

Prueba, ejecutada sobre la evidencia enterrada `necropolis/HASHES_R00_roto_evidencia.txt` (64 líneas): **60 `OK`, 4 problemas**, y los cuatro con causa conocida (`03` firmado, `Del Barrido` ausente, `paper-manifest-v2` modificado, `test_fuga` enterrado por D10). Cero fallos atribuibles al formato.

Lo que estaba roto era **mi método de verificación**: usé `awk '{print $2}'`, que sí trunca en el primer espacio, y atribuí al artefacto el defecto de mi herramienta. El fichero llamado `HASHES_R00_roto_evidencia.txt` no contiene una línea base rota; contiene la prueba de que funcionaba.

**Consecuencia:** la regeneración de la base fue inocua (ambas versiones son válidas) y la regla futura de D11 —re-ejecutar `sha256sum -c` antes de usar una base como autoridad— es **correcta**, pero por el motivo inverso al registrado: no protege contra bases mal escritas, protege contra auditores que verifican con la herramienta equivocada. Propongo que D11 se enmiende con esta causa real. Es una corrección de canon, y la firma es del Soberano.

---

## §1 · LOS 29 HALLAZGOS DE LA GUARDIA

**La lista literal de los 29 es `NO_DATA`:** no la observé; procede de una ejecución del Soberano de la que no hay artefacto en disco. Lo que sí hice es reproducir el comportamiento **actual** de la guardia, en modo `--files` (solo lectura, sin `git`).

Escaneo de los 62 ficheros de primer nivel de `Cuarentena/`: **0 hallazgos, EXIT=0, stderr vacío.**

Los 29 están silenciados por el bloque `DECISIONES_FIRMADAS` que R01 añadió a `guardia_higiene.py` (fichero hoy `M` en git status). La clasificación pedida —ruido ya firmado vs exposición real— tiene por tanto una respuesta incómoda: **no se puede separar, porque la exención no distingue.**

### §1.1 · CRÍTICO · la exención D8/D10 se aplica por línea, no por hallazgo

`es_permitido_por_canon(linea)` devuelve «permitido» si **cualquiera** de los patrones de D8/D10 aparece en la línea, **sea cual sea la regla que disparó**. D8 incluye `localhost`, `/home/pisky/`, `10\.\d+…`, `192\.168\.\d+…`, `tailscale`, `soberano\.`, `fragua:`.

Prueba determinista sobre un fichero sintético en `/tmp` (no se tocó el repositorio):

| Línea de prueba | Detectado |
|---|---|
| IP tailnet sola `<IP-DE-EJEMPLO>` | **sí** — `[IP-TAILNET]` |  # guardia:permitir IP-ejemplo-documentacion-regla-IP-TAILNET
| La misma IP tailnet + la palabra `localhost` | **NO** |
| Token de proveedor con forma viva `ghp_…` | **sí** — `[TOKEN-PROVEEDOR]` |
| El mismo token + `/home/pisky/p0x` en la línea | **NO** |
| Dominio privado `…​.ts.net` | **sí** — `[DOMINIO-PRIVADO]` |
| El mismo dominio + la palabra `tailscale` | **NO** |

**Un token de proveedor con forma de credencial viva pasa la guardia sin ser reportado si la línea menciona una ruta home.** Eso no es lo que D8 autorizó: D8 hizo visibles las IPs *para que Cowork pudiera proponer arquitectura*, no desactivó el detector de claves en los commits. Y choca con `04 §3.5` —«cero claves en nada publicable», regla que «manda sobre cualquier mejora»— y con `04 §3.7`: una comprobación que detecta y deja pasar no es comprobación, es decoración.

**BLOQUEADO.** El arreglo exige editar código productivo: prohibido en modo nocturno. No improviso el fix. La forma mínima que propongo, para que la firme o la rechace: la exención debe evaluarse **por regla**, no por línea — D8 exime a `IP-RFC1918`, `RUTA-HOME`, `DOMINIO-PRIVADO` y `NODO-*`; **nunca** a `TOKEN-PROVEEDOR` ni a `IP-TAILNET`.

### §1.2 · La exposición «0.0.0.0:8050» no se confirma

Se buscó en todo el árbol excluyendo `Cuarentena/` y `node_modules`:

- `0.0.0.0` aparece **dos veces, ambas en comentarios que prohíben ese bind**: `proxy/litellm_config.yaml:35` («Escucha en el tailnet, no en 0.0.0.0») y `deploy/soberano/cerebro-local-arranca.sh:43`. **No hay ningún bind a `0.0.0.0` en código.**
- `8050` aparece **solo en `mente/feedback/PENDIENTES.md`**, como backlog: pendiente #155 (servicio systemd `--user` para la cara de Aurelius), #160 (app Vite incompleta) y una nota de **crash-loop de `aurelius-interfaz` con ~29 953 reinicios** y un huérfano `servir_in…`.

**Veredicto: `NO_DATA` como exposición real.** La premisa de la misión no se sostiene en disco. Lo que sí hay es un servicio en crash-loop documentado y un puerto declarado en backlog — ninguna de las dos cosas es un bind abierto, y ninguna se verifica sin `curl`, que una ronda documental no hace (`04 §5`). **Coincidencia a descartar explícitamente:** los «~29 953 reinicios» y los «29 hallazgos» no tienen relación; no los mezclo.

---

## §2 · MATRIZ

Ninguna fila se ejecuta. `ELIMINAR` significa *propongo eliminar*, y su plan de reversión es la condición para que la propuesta sea legítima (`04 §6`).

| Componente | Acción | Justificación técnica | Coste / Beneficio (estimado) | Plan de reversión |
|---|---|---|---|---|
| `deploy/comun/hooks/guardia_higiene.py` — exención por línea (§1.1) | **REFACTORIZAR** | La exención se evalúa contra la línea completa e ignora qué regla disparó. Silencia `TOKEN-PROVEEDOR` cuando coincide un patrón de ruta. Viola `04 §3.5` y `04 §3.7` | Coste S: mapa `regla → decisión` y un caso de test por par. Beneficio alto: recupera el único freno de admisión verificado del proyecto | El fichero está versionado y hoy es `M`: `git checkout -- <ruta>` devuelve el estado del commit `bdf2595`. Los casos de test nuevos son aditivos |
| `Cuarentena/diez` | **ELIMINAR** | 0 bytes, vacío, versionado en `bdf2595`. Nombre sin semántica; compatible con un accidente de redirección de shell. No lo referencia ningún fichero | Coste S. Beneficio bajo pero real: un fichero vacío en la línea base obliga a explicarlo en cada ronda | Recuperable desde `bdf2595`. Al estar versionado, el borrado es reversible por historia |
| `Del Barrido al Borde … Medallion.md` (ausente) | **CONSERVAR** (restaurar) | Está en la línea base y en `bdf2595`, pero no en el árbol. Ninguna decisión declara su borrado. R00 lo marcó `REVISAR_SOBERANO` y D8 lo vincula al JWT quemado | Coste S. Beneficio: cierra un borrado no declarado, que es la clase de suceso que D13 existe para hacer reversible | Ya reversible: `git checkout bdf2595 -- <ruta>`. **No lo ejecuto**: restaurar es escribir fuera de `salida/` |
| `p0x-paper-manifest-v2.txt` (modificado sin declarar) | **REVISAR_SOBERANO** | Hash distinto del de la base; mtime posterior al commit de R01. No sé qué cambió ni quién | Coste S: un `git diff` del fichero lo resuelve | Contenido anterior recuperable desde `bdf2595` |
| `p0x-repositorios-tecnicas-unificado(1).txt` | **ELIMINAR** | `md5` idéntico byte a byte a `…unificado.txt` (`3faede4b704c`). Duplicado muerto, sin historia propia. `02 §7` lo clasifica como BASURA | Coste S. Beneficio: 33 623 B y una ambigüedad menos | Versionado en `bdf2595`; y el gemelo idéntico permanece en disco: pérdida de información nula por definición |
| `p0x-repositorios-tecnicas-qwen-v2 (1).txt` | **ELIMINAR** | `md5` idéntico a `…qwen-v2.txt` (`433e55754926`). Mismo caso | Coste S. Beneficio: 17 104 B | Ídem |
| `preceptor/__pycache__`, `deploy/comun/hooks/__pycache__` (2 `.pyc`) | **ELIMINAR** | Artefactos generados. Cubiertos por `.gitignore:9` y **no versionados**: no hay historia que perder | Coste S. Beneficio: higiene; se regeneran al importar | Ninguna reversión necesaria: Python los reconstruye. Es el único caso de la matriz con reversión trivial garantizada |
| `pipeline/out/bench_delta.json` (5685 B) | **REVISAR_SOBERANO** | `.gitignore:2` ignora `pipeline/out/`, **pero el fichero está VERSIONADO**: se comprometió antes de la regla, y `.gitignore` no destraquea lo ya seguido. La regla parece proteger y no protege | Coste S: `git rm --cached`. Beneficio: la intención declarada y el estado real coinciden | Al estar en historia, recuperable siempre. `git rm --cached` no borra del disco |
| `corpus/ingest_cGhI8tGY0Gw.log` (12 092 B) | **REVISAR_SOBERANO** | Log de ingesta **versionado**. `.gitignore` cubre `pipeline_build*.log` pero no este patrón. Un log en historia crece sin aportar historia real — el motivo que `.gitignore:23` da para excluir los `jsonl` | Coste S. Beneficio: coherencia con la política ya escrita para telemetría | Recuperable desde historia |
| `mente/telemetria/cerebro_local.jsonl`, `mente/necropolis/…/alfabeto.jsonl`, `…/runner.log` | **CONSERVAR** | No versionados y correctamente ignorados (`.gitignore:24`, `:30`). La política ya funciona aquí | Coste 0 | No aplica |
| Scripts: `bin/*` (4), `monje/genesis.py`, `preceptor/frontera.py`, `voz/*` (2), `pipeline/*.py` (5), `registro_tecnicas/models.py`, `skills/auditar-p0x/run_audit.sh` | **CONSERVAR** | **Cero huérfanos.** Los 15 tienen referencias externas (mínimo 1: `pipeline/bench_delta.py`; máximo 14: `bin/p0x-enqueue`). Ninguno cumple el criterio de código muerto | Coste 0. Se declara para que ninguna ronda futura los proponga sin evidencia | No aplica |
| Deps `psutil`, `requests`, `wasmtime` | **CONSERVAR** | Las tres se importan: `psutil` y `requests` en `monje/genesis.py`, `requests` también en `mente/pipeline/embed.py`, `wasmtime` en `preceptor/frontera.py`. **Ninguna dep declarada sin uso** | Coste 0 | No aplica |
| Configs `config/teaching_kernel.yaml`, `proxy/litellm_config.yaml`, `pipeline/delta_config.yaml` | **CONSERVAR** | Las tres referenciadas desde 3, 5 y 3 ficheros. **Ninguna config obsoleta**. `delta_config.yaml` lo lee código vivo (`pipeline/delta_engine.py`, `mente/pipeline/gen_niveles.py`) | Coste 0 | No aplica |
| `pipeline/` (raíz, 7) vs `mente/pipeline/` (9) | **REVISAR_SOBERANO** | Dos árboles distintos llamados `pipeline`. No son duplicados: contenidos disjuntos (delta/ingesta/observación vs chunk/embed/grafo/qdrant/voces). Pero `mente/pipeline/gen_niveles.py` lee `pipeline/delta_config.yaml`: hay acoplamiento cruzado entre los dos | Coste M: decidir una casa. Beneficio: quita la ambigüedad de «el pipeline» en cualquier futura misión | No aplica en esta ronda: no propongo mover nada |

---

## §3 · HALLAZGO, NO DECISIÓN · LA CASA DE LA DOCTRINA

`mente/doctrina/BLUEPRINT_DISENO_SOBERANO.md` · v1.2.0 · 271 líneas · `43e73ae74fb28d63`.

Estado por D12: borrador histórico sin autoridad, **no se mueve** hasta que una ronda decida la casa de la doctrina. Se respeta: no se toca, no se propone acción.

El hecho, expuesto y nada más: hoy el canon **visual** vive en la raíz (`BLUEPRINT_DISENO_SOBERANO.md`, v1.3.0, `cb767c464cc25631`), el canon **de sistema** vive también en la raíz (`BLUEPRINT_SISTEMA_P0X_v1.5.md`, 16 227 B, `8898524ed6e59458`, firmado por D15), y `mente/doctrina/` —el directorio cuyo nombre dice contener la doctrina— alberga la versión **más antigua y divergente** de las tres. Un agente futuro que busque doctrina por nombre de carpeta encontrará primero la equivocada. No es un riesgo de datos; es un riesgo de lectura, y esos se pagan en rondas.

## §4 · BLOQUEADO

- Arreglo de la exención de la guardia (§1.1) ← edición de código productivo, prohibida en modo nocturno.
- Restauración de `Del Barrido al Borde…` ← escritura fuera de `salida/`.
- Confirmación de qué cambió en `p0x-paper-manifest-v2.txt` ← `git diff` es solo lectura, pero la decisión de qué versión vale es del Soberano.
- Verificación del crash-loop de `aurelius-interfaz` y del puerto 8050 ← exige `systemctl`/`curl`: fuera del alcance de una ronda documental.
- Enmienda de D11 con la causa real (§0.1) ← firma del Soberano.

## §5 · NO_DATA

- Lista literal de los 29 hallazgos de la guardia: no observada, sin artefacto en disco.
- Motivo exacto de que el test de D11 contara 5 fallos y hoy la evidencia dé 4: el estado del árbol difería (`test_fuga.md`, `paper-manifest-v2`). No resuelto.
- Autor y contenido del cambio en `p0x-paper-manifest-v2.txt`.
- Quién borró `Del Barrido al Borde…` y por qué.
- Origen del fichero `diez`.
- Contenido de `deploy/fragua/`, `deploy/torre/`, `deploy/vigia/firmware/`, `deploy/soberano/openwebui/`: no leído en esta ronda.
- Estado real de cualquier servicio, puerto o proceso.

---

Pendiente de firma del Soberano para cierre de Ronda 2.

FIRMADO por el Soberano el 20260811: R2 cerrada.
