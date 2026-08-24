# ENMIENDAS v3.1 → v3.2

**Fecha:** noche del 2026-08-23 → 24 · **Estado:** ✅ **FIRMADO por el Soberano** el 2026-08-24. Las seis enmiendas son canon de v3.2.
**Fuente:** [`verificacion_cruzada_v31.md`](verificacion_cruzada_v31.md)

Tres correcciones de hecho y una condición. Nada más se toca de v3.1: el descarte de C.5, la
partición de B.1, el título, §6.6, las correcciones 4 y 5, y D1–D6, D9–D11 están verificados
y se mantienen.

---

## E1 · Revertir la enmienda de la tabla `hilos` (corrección de hecho)

**v3.1 dice:**

> 🟡 Tabla `hilos` no existe (el módulo sí). Acepto. Error de inventario. Enmienda:
> `hilos.py` existe; la tabla `hilos` no. Los hilos son engramas con `tipo='hilo'`, no tabla
> separada.

**v3.2 dice:**

> La tabla `hilos` existe (`memory.py:111`), y también `hilos_eventos` (`memory.py:117`),
> con `CHECK` sobre `('abierto','tocado','cerrado','reabierto')` — event sourcing, marcado
> en el fichero como «D14: Esquema de Hilos y Eventos». `test_hilos.py` corre 11 pruebas
> verdes contra ellas. El inventario de v3.0 era correcto; la crítica que lo enmendó, no.
> **Los hilos NO son engramas con `tipo='hilo'`**: `engrams` no tiene columna `tipo`, y su
> `CHECK` de `origin` solo admite `persona | intencion | importado`.

**Por qué importa:** C.3 y M5 se apoyan en esta línea. Ejecutada tal cual, reescribirían una
tabla viva y probada para sustituirla por un campo que no existe.

**Coste:** S. Dos párrafos y la fila del inventario doctrinal.

---

## E2 · Sustituir todas las cifras de pruebas por las medidas (corrección de hecho)

**v3.1 y sus antecesores citan** 20+, 254/19, 333/26, «30 ficheros» — ninguna con su
intérprete al lado, y ninguna es la de hoy.

**v3.2 dice:**

> Medido el 2026-08-23, Python 3.14.4 · `/usr/bin/python3` · `TMPDIR=/var/tmp` (ext4):
>
> - `bin/pruebas` → **282/282 · 17 suites · 6 corredores** · VERDE
> - Sabotajes → `test_idioma.py` 4/4 · `test_fuga.py` 6/6 detectadas
> - Suites `test_*.py` en el árbol → **30**
> - Las 13 que el corredor no declara → **103 pruebas, todas verdes**
> - **Total real: 385/385 · 30 suites**
>
> `bin/pruebas` certifica el **73 %** del árbol. La deuda S3 de `PENDIENTES.md` sigue
> abierta: subió de 241 a 282, pero las 13 suites que deja fuera son las mismas.

**Regla que se adopta con la cifra** (D79c, ya firmada): *una cifra sin su intérprete es un
rumor con decimales*. Ninguna cifra entra en un documento sin la máquina y la fecha en que se
corrió.

**Coste:** S.

---

## E3 · D-D: declarar que no existe (corrección de hecho)

**El encargo dice:** cronificar siete bucles (`afinador.sh`, `guardian.sh`, `centinela.sh`,
`peregrino.sh`, `medico.sh`, `escriba.sh`, `cronista.sh`), «puramente mecánico, no toca
doctrina».

**v3.2 dice:**

> Ninguno de los siete ficheros existe en el disco. Lo construido es L0/L4/S0 —`latido.py`,
> `director.py`, `s0.py`— y los siete nombres son los bucles de L1/L3 que `ARQ_LOOPS.md`
> marca `[pendiente]`, es decir, sin escribir.
>
> Además, cronificar **no es mecánico**: `ARQ_LOOPS.md` §«Lo que falta» lo condiciona a
> aprobación explícita, citando la regla de higiene del archivo *«no se crean servicios
> systemd sin aprobación explícita del Soberano»*.
>
> **Estado al cierre de la sesión del 23-ago: `crontab -l` → sin crontab. Ningún timer de
> usuario creado. La sesión no ejecutó D-D.**

**Coste:** S.

---

## E4 · D7 entra como registro crudo, no como índice (condición)

No es un descarte. Es la condición que el propio archivo impone.

**El precedente** — `REVISION_CRUZADA.md:24`, ideas que no deben resucitarse:

> **Índice I_DT** · Falsa precisión: un número compuesto que aparenta medir algo que nadie
> midió.

