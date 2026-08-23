# DPO · autorizado y BLOQUEADO · los pares están mancos

**2026-08-21** · autorización recibida · **no ejecutado**

## El bloqueo

DPO compara dos respuestas: la que se prefiere y la que se rechaza. Los 18
negativos firmados tienen **`rechazado` y no tienen `elegido`**:

```
[dpo] pares completos: 0 · mancos: 18
    manco negativo/en/F1-voseo  falta: elegido
[dpo] BLOQUEADO · DPO necesita las dos mitades y no las escribo yo.
```

Es el mismo fallo estructural que `salidas` guardando la respuesta sin su
prompt, y que llevó a construir el módulo de captura: **media pieza no es un
par.** Aquí se ve antes de gastar la corrida, no después.

**No he rellenado las mitades que faltan.** Escribir yo lo que Aurelius
*debería* haber contestado sería poner mis palabras donde va tu doctrina y
llamarlo dato firmado. Es exactamente lo que la Firma 1 prohíbe cuando dice
«nada de relleno sintético», y aquí pesa más: no es relleno para engordar un
número, es **inventar el criterio**.

## Lo que sí queda construido y verificado

**`forja/entrenar_dpo.py`** — la tubería entera, con cerrojo doble: `--ejecutar`
y pares completos. Se para sola sobre medio par.

**El truco que ahorra 8 GB.** DPO necesita un modelo de referencia congelado. Lo
obvio es cargar dos modelos de 4B: 16 GB en bf16. No hace falta — con un
adapter, la referencia **es el mismo modelo con el adapter apagado**.
`disable_adapter()` da eso y el pico se queda en ~9 GiB.

**`pruebas/humo_dpo.py`** — prueba de humo del instrumento, con tres pares de
juguete que **no entran en `data/`**. Verifica dos cosas:

```
antes   · perdida media 0.6931 · margen medio +0.0000
despues · perdida media 0.2425 · margen medio +15.1095
VERDE · el instrumento calcula lo que dice calcular
```

El margen **exactamente 0** al arrancar no es casualidad: con el adapter recién
inicializado, política y referencia son el mismo modelo, y esa es la prueba de
que `disable_adapter()` da una referencia de verdad y no una copia de la
política. Si eso fallara, DPO optimizaría contra sí mismo y la pérdida bajaría
igual, mintiendo.

**Regla R8 en el guardián de la Fase 1** — un registro de preferencia sin
`elegido` es **fallo, no aviso**. A diferencia de una cadena corta, que el
entrenador descarta solo, esto no se descarta: bloquea la pasada entera.

## Cómo se desbloquea · tres vías y una recomendación

**(A) Las escribes tú. Recomendada.** Nueve respuestas cortas — lo que Aurelius
debería haber dicho en cada caso — en los dos idiomas. Te dejé el hueco
preparado en **`datos/MITADES_QUE_FALTAN.md`**, con la pregunta, el rechazado
medido y tu motivo firmado delante de cada uno. Es una pasada de quince minutos
y deja el dataset íntegro.

**(B) Extraer del canon.** Solo funciona para F3 (primer arranque), donde la
conducta correcta ya existe en `textos.py`. F1 (tono) y F2 (sensor deshonesto)
no tienen respuesta enlatada: dependen del contexto. Daría 6 pares de 18, y un
subconjunto silencioso es justo lo que R8 existe para impedir.

**(C) Usar los pares de `edge_cases/casos.json`. La descarto, y digo por qué.**
Cada caso ya tiene su `candidato_doctrinal` y su `candidato_roto`: son pares
perfectos. **Y son el banco de pruebas.** Entrenar con ellos haría que el tester
midiera memorización en vez de comportamiento, la Regla C daría verde por
construcción, y EC-2.4 «mejoraría» sin que el modelo hubiera aprendido nada.
Sería fabricar el resultado que buscamos.

## Lo que no cambia

La corrida de DPO, cuando haya pares, entrena sobre **18 ejemplos**. Eso no va a
enseñar una voz — va a enseñar **una cosa concreta: que existe el no**. Es la
apuesta correcta precisamente porque es pequeña y específica: los cinco edge
cases que fallan comparten esa única carencia.

Y sigue en pie lo medido: `~3 609` tokens de canon no enseñan un registro. DPO
sobre 18 pares ataca el sesgo, no el tamaño. Son dos problemas distintos y este
solo toca uno.
