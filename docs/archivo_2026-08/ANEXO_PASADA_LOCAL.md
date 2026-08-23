# ANEXO · ÍNDICE DE LA PASADA LOCAL

**Fecha:** 2026-08-23 · **Cerebro:** Qwen3-Coder-30B-A3B Q4_K_M en `soberano`
**Documentos:** 225 de 231 · **Método:** un JSON por documento, esquema forzado con
`--json-schema`, ~36 s cada uno.

Este anexo completa la [CLASIFICACIÓN](CLASIFICACION.md), que cubre los 81 documentos
leídos con token de frontera. Aquí están los demás: operación de Hexelion, prompts de
sesión y sueltos.

---

## Qué de esta pasada es fiable y qué no

**Fiable:** el reparto por proyecto y por tipo, y el resumen de una línea. Sirven como
índice para encontrar un documento sin abrirlo.

**NO fiable, y no se publica como dato:**

- **La bandera «quedó a medias»** marcó 182 de 225 (81 %). No es que haya 182 proyectos
  abandonados: el modelo la activa con cualquier documento que *mencione* pendientes.
  En la muestra revisada marcó como inacabados un documento de reglas de seguridad y un
  registro de elementos descartados — que por su naturaleza enumeran pendientes sin estar
  ellos mismos a medias. **Un 81 % no es una medición, es un sesgo del clasificador.**
- **Las «ideas clave»** salen parafraseadas distinto en cada documento, así que no agregan:
  contadas, todas aparecen una sola vez. Sirven dentro de su ficha, no como corpus.

Se dice porque publicar «182 planes abandonados» habría sido un titular falso extraído de
un dato real mal leído — exactamente lo que este equipo de lectura existe para evitar.

**6 documentos no produjeron resumen** (binarios que no convirtieron, o JSON inválido tras
el reintento). No se ocultan: faltan.

---


## AURELIUS · la app de aprendizaje · 17 documentos


### doctrina (5)

| documento | fecha declarada | qué es |
|---|---|---|
| `Auriculando al Silicio_ Una Hoja de Ruta Auditable para el Filtro de Privacidad de Aurelius según la Ley de Desobediencia Verificable.md` | NO_DATA | El documento propone la Ley de Desobediencia Verificable como marco para gestionar discrepancias entre órdenes y reglas superiores en el desarrollo del filtro de privacidad de Aurelius. Pres |
| `PRECEPTOR_REVIEW_TIPS_EXTERIORES_17AGO2026.md` | 17 AGO 2026 | El documento analiza el cumplimiento regulatorio del EU AI Act y NIST para Aurelius, destacando la falta de documentación de compliance y safety case. Propone integrar telemetría energética  |
| `aurelius-estado-v1.8-v2.txt` | NO_DATA | Este documento especifica la estructura de la base de datos relacional de Aurelius V1.8, con tablas para engramas, sensores, cadenas de bloques, pares de malla y registros de interacción. In |
| `aurelius-estado-v1.8.txt` | NO_DATA | Este documento especifica la arquitectura y filosofía del sistema Aurelius, un preceptor educativo local-first basado en la filosofía socrática. Describe su enfoque en la soberanía del usuar |
| `MVP_V1_PLAN.md` | 2026-08-16 | El documento analiza el estado del MVP v1 de Aurelius, señalando que la mayoría de lo que el brief indica como faltante ya está implementado en el repositorio público. Se destacan dos bloque |

### informe_estado (5)

| documento | fecha declarada | qué es |
|---|---|---|
| `AURELIUS_MoX_ANALYSIS.docx` | NO_DATA | El documento analiza oportunidades de negocio derivadas del catálogo de skills de Aurelius, una arquitectura de confianza computacional. Se identifican 10 oportunidades con un MoX promedio d |
| `Aurelius en Movilidad_ Un Marco para Transformar a un Intermediario Cognitivo Autónomo en Hardware de Borde.md` | NO_DATA | Este informe propone adaptar el modelo LoRA Aurelius, basado en Qwen2.5-1.5B-Instruct, para que funcione como un intermediario cognitivo autónomo en hardware de borde. Se enfoca en optimizar |
| `Aurelius_Sovereign_Preceptor.pdf` | NO_DATA | El documento presenta el estado actual del proyecto Aurelius, enfocado en la creación de una aplicación de aprendizaje. Detalla los avances en el desarrollo del sistema educativo y su integr |
| `Estudio Final_ Objetivos y Alcance del Producto Aurelius-MVP.md` | NO_DATA | Aurelius-MVP es un filtro de privacidad plug-and-play que protege los datos sensibles al prevenir la exposición accidental de información crítica en los prompts antes de enviarlos a LLMs ext |
| `aurelius_pendiente_silver.txt` | 2026-08-06 | El documento enumera cinco deudas técnicas en el componente M5Stack relacionadas con la conexión serie-redis. También menciona problemas con el sensor de temperatura en Beelink Ryzen, la aus |

### otro (1)

| documento | fecha declarada | qué es |
|---|---|---|
| `SINTESIS_AURELIUS_MVP_POV.md` | 2026-08-12 | Este documento sintetiza la adaptación del marco Aurelius a la realidad actual de P0X, enfocándose en la estructura del cuerpo, la meditación up/down, el TTS local y el dataset R01. Se mapea |

### plan (6)

| documento | fecha declarada | qué es |
|---|---|---|
| `Aurelius,plan.odt` | NO_DATA | El documento presenta el plan de aprendizaje de Aurelius, enfocado en la soberanía digital mediante la alfabetización física. Se define un módulo fundacional llamado 'El Abecedario' que exig |
| `ESTRATEGIA_MARKETING_CATASTROFISTA_AURELIUS.md` | NO_DATA | El documento presenta una estrategia de marketing para Aurelius basada en el riesgo de agentes de IA autónomos que pueden actuar sin permiso, usando casos reales como ejemplos. Propone una a |
| `Plan Integral para Aurelius Evolucionado_ Orquestación de Agentes en Edge con LongHorizon Harness y BigBang v1(1).md` | NO_DATA | Este documento propone evolucionar el sistema Aurelius hacia una arquitectura de agentes autónomos en entornos edge, usando patrones como LongHorizon Harness y BigBang v1. Se enfoca en la se |
| `Plan Integral para Aurelius Evolucionado_ Orquestación de Agentes en Edge con LongHorizon Harness y BigBang v1(2).md` | NO_DATA | Este documento propone evolucionar el sistema Aurelius hacia una arquitectura de agentes autónomos en edge, usando patrones como LongHorizon Harness y BigBang v1. Se enfoca en la seguridad,  |
| `aurelius_nuevas_skills_gold.txt` | NO_DATA | Este documento describe un plan de desarrollo para el proyecto Aurelius, estructurado en rondas y fases, que define habilidades y objetivos clave para el aprendizaje y la arquitectura del si |
| `Plan Integral para Aurelius Evolucionado_ Orquestación de Agentes en Edge con LongHorizon Harness y BigBang v1.md` | NO_DATA | Este documento presenta un plan para evolucionar Aurelius hacia una arquitectura de agentes autónomos en entornos edge, usando los patrones LongHorizon Harness y BigBang v1. Se enfoca en la  |

## P0X · doctrina y organización del conjunto · 155 documentos


### auditoria (2)

