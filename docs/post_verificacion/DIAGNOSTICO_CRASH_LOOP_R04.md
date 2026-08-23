---
id: diagnostico-crash-loop-r04
titulo: Diagnóstico del crash-loop de aurelius-interfaz (D21)
tipo: operativo
clase: operativo
version: 1.0.0
dominio: operativa-crash-loop
modo: SOLO_LECTURA
estado: PROPUESTA
actualizado: 2026-08-11
---

# DIAGNÓSTICO · R04 · CRASH-LOOP `aurelius-interfaz` (D21)
### El crash-loop está cerrado desde el 2026-08-01. Lo que sigue abierto es otra cosa, y es peor.

---

## §0 · LOS DOS COMANDOS DE RUNTIME NO PRODUCEN DATO. NO_DATA, Y EL MOTIVO.

**`systemctl status aurelius-interfaz --no-pager`**
salida literal: `Unit aurelius-interfaz.service could not be found.`

**`journalctl -u aurelius-interfaz --no-pager -n 200`**
salida literal:
`Hint: You are currently not seeing messages from other users and the system.`
`No journal files were opened due to insufficient permissions.`

**Causa, verificada:** esta sesión no corre en `soberano`. `hostname` → `claude`; PID 1 → `bwrap` (sandbox). Del árbol del Soberano solo hay tres monturas: `p0x`, `outputs`, `uploads`. `/home/pisky/` **no existe** en este sistema de ficheros.

Por tanto: **cero evidencia de runtime. Ningún estado de servicio, ningún contador de reinicios, ninguna línea de journal se afirma en este documento.** Un agente documental no ve un servicio; ve el fichero que lo declara. Es un resultado válido, no un fracaso de la ronda.

Lo que sí es lectura legítima de disco, y es donde está el diagnóstico: la unit file y el registro documental.

## §1 · CAUSA RAÍZ · EVIDENCIA LITERAL

La causa raíz está escrita, con su prueba de cierre, en `mente/feedback/PENDIENTES.md` línea 423. Cita literal, íntegra:

> `- **aurelius-interfaz crash-loop** (~29 953 reinicios; huérfano \`servir_interfaz.py\` PID 690249 ocupaba :8050 → \`[Errno 98]\`) — prueba: huérfano matado, systemd rebindeó fresco (\`active\`), camino.html + /api/estado 200. *Endurecimiento del servicio → C4.*`

**Sección en la que vive esa línea:** `### 🟢 CERRADO (con la prueba que lo cierra)`, bajo `## 2026-08-01 · ESTADO CONSOLIDADO (tri-estado) — Ronda Secuencial · C0`.

Reconstrucción de la mecánica, con la unit file (`deploy/soberano/aurelius-interfaz.service`) delante:

1. Un proceso huérfano `servir_interfaz.py` (PID 690249) quedó vivo ocupando el puerto 8050 — probablemente un arranque manual anterior a la unidad, o un `stop` que no cosechó al hijo.
2. `systemd` arrancó su propia instancia. El `bind` falló con `[Errno 98] Address already in use`.
3. Salida distinta de cero → `Restart=on-failure` (línea 13) → espera `RestartSec=3` (línea 14) → reintento. El huérfano seguía ahí. Bucle.
4. **La unidad no declara `StartLimitBurst` ni `StartLimitIntervalSec`.** Sin límite de arranques, systemd no aplica el corte por defecto de `5 arranques / 10 s` que sí aplicaría con esas directivas presentes en la sección correcta. Nada frenó el bucle: de ahí que el contador llegara a ~29 953 y no a 5.
5. Cierre: se mató el huérfano, systemd rebindeó limpio (`active`), y se verificó la superficie que el humano abre — `camino.html` y `/api/estado` → 200. Eso es verificación en el sentido de `04 §5`, no una declaración de intención.

**Conclusión:** el crash-loop fue un síntoma de contención de puerto por un huérfano, ya resuelto y probado. **No es un fallo vivo.** Los ~29 953 reinicios son el registro histórico de un bucle que ya no gira.

**Causa estructural que sí permanece:** la unidad sigue sin límite de arranques. El huérfano concreto murió; la condición que convierte cualquier fallo de bind en un bucle ilimitado no se ha tocado. Esa es la parte de `*Endurecimiento del servicio → C4*` que quedó diferida.

