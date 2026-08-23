# aurelius-lora · la forja

> **Estado: STAGING · nada se ha ejecutado, nada se ha instalado.**
> Plan del Arquitecto recuperado del canon (`mente/backlog/BACKLOG_UI.md`,
> Apéndice A.6: *«`~/aurelius-lora/` → EN ESPERA»*, 2026-08-02) y sellado con
> hardware medido el **2026-08-20**.

**Desviación mínima aditiva declarada.** El canon nombra `~/aurelius-lora/`.
Esto vive en `~/p0x/aurelius-lora/`. Motivo: fuera del repo no hay historia, y
el encargo pide commits. El nombre se conserva; cambia el padre.

---

## §0 · El metal, medido

| | Beelink · la Forja | Doogee S110 · el Campo |
|---|---|---|
| CPU | Ryzen 7 255, 8 núcleos / 16 hilos | aarch64 |
| RAM | 57 GiB · **40 GiB disponibles** | 8 GB |
| Disco | 915 GB · **534 GB libres** (39 % usado) | — |
| GPU | Radeon 780M **integrada** (HawkPoint1). **Sin GPU discreta.** | Vulkan: `No devices found` |
| Inferencia | 14,5 tok/s | 2,93 ± 0,38 tok/s · **5,4–6,3 min/turno** (tope 80) |

> **Aviso de nomenclatura.** Aquí «la Forja» es el **Beelink**, que en el canon
> del rack se llama `soberano`. `la-fragua` es **otra máquina** (el RK3588). Dos
> nombres casi iguales para dos metales distintos: una sesión futura puede
> entrenar en el sitio equivocado. Se declara, no se resuelve por iniciativa.

---

## §1 · Las siete respuestas, firmadas

| | Decisión del Soberano |
|---|---|
| **P1 · Datos** | **No** chats crudos como voz primaria. Primario: canon del producto (`textos.py`, `narrador.py`, `LORE.md`, `CIERRE_M*.md`, turnos reales de `--charla`). Secundario: correcciones del Soberano como pares de preferencia, y las tres familias de fallos del sprint como negativos. **v1 = los 226 registros del canon** (208 de voz + 18 negativos), firmado el 2026-08-20. El 1–2 MB es **horizonte, no condición de entrada**: el guardián añade turnos reales y correcciones sesión a sesión. **Nada de relleno sintético para alcanzar el número.** |
| **P2 · Espacio** | Sí, medido. Sobra. |
| **P3 · Idioma** | **Bilingüe** EN+ES en pares paralelos, como `textos.py`. ES como ancla de tono. **No** ES-first. |
| **P4 · Forja** | **Todo local, todo soberano.** Beelink de noche. **Nunca cloud:** el dataset es el alma. |
| **P5 · Guardián** | Beelink. Forja y guardián comparten hogar. |
| **P6 · Frecuencia** | Por milestone al principio; mensual tras estabilizar. |
| **P7 · Base** | Qwen3-4B-Instruct, ya validado en el Doogee. |

---

## §2 · Cuatro cosas que el plan da por hechas y no lo están

Ninguna se resuelve aquí por iniciativa. Se miden en la Fase 0 y **el veredicto
lo firma el Soberano**.

### B1 · «QLoRA CPU» es casi una contradicción

La **Q** de QLoRA es la cuantización NF4 de `bitsandbytes`, y ese kernel es
**CUDA**. En una máquina sin GPU NVIDIA no hay NF4: hay **LoRA a secas**, en
bf16 o fp32.

No es un problema de espacio — con 40 GiB caben los ~8 GB de Qwen3-4B en bf16
más los estados del optimizador, que en LoRA son pequeños porque solo entrenan
los adaptadores. Es un problema de **nombre**: llamarlo QLoRA haría esperar el
consumo de memoria de QLoRA y el resultado de QLoRA. La Fase 2 se escribe como
**LoRA en CPU**, y si algún día hay NF4, se renombra con la medida delante.

### B2 · Unsloth espera GPU NVIDIA

Unsloth se construye sobre CUDA/Triton. En este nodo — Radeon 780M integrada,
sin discreta — la expectativa razonable es que **falle al importar**, no que
vaya lento. Tú ya lo marcaste como «sin verificar en ESTE nodo»; `forja/minirun.py`
existe para convertir esa expectativa en un dato con fecha, barato: si Unsloth
no importa, lo escribe y pasa al siguiente candidato sin gastar más.

