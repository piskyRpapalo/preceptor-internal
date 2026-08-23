# EL FARO · ESTADO FINAL (2026-08-23)

**Decisión del Soberano:** Opción B (documentar, no tocar).
**Fecha de decisión:** 2026-08-23
**Próxima revisión:** cuando haya cliente MCP real o fallo del servicio.

## Dónde vive
- Nodo: la-fragua (100.82.94.83, usuario ubuntu)
- Ruta: ~/hexelion/faro/
- Servicio: hexelion-faro.service (systemd, enabled)
- Puerto: :8100 (HTTP público)
- Uptime al documentar: 4+ días sin interrupción

## Qué sirve
Endpoints públicos: /health · /selftest · /manifest · /price · /ships/live · /ships/attested · /v1/attested · /v1/credits/claim · /.well-known/hexelion-attestation.json
Modo: Testnet (agung, chain_id 9990), DRY_RUN, firma ed25519 real.

## Claves
- Privadas en la-fragua con permisos 0600 (no se leen, no se copian, no se tocan)
- Públicas viajan en el repo

## Quién lo mantiene
Hoy: nadie (deuda declarada). Cuando falle: el Soberano decide si reparar o @sleeping.

## MCP en :8200
Código escrito pero no levantado como servicio. Se levanta cuando haya cliente MCP real.

## Incoherencia de identidad (deuda menor)
El .well-known declara node: hexelion.near (mainnet) pero opera en testnet.
Fix propuesto (no aplicado): sed sobre el campo node + restart del servicio.

## Contexto del Paso 1 (peaq)
El plano de junio estaba equivocado: UMT es reloj PTP (no token), y peaq Verify Tier 2/3 no existen hoy.
El Faro ya cumple Tier 1 sin construir nada nuevo.

## Cuándo cambiar esta decisión
- Encender MCP: cuando haya cliente MCP real.
- @sleeping: si falla y no hay tiempo de reparar, o si Hexelion se reduce a mueble.
- Fix identidad: en próxima revisión o si hay confusión.