### §1.1 · RECTIFICACIÓN 1 · D21 se registró sobre una lectura mía equivocada

En R02 cité «~29 953 reinicios según PENDIENTES.md» como *hallazgo operativo real*. D21 se firmó con esa frase. **Era una línea de la sección `🟢 CERRADO`**, con su prueba de cierre en la misma línea, y no la comprobé. Leí un registro de algo resuelto y lo reporté como algo pendiente.

D21 dice «Hallazgo operativo real. Ronda dedicada futura». La primera mitad es falsa; la segunda produjo esta ronda. Propongo cerrar D21 declarando que se resolvió el 2026-08-01, antes de registrarse.

### §1.2 · RECTIFICACIÓN 2 · la exposición `0.0.0.0:8050` EXISTE. Mi R02 la descartó por un grep corto.

`deploy/soberano/aurelius-interfaz.service`, línea 12, literal:

> `ExecStart=/usr/bin/python3 /home/pisky/aurelius/scripts/servir_interfaz.py --host 0.0.0.0 --puerto 8050`

En R02 §1.2 escribí: *«No hay ningún bind a `0.0.0.0` en código»* y *«`8050` aparece solo en `mente/feedback/PENDIENTES.md`, como backlog»*. Ambas frases son **falsas**. El motivo es mi método: el grep llevaba `--include='*.py' --include='*.yaml' --include='*.yml' --include='*.sh' --include='*.json'` y `--include='*.md'`. **No incluí `*.service`.** Un servicio no se declara en ninguna de esas extensiones. Busqué donde no estaba y concluí que no existía.

Consecuencia de canon: **D19 está firmada sobre una premisa falsa.** Dice *«guardia:permitir 0.0.0.0:8050 en p0x-paper-manifest-v2.txt fue innecesaria (no habia exposicion)»*. Sí había exposición. Si la excepción era innecesaria o no es discutible por otros motivos, pero no por ese. D19 necesita enmienda con la causa real, igual que D11 en R02.

**Y el fondo del asunto:** el servicio escucha en todas las interfaces, no solo en el tailnet. Eso contradice frontalmente la banda de higiene que el propio árbol repite en cuatro sitios distintos — `proxy/litellm_config.yaml:35` («Escucha en el tailnet, no en 0.0.0.0»), `deploy/soberano/cerebro-local-arranca.sh:43`, `deploy/soberano/OPENWEBUI.md:18` y `:26` (donde `ss -tlnp` confirma un único socket en `…:8080`, no en `0.0.0.0`). Todos los demás servicios se bindean a la IP del tailnet. Este no. La descripción de la propia unidad dice «interfaz estatica :8050, **tailnet**» — la intención declarada y el `ExecStart` no coinciden.

Esto es un hallazgo de seguridad real, y es el único ítem verdaderamente abierto de esta ronda. No lo toco: `PROHIBIDO editar servicios`.

## §2 · MATRIZ

