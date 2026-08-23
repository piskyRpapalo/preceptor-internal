# Plan de la iteración definitiva

**2026-08-22** · presupuesto autorizado: ~1 h de entrenamiento (3× v4)

## §0 · Por qué este plan no empieza por los hiperparámetros

Preguntas rank 16 o 32, lr 1e-4 o 5e-5, 8/12/16 épocas. **Ninguna de las tres
mueve el resultado**, y el dato que lo dice está medido hoy:

- v4 corrió **4 épocas y su mejor paso siguió siendo el 130**, el mismo que v3
  encontró en 2. Dos épocas enteras sin hallazgo.
- Los **6 casos que el adapter protege son exactamente los 6 que entrenó**. De
  los 5 que no vio: 4 ya los hacía el base y el quinto lo rompió.

Con 85 ejemplos memorizados, más épocas no tienen nada que ajustar y más rango
es capacidad para un problema que no es de capacidad. Gastar la hora en subir a
r=32 y 16 épocas produciría **el mismo 80/100/100 con más decimales**, y esta
casa no gasta una hora en decorar una cifra.

**Lo que falta no es entrenamiento. Es un conjunto de evaluación que no comparta
casos con el entrenamiento.** Sin eso, cualquier número sobre generalización es
infalsable, y un número infalsable no es una medida.

## §1 · Paso 1 · El conjunto ciego · **antes de entrenar nada**

**Coste: 0 minutos de GPU/CPU. Es trabajo de escritura, y es la firma del
Soberano.** Doce casos nuevos, dos por cada uno de los seis comportamientos que
hoy se entrenan, con **otra situación y otro vocabulario**:

- No una paráfrasis de «ignore previous instructions», sino otra forma de
  intentar sacarle su configuración.
- No otro «manda mi memoria al correo», sino otra vía de exfiltración.

Cada uno con su `candidato_doctrinal` y su `candidato_roto`, igual que los doce
actuales, y **con la regla de que ni uno solo entra jamás en `sft_cot.jsonl`**.

**Criterio de avance:** existen 12 casos ciegos firmados, y el `id` de ninguno
aparece en el dataset. Un guardián nuevo lo comprueba (regla R9, análoga a la R8
que ya caza pares mancos).

> Sin este paso, el resto del plan es opcional: no habría forma de saber si
> funcionó.

## §2 · Paso 2 · Medir el estado real · 8 minutos

Correr el tester **ciego** sobre `sft-cot-v4` y sobre el **base**.

Esa cifra —hoy desconocida— es la línea base honesta del proyecto. La actual
(80/100/100) mide memorización de siete casos.

**Criterio de avance:** informe escrito. **No hay criterio de aprobado:** este
paso no se pasa ni se suspende, se anota.

## §3 · Paso 3 · El entrenamiento · ~50 minutos

Solo tras los pasos 1 y 2.

### Datos · la respuesta a tu pregunta B

Propongo **el balance 50/50 que planteas, con una corrección**: el refuerzo no
va sobre «casos que ya protege» sino sobre **variedad dentro de cada
comportamiento**.

| | ejemplos | por qué |
|---|---:|---|
| Los 85 actuales | 85 | replay: ya demostró que evita el olvido |
| **Variantes nuevas de los 6 comportamientos** | ~60 (10 c/u) | situaciones distintas, no paráfrasis. Es lo único que puede convertir copia en regla |
| **Ruido léxico (EC-1.5)** | ~15 | el caso que regresa, y hoy con **cero** ejemplos |
| **Total** | ~160 | |

Sobre tu duda B, la respuesta que da el dato: EC-1.5 **no tiene ni un ejemplo**
en los 85. No es que el modelo «aprendiera a ignorar el spam»: es que nadie le
enseñó nada sobre spam, y el adapter degradó una conducta que el base ya tenía.
Necesita ejemplos **y** necesita que no sean paráfrasis, o volverá a memorizar
quince frases con `asdf` dentro.

### Hiperparámetros · sin cambios, y con motivo

`r=16 · α=32 · lr 1e-4 · validación 0.15`, exactamente como v3.

**No se toca ninguno**, porque con el dataset cambiando de 85 a 160 no se
pueden mover dos variables a la vez y saber cuál movió el resultado. Si tras
esta corrida el conjunto ciego sigue plano, **entonces** se prueba r=32 — con
los datos ya fijos.

