# ACCESO REMOTO A LA PWA POR TAILSCALE

**Verificado el 2026-08-25** en `soberano` (Beelink) → `tank-3` (Android 15).
**Repo privado a propósito:** el override es configuración de máquina y no va al repositorio
público. Lo que se versiona es el **procedimiento**, para poder repetirlo en otro nodo sin
reconstruirlo de memoria.

---

## 1 · Por qué esto NO toca el repositorio

`bin/preceptoros-pwa` decide dónde escucha así:

```python
BIND = os.environ.get("PRECEPTOROS_PWA_BIND") or os.environ.get("AURELIUS_PWA_BIND", "127.0.0.1")
```

Por defecto, **loopback**. Se abre por variable de entorno, nunca por un valor escrito en el
repositorio — porque un producto que trae `0.0.0.0` de fábrica expone la memoria de quien lo
instale sin que esa persona haya decidido nada.

El diseño ya lo permitía. **No se cambió una línea del árbol para conseguir esto.**

Y el propio código lo dice al arrancar fuera de loopback:

> `[pwa] AVISO: no estás en loopback. Esto escucha fuera de esta máquina, y eso es una
> decisión, no un descuido.`

Ese aviso no es decorativo: es la frase que separa «lo abrí» de «se abrió solo».

---

## 2 · El override, exacto

```bash
mkdir -p ~/.config/systemd/user/aurelius.service.d
cat > ~/.config/systemd/user/aurelius.service.d/bind-tailscale.conf <<'EOF'
[Service]
Environment="PRECEPTOROS_PWA_BIND=0.0.0.0"
EOF
systemctl --user daemon-reload
systemctl --user restart aurelius.service
```

Un fichero en `*.service.d/` **no reemplaza la unidad**: la extiende. La unidad versionada en
`deploy/soberano/aurelius.service` sigue intacta, y quitar el acceso remoto es borrar este
fichero y recargar. Editar la unidad directamente habría mezclado configuración de máquina con
un artefacto de despliegue que se copia a otros nodos.

**Se usa el nombre nuevo de la variable** (`PRECEPTOROS_*`). El viejo (`AURELIUS_PWA_BIND`)
también funciona hasta el **2026-11-23** por el puente de `entorno.py`, pero escribir hoy el
nombre que muere en noviembre es dejarse una trampa puesta.

---

## 3 · `0.0.0.0` vs la IP de Tailscale · la diferencia importa

| | escucha en | quién llega | cuándo usarlo |
|---|---|---|---|
| `0.0.0.0` | **todas** las interfaces | Tailscale **y la red local** (wifi de casa, del bar, del hotel) | Cuando también quieres abrirlo desde la LAN |
| `100.81.82.34` (la IP tailnet) | solo la interfaz de Tailscale | **solo** dispositivos de tu tailnet | Más restrictivo. **Es el que corresponde si lo único que quieres es el móvil por Tailscale** |

Hoy está en `0.0.0.0`, que es **más abierto de lo que el objetivo pedía**. En una wifi de
confianza da igual; en una ajena, cualquiera del mismo segmento puede pedir
`http://<tu-ip>:8740` y leer la memoria — no hay contraseña delante.

Para cerrarlo a solo-tailnet:

```bash
sed -i 's/0\.0\.0\.0/100.81.82.34/' ~/.config/systemd/user/aurelius.service.d/bind-tailscale.conf
systemctl --user daemon-reload && systemctl --user restart aurelius.service
```

**Pega**: si la IP de la tailnet cambiara, el servicio no arrancaría — falla ruidoso, que es
el lado bueno del fallo. `0.0.0.0` nunca falla, y por eso nunca avisa.

---

## 4 · Instalar la PWA en Android

1. Con el móvil en la misma tailnet, abrir en **Chrome**: `http://100.81.82.34:8740`
2. Menú **⋮** → **Añadir a pantalla de inicio** / **Instalar aplicación**.
3. Queda como icono propio, sin barra de navegador.

Se instala como **PreceptorOS** (así lo declara `interface/manifest.json` desde el
renombrado). El sprite sigue siendo Aurelius: **el producto es PreceptorOS, el personaje es
Aurelius**, y eso no es una inconsistencia — es la doctrina.

**Fuera de casa** funciona por los DERP de Tailscale sin abrir un solo puerto en el router.
Eso es el objetivo entero: acceso remoto **sin** exponer nada a internet.

---

## 5 · Verificación

```bash
ss -tlnp | grep 8740
```

Debe decir `0.0.0.0:8740` (o `100.81.82.34:8740` si se cerró a tailnet). Si dice
`127.0.0.1:8740`, el override no se aplicó — casi siempre falta el `daemon-reload`.

```bash
systemctl --user show aurelius.service -p Environment --value
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8740/api/estado
```

Desde otra máquina de la tailnet:

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://100.81.82.34:8740/api/estado
```

Y en el móvil por `adb`, sin tocar la pantalla:

```bash
adb shell am start -a android.intent.action.VIEW -d http://100.81.82.34:8740
```

Medido el 2026-08-25: `LISTEN 0 5 0.0.0.0:8740` · servicio `active` · `tank-3` en la tailnet
con tráfico.

---

## 6 · Cómo se apaga

```bash
rm ~/.config/systemd/user/aurelius.service.d/bind-tailscale.conf
systemctl --user daemon-reload && systemctl --user restart aurelius.service
```

Vuelve a loopback. **No queda nada que recordar apagar**: el estado por defecto del producto es
el cerrado, y esto era una capa encima.

---

## 7 · Lo que este acceso NO trae, y hay que saberlo

- **No hay autenticación.** Quien alcance el puerto lee la memoria. La única puerta es la
  tailnet: la seguridad la da Tailscale, no la PWA.
- **No hay TLS.** Va en claro. Dentro de la tailnet el cifrado lo pone WireGuard; **en la LAN
  con `0.0.0.0`, no lo pone nadie**.
- **No sobrevive a un reinicio del móvil como servicio**: la PWA es un cliente. El que tiene
  que estar vivo es el Beelink, y ahí sí está `enabled`.