**El hecho:** ninguno de los cuatro ejes de la brújula (S, X, Z, W) tiene sensor hoy. Nada en
el árbol registra dificultad, recuperación ni dominio.

**v3.2 dice:**

> D7 se construye en dos tiempos, y el segundo no empieza hasta que el primero dé dato:
>
> **D7a · el sensor.** `brujula_estado` dentro de `memory.db`, misma regla de cero `DELETE`.
> Guarda **eventos medidos** —qué se intentó, cuándo, cuántas veces, si salió— y nada más.
> Cero columnas calculadas. Cero dirección. Cero `ln(t)`.
>
> **D7b · la ecuación.** `R = dS/dt = ln(t)` sobre los cuatro ejes, en stdlib puro. **Entra
> cuando `brujula_estado` tenga historia suficiente para que los cuatro ejes se deriven de
> algo medido**, y no antes. Criterio de entrada: 30 días de eventos reales de una persona
> real, o el set etiquetado a mano que exige el lazo de comprensión (§4.2 de la
> verificación).
>
> **Condición de muerte de D7b:** si a los 30 días los ejes no se pueden derivar de
> `brujula_estado` sin inventar constantes, D7b se marca `@sleeping` con su motivo, y la
> Pizarra sigue diciendo `NO_DATA` — que es información verdadera.

**Arrastra:**

- **D9 (SVG del campo vectorial)** pasa a depender de D7b. Dibujar un campo sin ejes medidos
  es decoración, y decoración que aparenta medida es exactamente el I_DT.
- **D10 (Aviso de Caída)** entra ya, pero **solo por su rama honesta**: sin datos, `NO_DATA`.
  El aviso «tu retención está cayendo» espera a D7b.

---

## E5 · Dos genealogías que faltan (adición)

v3.1 documenta FSRS como prior art (D11) y hace bien. Faltan dos del propio archivo, y las
dos tocan el hueco de E4:

- **El Gólem · «CALIBRA TU RADIO»** (`REVISION_CRUZADA.md` §2.4) — mini-juego que etiquetaba
  dato real sin que el usuario supiera que etiquetaba. **Es el antepasado directo de D2+D7**
  y responde a la pregunta de dónde salen las medidas sin convertir el Camino en un
  formulario. Entra como genealogía de D2, con su deuda y su divergencia declaradas, igual
  que FSRS.
- **La Doctrina del Silencio** (`REVISION_CRUZADA.md` §5) — cinco criterios cuantitativos
  **sostenidos 14 días** más voto explícito, con circuit breaker. Es el molde del que v3.1
  deriva sus columnas «criterio de éxito / condición de muerte», y trae la ventana temporal
  que a D8 le falta.

---

## E6 · D8 sale del sprint hasta llevar histéresis (aplazamiento)

D8 dispara con umbral seco: `dS/dt < -0.5 y W >= 4`.

El archivo ya pagó ese error (Filtro de Eficiencia, histéresis de 5 min contra el flapping) y
el rack ya lo tiene resuelto: `latido.cambiar_estado()` exige **dos ventanas de evidencia
sostenida Y descanso mínimo de 300 s**, y es el único camino para mover un estado.

**v3.2 dice:** D8 mantiene su intención —fallo cerrado, determinista, nunca dependiente del
LLM— y añade histéresis antes de escribirse: evidencia sostenida en N ventanas más descanso
mínimo, con los dos parámetros ajustables sin tocar código. Se rediseña sobre el patrón de
`latido.py`, no de cero.

---

## Resumen para la firma

| # | Qué | Tipo | Coste |
|---|---|---|---|
| E1 | La tabla `hilos` existe · revertir la enmienda | Corrección de hecho | S |
| E2 | Cifras reales: 385/385 · 30 suites (282 certificadas) | Corrección de hecho | S |
| E3 | D-D no existe y requiere firma · no ejecutado | Corrección de hecho | S |
| E4 | D7 en dos tiempos: sensor primero, ecuación después | Condición | S |
| E5 | El Gólem y la Doctrina del Silencio como genealogía | Adición | S |
| E6 | D8 aplazado hasta llevar histéresis | Aplazamiento | S |

Las seis son de coste S. **v3.2 es una tarde de café, no una reescritura.**

---

## Firma

**2026-08-24 · el Soberano firma v3.2** y ordena empezar por B.1a (FTS5).
Ejecutado el mismo día: ver `sprint_mañana.md` §5, tarea 3.

Queda **sin responder** la segunda pregunta del sprint: si se alinean el Doogee y
`aurelius-mvp` con `origin/main` antes del ticket a GitHub Support. Mientras no se
responda, los dos clones siguen pudiendo resucitar el blob de 3,54 MB.
