# ARQUITECTURA DE BUCLES

**Fecha:** 2026-08-23 · **Estado:** L0, L4 y S0 construidos y probados. El resto, pendiente.

> Un bucle sin realimentación es un cron. Todo bucle lee su propia salida anterior y se
> compara: sin delta no hay aprendizaje, solo repetición.

---

## Las cuatro refinaciones, y de dónde salen

Esto es lo que separa esta arquitectura de una carpeta de crontabs. **Las cuatro salen del
archivo del propio Soberano**, no de un manual: se aprendieron pagando entre mayo y julio
de 2026, se perdieron con el resto del material disperso, y volvieron con el equipo de
lectura del 23 de agosto.

### (a) Histéresis · ningún estado cambia por un solo evento

Un bucle no pasa a muerto porque una ejecución falló, ni revive porque una salió bien.
Hace falta **evidencia sostenida** (dos ventanas sin latido) **y** que el estado actual
lleve puesto un **descanso mínimo** de 300 s.

*Antepasado:* el Filtro de Eficiencia de la Doctrina Sol-Síncrono, que ya llevaba
histéresis de cinco minutos contra el flapping.

*Por qué:* con la carga oscilando alrededor del umbral, un bucle entra y sale de servicio
sin llegar a hacer nada, y la bandeja de firmas recibe el mismo aviso diez veces hasta que
alguien deja de mirarla. **Ese es el momento en que el sistema de vigilancia deja de
vigilar, sin que nadie lo haya apagado.**

*Dónde vive:* `latido.cambiar_estado()`. Es el único camino para mover un estado.
`registrar()` no puede tocarlo — si pudiera, cualquier arranque resucitaría al muerto y el
Director no se enteraría.

### (b) `@sleeping` · retirar sin borrar, con la llave puesta

Una capacidad que deja de aplicar se marca dormida **con motivo y con condición de
despertar escrita**, y queda detrás de un solo flag.

*Antepasado:* el addendum energético del 15 de mayo, cuando se perdió la batería.
*«El organismo no rompe con su pasado. Lo pone en pausa, y guarda la llave.»*

*Cómo se impone:* `dormir()` levanta `ValueError` sin condición de despertar, y el esquema
lo repite con un `CHECK`. Un dormido **no entra en la cola** y **no se marca muerto** —
confundir dormido con muerto generaría una alerta cada noche sobre algo que se apagó a
propósito.

### (c) Latido append-only · la historia no se reescribe

`loops.db` **solo inserta**. Nunca edita, nunca borra.

*Antepasado:* el registro de drills del Protocolo de Reencarnación, donde las filas nunca
se editan.

*Cómo se impone:* **cuatro disparadores de SQLite** que abortan cualquier `UPDATE` o
`DELETE` sobre `latidos` y `estados`. No es una convención que dependa de la disciplina de
quien escriba el próximo bucle a las tres de la mañana: es el motor.

*Por qué:* un latido que se puede sobrescribir pierde la historia del fallo, que es justo
lo que se quiere leer cuando algo lleva tres semanas muriéndose despacio.

### (d) S0 · el monitor de fallo silencioso

Un bucle semanal que **vigila a los vigilantes**: cuenta hallazgos por filtro y sospecha
del que lleva siete días corriendo bien sin encontrar nada.

*Antepasado:* el Score S0 del Códice 14 — *«si nada supera el filtro en 7 días, sospecha
del filtro»*.

*Por qué:* es el modo de fallo que ninguna alerta detecta, porque no produce ninguna
alerta. El detector se rompe y **todo se queda verde**.

*Un caso real, medido el mismo día:* el guardián de dependencias propuesto usaba
`grep "^import" *.py`, que en bash se expande solo a la raíz. Medido en `aurelius-mvp`: 58
ficheros frente a los 60 que hay. Los dos que se escapaban eran `empaquetado/lanzador.py`
y `laminas/recortar.py` — **el único fichero del proyecto que importa algo fuera de la
biblioteca estándar**. Ese guardián habría dado verde todas las noches sin ver lo único
que tenía que ver.

*Detalle que importa:* S0 distingue **callado** de **parado**. De un bucle que no corre ya
avisa el Director; si S0 avisara también, habría dos alertas de lo mismo y ninguna diría la
verdad. Y S0 **se registra a sí mismo**, para que el siguiente S0 sospeche de S0.

---

## El mapa

