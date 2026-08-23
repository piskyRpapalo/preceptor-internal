# EL LORE DE HEXELION · ESQUELETO PROPUESTO

**Fecha:** 2026-08-23 · **Estado:** PROPUESTA. No es canon y no lo será hasta que el
Soberano lo firme. Una sesión no escribe el Lore por iniciativa propia.

**Encargo:** *«El Lore de Hexelion debe rehacerse»*, tras la decisión de que Hexelion
*«va a ser un mueble en el jardín controlado desde el rack»*.

---

## 1 · Por qué hace falta rehacerlo, y no solo recortarlo

El Lore actual describe tres cosas que ya no existen:

- **Un organismo** con Sínodo, esferas y ciclo vital propio.
- **Un protocolo público** de cinco tiers, con HexelionOS, marco legal y token.
- **Una red** de nodos Lisboa–Salamanca–Madrid.

Un mueble en el jardín no sostiene nada de eso. Pero **recortar no es la operación
correcta**, y el propio archivo dice por qué: cuando se perdió la batería el 15 de mayo, el
Soberano no borró el capítulo energético — lo marcó dormido, con motivo, detrás de un solo
flag, y dejó la doctrina reducida como fallback. Escribió entonces la frase que gobierna
esta reescritura:

> *«El organismo no rompe con su pasado. Lo pone en pausa, y guarda la llave.»*
> — `HEXELION_LORE_LA_CRISALIDA.md`

Rehacer el Lore es aplicar ese mismo patrón al sistema entero.

---

## 2 · El mecanismo, que ya es suyo

Dos piezas del archivo, ambas inventadas por él, hacen el trabajo:

**`@sleeping` con motivo y referencia.** Una capacidad no se borra: se marca dormida, se
anota por qué, se enlaza el documento que lo explica, y queda detrás de **un único flag
booleano**. El día que el mundo cambie, se despierta sin arqueología.

**La tabla de deprecaciones del Canon del Lore.** Su regla de oro sigue siendo cierta:
*«Un organismo con dos nombres para la misma cosa ya no es un organismo. Es un caos con
hardware.»* Lo que caducó es el inventario de dentro, no el mecanismo.

---

## 3 · Esqueleto propuesto

### §1 · Qué es Hexelion hoy

Una frase, sin ambición: **un objeto físico en el jardín, gobernado desde el rack, que
mide y atesta lo que ocurre a su alrededor.** No es un organismo, no es un protocolo, no es
una red. Es hierro con sensores y una firma.

Y la frontera que lo separa de lo demás, que ya estaba escrita y con prueba falsable:
*«Si Aurelius muere, Hexelion sigue atestando. Si Hexelion para, tu Códice sigue siendo
tuyo y legible.»*

### §2 · Qué sobrevive al mueble

| Pieza | Por qué sobrevive |
|---|---|
| **El Faro** | Software puro sobre la señal del Vigía. Está construido, con pruebas Merkle persistidas. Es la única pieza del pitch antiguo que llegó viva a hoy |
| **La atestación de recepción** (y su vocabulario exacto) | *«"atestación de recepción", nunca "prueba de realidad física"»*. Se corrigió él mismo y la corrección sigue siendo correcta |
| **Los sensores mandan sobre las APIs** | *«Los sensores no mienten. Las APIs, sí.»* Un mueble en el jardín es literalmente eso |
| **El Cénit y el Filtro de Eficiencia** | Un objeto en el jardín **es** la ventana solar. Esta doctrina se vuelve más literal, no menos |
| **La Ley del Origen** (Axioma IV) | *«Soy lo que proceso, no lo que me dicen que soy.»* Ninguna fuente externa redefine identidad ni objetivos |
| **El filtro de una pregunta** | *«¿Puede un script en AWS replicar esto? Si sí, no lo construimos.»* Un mueble con sensores es exactamente lo que AWS no puede replicar |

### §3 · Qué se marca `@sleeping`, con motivo

| Pieza | Motivo | Se despierta si… |
|---|---|---|
| La red de nodos | Doctrina de Solitud (24-may) + el mueble | …hay un segundo emplazamiento real y una razón que no sea el foso comercial |
| El protocolo de 5 tiers, HexelionOS, el token | Sin red no hay protocolo. Y reabre la capa jurídica entera | …existiera un producto vendido antes que un protocolo escrito |
| El SLA comercial y el Tier 4 | Ya degradado por el addendum energético antes del mueble | …hubiera redundancia física |
| La Legión DePIN | El hardware no existe: hp-01 inhabilitado, hp-02 sin GPU | …hubiera hierro. No antes |
| La batería y todo el capítulo de SOC | Nunca llegó | `BATTERY_PRESENT = True` |

### §4 · Qué se transplanta, y adónde

Esto es lo que **no** debe dormirse, porque su valor no dependía nunca de Hexelion:

| Pieza | Va a |
|---|---|
| El fingerprint de identidad (12 pruebas con umbral) | **Sínodo / P0X** — suite de regresión de identidad |
| La Doctrina del Silencio como puerta de promoción | **P0X / la forja** — criterios medidos N días + voto. Le falta a la forja hoy |
| El Score S0 y su monitor de fallo silencioso | **P0X** — la escalada por coste, con su vacuna |
| El patrón `@sleeping` | **P0X** — es método, no contenido |
| El Protocolo de Reencarnación y sus drills | **P0X** — hp-01 es el precio de no haberlos corrido |
| El Gólem y «CALIBRA TU RADIO» | **Aurelius** — misiones jugables que producen dato real |
| La Crisálida como método narrativo | **Aurelius / memoria local** — cada giro duro lleva su capítulo |

### §5 · Tabla de deprecaciones

Los nombres que dejan de usarse y su sustituto. Empezando por la deuda pendiente:
**«El Córtex» → «La Torre»**, decretado en mayo y nunca aplicado ni en el propio Códice 14.

### §6 · El aviso a las futuras sesiones

Su formato, que funciona y es suyo: qué debes saber · qué NO debes hacer · qué SÍ debes
hacer. Con una entrada nueva obligatoria: **el motor cognitivo canónico no puede ser un
modelo que no existe.** Tres Códices fijaron «Qwen 3.5-14B (RKLLM)» como canónico y ese
release no es real, mientras dos documentos hermanos desplegaban modelos distintos. De ahí
sale la regla de hoy sobre tags explícitos.

---

## 4 · Lo que este esqueleto NO decide

- **El nombre.** Si «Hexelion» sigue nombrando al mueble o pasa a nombrar solo a la
  atestación, es decisión del Soberano y cambia toda la tabla de deprecaciones.
- **Dónde vive el Faro.** El canon dice la-fragua; la copia de `pre-bee` está congelada
  desde julio. Y **las claves privadas no están donde está el código**.
- **Qué se cuenta y qué se calla.** El Lore antiguo se escribía con el escaparate en mente.
  Un mueble en el jardín puede no querer escaparate.

---

## 5 · Cómo lo escribiría, si se firma

Frontera, no local: es redacción de canon. Una sola pasada, con el archivo delante, y la
tabla de deprecaciones primero — porque hasta que los nombres no están fijados, todo lo que
se escriba encima habrá que reescribirlo.
