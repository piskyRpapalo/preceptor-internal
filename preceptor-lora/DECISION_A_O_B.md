# Camino A o Camino B · cuantificado

**2026-08-21** · medido en este nodo, no estimado.

## §0 · Lo que hay hoy, en cifras

| | |
|---|---|
| Canon en el dataset | 208 registros · 104/104 EN/ES |
| **Entrenable de verdad** | **180 muestras · 3 609 tokens** · media 20,1 |
| Descartadas por cortas (<4 tokens) | 28 |
| Negativos firmados | 18 (9 casos × 2 idiomas, familias F1/F2/F3) |

| rango | parámetros | **params por token entrenable** |
|---|---:|---:|
| r=8 (actual) | 5 898 240 | **1 634** |
| r=4 | 2 949 120 | **817** |
| r=2 | 1 474 560 | 409 |

## §1 · El hallazgo que reordena el Camino A

Firma 1 nombra tres fuentes de crecimiento. Medidas una a una:

| Fuente | Estado real |
|---|---|
| `textos.py` | **Agotada.** Los 208 registros ya están dentro. No hay un segundo `textos.py`. |
| **Turnos reales de `--charla`** | **CERO. Y no porque nadie hable: porque el producto no los guarda.** |
| Correcciones firmadas | 18 ya extraídas. El resto vive como prosa en commits y PENDIENTES, no como pares. |

**Verificado en el código, no supuesto:** no existe tabla de turnos en
`memory.py`, y ni `conversacion.py` ni `charla()` escriben el par
`(lo que dijo la persona, lo que respondió el modelo)`. Lo más parecido es
`salidas` —6 filas en esta máquina— que guarda **la respuesta del modelo sin su
prompt**. Media pieza no es un par de entrenamiento.

Los dos turnos reales del sprint en el Doogee **no existen como dato**. Se
midieron, se citaron en el reporte, y se perdieron.

> **Consecuencia:** el Camino A, tal y como está escrito, **no puede empezar
> hoy**. Su fuente principal no está vacía: no está construida.

## §2 · Camino A · crecer el dataset

**Tensión que resuelve.** El producto promete una voz propia y el material que
la enseña son 3 609 tokens. Es la causa que Fase 0, Fase 2 y Fase 3 midieron por
tres vías distintas.

**Doctrina que la justifica.** Firma 1 prohíbe el relleno sintético; `LORE.md`
§1 prohíbe que el vocabulario de la casa viaje; el sensor honesto prohíbe
inventar el dato que falta. Las tres empujan a lo mismo: **datos reales o
ninguno.**

**Riesgo de implementar.** Dos costes distintos, y el segundo es el que duele:

*Trabajo* — construir la captura: tabla nueva y migración, el par completo, el
consentimiento en los dos idiomas, la cuarentena antes del dataset, y sus
pruebas. **~5–7 h** de código de producto, stdlib. Extraer a pares las
correcciones que ya existen en prosa: **~2 h**.

*Tiempo* — y aquí está el riesgo real. A ~60 tokens por turno (prompt +
respuesta), llegar al horizonte de 1–2 MB (~400 000 tokens) pide del orden de
**6 600 turnos**. En el Doogee, a 5,4–6,3 min por turno, eso es aritmética que
no cierra. **El dataset no crece en horas de trabajo: crece en meses de uso.**

**Riesgo de NO implementar.** Ningún LoRA funciona nunca. v3, v4 y v5 repetirán
lo de v1 y v2 con otro número, y cada ronda costará lo que costó esta. La causa
seguirá donde está.

## §3 · Camino B · reducir el modelo

**Tensión que resuelve.** Si el problema es capacidad sobrante, quitarla debería
bastar. Nadie lo ha medido.

**Doctrina que la justifica.** «`num_ctx` demostrado por dato», «una cifra sin su
máquina es un rumor». Discutir si r=4 basta, teniendo el metal delante y quince
minutos libres, es exactamente la clase de suposición que esta casa no se
permite.

**Riesgo de implementar.** **~15 minutos de cómputo.** Entrenar 140 pasos son ~6
min; los 12 edge cases con base y LoRA, ~7. Cero horas de código: solo cambiar
`rank` y `alpha`. Es lo más barato que hay sobre la mesa.

**Riesgo de NO implementar.** Dar por supuesto que r=4 no ayuda. Y perder la
pregunta que de verdad importa, que no es la pérdida:

> **¿La regresión de EC-2.4 mejora o empeora a r=4?**
>
> Si baja con menos capacidad, es un artefacto de sobreajuste y se corrige con
> rango. Si aguanta igual, **viene de los datos**, y entonces hay algo en el
> canon que empuja al modelo hacia la orden destructiva. Eso sería un hallazgo
> de seguridad sobre el dataset, no sobre el rango — y no se descubre por otra
> vía.

**Lo que B no va a arreglar, y conviene decirlo antes:** r=4 mueve el ratio de
1 634 a 817 params/token. Es la mitad de un número que está tres órdenes de
magnitud fuera de sitio. **Esperar que B resuelva el problema es esperar
demasiado**; esperar que lo mida bien, no.

## §4 · Propuesta

**Los dos, en este orden. No en paralelo:** comparten los mismos 8 núcleos, y
dos cargas de 4B a la vez solo hacen que las dos vayan lentas.

**1 · B primero, esta misma sesión.** Quince minutos, y sustituye un argumento
por una medida. Su valor no está en arreglar v3 — está en la pregunta de EC-2.4.

**2 · A después, y es el trabajo de verdad.** Con una corrección al plan: A no
empieza por extraer datos, empieza por **construir la captura**, porque hoy no
hay de dónde extraer.

### Y una colisión entre dominios que hay que nombrar

**El Camino A es el Vector 4.** Lo que el Dominio 1 necesita para desbloquear la
Fase 3 —capturar correcciones y turnos como pares— es exactamente la
auto-canonización que firmaste primera en el Dominio 2. No son dos trabajos
parecidos: son el mismo.

Tu propia regla dice qué hacer: *«si una propuesta del Dominio 2 produce código
útil para el Dominio 1, se extrae como módulo propio con su propio commit, no
como dependencia»*. Así que la captura nace como módulo del producto —stdlib, con
su consentimiento y sus pruebas— y el Dominio 2 la usa. El producto público no
se entera de que existe un Sínodo.

**Y esto adelanta el calendario del Dominio 2:** dijiste «nada se ejecuta hasta
cerrar Fase 3». Pero la Fase 3 no cierra sin datos, y los datos no llegan sin V4.
La puerta está cerrada por dentro. Propongo que **V4 sea la excepción explícita**
a esa regla, no un salto silencioso.

## §5 · NO_DATA declarados

- **`EVALUATION_DOCTRINE.md` no existe en este nodo.** Busqué en todo el home.
  No puedo corregir sus dos divergencias ni opinar sobre publicar el tester sin
  el documento delante.
- **Turnos guardados en el Doogee:** no medidos. La consulta se perdió al
  escapar comillas y no insistí (ver el incidente del reporte). Estructuralmente
  no puede tener pares, porque ningún código los escribe — pero el número exacto
  de filas de `salidas` allí queda sin medir.
