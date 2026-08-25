# LA FRONTERA D68 · dónde puede haber un servidor y dónde no

**Fecha:** 2026-08-25 · **Estado:** PROPUESTA. Firma el Soberano.
**Motivo:** antes de que exista `llama-server` en `:8080`, no después.

> Una regla escrita después del hecho no es una regla: es una justificación.

---

## 1 · La regla que ya existe

Está en el código del producto, en `conversacion.motor_llama`:

> *«Proceso hijo por entrada y salida estándar. **Ni un socket: un puerto local es
> indistinguible de un túnel**, y esa es la razón por la que el gerente no puede ser un
> servidor (D68).»*

El razonamiento, entero: desde fuera de la máquina, un proceso que escucha en `127.0.0.1` y
uno que escucha hacia internet **se parecen**. La diferencia la sostiene una configuración que
alguien puede cambiar sin querer — como se cambió esta misma noche, con una línea, para la
PWA. Que fuera deliberado no quita que fuera **una línea**.

Por eso el motor del producto no es un servidor: es un proceso hijo por `stdin`/`stdout`, que
no tiene puerto que abrir aunque alguien se equivoque.

---

## 2 · Lo que D68 gobierna, y lo que no

D68 se escribió para **el producto**. Aplicarla al rack entero sería leerla de más; ignorarla
en el rack sería leerla de menos. La frontera:

| | ¿puede ser servidor? | por qué |
|---|---|---|
| **PreceptorOS** — el motor de conversación, la memoria, la frontera | **NO. Nunca.** | Es la promesa del producto. Quien lo instale no debe tener un puerto abierto que no pidió |
| **La cara (PWA)** de PreceptorOS | **Sí, y ya lo es** — pero **en loopback por defecto**, y se abre solo por variable de entorno, con aviso impreso | La excepción existe desde antes y está diseñada: el valor por defecto es el cerrado |
| **Los bucles del lab** (L1/L2/L3) | **Sí**, si el Soberano lo firma | Son infraestructura de su rack, no producto que nadie instale |
| **CineK y herramientas del nodo** | **Sí** | Ídem |

---

## 3 · Las tres condiciones si se levanta `llama-server`

Si se firma, va con estas tres puestas. Sin ellas, no.

### 3.1 · PreceptorOS no lo usa. Nunca.

**Esta es la condición que importa.** El día que exista un `llama-server` en `:8080`, la
tentación de que `conversacion.py` le pegue por HTTP —y ahorrarse el arranque del modelo en
cada turno— será enorme. Y sería el final de D68: el producto dependería de un servidor.

Se propone que sea **imposible por prueba, no por disciplina**. Ya existe el molde: la suite
`test_path` comprueba sobre el árbol de sintaxis que `path.py` no importa red, y
`test_cerebro` hace lo mismo con el cerebro de los bucles. Una prueba equivalente en el
público:

```python
def test_el_producto_no_habla_por_red(self):
    """D68. Si esto se pone rojo, alguien conectó el producto a un servidor."""
    for modulo in ("conversacion.py", "memory.py", "preceptoros.py", "fuga.py"):
        # ningún import de socket/http/urllib/requests, ni directo ni indirecto
```

Con eso, romper D68 deja de ser una decisión de madrugada y pasa a ser un rojo en la tanda.

### 3.2 · Loopback, y el `0.0.0.0` cuesta una firma aparte

`--host 127.0.0.1`. Abrirlo a la tailnet es **otra** decisión, con su fila en
`unidades.md`, como la tuvo la PWA esta noche.

### 3.3 · El contrato de recursos se reescribe antes, no después

La arquitectura de bucles reparte por clases: `MEDIO` se pospone si `load > 2`, `PESADO` corre
de 01:00 a 06:00 con cerrojo, uno cada vez. **Todo eso supone que el modelo se carga y se
suelta.**

Un `llama-server` residente retiene **16 GB permanentemente** y rompe ese contrato: ya no hay
«uno cada vez», hay uno siempre. Con la GPU asignando 32,8 GiB compartidos con la RAM del
sistema, y **con el cuelgue de anoche todavía fresco**, eso no es un detalle de configuración.

Si se levanta, `ARQ_LOOPS.md` necesita una clase nueva —«RESIDENTE»— con su presupuesto
escrito, antes de que el primer bucle la use.

---

## 4 · Lo que se gana, para que la decisión sea justa

No es una propuesta a la que oponerse. Lo que da un servidor local:

- **El modelo se carga una vez.** Medido hoy: ~6,7 s de arranque por llamada con shell-out. Un
  bucle que llama 50 veces paga 5 minutos solo en abrir el fichero.
- **API compatible con OpenAI**, así que CineK y cualquier herramienta futura pegan sin
  adaptador.
- **Varios agentes en paralelo** sin recargar 16 GB por cada uno.

Es real y es mucho. La propuesta **no es no hacerlo**: es hacerlo con la frontera escrita.

---

## 5 · Por qué los bucles no esperan a esta decisión

`agentes/bucles/cerebro.py` ya está construido con shell-out y **no abre ningún puerto** (hay
prueba). Los bucles L3 se pueden construir hoy sobre él.

El día que se firme el servidor, `cerebro.py` gana un segundo camino por dentro y **ningún
bucle se entera**. Esa es exactamente la razón de que exista un módulo común en vez de que
cada bucle llame al binario por su cuenta.

---

## 6 · Para la firma

| # | Qué se firma | |
|---|---|---|
| F1 | D68 gobierna **el producto**; el rack queda fuera | ⬜ |
| F2 | PreceptorOS **jamás** consume un servidor de modelo, y se comprueba con una prueba en la tanda pública | ⬜ |
| F3 | Si se levanta `llama-server`: loopback, fila en `unidades.md`, y `0.0.0.0` es firma aparte | ⬜ |
| F4 | Antes del primer bucle residente, `ARQ_LOOPS.md` gana la clase RESIDENTE con su presupuesto | ⬜ |

Mientras F1–F4 no estén firmadas, **no se levanta ningún servidor de modelo** y los bucles
siguen por `cerebro.py`, que no los necesita.