### B3 · El «fallback soberano» no existe como binario aquí

`llama.cpp` build **10488** en este nodo trae exactamente dos binarios:
`llama-cli` y `llama-completion`. **No hay `llama-finetune` ni
`llama-export-lora`.** El fallback no es «el mismo stack que la inferencia»
hasta que alguien lo compile y compruebe que el ejemplo de entrenamiento sigue
existiendo aguas arriba y admite esta arquitectura. `forja/verificar_llamacpp.sh`
lo comprueba **sin compilar nada**.

Mientras tanto, el candidato con más probabilidad de funcionar hoy es el que el
plan no nombra: **PEFT + transformers sobre torch-CPU**. Lento y real.

### B4 · Y torch no soporta el Python de este nodo

El intérprete del sistema es **3.14.4**. PyTorch no publica ruedas para 3.14.
Cualquier camino que pase por torch necesita **su propio entorno** en 3.11/3.12
— `uv` ya está instalado, así que no hace falta `sudo` ni tocar el sistema.

> **Y la frontera que esto no cruza:** la forja tendrá dependencias pesadas. **El
> producto no.** `aurelius` es biblioteca estándar y se queda así: lo único que
> cruza de aquí allí es **un fichero GGUF y su huella**. Nada de `torch` entra
> jamás en el árbol publicable.

---

## §3 · El hallazgo que decide la Fase 4

El producto verifica su cerebro contra una huella firmada:

```python
# descarga.py
return huella_fichero(ruta) == pieza.sha256
```

**Un GGUF afinado es otro fichero, con otro sha256.** Si la Fase 4 sobrescribe
`modelos/qwen3-4b-instruct-2507-Q4_K_M.gguf`, `presente(CEREBRO)` devuelve
`False` y el producto — correctamente — dirá que su cerebro no está y ofrecerá
bajarlo otra vez. El «hot-swap sin reinicio» tal y como está escrito en la Fase 4
**rompe la integridad que el producto promete**.

Por eso el modelo afinado **no sustituye al cerebro: se pone al lado**, como
pieza propia con su huella medida y firmada — la misma disciplina del catálogo
(«huellas medidas, no heredadas»). El producto lo elige solo si verifica, y el
rollback es dejar de elegirlo. Implementado en `integracion/motor_afinado.py`.

---

## §4 · Las cinco fases, y qué hay escrito de cada una

| Fase | Guardián | Fichero | Estado |
|---|---|---|---|
| **0** | Veredicto de entrenador | `forja/minirun.py`, `forja/verificar_llamacpp.sh` | escrito · **no ejecutado** |
| **1** | Dataset | `datos/guardian_dataset.py`, `datos/construir_dataset.py` | escrito · **no ejecutado** |
| **2** | Trainer | `forja/entrenar_lora.py` | escrito · **con cerrojo** |
| **3** | Tester | `pruebas/guardian_tester.py` | escrito · **no ejecutado** |
| **4** | Sync | `sincronizar/guardian_sync.sh` | escrito · **no ejecutado** |
| **5** | Health | `salud/guardian_health.py` | escrito · **no ejecutado** |

La Fase 0 no estaba en tu lista de cinco. La añado porque las fases 2 a 5 se
apoyan en un entrenador que hoy no está elegido, y elegirlo por intuición es
justo lo que este proyecto no hace.

**Todos los guiones llevan cerrojo:** sin `--ejecutar` explícito imprimen lo que
harían y salen con 0. Ninguno instala, descarga ni entrena por defecto.

---

## §5 · `<|fusible|>` · decisión de diseño a probar

Marcarlo como probable **no** lo hace cierto. Lo que hay que medir antes de
comprometerlo:

1. **Coste de vocabulario.** Un token nuevo obliga a redimensionar la matriz de
   embeddings. Eso cambia el modelo y complica la conversión a GGUF y el
   intercambio con el base.
2. **La alternativa barata.** Qwen3 trae tokens especiales reservados sin uso.
   Reutilizar uno evita el redimensionado entero.
3. **La alternativa sin vocabulario.** Un centinela en texto plano que no aparece
   jamás en datos naturales. Cero coste de arquitectura; menos garantía.
4. **Lo que se mide para decidir:** si el modelo emite el marcador cuando debe y
   solo cuando debe, en las tres formas, sobre los negativos del sprint.

`pruebas/guardian_tester.py --test-fusible` compara las tres. **La decisión es
tuya, después del dato.**