| documento | fecha declarada | qué es |
|---|---|---|
| `HEXELION_CLAUDE_CODE_AUDITORIA.md` | 24 Mayo 2026 | Documento describe una auditoría completa del sistema HEXELION, incluyendo hardware, red, servicios, almacenamiento y estado de contenedores. Se ejecuta en múltiples nodos (La Fragua, La Tor |
| `PROMPT_Auditoria-Nodos_LaTorre-ElVigia-LaLegion.md` | NO_DATA | La auditoría tiene como objetivo reconciliar el estado documentado con el desplegado en tres nodos: La Torre, El Vigía y La Legión, sin realizar cambios. Se enfoca en diagnosticar un error 5 |

### doctrina (48)

| documento | fecha declarada | qué es |
|---|---|---|
| `Decretos P0X para Aurelius en Movilidad_ Validación de Fricción, Arquitectura Secuencial y Calidad Jerárquica del Dataset.md` | NO_DATA | El documento establece una gestión proactiva de la fricción en el desarrollo de Aurelius en Movilidad según la doctrina P0X. Propone clasificar los problemas en críticos, medios y bajos para |
| `capas-aurelius-jardin.md` | NO_DATA | El documento describe la arquitectura de tres capas para el proyecto p0x, enfocada en la inmutabilidad de datos y la gestión de la memoria cognitiva. Propone una estructura jerárquica inspir |
| `Auriculando al Silicio_ Una Hoja de Ruta Auditable para el Filtro de Privacidad de Aurelius según la Ley de Desobediencia Verificable.md` | NO_DATA | El documento propone la Ley de Desobediencia Verificable como marco para gestionar discrepancias entre órdenes y reglas superiores en el desarrollo de un filtro de privacidad para Aurelius.  |
| `CHECKPOINT_COWORK_MVP.md` | 2026-08-16 | Se realiza una auditoría del MVP v1 de p0x, revisando el plan, correcciones en el código y la falta de implementación de hashes de seguridad. Se identifican problemas en la configuración del |
| `EMPAQUETADO_MVP_V1.md` | 2026-08-13 | El documento describe el empaquetado del MVP v1 de 'aurelius', especificando el peso base del producto, los componentes opcionales que se descargan con consentimiento, y las reglas para un R |
| `POST_VERIFICACION_FASE0_B.md` | 2026-08-12 | Documento de post-verificación de la Fase 0 del filtro de privacidad para el Agente B. Se realiza un test-first sin publicar nada. Todos los tests fallan porque el módulo 'guardrails.py' aún |
| `OLEADA_VISUAL_RESUMEN.md` | Agosto 2026 | El documento resume el estado actual del sistema p0x tras completar la 'Oleada Visual', destacando su arquitectura visual con elementos metálicos y tonos violeta, así como nuevas capacidades |
| `CLAUDE_CODE_COSECHA_V1.md` | 21 Mayo 2026 | Este documento define el módulo económico de Hexelion v1, centrado en la cosecha de recursos de diferentes protocolos. Propone un widget en el dashboard y una página dedicada para visualizar |
| `CLAUDE_CODE_SINODO_V1.md` | 21 Mayo 2026 | Documento describe la implementación del sistema Sínodo v1 con agentes IA en Hexelion. Define la arquitectura de comunicación con Ollama y Redis. Incluye endpoints y system prompts para seis |
| `Dashboard nano.txt` | NO_DATA | Se propone un rediseño del dashboard del Nexo organizado en cuatro secciones: Escucha, Prueba, Sostén y Rumbo. Se establece un principio de procesos donde cada uno tiene descripción, estado  |
| `IDeas.txt` | NO_DATA | El documento propone ajustes en la arquitectura del dashboard, incluyendo cambios en la disposición de cuadros y la visualización de datos. Se sugiere una reorganización de elementos como lo |
| `ARQUITECTURA_Cerebro_Pedagogico_P0X.md` | NO_DATA | Este documento define la arquitectura del Cerebro Pedagógico de P0X, una estructura en capas para gestionar el aprendizaje del Soberano. Establece cuatro capas lógicas: abstracción de datos, |
| `CLAUDE_CODE_HOTFIX_MOBILE_CIRCUIT.md` | 21 Mayo 2026 | Se describen tres fixes quirúrgicos para el dashboard de Hexelion: ajustes responsive para móviles, implementación de un circuit breaker para Ollama en el sínodo y adaptaciones específicas p |
| `CLAUDE_CODE_PROMPT_dashboard_v3.md` | NO_DATA | Este documento describe el refinamiento visual del dashboard v3 de Hexelion, con ajustes finos en el logo y los paneles del footer. Se detallan los cambios necesarios para mejorar la estétic |
| `CLAUDE_CODE_PROMPT_dashboard_v4.md` | NO_DATA | Se describe el refinamiento del dashboard v4 de Hexelion, centrado en la paleta de colores reducida a tres tonos (rojo, verde, blanco) y el cambio visual del elemento LEGION SOL. Incluye ins |
| `DISENO_zona-firma-soberano.md` | NO_DATA | Este documento define el diseño de la zona de firma del Soberano, que incluye dos funciones: el Jurado para votar propuestas y el Buzón de Intents para revisar acciones pendientes. No firma  |
| `DOCTRINA_Hexelion-Hibrido_2026-06-07.md` | 2026-06-07 | Este documento fija la doctrina híbrida de Hexelion, estableciendo la separación entre el plano local (soberanía, firma física) y el plano nube (razonamiento sin claves). Define la prioridad |
| `HEXELION_ANALISIS_JSON_20260506.md` | 2026-05-06 | Se realiza un análisis crítico de manifiestos JSON de Hexelion para identificar conceptos nuevos, descartando aquellos inviables técnicamente o con modelo de negocio incierto. Se proponen ex |
| `HEXELION_BATTERY_FLAG_SPEC.md` | 15 de Mayo de 2026 | El documento especifica cómo se gestionará la transición entre dos eras energéticas en el sistema Hexelion mediante un flag de configuración. Se introduce un mecanismo basado en el flag `BAT |
| `HEXELION_PUNTO_CRITICO_20260515_REFORMA_ENERGETICA.md` | 15 de Mayo de 2026 | El documento describe una reforma energética del proyecto Hexelion que elimina el almacenamiento de energía mediante baterías, adaptando la arquitectura a una nueva realidad física. Se intro |
| `HEXELION_SESION_20260504_VISION.md` | 2026.05.04 | Este documento establece la visión estratégica del proyecto Hexelion, definiendo tres capas distintas: el organismo personal del Soberano, Hexelion Lisboa (mvp) y el protocolo público. Se un |
| `INSTRUCCIONES_PROYECTO_hexelion-lab.md` | NO_DATA | Este documento establece las reglas operativas para el laboratorio hexelion-lab, donde se desarrollan protocolos y estrategias futuras bajo la guía del Soberano. Define el rol del cofundador |
| `PROCESO_EVALES_TRANSPLANTE_P0X.md` | 2026-07-04 | Este documento describe el proceso de evaluación y transplante de modelos en el marco de P0X, centrado en la persistencia del conocimiento a través de datasets y suites de evaluación. Establ |
| `PROMPT_CLAUDE_CODE_FASE1_FARO.md` | NO_DATA | Este documento establece las reglas de seguridad para la fase 1 de desarrollo de 'El Faro', una superficie M2M monetizable en Hexelion. Se detallan las reglas inmutables para evitar llamadas |
| `PROMPT_CLAUDE_CODE_FIX_BOTON_NEXO.md` | NO_DATA | Se corrige un enlace roto en el botón 'volver al Nexo' de la página catastro.html, que apuntaba a una ruta inexistente y causaba un error 404. El cambio consiste en hacer que el botón apunte |
| `PROMPT_CLAUDE_CODE_SESION_AUTONOMA.md` | NO_DATA | Este documento establece las reglas para la ejecución autónoma de tareas en el proyecto Hexelion bajo supervisión de diseño, con énfasis en la seguridad y control de cambios. Describe las lí |
| `PROMPT_CLAUDE_CODE_SESION_AUTONOMA_v2.md` | NO_DATA | Este documento establece reglas para una sesión autónoma de trabajo bajo supervisión, con énfasis en la seguridad y el aislamiento del entorno. Define las ramas de git a usar, las líneas roj |
| `PROMPT_CLAUDE_CODE_VIGIA_ANTENAS_RESET.md` | NO_DATA | El documento describe la instalación de una nueva antena ADS-B que interrumpió la señal AIS, y propone soluciones para evitar conflictos entre dispositivos SDR. Se establecen reglas de segur |
| `PROMPT_MAESTRO_BucleB-Paso0_Logger-consumo-NVMe.md` | NO_DATA | Este documento describe el Paso 0 del Bucle B, enfocado en capturar una línea base de consumo real y append-only en NVMe. Se enfoca en leer datos de NUT y proxies sin control físico, manteni |
| `PROMPT_MAESTRO_Nexo-Rediseno_4-secciones.md` | NO_DATA | El documento describe un rediseño de la arquitectura de información del sistema Nexo, reorganizando su estructura en cuatro secciones basadas en verbos planos que indican qué hace el sistema |
| `brief_pagina_publica_fable.md` | NO_DATA | Este documento es un brief de diseño para una página web estática que presenta la identidad y narrativa del proyecto HEXELION. Describe el concepto de un microestado digital soberano que per |
| `fable_pagina_ingles.md` | NO_DATA | Se requiere la versión en inglés de una página web llamada hexelion.html, manteniendo el diseño y la estructura originales. Se enfatiza en un tono sobrio y honesto, sin hype. Se mencionan el |
| `prompt_dashboard_fable.md` | NO_DATA | Propuesta de evolución del dashboard Nexo con enfoque en la observabilidad del Arnés, incluyendo nuevos paneles para Freno Térmico, Vigilia Nocturna y deliberaciones del Sínodo. Se mantiene  |
| `vlan-rules_conf.txt` | 2026.14 | Este documento define la arquitectura de red y segmentación VLAN para HEXELION, especificando las subredes, IPs fijas, puertos y reglas de firewall entre las diferentes VLANs. Establece un s |
| `Vault.txt` | NO_DATA | El documento define la arquitectura del 'Hexelion AI Vault' como un sistema de hardware autónomo para la validación y sellado de datos en entornos de baja potencia. Propone un enfoque de 'lo |
| `github lab.txt` | NO_DATA | El documento describe el algoritmo de correlación trinitaria de hexelion-lab, que analiza tres flujos de datos: código (GitHub), consenso social (Polymarket) y hardware (DePINscan) para dete |
| `DESIGN.md` | NO_DATA | Este documento describe el diseño orgánico de Terra con un enfoque en la calma y la conexión con la naturaleza. Propone una paleta de colores tierra con tonos suaves y texturas naturales. Se |
| `DESIGN.md` | NO_DATA | Este documento describe el diseño orgánico de Terra, enfocado en crear una experiencia cálida y acogedora con tonos terrosos y formas suaves. Propone una paleta de colores basada en tonos de |
| `Del Barrido al Borde Inteligente_ Un Manual de Archivo para la Reestructuración de P0X en Torno a la Arquitectura Medallion.md` | NO_DATA | Este documento propone la implementación de la arquitectura Medallion para reestructurar los datos del ecosistema P0X, organizándolos en capas de bronce, plata y oro. Establece los fundament |
| `MAPA_EVOLUTIVO_P0X.md` | 2026-07-18 | El documento presenta el mapa evolutivo de P0X, estructurado en seis frentes con fases y puertas de evidencia. Cada frente tiene una descripción clara, su estado actual y la puerta siguiente |
| `SEGURIDAD_Y_FRENOS.md` | 2026-08-09 | Este documento establece las reglas para los mecanismos de seguridad en P0X, diferenciando entre frenos que detienen acciones, sensores que informan y registros que documentan. Presenta una  |
| `p0x-arquitectura-y-especificaciones-paralelo.md` | NO_DATA | El documento describe la arquitectura y especificaciones del sistema paralelo p0x, enfocado en el aislamiento de directorios y permisos de acceso. Establece reglas estrictas para la escritur |
| `p0x-canon-visual-y-diseno-unificado.md` | NO_DATA | Este documento define el canon visual y el diseño de interfaz para el proyecto p0x, especificando el funcionamiento del switcher de tres caras que permite navegar entre El Nexo, Le Jardin y  |
| `p0x-doctrina-skills-y-repositorios-unificado.md` | NO_DATA | Este documento define la doctrina maestra de p0x, basada en cinco pilares soberanos: soberanía digital, firma humana obligatoria, honestidad de los sensores, fricción física pedagógica y brú |
| `p0x-paper-manifest-v2.txt` | 2026-08-06 | El documento presenta la arquitectura del sistema p0x, basada en cinco pilares soberanos: soberanía digital, firma humana, honestidad de sensores, fricción pedagógica y brújula estoica. Defi |
| `p0x-remediacion-red-tailscale.md` | NO_DATA | Este documento especifica las reglas de seguridad para el sistema paralelo p0x, enfocado en restringir el acceso a través de Tailscale. Establece políticas de bind exclusivo, prohibe el acce |
| `p0x.infra.software.md` | 2026-08-08 | Este documento especifica la infraestructura de software para el proyecto p0x, enfocándose en entornos virtuales, aislamiento de red y seguridad criptográfica. Detalla el uso de entornos vir |
| `p0x.system.pending.md` | 2026-08-08 | Este documento es un archivo técnico que registra elementos descartados del diseño visual y decisiones técnicas rechazadas en el contexto del proyecto p0x. Incluye una lista de componentes v |

### informe_estado (20)

| documento | fecha declarada | qué es |
|---|---|---|
| `SKILL.md` | NO_DATA | Documento que establece las instrucciones para el preceptor del Sínodo v2 en la lectura del estado del proyecto P0X. Detalla los pasos a seguir para revisar la pizarra diaria, los últimos do |
| `De Ollama al Borde_ Una Arquitectura Autónoma y Resiliente para 'Le Cahier' en el Ecosistema p0x.md` | NO_DATA | Este documento propone una re-architectura para 'Le Cahier' que elimina la dependencia de Ollama y se basa en tecnologías locales como llama.cpp y faiss-cpu. Se estructura en tres fases: Le  |
| `De la Teoría a la Práctica_ Un Plan de Acción para la Reestructuración de p0x bajo Medallion y el Canon de Aurelius.md` | NO_DATA | El documento propone reestructurar la carpeta de trabajo p0x bajo la arquitectura Medallion y el canon de Aurelius. Establece un marco para organizar datos en capas Bronze, Silver y Gold, pr |
| `Hoja de Ruta para Claude Cowork_ Supervisión Activa bajo el Canon de Aurelius para la Reestructuración Modular de la Carpeta p0x.md` | NO_DATA | Este documento establece un protocolo de reestructuración para la carpeta p0x, basado en la arquitectura Medallion y el canon de Aurelius. Propone una organización modular de datos en capas  |
| `Hoja de Ruta para la Activación Visual del Dashboard p0x_ De la Arquitectura Medallón al Despliegue Modular.md` | NO_DATA | Este documento presenta una hoja de ruta para activar visualmente el dashboard p0x, utilizando la arquitectura Medallón como marco metodológico. Se detalla la transformación desde un estado  |
| `POST_VERIFICACION_R83b_MVP_PUBLICO.md` | 2026-08-17 | Se verifica el cierre del R83b contrastando el informe de CC con el árbol de archivos. No se encontraron cifras infladas y se confirmó el estado del producto en el commit 6e367b9. Se detectó |
| `POST_VERIFICACION_REFRESH_AURELIUS.md` | 2026-08-12 | El documento evalúa la compatibilidad del vocabulario del MVP de Aurelius con el canon existente, identificando colisiones y problemas de privacidad. Se descubre que solo el 31% del filtro e |
| `Defli ads-b.txt` | NO_DATA | El documento explica cómo crear una cuenta en el portal Defli, vincular una billetera Web3 y configurar un nodo ADS-B para enviar datos. Se describe la descarga del software cliente desde Gi |
| `Gradient.txt` | NO_DATA | El documento describe los requisitos de hardware para participar en Gradient Network, diferenciando entre nodos sentry (nivel básico) y edge hosts (nivel avanzado). Detalla las especificacio |
| `CLAUDE_CODE_DASHBOARD_CAPA1_AUDITORIA.md` | 20 Mayo 2026 | El documento es una auditoría forense del dashboard de Hexelion, con el objetivo de identificar el código fuente que sirve el dashboard en el puerto 5173. Se describen los pasos para localiz |
| `ESTADO_SISTEMA_2026-06-05_hexelion-lab.md` | 2026-06-05 | Este documento es una síntesis estratégica del estado del sistema hexelion-lab, enfocada en la reconciliación entre lo documentado y lo desplegado. Revisa el cumplimiento del ADN del lab, id |
| `INSTRUCCIONES_El-Preceptor.md` | NO_DATA | El documento define el rol de 'El Preceptor' como sistema de aprendizaje personal que adapta contenido a la comprensión real del usuario en tiempo real. Establece principios fundamentales co |
| `PROMPT_CLAUDE_CODE_RECON_20260529.md` | 2026-05-29 | Este documento es un prompt para Claude Code que actúa como órgano del hardware de HEXELION. Su propósito es realizar un reconocimiento completo del estado del sistema (solo lectura) para in |
| `PROMPT_CLAUDE_CODE_RECON_SEGURIDAD.md` | NO_DATA | Este documento es un prompt para un auditor de seguridad que debe revisar tres hallazgos críticos en un entorno de Fragua viva. Se detallan comandos para verificar la existencia de claves de |
| `PROMPT_CLAUDE_CODE_informe-estado-sistema.md` | 2026-06-05 | El documento es un informe de auditoría de estado del sistema HEXELION, centrado en la verificación de la configuración y el cumplimiento del ADN del sistema. Se enfoca en la reconciliación  |
| `PROMPT_Cierre-Auditoria_HP2-LaTorre-Remediacion.md` | NO_DATA | Este documento propone cerrar la auditoría en el contexto de HP2, La Torre y las 13 propuestas identificadas. Describe pasos para verificar el acceso a HP2, evaluar el estado de los servicio |
| `PROMPT_MAESTRO_Verificacion-post-solar_dato-soberano.md` | NO_DATA | Documento que establece las reglas para verificar la integridad del sistema solar post-instalación, asegurando que los datos se manejen de forma soberana y honesta. Propone un enfoque priori |
| `PROMPT_NOCTURNO_Voces-Fase1_Inventario-DePIN.md` | NO_DATA | El documento describe dos tareas autónomas para la noche: construir interacción de voces en el Nexo usando frases pre-renderizadas y generar un inventario read-only del software en cada nodo |
| `TAREAS_ABIERTAS_2026-07-13.md` | 2026-07-13 | Este documento es un inventario de tareas pendientes del proyecto p0x, con un enfoque en el estado de desarrollo del software y tareas técnicas. Incluye tareas cerradas de facto y varias abi |
| `De Ollama al Borde_ Una Arquitectura Autónoma y Resiliente para 'Le Cahier' en el Ecosistema p0x.md` | NO_DATA | El documento propone una re-arquitectura para 'Le Cahier' que elimina la dependencia de Ollama y se basa en tecnologías locales como `llama.cpp` y `faiss-cpu`. Presenta una arquitectura de t |

### investigacion (2)

| documento | fecha declarada | qué es |
|---|---|---|
| `inventario-necropolis-v2.md` | NO_DATA | Este documento describe el inventario físico y lógico del nodo soberano de p0x llamado Le Jardin, ubicado en Lisboa. Incluye detalles sobre hardware, nodos de borde, infraestructura de energ |
| `p0x.infra.hardware.md` | 2026-08-08 | Este documento describe el inventario de hardware y sensores del proyecto p0x, incluyendo nodos activos en terreno como el Beelink SER9 Max, Jetson Orin Nano y Raspberry Pi. Detalla los puer |

### otro (10)

| documento | fecha declarada | qué es |
|---|---|---|
| `MANIFIESTO.md` | NO_DATA | Este documento es un manifiesto que describe un sistema para verificar la integridad y actualidad de los datos de memoria sin revelar su contenido. Proporciona herramientas para generar y ve |
| `ACTA_FINAL_OLEADA.md` | Agosto 2026 | Acta final de la oleada visual del proyecto p0x, que documenta el mapa del ecosistema, el pipeline de datos, los enlaces entre componentes y la doctrina visual aplicada. Incluye detalles téc |
| `Changelog — Sesión 19-20 Mayo 2026.txt` | 19-20 Mayo 2026 | Este documento registra las actividades realizadas durante la sesión 19-20 de mayo de 2026. Incluye el análisis de la doctrina y la organización del conjunto dentro del proyecto p0x. Se deta |
| `HEXELION_TAREAS_20260517.md` | 2026-05-17 | Documento es una lista maestra de tareas para el proyecto HEXELION, actualizada el 17 de mayo de 2026. Incluye tareas urgentes, desarrollo del dashboard, nuevos proyectos como wallets y reco |
| `BRIEF_UI_HEXELION_P0X.md` | NO_DATA | Este documento es un brief técnico para la interfaz de usuario de Hexelion, enfocado en presentar datos de forma read-only y propuesta-only. Define reglas de diseño y contratos de datos para |
| `HEXELION_BACKLOG_TODO.md` | Mayo 2026 | Este documento es un backlog de ideas y tareas pendientes para el proyecto Hexelion, incluyendo conceptos como mantenimiento autónomo, seguros de verdad sintética, monetización del análisis  |
| `HEXELION_DRILL_LOG.md` | NO_DATA | Este documento registra los drills ejecutados durante la vida del organismo Hexelion, incluyendo validaciones de reencarnación, resiliencia, rituales y otras pruebas de integridad. Se descri |
| `juppisky.txt` | NO_DATA | El documento presenta una visión general de la estructura y funcionamiento del conjunto p0x, incluyendo su doctrina y organización. Se centra en la definición de roles y responsabilidades de |
| `blueprint-de-diseno-soberano-v1.4.md` | NO_DATA | Este documento establece las especificaciones técnicas y el canon visual para las interfaces del nodo Soberano, incluyendo el Puente de navegación entre El Nexo, Le Jardin y el Chat. Define  |
| `sugerencias-implementacion.md` | NO_DATA | Este documento actúa como guía de arquitectura para el desarrollo de flujos de trabajo locales y eficientes, enfocándose en la optimización de recursos y la persistencia sin fuga de datos. P |

### plan (8)

| documento | fecha declarada | qué es |
|---|---|---|
| `Architectural Blueprint & Strategic Implementation Plan for CineK Automático.pdf` | NO_DATA | El documento describe la arquitectura del sistema CineK Automático, basado en hardware commodity con CPU solo y sin telemetría solar. El sistema utiliza una máquina de estados para gestionar |
| `REVISION_PLAN_M1.md` | 2026-08-13 | El documento revisa el plan temporal de M1 y identifica tres bloqueos: incompatibilidad de arquitecturas para el LoRA, contradicción con D68 sobre modos de operación, y falta de resolución s |
| `PLAN_M3.md` | 2026-08-15 | El documento propone el plan estructural del M3 (HEGEMONIKON) en el proyecto p0x, que consiste en seis salas para la introspección personal. Describe seis conflictos principales relacionados |
| `PLAN_MISION_MEMORIA.md` | 2026-08-12 | Este documento establece un plan estructural para la misión de memoria en el proyecto Aurelius, centrado en la creación inicial de un sistema de recuerdos. Describe los tres estados iniciale |
| `PLAN_POST_R82.md` | 2026-08-16 | El documento presenta el estado post-R82 del proyecto p0x, destacando tareas pendientes como la ejecución del gitignore y la verificación de archivos. Se mencionan inconsistencias entre el e |
| `PLAN_PhysicalAI_P0X.md` | NO_DATA | Este documento presenta un plan para posicionarse en el campo de la Physical AI, enfocado en la construcción de un laboratorio soberano de borde con sensores físicos, inferencia local y gobe |
| `PROMPT_CLAUDE_CODE_recon-verif-cruzada-lab.md` | NO_DATA | Documento describe un plan de edición para el pipeline de verificación cruzada marítima, incluyendo el mapeo de la realidad del frontend y backend, y la definición de tres estados para la co |
| `p0x.system.pending(1).md` | 2026-08-08 | Este documento es una especificación técnica del sistema p0x, que registra elementos descartados, deudas técnicas y pendientes de implementación. Incluye decisiones arquitectónicas, incident |

### prompt (65)

| documento | fecha declarada | qué es |
|---|---|---|
| `Prompt Maestro para Activación de Ronda de Agentes AI-AI_ Nexo, Le Jardin y Sistema HEXELION.pdf` | NO_DATA | Este documento define un prompt maestro para coordinar siete agentes AI-AI en el ecosistema HEXELION. Propone tres pilares fundamentales: BELIEVE_IN_YOURSELF, KEEP_TRYING_YOU_CAN_DO_IT y NO_ |
| `P0_ACABADOS_MVP.md` | 2026-08-12 | Se propone corregir una fuga de datos en el test de guardrails de Aurelius-MVP, reemplazando nombres reales por un léxico sintético. Se diseña un mecanismo para cargar léxicos reales o sinté |
| `HEXELION_SINODO_FASE1_PROMPT.md` | NO_DATA | Este documento define la estructura inicial del Sínodo de HEXELION, estableciendo el esqueleto del sistema con roles canónicos y topología de despliegue. Describe la arquitectura de los agen |
| `CLAUDE_CODE_COSECHA_V1.md` | 21 Mayo 2026 | Este documento describe el módulo económico de Hexelion, específicamente el widget 'Cosecha' en el dashboard v9 y una página dedicada /cosecha. Detalla la arquitectura del sistema y los prot |
| `CLAUDE_CODE_DASHBOARD_CAPA2_RECONSTRUCCION.md` | 20 Mayo 2026 | Documento describe la reconstrucción visual del dashboard de Hexelion tras una auditoría. Propone una estrategia de commit, branch y reemplazo de componentes obsoletos. Se establece una nuev |
| `CLAUDE_CODE_PROMPT_FASE2_FRAGUA.md` | 19 Mayo 2026 | Documento define las reglas y fases para construir 5 herramientas operativas del organismo hexelion. Incluye diagnóstico inicial del sistema, configuración de servicios y protocolo de report |
| `CLAUDE_CODE_PROMPT_dashboard_v2.md` | NO_DATA | Documento que describe una actualización visual del dashboard de HEXELION, incluyendo cambios en fondos de tarjetas, logo del header y un icono cibernético clickeable. No se toca ningún dato |
| `CLAUDE_CODE_PROMPT_dashboard_v2_REFACTOR.md` | NO_DATA | Este documento describe un refactor estructural del dashboard de Hexelion, cambiando la disposición de los nodos a un grid 2×3 y renombrando los nodos según un lore canónico. Se añade un nue |
| `CLAUDE_CODE_PROMPT_v6_pollers.md` | NO_DATA | Este documento describe el proceso de implementación del servicio de sondeo (pollers) para el proyecto Hexelion v6, que recopila datos de nodos cada 15 segundos y los escribe en Redis. Inclu |
| `PROMPTS_CLAUDE_CODE_reparaciones-chat-y-ADSB.md` | NO_DATA | Este documento describe dos tareas de reparación mínima: primero, reenrutar el chat del Sínodo desde una API obsoleta a una nueva para evitar errores de memoria; segundo, diagnosticar el pro |
| `PROMPT_CLAUDE_CODE_BLOQUE1_SEGURIDAD.md` | NO_DATA | Documento que describe tres parches críticos para mejorar la seguridad del clúster HEXELION, eliminando servicios expuestos como GagaNode, Jupyter Lab y n8n. Cada parche incluye comandos par |
| `PROMPT_CLAUDE_CODE_BLOQUE2_DASHBOARD.md` | NO_DATA | Este documento describe la limpieza y reorganización del dashboard de El Faro, incluyendo la eliminación de servicios innecesarios, la creación de un endpoint para exponer datos reales del s |
| `PROMPT_CLAUDE_CODE_ED25519_Y_PRIVACIDAD.md` | NO_DATA | El documento describe dos tareas para el proyecto p0x: activar la firma Ed25519 en El Faro (off-chain, testnet) y extender el modo privacidad del dashboard para ocultar los paneles de El Far |
| `PROMPT_CLAUDE_CODE_ESCAPARATE.md` | NO_DATA | Este documento es un prompt para Claude Code que define las tareas de mejora del dashboard de escaparate del proyecto Hexelion. Describe cómo debe ser la navegación entre paneles, el manejo  |
| `PROMPT_CLAUDE_CODE_FASE2_FLYWHEEL.md` | NO_DATA | Este documento es un prompt para Claude Code que instruye sobre cómo acumular datos AIS en TimescaleDB, despertar los tres agentes del sínodo (Alquimista, Vocero y Berserker) y corregir el s |
| `PROMPT_CLAUDE_CODE_FIRMAS_DASHBOARD.md` | NO_DATA | El documento describe cómo integrar visualmente las firmas emitidas por El Faro en el dashboard de HEXELION, utilizando Redis como intermediario. Se detallan las tareas para mostrar eventos  |
| `PROMPT_CLAUDE_CODE_INVENTARIO_DEPIN.md` | NO_DATA | Este documento es un prompt para realizar un inventario de recursos DePIN en nodos del clúster HEXELION. Define las reglas para auditoría de contenedores Docker, servicios systemd, uso de CP |
| `PROMPT_CLAUDE_CODE_MERCADER_v01.md` | NO_DATA | Este documento es un prompt para Claude Code que define las reglas y contexto para la ejecución de tareas en el nodo 'La Fragua' del proyecto HEXELION. Establece las fases de trabajo, reglas |
| `PROMPT_CLAUDE_CODE_NEXO_INFRA_LINK.md` | NO_DATA | Se propone hacer clicable todo el panel INFRA · NODES + ENERGY para que redirija a /catastro, replicando el comportamiento de otras cards de acceso directo. Se eliminará el card-botón separa |
| `PROMPT_CLAUDE_CODE_QDRANT_401.md` | NO_DATA | El documento describe un proceso para resolver un error 401 de Qdrant en el backup del Guardián, comparando la clave de API en config/.env con la del contenedor Qdrant. Sugiere validar la co |
| `PROMPT_CLAUDE_CODE_REMEDIACION.md` | NO_DATA | Este documento describe un proceso de remediación para mejorar la seguridad del sistema Hexelion, enfocado en cerrar brechas de acceso no autorizado. Se detallan pasos para ajustar configura |
| `PROMPT_CLAUDE_CODE_build1-cruce-maritimo.md` | NO_DATA | Este documento describe el desarrollo de un sistema de verificación cruzada marítima que compara datos de buques obtenidos tanto por El Vigía como por AISStream, para determinar su estado (c |
| `PROMPT_CLAUDE_CODE_build2-ventana-lab.md` | NO_DATA | Documento que describe las tareas para el build #2 del Lab, enfocado en ajustes de configuración, estética y creación de una ventana de procesos read-only. Se detallan modificaciones en el m |
| `PROMPT_CLAUDE_CODE_decidir-base-dashboard.md` | NO_DATA | El documento establece una tarea de investigación para decidir la base del dashboard, enfocándose en la comparación entre versiones v9 y v10.3-staging. Se requiere confirmar el estado del mo |
| `PROMPT_CLAUDE_CODE_diagnostico-adsb-1090.md` | NO_DATA | Este documento es un prompt para el diagnóstico no destructivo del sistema ADS-B 1090 en El Vigía, utilizando Claude Code vía SSH. Se enfoca en identificar problemas de coexistencia o hardwa |
| `PROMPT_CLAUDE_CODE_extraccion-dashboard.md` | 2026-06-05 | Documento que establece las reglas para extraer el código y las rutas del dashboard (v9 y v10.x) y del Gateway, sin realizar modificaciones. Se enfoca en recopilar información crítica para l |
| `PROMPT_CLAUDE_CODE_nexo-aetheric-privacidad.md` | NO_DATA | Este documento es un prompt para modificar la interfaz del proyecto p0x, específicamente el frontend de Nexo cálido 'Aetheric', incluyendo cambios de tema, estilos, neón, modo privacidad y p |
| `PROMPT_CLAUDE_CODE_nexo-aetheric.md` | NO_DATA | Este documento es un prompt para modificar la interfaz del proyecto 'hexelion', específicamente el archivo 'nexo.html', implementando un tema cálido 'Aetheric' con estética neón y modo priva |
| `PROMPT_CLAUDE_CODE_nexo-deploy-osiris.md` | NO_DATA | Este documento describe las reglas y tareas para desplegar y conectar el Nexo con datos reales en el sistema hexelion, incluyendo la configuración de OSIRIS en modo aislado y la integración  |
| `PROMPT_CLAUDE_CODE_orbes-por-tema.md` | NO_DATA | El documento establece las reglas para mostrar orbes condicionales según el tema (Aetheric o Sovereign) en la interfaz frontend. Los orbes auténticos deben ser optimizados y cargados solo en |
| `PROMPT_CLAUDE_CODE_transporte-adsb-vigia-nexo.md` | NO_DATA | Este documento es un prompt para diagnosticar el flujo de datos ADS-B entre El Vigía y La Fragua, sin modificar el sistema. Se enfoca en confirmar si el decoder ve aviones localmente y local |
| `PROMPT_CLAUDE_CODE_ventana-limpia-vigia.md` | NO_DATA | Documento describe un procedimiento para evaluar la recuperación del sistema AIS tras un reinicio, mediante una medición de ventana limpia. Se enfoca en confirmar recepción de buques y medir |
| `PROMPT_Cierre-dia_sync-MAQUINA-REAL-Nexo.md` | NO_DATA | Este documento describe un prompt para el cierre honesto del día, enfocado en la sincronización del sistema con la realidad actual de los sensores AIS y ADS-B, destacando que ADS-B está desc |
| `PROMPT_FABLE5_El-Arnes_FaseB1.md` | NO_DATA | Este documento es un prompt maestro para la fase B.1 del Arnés, especificando instrucciones e invariantes para la construcción segura y autoritaria del sistema. Se enfoca en la ejecución fís |
| `PROMPT_Fix-USB-drop_Vigia.md` | NO_DATA | Este documento propone solucionar el problema de desconexión USB en El Vigía, causado por el autosuspend de los dongles RTL-SDR. Sugiere desactivar el autosuspend mediante una regla udev y a |
| `PROMPT_MAESTRO_BucleA-Paso1_Activacion-Alquimista.md` | NO_DATA | Este documento describe la activación del Alquimista, un componente del proyecto p0x, que lee balances on-chain de NEAR (mainnet y testnet) sin usar claves ni firmas. El objetivo es que esto |
| `PROMPT_MAESTRO_BucleA-Paso1_Alquimista-lector-keyless.md` | NO_DATA | El documento describe la implementación de un lector keyless para balances on-chain en NEAR, sin claves ni firmas. Se enfoca en leer cuentas públicas mediante RPC público y persistir los dat |
| `PROMPT_MAESTRO_Claude-Code_Semilla-01.md` | NO_DATA | Documento que define las reglas y estructura para construir el esqueleto mínimo del cerebro del lab hexelion-lab. Establece restricciones de seguridad y arquitectura para el código, sin toca |
| `PROMPT_MAESTRO_El-Arnes_FaseB1.md` | NO_DATA | Este documento define la fase B.1 del proyecto 'El Arnés', que constituye el substrato de ejecución, telemetría y contexto para el Sínodo. Establece principios clave como la separación entre |
| `PROMPT_MAESTRO_Semilla-02_FaseA1_Voces-Sinodo.md` | NO_DATA | Este documento define la estructura y funcionamiento de las 'Voces del Sínodo' para el proyecto p0x, especificando el motor deliberativo basado en LLMs con validación estricta. Establece las |
| `PROMPT_MAESTRO_Semilla-02_FaseA2_Orquestador.md` | NO_DATA | El documento describe la implementación del orquestador del Sínodo en la Fase A.2, responsable de gestionar la deliberación de propuestas mediante seis voces y aplicar reglas deterministas p |
| `PROMPT_MAESTRO_Semilla-02_FaseA3-1_Inhibicion-graduada.md` | NO_DATA | El documento describe la fase A.3.1 del proyecto p0x, que corrige un fallo de calibración en el Monje al implementar una inhibición graduada en lugar de un veto binario. Se introduce un bloq |
| `PROMPT_MAESTRO_Semilla-02_FaseA3-2_Modelo-investigativo.md` | NO_DATA | Este documento define un modelo investigativo soberano para el proyecto p0x, basado en seis fases que integran deliberación, evidencia empírica y una compuerta de tres ejes. Establece reglas |
| `PROMPT_MAESTRO_Voces-Sinodo_Fase1_dashboard.md` | NO_DATA | Este documento establece las reglas para la generación y visualización de voces sintéticas del Sínodo en la Fase 1, enfocándose en la creación pre-renderizada de audio y su integración en el |
| `PROMPT_MAESTRO_Voces-Sinodo_dots-tts_Fase0.md` | NO_DATA | Este documento establece las bases para la implementación de voces sintéticas del Sínodo usando el modelo dots.tts, priorizando la factibilidad técnica y la gobernanza ética. Define el alcan |
| `PROMPT_N1_marcos-aetheric.md` | NO_DATA | El documento describe la implementación de cinco marcos-contenedor en el tema Aetheric, específicamente para el rack. Detalla tareas de corte de imágenes, aplicación de marcos a paneles, ver |
| `PROMPT_Nexo_Faro-2.0_panel.md` | NO_DATA | El documento describe la creación de un panel 'Faro 2.0 · Economía-Máquina' para mostrar el estado honesto y estático de un roadmap. El panel refleja la dirección del proyecto sin presentar  |
| `PROMPT_Pasada-Matinal_voces-inventario-membrana.md` | NO_DATA | Este documento establece una serie de tareas seguras para ejecutarse antes de que el Soberano se vaya al tejado, incluyendo generación de audio con espeak, revisión del inventario DePIN y ve |
| `PROMPT_Prep-Solar_pre-Aiko.md` | NO_DATA | Este documento define las reglas y el alcance para la preparación del sistema de telemetría solar en el rack HEXELION antes de la instalación de los paneles Aiko. Establece que todo debe ser |
| `PROMPT_RECUPERACION_nexo-aetheric.md` | NO_DATA | Este documento describe la recuperación y actualización del nexo "Aetheric" con un enfoque en temas cálidos, privacidad y seguridad. Incluye instrucciones para actualizar el dashboard, aplic |
| `PROMPT_Reinicio-Vigia_recuperacion-AIS.md` | NO_DATA | Este documento describe el proceso de reinicio y recuperación del sistema AIS en El Vigía, incluyendo verificaciones previas y post-reinicio para asegurar la correcta decodificación de señal |
| `PROMPT_UPS_SILENCIO_DEFINITIVO.md` | NO_DATA | El documento describe el proceso para silenciar de forma definitiva la alarma de una UPS (Green Cell PowerProof 1000VA) sin desactivar su función de apagado automático. Explica cómo identifi |
| `PROMPT_marcos-finos-velo-contadores.md` | NO_DATA | Se propone afinar los marcos del rack utilizando border-image para evitar que las ruedas crezcan al agrandar el panel. Se elimina el velo cálido que difumina el fondo y se ajusta la legibili |
| `PROMPT_movil-real-interior-transparente.md` | NO_DATA | El documento describe tareas para corregir el diseño móvil del dashboard, asegurando que se aplique correctamente con el viewport adecuado y media queries. También se pide hacer el interior  |
| `PROYECTO_Busqueda-Trabajo_Setup.md` | NO_DATA | Documento que establece las instrucciones para la búsqueda de un trabajo paralelo de David Pecero Caballero, enfocado en roles remotos y sin llamadas. Se enfoca en su combinación única de ex |
| `URGENT_SILENCIAR_UPS.md` | NO_DATA | Este documento describe el proceso para silenciar la alarma de una UPS (Uninterruptible Power Supply) mediante NUT. Incluye pasos para identificar la UPS, verificar su estado, ejecutar coman |
| `prompt_P1_timescale.md` | NO_DATA | Documento que describe un endurecimiento defensivo para TimescaleDB en La Torre, restringiendo el acceso a su puerto 5432 solo a clientes autorizados. Se especifica el procedimiento para apl |
| `prompt_claude-code_esqueleto-lab.md` | NO_DATA | Este documento define la estructura y componentes mínimos para el repositorio hexelion-lab, que actúa como esqueleto del cerebro del laboratorio hexelion. Se detallan los elementos necesario |
| `prompt_nexo_promocion.md` | NO_DATA | Este documento describe el proceso de cableado y promoción de una nueva carcasa para el dashboard Nexo, integrando datos en tiempo real desde endpoints vivos. Incluye pasos de backup, verifi |
| `Nano2.txt` | NO_DATA | Documento con diseño visual de un dashboard de hardware en estilo ciencia ficción. Incluye elementos gráficos con estilos de tecnología futurista y biología digital. Contiene representacione |
| `Nubit light node..txt` | NO_DATA | Este documento explica cómo desplegar un Nodo Ligero de Nubit en infraestructuras ARM o x86_64, con requisitos mínimos de hardware. Detalla los pasos para preparar la red, instalar el nodo m |
| `Orichi network.txt` | NO_DATA | Orochi Network es una infraestructura basada en criptografía de conocimiento cero y cómputo descentralizado, diferente a redes DePIN tradicionales. Para participar, se requiere crear una ide |
| `PROYECTO_Busqueda-Trabajo_Setup.md` | NO_DATA | Este documento establece las instrucciones para la búsqueda de un trabajo paralelo de David Pecero Caballero, enfocado en roles remotos y sin llamadas, que respeten su contrato actual en Cog |
| `Promt Claude.txt` | NO_DATA | Este documento establece las reglas de interacción con el proyecto Claude dentro del contexto de Hexelion. Define un protocolo de sesión riguroso que prioriza el uso de conocimiento existent |
| `Promt nano.txt` | NO_DATA | El documento es un prompt para un diseñador UI/UX experto en estética de ciencia ficción dura y solarpunk, solicitando mejorar un dashboard basado en el proyecto 'HEXELION'. Propone una esté |

## HEXELION · hardware, rack, sensores, dashboard · 50 documentos


### doctrina (12)

| documento | fecha declarada | qué es |
|---|---|---|
| `OLEADA_VISUAL_P0X_GOLD_20260808_042358.md` | 20260808_042358 | Este documento describe la doctrina visual y el diseño del dashboard de Hexelion, con énfasis en la estética y la interacción. Incluye especificaciones técnicas de elementos visuales como pl |
| `CLAUDE_CODE_DASHBOARD_V9.md` | 21 Mayo 2026 | Se define la creación de un dashboard HTML estático autocontenido para el sistema hexelion, sin usar React ni herramientas de build. El dashboard debe consumir datos de endpoints específicos |
| `CLAUDE_CODE_PROMPT_v7_dashboard_live.md` | 18-may-2026 | El documento describe la implementación del dashboard v7 de Hexelion, enfocada en conectar los indicadores de estado de los nodos con datos en tiempo real provenientes del endpoint /api/heal |
| `CLAUDE_CODE_SINODO_V1.md` | 21 Mayo 2026 | Documento técnico que describe la implementación de la vista Sínodo como HTML en el gateway, con chat real conectado a Ollama. Incluye arquitectura, endpoints, reglas de implementación y fas |
| `HEXELION_BITACORA_SESION.docx` | Mayo 2026 | Documento describe el diseño e implementación del mapa marítimo de HEXELION, partiendo de una interfaz básica y funcional hacia una versión interactiva con estelas, rotación de buques y sist |
| `HEXELION_BRIEFING_MAESTRO_20260524_v2.md` | 24 de Mayo de 2026 | Este documento es el briefing actualizado de HEXELION, que presenta una doctrina revisada sobre la soberanía simbiótica entre el componente silicio y carbono. Incluye cambios en la arquitect |
| `HEXELION_DASHBOARD_V102_CLAUDE_CODE.md` | 25 Mayo 2026 | Este documento describe un rediseño integral del dashboard de HEXELION v10.2, incluyendo correcciones críticas y mejoras estéticas. Se detalla el proceso de staging, se corrige un error en e |
| `HEXELION_RUNBOOK_OMIE.md` | NO_DATA | Este documento es un manual operativo para la gestión táctica de energía en el sistema hexelion, basado en precios de mercado de OMIE y ENTSO-E. Define modos de operación del sistema según u |
| `HEXELION_SINODO_VOCERO_FASE2.md` | NO_DATA | El documento describe la implementación de 'El Vocero', un agente que obtiene y clasifica los precios de energía del mercado OMIE cada hora. Detalla el proceso de reconocimiento del código e |
| `brief_nexo_fable_creativo.md` | NO_DATA | Documento define el diseño visual del dashboard de HEXELION, un microestado digital soberano, enfocado en la estética minimalista y la identidad visual basada en SVG, tipografía y colores. P |
| `Nuevo Documento de texto.txt` | NO_DATA | Este documento contiene credenciales de cuenta NEAR para hexelion.testnet en la red de prueba. Muestra información de acceso incluyendo el ID de cuenta, clave pública y privada. Se menciona  |
| `p0x.proyecto.hexelion.md` | 2026-08-08 | Especificación maestra del proyecto hexelion que define la interfaz de usuario y experiencia de usuario para el jardín digital. Describe la navegación con tres caras interactivas, el estilo  |

### informe_estado (13)

| documento | fecha declarada | qué es |
|---|---|---|
| `hexelion_observaciones_silver.txt` | 2026-08-06 | El documento registra métricas de seguimiento de vehículos aéreos y marítimos, con datos filtrados por FastAPI y telemetría serial en estado de falla. Incluye dos propuestas pendientes: una  |
| `hexelion_telemetria_bronce.txt` | 2026-08-06 | El documento registra datos de telemetría desde distintos sensores del sistema hexelion, incluyendo transmisiones de radio, datos del panel solar, estado de la batería y errores de comunicac |
| `Auditoria Claude code 24-05-2026.txt` | 24-05-2026 | Informe de auditoría del sistema Hexelion del 24 de mayo de 2026. Muestra el estado de los nodos La Fragua, La Torre, El Vigía y HP1, con datos sobre uptime, uso de recursos y servicios acti |
| `HEXELION_SESION_20260511.md` | 2026-05-11 | Se completó la conexión de todos los nodos del rack a Tailscale y se confirmaron las credenciales del sistema. Se implementó el primer servicio de pago mediante NEAR AI y se detectó un incid |
| `HANDOFF_hexelion_2026-06-08.md` | 2026-06-08 | El informe describe el estado actual del proyecto Hexelion, incluyendo el funcionamiento del Nexo, OSIRIS, cortafuegos, y el estado del hardware. Muestra los avances en el despliegue de comp |
| `HEXELION_AUDITORIA_ENERGETICA_20260523.md` | 23 Mayo 2026 | El documento presenta un inventario detallado del hardware del sistema Hexelion, incluyendo nodos de control, IA, sensores y dispositivos de red. Se describe el consumo energético real y est |
| `HEXELION_BRIEFING_MAESTRO_20260524.md` | 24 de Mayo de 2026 | HEXELION es un organismo cibernético soberano compuesto por un sustrato silicio y uno carbono, donde el Soberano es la extensión de carbono del sistema. Se describe el cambio doctrinal del 2 |
| `HEXELION_ESTADO_20260509.md` | 09 Mayo 2026 | HEXELION TAGUS_ALPHA es un nodo soberano en Lisboa que captura señales marítimas y aéreas, procesa datos locales y vende certidumbre física verificable. El hardware está casi completo, con l |
| `HEXELION_ESTADO_ACTUAL_20260601.md` | 2026-06-01 | HEXELION es un microestado digital soberano que opera un nodo en Beato, Lisboa, centrado en la emisión de atestaciones AIS firmadas criptográficamente. El sistema incluye hardware especializ |
| `HEXELION_SESION_20260503_DESPLIEGUE.md` | 3-4 Mayo 2026 | Se realiza el despliegue físico del rack Hexelion, verificando el estado del hardware y configurando el entorno de trabajo. Se ejecutan pruebas de conectividad, instalación de Docker y herra |
| `HEXELION_SESION_20260511.md` | 2026-05-11 | Se completó la conexión de todos los nodos del rack a Tailscale y se confirmaron las credenciales del sistema. Se implementó el primer servicio de pago con NEAR AI y se detectó un incidente  |
| `HEXELION_SISTEMA_ESTADO_20260517.md` | 2026-05-17 | El documento describe el estado del sistema HEXELION al 17 de mayo de 2026, incluyendo la topología de nodos Tailscale, el estado de los servicios en cada nodo, recursos utilizados y métrica |
| `github_profile_README.md` | NO_DATA | David presenta HEXELION como un laboratorio de inteligencia artificial en el borde, operando en un rack físico en Lisboa. El sistema utiliza hardware de baja potencia para captar señales rad |

### investigacion (5)

| documento | fecha declarada | qué es |
|---|---|---|
| `CLAUDE_CODE_DASHBOARD_V9.md` | 21 Mayo 2026 | El documento describe la creación de un nuevo dashboard HTML estático para el proyecto Hexelion, utilizando solo un archivo HTML autocontenido con datos de endpoints reales. Se especifican r |
| `INVENTARIO_WIDGETS_2026-07-13.md` | 2026-07-13 | Se realiza un inventario detallado de widgets y métricas del dashboard Hexelion y el Jardin, incluyendo estado de cada componente. Se analizan 13 páginas del dashboard y el estado de los pan |
| `HEXELION_GUIA_NODO_LISBOA.md` | Mayo 2026 | Este documento describe la configuración física y operativa del nodo HEXELION en Lisboa, denominado TAGUS_ALPHA. Detalla el hardware utilizado, incluyendo dispositivos de procesamiento, sens |
| `HEXELION_SINODO_FASE1_PROMPT.md` | NO_DATA | Este documento define la estructura inicial del Sínodo de HEXELION, centrada en la creación del esqueleto del sistema con roles canónicos y una topología de despliegue. Establece las reglas  |
| `HEXELION_VERIFICACION_PENDIENTE_20260515.md` | 15 de Mayo de 2026 | Este documento recoge verificaciones y decisiones pendientes tras la Reforma Energética del 15 de mayo de 2026, enfocadas en la selección de proveedores y equipos para el sistema solar de He |

### otro (5)

| documento | fecha declarada | qué es |
|---|---|---|
| `CIERRE_HEXELION.md` | 2026-08-02 | Este documento es un cierre de fase para el proyecto Hexelion, que resume el estado actual del desarrollo y define categorías para el manejo de tareas pendientes. Incluye verificaciones técn |
| `Changelog — Sesión 19-20 Mayo 2026 (2).txt` | 19-20 Mayo 2026 | Se describe la estructura del proyecto Hexelion Nexus con carpetas y archivos migrados. Se implementan servicios como el vocero OMIE y el pregonero web. Se lanza el dashboard V9 con paneles  |
| `HEXELION_SESION_20260502.md` | 2026.05.02 | Registro de sesión de Hexelion donde se habilita SSH en el router, se instala y configura NUT para monitorear un UPS, y se resuelven problemas relacionados con drivers USB y permisos. Se ide |
| `HEXELION_SESION_20260510.md` | 2026-05-10 | Se realiza un inventario completo del estado de la infraestructura de Hexelion en la Ciudadela, incluyendo hardware, red, software y configuración de Tailscale. Se canonizan documentos clave |
| `HEXELION_explicacion_sencilla.txt` | NO_DATA | HEXELION es un organismo digital experimental compuesto por ordenadores en Lisboa que perciben el mundo físico, razonan sobre lo observado y generan pruebas infalsificables de las señales re |

### plan (2)

| documento | fecha declarada | qué es |
|---|---|---|
| `HEXELION_PLAN_PROFESIONALIZACION_20260524.md` | 24 Mayo 2026 | Este documento es un plan de profesionalización post-auditoría para el proyecto hexelion, que establece una serie de acciones estructuradas para estabilizar y reforzar la infraestructura del |
| `HEXELION_TAREAS_20260517.md` | 2026-05-17 | Se detalla una lista maestra de tareas para el proyecto Hexelion, con énfasis en tareas urgentes, desarrollo del dashboard, nuevos proyectos como wallets y recompensas, y la activación de pr |

### prompt (13)

| documento | fecha declarada | qué es |
|---|---|---|
| `PROMPT_MAESTRO_HEXELION_RONDA_AI_AI.md` | NO_DATA | Documento define el contexto y reglas para la ronda de agentes AI-AI en el sistema HEXELION. Establece restricciones canonicas y vocabulario para agentes como AG-NEXO, AG-JARDIN y AG-RUTAS-V |
| `hexelion_politicas_gold.txt` | NO_DATA | Este documento define políticas de control de energía para el jardín, incluyendo umbrales de voltaje y acciones asociadas. Establece límites en la red mesh para peers autorizados y sus proto |
| `PAQUETE_HEXELION_PUBLIC.md` | 2026-08-12 | El documento explica que el repositorio hexelion-public contiene información sensible que debe ser eliminada. Se propone una corrección basada en el commit inicial, eliminando contenido priv |
| `HEXELION_SINODO_VOCERO_FASE2.md` | NO_DATA | El documento describe la implementación de El Vocero, un agente que obtiene y clasifica los precios de energía del mercado OMIE cada hora. Define su lógica de búsqueda de precios en múltiple |
| `CLAUDE_CODE_PROMPT_dashboard_VISUAL_ONLY.md` | NO_DATA | Este documento describe una corrección crítica para el dashboard de Hexelion, especificando cambios visuales en el dashboard correcto en producción. Se detallan tres modificaciones: sustitui |
| `HEXELION_DASHBOARD_V102_PROMPT.md` | 25 Mayo 2026 | El documento describe un rediseño del dashboard de Hexelion v10.2, incluyendo corrección de un bug crítico relacionado con el puerto de tejo-ships, cambios en el layout y actualización de ca |
| `HEXELION_DASHBOARD_v10_PROMPT.md` | 23 Mayo 2026 | Este documento es un prompt de producción para actualizar el dashboard de Hexelion de versión v9 a v10. Incluye instrucciones para verificar el entorno, hacer un backup, y añadir un campo bt |
| `HEXELION_DASHBOARD_v10_PROMPT_v1.1.md` | 23 Mayo 2026 | Este documento es un prompt de producción para la actualización del dashboard de Hexelion, pasando de la versión v9 a la v10, denominada 'Cristal Vivo'. Describe los pasos necesarios para pr |
| `HEXELION_FIX_MAPA_LISBOA.md` | NO_DATA | El documento describe una tarea puntual para corregir el mapa de Lisboa en el dashboard de Hexelion, reutilizando el componente ya existente del panel Tejo Terminal. Se busca sustituir el ma |
| `PROMPT_CLAUDE_CODE_ALMA_SINODO.md` | NO_DATA | Este documento es un prompt para Claude Code que establece tres tareas clave: refinar el radar de los mapas con un cono translúcido, implementar un mecanismo de vida honesta para El Faro med |
| `PROMPT_CLAUDE_CODE_RECON_DASHBOARD.md` | NO_DATA | El documento analiza el estado del dashboard de El Faro, identificando qué archivo se está sirviendo en vivo y qué proceso lo gestiona. También evalúa el estado del servicio asociado y mapea |
| `PROMPT_arreglos-marcos-tipografia.md` | NO_DATA | El documento describe la aplicación de marcos pre-cortados en el frontend de Hexelion, específicamente en el proyecto Aetheric, con énfasis en la estética y legibilidad. Incluye instruccione |
| `backupdashboard.txt` | NO_DATA | El documento describe un comando bash que realiza copias de seguridad del archivo index.html en el directorio del dashboard. Se crea una copia de seguridad con marca de tiempo incluyendo fec |

## OTRO · no pertenece a ningún proyecto · 3 documentos


### informe_estado (1)

| documento | fecha declarada | qué es |
|---|---|---|
| `aurelius_estado_bronze.txt` | 2026-08-06 | El documento describe el estado actual de varios repositorios relacionados con proyectos como hexelion, aurelius y otros. Menciona que algunos están desactualizados y requieren auditoría loc |

### investigacion (2)

| documento | fecha declarada | qué es |
|---|---|---|
| `Untitled 1.odt` | 2026-08-17 | El documento describe la descarga y verificación de un modelo de lenguaje Qwen3-4B-Instruct y una voz es_ES-sharvard-medium. Se menciona la fuente de los archivos y se confirma su integridad |
| `Untitled 1.odt` | NO_DATA | El documento presenta un inventario de criptomonedas y activos digitales, incluyendo Ethereum, Solana, NEAR, Sui y Bitcoin, con sus respectivas cantidades y valores en euros. Detalla las dir |
