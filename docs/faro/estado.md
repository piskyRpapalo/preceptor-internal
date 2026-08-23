# EL FARO · ESTADO REAL

**Fecha:** 2026-08-23 · **Verificado por consulta directa a `la-fragua`, en solo lectura.**
**Decide:** el Soberano.

---

## 0 · Corrección de lo que escribí ayer

En la `CLASIFICACION` dije que El Faro estaba *«apagado desde julio»*. **Era falso.** Lo
dije mirando la copia congelada de `~/pre-bee/hexelion/faro/`, que es un *snapshot* del 18
de julio, y no consulté el nodo donde el canon dice que vive.

**El Faro lleva cuatro días corriendo sin interrupción.** Y la pregunta que el Soberano puso
como bloqueante —«nada se da por vivo hasta resolver las claves»— tiene respuesta:
**las claves privadas existen y están donde deben estar.**

---

## 1 · Lo que hay, medido

**Nodo:** `la-fragua` (100.82.94.83, usuario `ubuntu`) · ruta `~/hexelion/faro/`

```
● hexelion-faro.service — HEXELION El Faro v0.1 — M2M public surface :8100
     Loaded: loaded (/etc/systemd/system/hexelion-faro.service; enabled)
     Active: active (running) since Tue 2026-08-18 06:03:07 UTC; 4 days ago
   Main PID: 5734 (uvicorn)     Memory: 60.3M     CPU: 8min 51s
```

### Las claves — la pregunta que bloqueaba todo

```
-rw-------  45  anchor_fc.key          ← privada de anclaje
-rw-rw-r-- 152  anchor_fc.pub
-rw-------  45  attest_ed25519.key     ← privada de atestación
-rw-rw-r-- 107  attest_ed25519.pub
```

Existen, están en `la-fragua`, y tienen permisos **0600**. Se listaron; **no se leyeron, no
se copiaron y no se tocaron.**

La copia de `~/pre-bee/` solo tiene los `.pub`, y eso **no es una pérdida: es el
comportamiento correcto.** Una copia de trabajo del código no debe llevar las privadas.
Lo que faltaba no era la clave: era mirar el nodo correcto.

### Que firma de verdad

```
GET /selftest
{"ok":true, "sha256":"4e489900…", "signing_method":"sha256+ed25519",
 "ed25519_signature":"rGjwGwtsvOn0eEDdL6j0b2KdbhxTmPRFnwFxlm5wHHRlpPCaZU…"}
```

No es una maqueta: produce una firma ed25519 real contra el material que tiene cargado.

### Estado declarado

```
GET /health
{"service":"el-faro","status":"ok","mode":"DRY_RUN","network":"testnet",
 "node":"hexelion-beato-01","redis":true,"ed25519_configured":true}
```

**Modo DRY_RUN sobre testnet.** Exactamente donde la Doctrina del Silencio manda que esté.

### Superficie pública

`/health` · `/selftest` · `/manifest` · `/price` · `/ships/live` · `/ships/attested` ·
`/v1/attested` · `/v1/credits/claim` · `/.well-known/hexelion-attestation.json`

Y el documento de atestación pública dice, literalmente:

> `"note": "attestation of reception; not proof of physical reality"`

**La corrección de vocabulario que el Soberano se hizo a sí mismo en mayo de 2026 está
implementada en el servicio y sirviéndose hoy.** No se quedó en el pitch.

### Servicios hermanos, vivos en la-fragua

`ais-catcher.service` (captura AIS por RTL-SDR) · `aisstream-consumer.service` (el
comparador público para verificación cruzada) · `dump1090.service` (ADS-B) ·
`consumo-logger.service`.

---

## 2 · Lo que NO está

| Qué | Estado |
|---|---|
| **El servidor MCP en `:8200`** | **No responde.** Solo existe `hexelion-faro.service`; no hay unidad de systemd para el MCP. El código está (`faro_mcp.py`, 26 kB, con `test_faro_mcp.py`) y su informe de ejecución también. Está escrito y desplegado a medias |
| **El Escudo RF** (`rf_plausibility`) | Confirmado ausente del payload, como decía la clasificación |
| **peaq** | Nada. Es lo que el Paso 1 está explorando esta noche |

---

## 3 · Una incoherencia de identidad que conviene mirar

El documento de atestación pública declara:

```json
{"node": "hexelion.near", ...}
```

…mientras `/price` declara `"receiver": "hexelion.testnet"` y `/health` dice
`"network":"testnet"`.

Es decir: **el servicio se anuncia al mundo con el nombre de la cuenta de mainnet mientras
opera en testnet.** No es una vulnerabilidad —no hay clave de mainnet en juego, y el modo es
DRY_RUN— pero sí es la misma clase de cosa que la auditoría de mayo llamó «los dos
HEXELION»: dos verdades sobre el mismo dato. Y `hexelion.near` es precisamente la cuenta que
el manifiesto M2M retirado publicaba como identidad de máquina.

**Propuesta:** que el `node` del `.well-known` refleje la red en la que se está operando. Es
un campo, y es de una línea. No lo he tocado.

---

## 4 · Las tres opciones, con su coste

La pregunta ya no es «¿aparecen las claves?». Es **qué hacer con un Faro que lleva cuatro
días vivo y del que nadie se acordaba.**

### Opción A · Encenderlo del todo

Levantar el MCP en `:8200` como unidad de systemd, enchufarlo como conector, y cerrar la
incoherencia de identidad del §3.

- **Coste:** una unidad de systemd + una línea de configuración. Horas, no días.
- **A favor:** hoy hay cliente MCP nativo, que en mayo no existía. Es la diferencia entre
  un servicio que existe y un servicio que se usa.
- **En contra:** una unidad nueva de systemd exige aprobación explícita — es justo la regla
  de higiene que el archivo tiene escrita y que nunca llegó al repositorio.

### Opción B · Dejarlo como está, y documentarlo

No tocar nada. Escribir dónde vive, qué sirve y quién lo mantiene.

- **Coste:** cero.
- **A favor:** lleva cuatro días sin caerse. Funciona.
- **En contra:** un servicio del que nadie se acuerda es un servicio que nadie parchea. Y
  expone `0.0.0.0:8100`.

### Opción C · `@sleeping`

Parar el servicio, marcarlo dormido con motivo y condición de despertar, y conservar
claves, pruebas y ledger.

- **Coste:** minutos.
- **A favor:** coherente con Hexelion reducido a mueble. Menos superficie viva.
- **En contra:** **es la única pieza del pitch antiguo que llegó viva a hoy**, y apagarla
  cierra la puerta de la economía máquina-a-máquina justo la noche en que se está
  explorando peaq.

**Mi recomendación, para lo que valga:** **A, recortada.** Cerrar la incoherencia de
identidad (una línea) y decidir el MCP por separado. Lo que no haría es C: apagar hoy lo
único que funciona, mientras se estudia cómo extenderlo, sería enterrar la respuesta antes
de leer la pregunta.

---

## 5 · Qué NO se ha hecho

No se ha tocado `la-fragua`: solo lecturas (`systemctl status`, `ls`, `curl` a `127.0.0.1`).
No se ha leído ni copiado ninguna clave. No se ha creado, parado ni modificado ningún
servicio. No se ha escrito nada en cadena.

Es propose-only hacia otro nodo, como manda el canon.
