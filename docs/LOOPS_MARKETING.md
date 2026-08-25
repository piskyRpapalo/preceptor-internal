# LOOPS DE MARKETING · propuesta, no construcción

**Fecha:** 2026-08-25 · **Estado:** PROPUESTA. **No se ha construido nada.**
**Origen:** el otro arquitecto. **Encargo del Soberano:** documentarlos, no construirlos.

> Los tres preparan. El carbono firma. Ninguno publica.

---

## 0 · La regla de los tres, y por qué no es opcional

- **Cero nube.** El 27B local hace el trabajo. Nada sale del nodo hasta que el Soberano lo
  pega él mismo, a mano.
- **Human-in-the-loop.** Escriben a `~/marketing/borradores/`. Ninguno tiene credencial de
  ninguna red, ni la puede tener.
- **El carbono firma.** Un bucle que publica solo es un bucle que puede publicar cualquier
  cosa a las cuatro de la mañana, y el primero en enterarse será un desconocido.

Esto último no es prudencia: es la misma familia que *«jamás firmas valor»*. Publicar en tu
nombre es firmar en tu nombre.

---

## 1 · El Heraldo · git log → hilos técnicos

**Qué hace.** Lee `git log` de la semana, elige lo que tiene una cifra medida detrás, y
redacta borradores. A `~/marketing/borradores/AAAA-MM-DD-<tema>.md`.

**Por qué es el primero.** Es el único cuya materia prima **ya existe y ya está medida**. Los
mensajes de commit de este repositorio llevan las cifras y el porqué dentro; el Heraldo no
inventa contenido, lo reformatea. Un bucle que reformatea se puede juzgar; uno que inventa,
no.

**Ejemplo, con material real de esta semana:**

> «67 tok/s de prompt en una 780M. El binario que teníamos en el PATH no traía backend
> Vulkan — `--list-devices` decía `(none)` — y el `-ngl 999` del lanzador era un no-op
> silencioso. El Vulkan ya estaba en el disco, sin usar. ×2,95 en prompt por cambiar de
> binario, no de hardware.»

**Lo que hay que vigilar.** La tentación de que el Heraldo *adorne*. Regla propuesta: **no
puede escribir una cifra que no esté en un commit o en un fichero de `docs/`**. Comprobable
con una prueba, como el Guardián comprueba los imports.

**Clase:** MEDIO. **Cadencia:** semanal, después del Cronista.

---

## 2 · La Vitrina · jobs de CineK → piezas de marca

**Qué hace.** De un job terminado saca tres piezas: miniatura 1:1, banner 16:9, fondo 9:16. A
`~/marketing/out/`.

⚠️ **Bloqueado por decisión vigente: CineK está cancelado hasta nueva orden.** Sin jobs no
hay materia prima. Queda escrito para cuando se reabra.

**Lo que habrá que resolver entonces:** esto no es texto, es imagen. `laminas/recortar.py` es
hoy el único fichero del árbol que importa algo fuera de la stdlib (PIL). Un bucle de imagen
**añade dependencias al nodo**, y eso es una decisión aparte con su fila en el registro.

**Clase:** PESADO.

---

## 3 · El Sembrador · RSS → borradores de respuesta

**Qué hace.** Lee RSS de HN y r/LocalLLaMA, encuentra hilos donde lo que se ha medido aquí
responde algo, y deja borradores en `~/marketing/respuestas/`.

🔴 **Es el único de los tres que toca la red, y por eso es el último.**

Los otros dos leen del disco. Este trae texto de fuera y se lo da al modelo local. Eso abre
una puerta que ninguno de los bucles construidos tiene:

- **Inyección por contenido ajeno.** Un post puede contener instrucciones dirigidas al modelo.
  Si el Sembrador se las pasa sin marco, está ejecutando texto de un desconocido. La defensa
  es tratar el RSS como **dato, nunca como instrucción**, y el prompt del modelo tiene que
  decirlo explícitamente.
- **Una petición HTTP es una huella.** Pedir un RSS dice a alguien que este nodo está mirando.
  Menor, pero real, y hay que decirlo antes y no después.

**Propuesta:** no se construye hasta que el Heraldo lleve un mes funcionando. El Heraldo es
inofensivo por construcción —solo lee lo que ya escribimos—; el Sembrador no.

**Clase:** MEDIO. **Cadencia:** diaria.

---

## 4 · Orden propuesto, y por qué

| # | Bucle | Cuándo | Motivo |
|---|---|---|---|
| 1 | **El Heraldo** | Cuando se firme | Materia prima medida y en casa. Riesgo mínimo |
| 2 | El Sembrador | Tras un mes del Heraldo | Trae texto de fuera: hay que ver primero que el patrón funciona con material propio |
| 3 | La Vitrina | Si CineK se reabre | Bloqueado, y añadiría dependencias de imagen |

**El Heraldo no necesita al Cronista.** La propuesta original decía «Cronista lee git log →
Escriba genera hilos». Son dos bucles donde basta uno: `git log` lo lee cualquiera. Partirlo
en dos añade un traspaso, un formato intermedio y un sitio más donde romperse — a cambio de
nada, porque no hay otro consumidor de lo que produciría el Cronista.

---

## 5 · Lo que estos tres comparten con los ya construidos

Los cinco bucles que ya corren (`director`, `s0`, `guardian`, `afinador`, `curador`) tienen la
misma forma, y estos tres deberían heredarla entera:

- **Latido siempre**, pase lo que pase, con recuento en la nota. Sin eso, S0 no puede
  sospechar de ellos.
- **Propone, no ejecuta.** Escriben a una carpeta; no publican.
- **Cero no es limpio.** «0 borradores esta semana» tiene que distinguir *no hubo commits con
  cifras* de *no miré*.
- **El modelo, por `cerebro.py`**, con `--reasoning off` y la escalada por coste delante.

---

## 6 · Para la firma

| # | Qué se firma | |
|---|---|---|
| M1 | Los tres **preparan y no publican**, nunca, ni con credencial disponible | ⬜ |
| M2 | El Heraldo primero, y solo el Heraldo, hasta que lleve un mes | ⬜ |
| M3 | El Heraldo **no puede escribir una cifra** que no esté en un commit o en `docs/`, y hay prueba que lo comprueba | ⬜ |
| M4 | El Sembrador trata el texto de fuera como **dato, jamás como instrucción** | ⬜ |
| M5 | La Vitrina espera a CineK, y sus dependencias de imagen son firma aparte | ⬜ |

**No se construye ninguno hasta que M1–M3 estén firmadas.**
