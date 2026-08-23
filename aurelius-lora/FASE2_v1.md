# FASE 2 · v1 · ABORTADA POR SOBREAJUSTE

**2026-08-20** · Beelink `soberano` · PEFT + torch 2.13.0+cpu · bf16
`r=8 · alpha=16 · lr=2e-4 · 1 época` · 5 898 240 parámetros entrenables

## Lo que pasó

El guardián abortó en el paso **120 de 163** (74 % de la época) y **no guardó
el adapter**. Hizo exactamente lo que se firmó que hiciera.

| paso | train | validación |
|---:|---:|---:|
| 20 | 5,2859 | 5,0260 |
| 40 | 4,2582 | 4,7125 |
| 60 | 3,6457 | 4,5866 |
| 80 | 3,7060 | 4,4309 |
| 100 | 3,6722 | 4,2756 |
| **120** | **3,3630** | **5,6215** ↑ |

Cinco evaluaciones seguidas con las dos bajando, y a la sexta la validación
sube 1,35 mientras el tren sigue cayendo. Las dos condiciones firmadas se
cumplieron a la vez y el guardián paró.

**Sin `nan` en 120 pasos.** El descarte por debajo de 4 tokens funcionó: 25
muestras fuera del tren y 3 de la validación. El fallo que envenenó el mini-run
de la Fase 0 no volvió a aparecer.

## La decisión que salvó esto fue tuya

Sin el corte de validación —el que firmaste el 2026-08-20 y que la Fase 0 no
tenía— esta corrida habría terminado sus 163 pasos, habría guardado un adapter
con la pérdida de entrenamiento cayendo bonito de 5,29 a 3,36, y habría parecido
un éxito. Lo que había debajo era un modelo empezando a recitar `textos.py`.

La pérdida de entrenamiento sigue bajando en el momento del aborto. **Esa es
justo la trampa**: mirada sola, dice que todo va bien.

## Lo que este dato NO demuestra

**El aborto se apoya en una sola evaluación sobre 17 muestras.** Un salto de
+1,35 después de cinco caídas puede ser el giro real de la curva, o puede ser
ruido de una validación diminuta. La regla firmada es correcta y disparó bien;
lo que es débil es la **evidencia**, no la regla.

Antes de darle a v1 por muerto, dos cosas que lo dirían con certeza y ninguna
es cara:

1. **Exigir dos subidas consecutivas** antes de abortar. Cuesta 20 pasos más
   (~20 s) y separa el giro del ruido.
2. **Ampliar la validación.** 17 muestras es poco para un umbral. Subir el
   corte al 20 % da ~34, y con 163 pasos de tren la pérdida es asumible.

**Y la lectura de fondo, que ya estaba en el veredicto de la Fase 0:** 5,9 M de
parámetros entrenables contra ~3 000 tokens de texto entrenable siguen siendo
demasiados parámetros por token. Bajar a `r=8` redujo el problema a la mitad y
no lo eliminó. Lo que de verdad lo arregla no es un hiperparámetro: **es que el
dataset crezca**, que es exactamente lo que la Firma 1 puso como horizonte.

## Recomendación, sin ejecutarla

No propongo repetir con otro rango a ciegas. Propongo, en este orden:

1. Reintentar v1 con **dos subidas consecutivas** y **validación al 20 %**. Si
   aborta otra vez en el mismo sitio, el sobreajuste es real y v1 necesita más
   datos, no otro hiperparámetro.
2. Si no aborta, la corrida termina y el adapter existe: entonces la Fase 3
   decide si se lo ha ganado, y la 4 lo lleva al teléfono.

Ninguna de las dos se toca sin tu firma. Los hiperparámetros de
`forja/entrenar_lora.py` siguen en `r=8 · 1 época · validación 10 %`.
