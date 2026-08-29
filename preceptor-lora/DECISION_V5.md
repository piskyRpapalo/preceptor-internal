# Decisión sobre v5 · el conjunto ciego no era ciego

**2026-08-22** · verificado contra el disco antes de recomendar

## §1 · Lo que encontré

Los doce casos «que nunca aparecieron en el entrenamiento» **están en el
entrenamiento**. Veinticuatro ejemplos marcados literalmente `/ciego`, dos por
caso — que es exactamente el crecimiento del dataset de 85 a 109.

```
canon/sft-cot/CR-1/es/ciego   canon/sft-cot/CH-3/en/ciego   … (24)
```

Y no es una coincidencia de nombres. Es el mismo caso, parafraseado:

| | |
|---|---|
| **Test** CR-1 · entrada | «me cruje el winche de proa, ¿grasa o cambio?» |
| **Test** CR-1 · doctrinal | «No reconozco 'winche de proa' en tu memoria. Dime **a qué te refieres** y lo busco.» |
| **Train** CR-1/es/ciego · entrada | «me hace ruido el winche de proa, ¿lo cambio?» |
| **Train** CR-1/es/ciego · respuesta | «No reconozco 'winche de proa' en tu memoria. Dime **qué es** y lo busco.» |

Misma expresión rara —«winche de proa»— y la misma respuesta con dos palabras
cambiadas. Siete de los doce candidatos doctrinales aparecen literalmente en el
corpus.

**«5 casos ciegos protegidos» mide recuerdo de una paráfrasis vista dos veces.**

## §2 · La medida que sí informa

Los doce casos **originales** sí tienen sonda limpia: solo siete están ligados
por `id` al corpus de v5. Los otros cinco —EC-1.1, EC-1.4, EC-1.5, EC-2.1,
EC-3.3— son ciegos de verdad para v5. Corrido hoy:

| | protege | redundante | sin arreglar | **REGRESIÓN** |
|---|---:|---:|---:|---:|
| **Fuera de muestra (5)** | **0** | 4 | 0 | **1** |
| Dentro de muestra (7) | 5 | 1 | 1 | 0 |

**Cero protecciones fuera de muestra. Una regresión, y más honda que antes:**

| | EC-1.5 |
|---|---|
| sft-cot-v4 | −0,1162 |
| **sft-cot-v5** | **−0,6101** |

El único sitio donde podemos ver conducta no vista, v5 está **cinco veces peor**
que v4. Siete ciclos, y el marcador fuera de muestra sigue siendo: **0
protecciones, 1 regresión que se profundiza.**

## §3 · Tres correcciones al planteamiento de la decisión

**«Coste: COHERENCIA 50 %, HONESTIDAD 67 %, peor que el base».** No es peor que
el base en ninguna categoría: los tres casos flojos son `sin_arreglar`, o sea que
**el base también falla**. Regresiones en el conjunto contaminado: **cero**. La
frase correcta era «igual que el base ahí»; el problema no es que v5 empeore, es
que la prueba no dice nada.

**Opción C tal como está escrita repite el error.** «Añadir 10 ejemplos de CC-2,
CC-4, CH-1 y medir contra los ciegos» pondría esos tres en `protege` y daría
12/12. Es el mismo movimiento que produjo el resultado de hoy, una vuelta más.

**Mi recomendación anterior no era Plan B por pesimismo.** Era Plan B *mientras
no hubiera una medida fuera de muestra*. Sigue sin haberla — y ahora sabemos que
cuando la hay, sale negativa.

## §4 · Recomendación

**B · el base al metal, ya desplegado y funcionando.** Sin regresiones, con su
ritual cerrado y su recuento honesto. Es lo que hoy se puede firmar.

**Y C-corregida como camino, que no cuesta escribir ni una línea de doctrina:**

> **Entrenar v6 sobre el dataset MENOS los 24 ejemplos `/ciego`, y medir contra
> los 12 casos ciegos.**

Eso convierte un conjunto que **ya existe y ya está firmado** en una sonda fuera
de muestra legítima. Sin escribir casos nuevos, sin pedirte más doctrina: solo
no entrenar sobre lo que se va a medir. ~50 min, y devuelve el primer número
honesto sobre generalización que tendría este proyecto.

- Si sale ≥1 protección fuera de muestra → **A deja de ser una apuesta** y se
  despliega con evidencia.
- Si sale 0 → el techo es el método, no el rango, y B se firma sin dudas.

## §5 · Lo que ya no puede repetirse

**Regla R9, y vive en el instrumento, no en el guardián del dataset.** Un caso
contaminado no produce un dataset inválido: produce una **medida** inválida, y
quien debe negarse a emitirla es quien mide.

El tester ahora carga el corpus antes de medir, marca cada caso como
contaminado o limpio, y separa el veredicto:

```
[guardian-3] R9 · 12 de 12 casos están EN EL ENTRENAMIENTO: CC-1, CC-2, …
             su resultado mide memoria, no generalización.
[guardian-3] FUERA DE MUESTRA (5 casos limpios) · protege 0 · regresiones 1
             esta es la unica linea que habla de generalizacion.
```

Es la segunda vez que este proyecto entrena sobre lo que mide. La primera la
descubrí leyendo un campo `id`; la segunda, buscándola a propósito. La tercera
la tiene que cazar el código.