```
L4 · EL DIRECTOR      meta-bucle, cada 15 min · LIGERO
                      lee latidos + carga + hora → plan de ventanas
                      detecta muertos (con histéresis) → bandeja de firmas
L3 · APRENDIZAJE      PESADO · 30B · solo 01:00-06:00 · cerrojo
                      médico · escriba · cronista · vigía          [pendiente]
L2 · MEMORIA          MEDIO · ancla · rescatador                   [pendiente]
L1 · GUARDIA          LIGERO · afinador · guardián · centinela · peregrino
                                                                   [pendiente]
L0 · EL LATIDO        loops.db · latidos · estados · hallazgos · cerrojo
S0 · SOSPECHA         semanal · lee a todos los demás
```

## Clases y presupuesto

| Clase | Cuándo corre | Freno |
|---|---|---|
| **LIGERO** | siempre | ninguno |
| **MEDIO** | si `load ≤ 2.0` | se pospone **y lo registra** |
| **PESADO** | solo 01:00–06:00, con cerrojo `flock`, uno a la vez | ventana + cerrojo + carga |

Una posposición **siempre deja latido**. Un bucle que se pospone en silencio es
indistinguible de uno que no existe.

## La bandeja de firmas

`docs/bandeja_firmas.md`. El silicio propone; el carbono firma.

**Lo rechazado se memoriza:** antes de escribir, el Director lee el fichero y no repite una
propuesta que ya esté ahí. Sin eso, el mismo aviso reaparece cada noche y la bandeja se
vuelve ilegible — que es la forma educada de apagarla.

## Ficheros

| Fichero | Qué es |
|---|---|
| `agentes/bucles/latido.py` | L0 · la base de datos, el turno, los estados, `@sleeping` |
| `agentes/bucles/director.py` | L4 · revisa, aplica, planifica, escribe a la bandeja |
| `agentes/bucles/s0.py` | S0 · el monitor de fallo silencioso |
| `agentes/bucles/test_bucles.py` | 17 pruebas de las cuatro refinaciones |
| `~/.aurelius/loops.db` | los latidos. **Fuera del repositorio**: es estado, no código |
| `~/.aurelius/loops.lock` | el cerrojo de los pesados |

## Uso

```bash
python3 agentes/bucles/director.py --informe   # estado de todos los bucles
python3 agentes/bucles/director.py             # una pasada
python3 agentes/bucles/s0.py --informe         # filtros bajo sospecha
python3 agentes/bucles/test_bucles.py          # 17 pruebas
```

### El gate del enjambre

```bash
pytest agentes/ -q                             # 88 pruebas, medido 2026-08-31
```

**No se corre `pytest -q` a secas desde la raíz del repositorio.** Falla en
colección con `ModuleNotFoundError: No module named 'pydantic'` × 3, en
`faro_peaq/tests/`. Es una dependencia que ese módulo declara en su propio
`requirements.txt` y que no está instalada aquí; no tiene nada que ver con los
bucles, que pasan enteros. Si hace falta correrlo desde la raíz:

```bash
pytest -q --ignore=faro_peaq
```

Se escribe aquí porque el fallo engaña: un `pytest -q` en rojo desde la raíz
parece decir que el enjambre está roto, y lo que dice es que falta un paquete
de otro módulo.

Un bucle nuevo se escribe así, y el latido sale gratis:

```python
import latido as L

with L.turno("guardian", "LIGERO", 86400) as caja:
    hallados = revisar_imports()
    with L.abrir() as c:
        for h in hallados:
            L.hallazgo(c, "guardian", h["clave"], h["detalle"])
    caja["nota"] = f"{len(hallados)} imports nuevos"
```

`turno` late al entrar y al salir **pase lo que pase**: si el bucle revienta, deja su
latido de fallo escrito con la excepción. Sin eso, una excepción no controlada es
indistinguible de un bucle que nunca arrancó.

Y **registrar hallazgos no es opcional**: es lo que alimenta a S0. Un filtro que no
registra lo que encuentra no puede ser vigilado, y acabará dando verde por avería sin que
nadie lo note.

---

## Lo que falta

- Cronificar el Director (`*/15`) y su watchdog de 5 min. **Requiere aprobación explícita**:
  el archivo tiene una regla de higiene que nunca llegó al repositorio —*«no se crean
  servicios systemd sin aprobación explícita del Soberano»* y *«`systemctl list-units` al
  cerrar cada sesión»*— y con bucles 24/7 en el horizonte esa regla pasa de incómoda a
  necesaria. Se propone firmarla antes de cronificar nada.
- Los bucles de L1, L2 y L3.
- La telemetría del Doogee por tailnet (1/h): latencia de turnos, errores de voz, batería.
  Solo produce señales; no corre nada pesado.
