# FASE 2 · v2 · NO ABORTÓ, Y AUN ASÍ NO ESTÁ LISTA

**2026-08-21** · PEFT + torch 2.13.0+cpu · bf16 · `r=8 · alpha=16 · 1 época`
Ajustes firmados: **validación 20 %** (21 EN / 21 ES) · **dos subidas seguidas
para abortar**

## La corrida

140 pasos, la época entera. **Cero `nan`.** Descarte activo: 26 fuera del tren,
2 de la validación → **140 de tren · 40 de validación**.

| paso | train | validación | |
|---:|---:|---:|---|
| 20 | 5,2406 | 4,4178 | |
| 40 | 4,2785 | 4,0336 | |
| 60 | 4,0049 | 3,6414 | |
| **80** | 3,5490 | **3,5366** | **← el mejor modelo estuvo aquí** |
| 100 | 3,5887 | 4,5065 | sube la validación… y el tren también |
| 120 | 3,5327 | 4,8381 | primera subida que cuenta |
| 140 | 3,3825 | 4,5555 | la validación baja: se rompe la racha |

**El guardián no abortó, y obró bien.** La regla que firmaste exige dos subidas
**seguidas** con el tren bajando. En el paso 100 el tren subió un pelo
(3,5490 → 3,5887), lo que rompió la cadena antes de empezar; en el 140 bajó la
validación y la rompió otra vez. Nunca hubo dos seguidas.

## Lo que la regla no vio, y hay que decirlo

**v2 sobreajusta igual que v1.** La validación tocó fondo en el paso 80 con
3,5366 y terminó en 4,5555 — un **28,8 % peor**. Acabó incluso por encima de
donde empezó (4,4178).

Y lo que se guardó es el **paso 140**, porque el entrenador guarda el último, no
el mejor. El adapter que hay en disco es medible y **es peor que el que hubo**.

> Los dos ajustes hicieron lo que prometían: 40 muestras dieron una validación
> mucho más estable, y la exigencia de dos subidas evitó abortar por el ruido
> del paso 120. Ninguno de los dos era el problema. **El problema es que la
> regla vigila la pendiente y nadie vigila el récord.**

## El agujero, nombrado

No hay **checkpoint del mejor momento**. Una parada temprana de verdad no es
solo «deja de entrenar»: es **quédate con el mejor y tira el resto**. Hoy la
Fase 2 hace lo segundo al revés.

El guardián de salud tampoco lo veía: comparaba principio contra final y decía
«sin alertas» sobre este mismo dato. Corregido — ahora compara **mejor contra
guardado** y avisa si lo guardado es más de un 10 % peor. Sobre v2 dice:

```
el mejor momento fue el paso 80 (val 3.5366);
el adapter guardado es del paso 140 (val 4.5555, +28.8%)
ALERTA · se guardo un adapter medida peor que el mejor que hubo
```

## Veredicto

**El adapter existe pero no se ha ganado el sitio.** No lo mando a la Fase 3:
sería medir la copia peor de un modelo que ya sabemos que memoriza.

Tu condición decía «si v2 también aborta, declaramos v1 NO_DATA y esperamos al
dataset». v2 **no abortó** — así que la condición, literalmente, no se cumple.
Pero el dato dice lo mismo que habría dicho un aborto, y el fondo no ha
cambiado desde el veredicto de la Fase 0: **5,9 M de parámetros entrenables
contra ~3 000 tokens.** Con este dataset, cualquier corrida larga acaba
recitando; lo único en discusión es en qué paso.

Recomiendo, sin ejecutarlo:

1. **Guardar el mejor checkpoint**, no el último. Es el arreglo real y no toca
   ningún hiperparámetro que hayas firmado.
2. Con eso, v2 ya habría entregado el adapter del paso 80 — el único que este
   dataset ha producido con la validación en su mínimo.
3. Y el horizonte sigue siendo el mismo: **que el dataset crezca**. Ningún
   hiperparámetro arregla tres mil tokens.

`salida/v2/` se queda en disco. No se borra: es la prueba de lo que pasó.
