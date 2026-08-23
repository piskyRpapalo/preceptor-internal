# Integración en el producto · el parche, sin aplicar

**No he tocado `aurelius.py`.** El producto está publicado, es biblioteca
estándar y hoy pasa 344 pruebas. Meterle el punto de anclaje de una forja que
todavía no tiene entrenador elegido sería construir el desagüe antes que la
casa. El parche está escrito y medido; se aplica cuando la Fase 0 dé veredicto.

## Dónde engancha, exactamente

`aurelius.py:771`, dentro de `main`, hoy:

```python
        modelo = os.path.join(str(_casa.raiz()), CEREBRO.destino)
        return charla(a.db, motor=motor, motivo=motivo, modelo=modelo)
```

Propuesto:

```python
        base = os.path.join(str(_casa.raiz()), CEREBRO.destino)
        eleccion = _motor_afinado.elegir(_casa.raiz(), base)
        if eleccion.cual == "afinado":
            print(tx(idioma, "cerebro_afinado", motivo=eleccion.motivo))
        return charla(a.db, motor=motor, motivo=motivo, modelo=eleccion.ruta)
```

Más el import junto a los demás, y **una clave nueva en las dos columnas de
`textos.py`** — `cerebro_afinado`, en `en` y `es`. Una sola columna la caza el
caso 10 de `test_idioma.py`, que es exactamente para lo que existe.

## Lo que el parche NO hace

* **No toca `CEREBRO`.** La pieza del catálogo, su URL y su sha256 firmado se
  quedan intactos. El afinado es una pieza distinta que vive al lado.
* **No toca `descarga.py`.** `presente(CEREBRO)` sigue significando lo mismo.
* **No reinicia nada.** No hace falta: `motor_llama` lanza el proceso hijo en
  cada turno, así que el turno siguiente ya coge el fichero nuevo. El
  «hot-swap sin reinicio» de la Fase 4 sale gratis por cómo está construido el
  producto — no hay que añadirle nada.

## Pruebas que el parche debe traer consigo

Cada cambio trae una prueba que falla sin él. Cinco, sobre `motor_afinado`:

1. Sin registro → elige base, y lo dice.
2. Afinado declarado y verificado → elige afinado.
3. Afinado declarado, fichero ausente → base.
4. **Afinado presente con huella que no cuadra → base.** Es la que protege la
   promesa de integridad; si alguna se salta, que no sea esta.
5. Tras `rollback()` → base, aunque el afinado verifique.

Las cinco se ejercitaron a mano el 2026-08-20 y las cuatro rutas de `elegir()`
se comportan. Como pruebas de `unittest` se escriben al aplicar el parche, para
que entren en el mismo commit que el código.

## Efecto en la línea base

Suma una suite (`test_afinado.py`) al árbol. **Recuerda que `bin/pruebas` solo
mira 13 de las 26 suites** (S3 de PENDIENTES): si la nueva no entra en su lista,
nacerá invisible para el corredor que canta verde.
