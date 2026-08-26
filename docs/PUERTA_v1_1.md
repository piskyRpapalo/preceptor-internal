# PUERTA DE LA v1.1 · lo que se comprueba antes de etiquetar

**Fecha:** 2026-08-26 · **Estado:** PROPUESTA. Firma el Soberano (F14).

Tres de estos puntos los propuso el **27B local** y no yo, y se marcan como
tales: son las tres que aportó de verdad sobre las cinco preguntas que se le
hicieron. El resto sale del plan de fase.

## Automático · la tanda tiene que estar verde

- [ ] `bash bin/pruebas` en verde, con su cifra escrita en el informe.
- [ ] Cero fugas de idioma **en las dos direcciones** (`test_idioma`, las dos
      guardias de cara).
- [ ] Personalidad: se presenta una vez y no se repite (`test_conversacion`,
      incluido el caso de memoria fresca sin modelo).

## Del cerebro local · adoptadas

- [ ] **Filtro de consentimiento en la capa de datos.** Rechazar toda consulta
      de «memoria activa» que no filtre por estado de consentimiento — guardia
      estructural, no convención. Hoy la regla existe por disciplina; esto la
      pone en el motor.
- [ ] **Prueba de migración 1.0 → 1.1.** Abrir una `memory.db` creada por la
      v1.0 con el código de la v1.1 y comprobar que no se pierde una fila.
      Nadie la había pedido, y una memoria portable que se rompe al actualizar
      deja de ser portable.
- [ ] **Terminal ficticia contra patrón exacto**, nunca contra texto libre: un
      paso no puede darse por aprobado con una entrada ambigua.

## Del producto · lo que promete el README

- [ ] `version` idéntica en los dos dispositivos (F12).
- [ ] Gate de novato pasado en el Doogee (F9).
- [ ] QA nocturno: dos noches seguidas sin hallazgos de severidad alta (F13).
- [ ] README y capturas al día (F8).
- [ ] `dist/` construido y los `INSTALACION_*` al día.

## Auditoría de sencillez

- [ ] Toda función que no se explique en una frase en el README se corta o se
      marca `[sleeping]` para la v1.1.

> El criterio lo pone el carbono. Cuando esta pregunta se le hizo al cerebro
> local, devolvió veredictos en vez de criterios — está anotado en la bandeja
> como fuera de carril, con su motivo.
