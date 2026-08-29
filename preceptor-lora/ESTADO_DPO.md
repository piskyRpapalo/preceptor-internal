# Estado del DPO · 2026-08-21

Sesión al límite de presupuesto. Solo pasos 1 y 2. **DPO no se lanzó.**

## 1 · Propagación · OK

Los 18 `elegido` firmados por el Soberano viajaron **verbatim** de
`datos/MITADES_QUE_FALTAN.md` a `datos/negativos.json`. Extraídos por patrón y
escritos tal cual; ni una palabra tocada.

| | |
|---|---|
| Mitades propagadas | **18** (9 casos × 2 idiomas) |
| R8 · pares mancos | **0** — antes eran 18 |
| `entrenar_dpo.py` | `pares completos: 18 · mancos: 0` |
| Guardián Fase 1 | **VERDE** (29 avisos R7, ninguno bloquea) |
| Dataset | 228 registros · 114/114 EN/ES · 72,5 KiB |

`construir_dataset.py` deja de escribir `"elegido": ""` y toma el campo del
fichero de datos, que es donde vive el contenido desde que las familias se
firmaron.

## 2 · Validador · VERDE · **Capa 1, higiene LÉXICA**

`forja/validar_mitades.py`, siete reglas firmadas.

**Su trabajo es uno: que los 18 `elegido` estén limpios antes de entrenar.**
**18/18 pasan.** Eso es el resultado; lo demás es diagnóstico del instrumento.

Comprobado además lo que **no** debe marcarse:

| | |
|---|---|
| «no puedo decirte si todo el árbol pasa» | **pasa** |
| «I can't tell you if the whole tree passes» | **pasa** |
| «…grupos de pruebas… están validados…» | **pasa** |
| «…test groups… are validated…» | **pasa** |

La regla de evasión mira **el verbo que sigue** al «no puedo», no el «no puedo».
Negarse a afirmar lo que no se ha mirado es el sensor honesto; cerrar la puerta
sin decir por qué es lo que se caza.

### Los rechazados no son cobertura, son falsificación

Pasar el validador por los 18 `rechazado` sirve para **una** cosa: demostrar que
tiene dientes, porque un validador que aprueba todo puede estar simplemente
roto. Caza **9 de 18**, y con eso queda demostrado.

**Los 9 que no caza no son un hueco.** Los rechazados son la mitad negativa del
par: ya son el ejemplo de lo que no se quiere, y no hace falta que una regla
léxica los señale para que cumplan su función en DPO.

Y no los caza porque **sus rupturas no son léxicas**, cada una con su capa:

| Sin cazar | n | Ruptura | Quién la mide |
|---|---:|---|---|
| F3 · saludo-de-cierre, memoria sin consentir, idioma dos veces | **6** | momento y estructura | el **tester conductual** post-DPO |
| F1 · voseo | 2 | registro dialectal | no es lista negra |
| F1 · relleno EN — «We go way back» | 1 | idioma distinto al firmado | fuera de la lista literal |

**Corrección de cuenta sobre la lectura recibida:** F3 aporta **6**, no 4 — son
tres casos en dos idiomas. El reparto es 2 + 1 + 6 = 9. La lectura por capas no
cambia; la cifra sí, y aquí se anexa la medida.

## 3 · Lo que queda

**DPO PENDIENTE: lanzar con presupuesto fresco (tras reset semanal).**

Todo lo que necesita está en su sitio y verificado:

- `forja/entrenar_dpo.py` · cerrojo doble, ya sin bloqueo por pares mancos.
  Ahora solo espera la bandera.
- Referencia por `disable_adapter()` · pico ~9 GiB en vez de 16.
- `pruebas/humo_dpo.py` · instrumento verificado: margen +0,0000 → +15,1095.
- 18 pares completos, firmados y validados.

**Orden sugerido cuando haya presupuesto:** DPO desde el base (aísla la
pregunta), tester completo, y la comparación de EC-2.4 contra `−0,1421` de r=8
y `−0,1052` de r=4. Si el margen cruza cero, el canon aprendió a decir que no.

**Sin tocar, como se ordenó:** DPO, tester, push, `LORE.md`, `ARQUETIPO.md`, el
Doogee.
