# EL ICONO DEL TANK · lo hecho, lo que falta y por qué

**Fecha:** 2026-08-25, madrugada · **Estado:** arreglado lo que se puede arreglar sin el
Soberano delante. Queda un paso que **exige sudo** y otro que **exige una firma**.

---

## 1 · El diagnóstico, y no era el manifest

La orden suponía que el manifest no entregaba iconos válidos. **Los entregaba.** Medido
antes de tocar nada:

```
/manifest.json          HTTP 200 · application/manifest+json
/assets/icono-cyborg.png HTTP 200 · image/png · 111.968 B · PNG real 512x512
```

También estaban bien el service worker (`/sw.js`, HTTP 200, con manejador `fetch`) y su
registro (`dashboard.js:527`). Nada de la cadena declarada estaba roto.

**La captura del home dio el dato que faltaba:** el acceso directo se llama **«Aurelius»**,
no «PreceptorOS». Eso lo delata entero.

> Un acceso directo **no lee el manifest**. Usa el `<title>` de la página y su favicon.

Y la página **no tenía favicon**. Por eso Chrome generaba un cuadrado gris con una letra: el
famoso «1». El badge de Chrome en la esquina confirma lo mismo — es un *acceso directo*, no
una *app instalada*.

## 2 · Lo arreglado (commits `bc500fe` y `e362a83`, empujados)

| | |
|---|---|
| `<title>` en `app.html` y `dashboard.html` | «Aurelius» → **«PreceptorOS»**. El renombrado se había dejado los títulos |
| `rel="icon"` 192 y 512 + `apple-touch-icon` | No había ninguno. `apple-touch-icon` es el que Android prefiere para accesos directos |
| `assets/icono-192.png` | No existía. 192 es el mínimo que Android documenta |
| `assets/icono-512.png` | El anterior tenía las **esquinas transparentes** (alpha 0), y Android rellena eso de gris en un hueco `maskable`. El nuevo sale del avatar opaco sobre violeta, y lleva el contenido al **80 %** para que el recorte circular no le corte la cabeza al busto |

Los PNG los generó un guion **descartable** con PIL, fuera del árbol. El producto sigue sin
dependencias: el Guardián da 0 hallazgos. `VERDE 337/337`.

**Desviación declarada:** la orden decía `interface/icons/`. Van a `assets/` porque el
servidor sirve una lista blanca de ficheros de `interface/` más el prefijo `/assets/`;
`/icons/` no está en ninguna de las dos y **habría dado 404**.

## 3 · Lo que falta, y no lo puede hacer esta sesión

### 3.1 · Rehacer el acceso directo · **30 segundos, en el móvil**

El del home es el viejo: se creó antes del renombrado y con la página sin favicon. **No se
actualiza solo.**

1. Mantener pulsado el icono gris → **Quitar**.
2. `adb shell am start -a android.intent.action.VIEW -d 'http://100.81.82.34:8740'`
3. Chrome **⋮** → **Añadir a pantalla de inicio**.

Debe salir **«PreceptorOS»** con el busto. Si sale el busto: cerrado.

### 3.2 · «Instalar app» (WebAPK) · **bloqueado, y no por el icono**

La orden pedía **«Instalar app», no «añadir a inicio»**. Chrome solo ofrece instalar cuando el
origen es un **contexto seguro**: HTTPS o localhost. El Tank entra por
`http://100.81.82.34:8740` — HTTP plano contra una IP que no es localhost.

Sin contexto seguro, Chrome **no registra el service worker** (el `.catch(() => {})` de
`dashboard.js:528` se traga ese error en silencio, que es por lo que nadie lo vio) y **nunca
ofrece instalar**. Solo queda el acceso directo.

**La salida existe y es limpia:** `tailscale serve` da HTTPS con certificado real de Let's
Encrypt sobre `soberano.tailb9e0f7.ts.net` (MagicDNS confirmado activo). Eso convierte el
origen en seguro → el service worker registra → Chrome ofrece instalar → WebAPK con el icono
de verdad, sin badge.

Y **es más restrictivo que lo de ahora**, no menos: solo tailnet, con TLS, en vez del
`0.0.0.0` en claro que escucha también en la wifi local.

```bash
sudo tailscale serve --bg 8740
```

**Exige root.** Este nodo no tiene sudo no interactivo — está en el canon — así que la
sesión no puede. Es una línea, y va con su fila en `unidades.md`.

### 3.3 · El choque de D67 · **exige firma, no comando**

`test_cara` caso 1 exige que el léxico privado de la casa no aparezca en la cara, porque la
cara la lee cualquiera:

```python
LEXICO_PRIVADO = ("soberano", "preceptor", "ironclaw", "hexelion")
```

**«PreceptorOS» contiene «preceptor».** El renombrado creó ese choque y nadie lo había visto;
lo cazó la suite en el primer intento de poner el título nuevo en `cara.py`.

La palabra era privada cuando nombraba a **la IA de frontera**. Hoy es el **nombre público
del producto**, en la portada de GitHub. Las dos cosas no pueden ser ciertas a la vez.

- **Opción A:** afinar `LEXICO_PRIVADO` — lo privado era «el Preceptor» (el rol), no
  «PreceptorOS» (el producto).
- **Opción B:** dejar el título de `cara.html` como «Aurelius» para siempre, y aceptar que la
  cara offline lleva el nombre del personaje y la PWA el del producto.

**Hoy está en B**, porque cambiar `LEXICO_PRIVADO` es tocar doctrina y eso no se hace de paso
a las dos de la mañana. La suite queda verde en cualquiera de las dos.

---

## 4 · Resumen para el café

| | |
|---|---|
| ✅ | Iconos 192/512 opacos, con margen maskable, servidos y verificados |
| ✅ | Título «PreceptorOS» y favicon en la PWA · empujado |
| ⬜ | Rehacer el acceso directo en el Tank · **30 s, tú** |
| ⬜ | `sudo tailscale serve --bg 8740` para que Chrome ofrezca *instalar* · **una línea, tú** |
| ⬜ | Firmar A o B sobre «preceptor» en `LEXICO_PRIVADO` |