| Componente | Acción | Justificación técnica | Coste / Beneficio (estimado) | Plan de reversión |
|---|---|---|---|---|
| `deploy/soberano/aurelius-interfaz.service` línea 12 — `--host 0.0.0.0` | **REFACTORIZAR** | El servicio escucha en todas las interfaces (LAN incluida) cuando su propia `Description` dice «tailnet». Rompe la banda que el resto del árbol respeta (`litellm_config.yaml:35`, `OPENWEBUI.md:18`). Un `0.0.0.0` en un nodo con LAN y tailnet expone la cara a la LAN sin decirlo | Coste S: sustituir por la IP del tailnet, como ya hace `open-webui`. Beneficio alto: cierra exposición real y alinea intención con efecto | La unidad está versionada: `git checkout -- deploy/soberano/aurelius-interfaz.service`. Tras reinstalar, `systemctl --user daemon-reload` + restart. Prueba de reversión: `ss -tlnp \| grep 8050` debe mostrar un único socket |
| Misma unidad — ausencia de `StartLimitBurst` / `StartLimitIntervalSec` | **REFACTORIZAR** | `Restart=on-failure` + `RestartSec=3` sin límite de arranques convierte cualquier fallo de bind en un bucle ilimitado. Es la causa estructural de que el contador llegara a ~29 953 en vez de detenerse. Un servicio que reintenta 30 000 veces no está reintentando: está ocultando un fallo que nadie ve | Coste S: dos directivas en `[Unit]` (`StartLimitIntervalSec=60`, `StartLimitBurst=5`). Beneficio: el fallo se vuelve visible en `systemctl status` en vez de disolverse en el journal | Quitar las dos líneas y `daemon-reload`. Reversión sin estado |
| `Documentation=file:///home/pisky/aurelius/scripts/servir_interfaz.py` (línea 3) | **CONSERVAR** | Apunta correctamente al script real. No es una ruta a documentación, sino al código — poco ortodoxo pero honesto y útil. No genera fallo | Coste 0 | No aplica |
| `WorkingDirectory` + ruta absoluta a `/usr/bin/python3` (líneas 9, 12) y su comentario (10-11) | **CONSERVAR** | Correcto y bien razonado: el `PATH` de systemd no ve `~/.local/bin`, y el comentario lo declara. El script usa solo stdlib. Esto ya evitó un fallo | Coste 0 | No aplica |
| Manejo de `SIGTERM` declarado en el comentario (línea 15) | **CONSERVAR** | Cierre limpio vía `KeyboardInterrupt` → `stop` ordenado. Es lo que evita generar nuevos huérfanos por `stop`. Sin verificar en runtime: `NO_DATA` | Coste 0 | No aplica |
| Huérfano `servir_interfaz.py` PID 690249 | **CONSERVAR** (nada que hacer) | Ya resuelto el 2026-08-01 con prueba en la misma línea de `PENDIENTES.md`. Un PID de hace diez días no es un objeto sobre el que actuar | Coste 0 | No aplica |
| `/home/pisky/aurelius/scripts/servir_interfaz.py` | **NO_DATA** | Vive fuera de `p0x/` y fuera de mi alcance de lectura. No está en el repo: `find -iname 'servir_interfaz*'` en `p0x` → cero resultados. No puedo auditar si el `--host` se respeta, si valida el argumento, ni cómo cierra | No estimable | No aplica |
| D21 (la decisión) | **REFACTORIZAR** (enmendar) | Se firmó describiendo como «hallazgo operativo real» algo que estaba en la sección `🟢 CERRADO` desde el 2026-08-01. Ver §1.1 | Coste S: dos líneas de enmienda | La versión anterior queda en la historia de `03_ESTADO_FIRMADO.md` |
| D19 (la decisión) | **REFACTORIZAR** (enmendar) | Su justificación —«no habia exposicion»— es falsa. Ver §1.2 | Coste S | Ídem |

## §3 · DECIDE

**¿Se cierra D21 como resuelto el 2026-08-01 (con la prueba de `PENDIENTES.md` línea 423) y se abre en su lugar un ítem propio para el endurecimiento de la unidad — bind al tailnet en vez de `0.0.0.0`, más límite de arranques — que es lo único que sigue abierto y es un hallazgo de seguridad, no un crash-loop?**

## §4 · NO_DATA

- Estado actual del servicio, número real de reinicios hoy, contenido del journal: **NO_DATA**. No hay systemd de `soberano` en esta sesión.
- Contenido de `servir_interfaz.py`: **NO_DATA**. Fuera de `p0x/`.
- Si el bind a `0.0.0.0` está hoy activo o si el servicio está parado: **NO_DATA**. Solo consta lo que declara la unidad.
- Si la LAN del nodo está expuesta de hecho: **NO_DATA**. Exige `ss -tlnp` en la máquina, que es runtime.
- Qué es «C4» y si esa ronda existe o está planificada: **NO_DATA**.
- Si el huérfano se originó por arranque manual o por `stop` incompleto: **NO_DATA**. `PENDIENTES.md` no lo dice y no se conjetura.
- Fecha real: el entorno declara 2026-08-11; el reloj del sandbox, 2026-08-10. Sin resolver, ya declarada en R00.

---

Pendiente de firma del Soberano para cierre de Ronda 4.

FIRMADO por el Soberano el 20260811: R4 cerrada.