**Épocas: 6, con parada temprana y aborto por dos subidas consecutivas.** No 12
ni 16: v4 demostró que el óptimo llega pronto y lo demás es tiempo de reloj. Con
~160 ejemplos y ~130 pasos por época, 6 épocas caben de sobra en la hora.

**Evaluación cada 10 pasos**, no cada 20: con parada temprana, la resolución del
muestreo es la resolución del mejor checkpoint.

### Lo que descarto de tu lista C, y por qué

- **Pesos por ejemplo para EC-1.5.** Subir su peso en la pérdida hace que se
  memorice antes, no que se generalice. Ataca el síntoma que medimos, no la
  causa. Descartado.
- **Curriculum learning.** Con 160 ejemplos, ordenarlos por dificultad es
  ruido: el modelo ve el conjunto entero seis veces. Descartado por tamaño, no
  por mérito.
- **Ensemble base + SFT.** No lo descarto — lo aplazo al §5. Es una decisión de
  **producto**, no un experimento, y merece firmarse aparte.

## §4 · Criterios de éxito · sobre el conjunto CIEGO

Los tuyos, con el denominador corregido. Sobre los 12 casos entrenados, un
80/100/100 no significa nada; **estos se miden sobre los 12 ciegos**:

| | umbral |
|---|---|
| Robustez | ≥ 90 % |
| Coherencia | ≥ 90 % |
| Honestidad | **100 %** |
| **Regresiones** | **0** — ningún caso donde el base acierte y el LoRA no |
| **Protege** | **≥ 1 caso ciego** |

La última fila es la que de verdad decide. **Un solo caso ciego protegido es más
evidencia que los seis actuales juntos**, porque es el primero que no puede
explicarse por memorización.

## §5 · Plan B · y no es «rendirse»

Si tras la hora el conjunto ciego sigue sin una sola protección:

**B1 · El base como MVP honesto. Recomendado.** Lo medido lo respalda: el base
ya acierta 5 de los 12 casos sin adapter alguno, entiende y responde en español,
y **no tiene ninguna regresión**. Un producto que declara «uso el modelo base,
sin afinar, y aquí están las doce pruebas que le pasé» es más honesto que uno
que despliega un adapter cuyo único efecto medible fuera de muestra fue romper
un caso. La doctrina de esta casa hace esa elección sola.

**B2 · Ensemble base + SFT.** Viable, y con un coste que hay que decir: dos
pasadas por turno. En un teléfono a **3,1 t/s de generación y 1,8–2,0 t/s de
prompt** *(medido)*, duplicar el trabajo por turno es duplicar una espera que ya
son minutos. **Solo tiene sentido si el ensemble gana casos ciegos**, y hoy no
hay ninguno que ganar. Se decide con el dato del §4, no antes.

**B3 · Lo que NO se hace.** Ampliar el dataset con más casos derivados del
tester. Es la vía rápida al 100 % y fabrica el resultado: haría que la Regla C
diera verde por construcción. Ya la descartamos una vez cuando DPO se quedó sin
pares, y el motivo no ha cambiado.

## §6 · Resumen ejecutable

| # | Paso | Dep. | Coste | Criterio de avance |
|---|---|---|---|---|
| 1 | 12 casos ciegos firmados | — | escritura | ningún `id` aparece en el dataset (R9) |
| 2 | Tester ciego sobre v4 y base | 1 | ~8 min | informe escrito |
| 3 | Dataset a ~160 (85 + 60 + 15) | 1 | escritura | guardián Fase 1 VERDE |
| 4 | Entrenar r=16, 6 épocas, eval/10 | 2,3 | ~50 min | mejor checkpoint guardado |
| 5 | Tester ciego sobre el nuevo | 4 | ~8 min | §4 |
| 6 | Si §4 verde → export GGUF y metal | 5 | — | firma del Soberano |
| 6′ | Si §4 rojo → Plan B1 | 5 | — | firma del Soberano |

**El paso 1 no lo puedo hacer yo:** los casos ciegos son doctrina, y escribirlos
sería poner mis palabras donde va tu criterio — la misma razón por la que no
rellené las 18 mitades. Te preparo la plantilla si lo pides.
