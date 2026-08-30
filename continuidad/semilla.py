#!/usr/bin/env python3
"""Siembra `continuidad.db` con lo que NO se deduce mirando el repo.

Existe para que la base sea reconstruible. La propia `continuidad.db` no se
versiona -- lleva mediciones del rack y datos que envejecen -- asi que sin este
fichero, un clon limpio perderia el conocimiento durable: la doctrina, el
glosario, los motivos de las decisiones y, sobre todo, los falsos rojos ya
desmentidos.

Es idempotente: se puede correr las veces que haga falta.

LO QUE MAS IMPORTA DE ESTE FICHERO son los falsos rojos. Cada uno costo tiempo
de una sesion antes de descubrirse que no existia, y sin dejarlos escritos la
sesion siguiente los vuelve a perseguir desde cero.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import continuidad as C  # noqa: E402

HOY = "2026-08-30"

DOCTRINA = [
    ("D1", "10 KB por fichero HTML/JS/CSS. Modelos binarios exentos.",
     "SOLO el Ágora (preceptoros-web/public). Firmado 2026-08-30.",
     "El test que la aplica (TOPE_FICHERO, test_web.py) solo escanea public/. "
     "La interfaz de la app se sirve en local desde :8740 y no paga latencia de red: "
     "dashboard.js pesa 25 KB y dashboard.css 27 KB, y NO están en deuda."),
    ("D2", "esm.run única CDN · cero peticiones externas al cargar.", "Ágora", None),
    ("D3", "Veto localStorage como fuente de verdad. SQLite firmada es la soberanía; "
     "localStorage solo buffer de reconciliación.", "todo", None),
    ("D4", "Ed25519 para identidad y Libro · AES-256-GCM para exportación.", "todo", None),
    ("D5", "Honest sensors: lo ausente se declara NO_DATA con causa y remedio.", "todo",
     "El recolector lo impone por construcción: un no-verde sin causa se marca "
     "como defecto DEL RECOLECTOR."),
    ("D6", "Scaffolding faded · senda de los muertos en dead_path.jsonl.", "todo", None),
    ("D7", "IronClaw: el silicio propone y ejecuta sintaxis; el carbono firma valor.", "todo",
     "En la línea de comandos se traduce a: dry-run por defecto, --si para aplicar."),
    ("D8", "Canon visual: mármol violeta + bronce, procedural.", "todo",
     "Tokens reales: --violeta #6D5AE0, --bronce #78624C, --tinta #1E1826."),
    ("D9", "Red superpuesta + TLS · cero puertos crudos expuestos.", "rack",
     "Medido 2026-08-30: había un http.server en 0.0.0.0:8080 sin auth ni logs."),
    ("D10", "MVP Python stdlib only. Promesa pública, no se rompe.", "preceptor",
     "Comprobado: los 7 módulos stdlib que usa importan en Python 3.14.4."),
    ("D67", "«preceptor» y «preceptoros» son palabras públicas. El léxico privado "
     "conserva soberano, ironclaw, hexelion.", "guardián de higiene", None),
    ("DSL", "Los workflows de terceros son JSON declarativo, nunca código ejecutable. "
     "Lista blanca cerrada de acciones.", "Ágora", None),
    ("DREC", "Perder la clave es perder el pseudónimo, nunca la ciencia ni las ideas.",
     "identidad", None),
    ("DUNI", "Ninguna unidad systemd ni línea de cron sin firma explícita, una por una, "
     "anotada en deploy/soberano/unidades.md.", "rack",
     "«Un servicio fantasma con autoridad es la semilla del próximo IronClaw». "
     "Un bucle se construye y se prueba primero; cronificarlo es un paso aparte."),
]

# Cada uno costó tiempo antes de descubrirse que no existía.
FALSOS_ROJOS = [
    ("api-guia «inactive»",
     "Está ACTIVE y la levanta systemd (PID 1). Es unidad de SISTEMA: /etc/systemd/system/api-guia.service.",
     "El recolector preguntaba `systemctl --user api-guia`, y el manager de usuario "
     "responde «no existe» — cierto, y sin significado alguno."),
    ("guardian/curador/afinador «inactivos»",
     "Los tres con Result=success y ExecMainStatus=0. Sanos.",
     "Son Type=oneshot. Un oneshot está `inactive` el 99,99% del tiempo, entre "
     "disparos: es el estado SANO. `is-active` es la propiedad que no informa."),
    ("curador «cinco días sin correr»",
     "Es SEMANAL: OnCalendar=Sun *-*-* 05:00:00. Sus hermanos son diarios (03:00 y 04:00).",
     "Se comparó una cadencia semanal contra dos diarias. Por eso `cadencia` es "
     "ahora campo de primera clase del recolector."),
    ("Ollama «no responde»",
     "Vivo, 8 modelos, ~6 ms, backend Vulkan (OLLAMA_IGPU_ENABLE=1 en la unidad).",
     "OLLAMA_HOST vivía solo en ~/.bashrc, que no se carga en shells no "
     "interactivas. Existía para el carbono y no para las máquinas. Ahora está en "
     "~/.config/environment.d/50-p0x.conf y el recolector lo lee también a mano."),
    ("«falta playground.html»",
     "Existe en es/en/fr, con footer honesto y ejemplo sin IPs incrustadas.",
     "La Orden Maestra arrastraba estado de días atrás."),
    ("«paridad i18n rota · fr/lore.html da 404»",
     "Paridad COMPLETA: es/en/fr tienen los mismos 5 ficheros. `lore.html` no "
     "existe en NINGÚN idioma, así que no hay 404 que arreglar.", None),
    ("«chat.js pasa el límite»",
     "8 590 B, por debajo de los 10 240. Ya se refactorizó.", None),
    ("«console.log sueltos»",
     "Hay exactamente uno, y ya está tras `?debug` (chat.js:142).", None),
    ("«el índice FTS no está creado»",
     "`engrams_fts` existe en memory.db.",
     "Se creó después de aquel reporte y nadie actualizó el documento."),
    ("«el snapshot dice 8 modelos aquí y 7 doce líneas más abajo»",
     "Son 8. `oficial-inventario` no casaba con el `grep -E preceptor|qwen|llama`.",
     "Un inventario filtrado por nombre esconde justo los modelos con nombre nuevo."),
]

DECISIONES = [
    (HOY, "Capa aparte para el Ojo del Soberano",
     "El recolector y la consola viven en ~/p0x/Alejandria; `preceptor/estado.py` y "
     "`interface/dashboard.html` no se tocan.",
     "estado.py guarda las banderas de INSTALACIÓN del producto y su docstring "
     "prohíbe crear dos verdades; /api/estado ya existe sirviéndolas. Y el dashboard "
     "es la cara del usuario final: meterle el rack enviaría la red del Soberano a "
     "la app de cada persona.", "Soberano"),
    (HOY, "Los 10 KB son regla del Ágora",
     "No obligan a la interfaz de la app.",
     "El test solo escanea public/. La app se sirve en local y no paga latencia de "
     "red. Zanja una ambigüedad que si no obligaba a un refactor de 4 ficheros.",
     "Soberano"),
    (HOY, "La portada publica el número real del gate",
     "«526 pruebas en verde» pasa a la cifra que produce pytest, con un script que "
     "lo mantiene y un test que falla si divergen.",
     "Ningún comando producía 526. Era una reclamación pública no reproducible, en "
     "producción y en tres idiomas — justo lo que honest sensors existe para impedir.",
     "Soberano"),
    (HOY, "Email: local ahora, SMTP preparado y apagado",
     "resumen.html en Alejandria/resumenes/ con NO_DATA declarado; el envío escrito "
     "con smtplib+netrc pero desactivado.",
     "No hay ningún cliente instalado y sin sudo no hay apt. La contraseña de "
     "aplicación la crea el Soberano; la dirección está sin confirmar (piskycr@ vs "
     "davidpecero@). Enviar correo es acción hacia fuera.", "Soberano"),
    (HOY, "El timer de 15 min no se crea todavía",
     "Queda propuesto: OnCalendar=*-*-* 08..23:00/15, Persistent=false, --rapido.",
     "Canon DUNI: ninguna unidad sin firma explícita. Se construye y se prueba a "
     "mano primero; cronificarlo es un paso aparte con firma propia.", "Soberano"),
]

GLOSARIO = [
    ("Hexelion", "La parte física: rack, sensores, impresora, dashboard Nexo y Le Jardin.",
     "Aurelius y P0X"),
    ("Aurelius", "El proyecto de aprendizaje enfocado a crear comunidad. Bilingüe EN/ES.",
     "Hexelion y P0X. Ojo: `aurelius.service` es OTRA cosa — la PWA del producto en :8740"),
    ("P0X", "La suma de todos los proyectos más el Soberano. No tiene cara propia.",
     "Hexelion y Aurelius"),
    ("La Bóveda", "La app local: MVP Python stdlib, memoria en SQLite, Privacy Gateway.", None),
    ("El Ágora", "preceptoros.org: escaparate, playground, tablón, marketplace.", None),
    ("El Puente", "El Privacy Gateway: sanea el contexto antes de que salga.", None),
    ("El Ojo del Soberano", "La consola de operaciones del rack, en 127.0.0.1:8790. "
     "Es el taller, NO el producto.", "el dashboard de la app, que es la cara del usuario"),
    ("engrama", "Unidad de memoria destilada en memory.db, tabla `engrams`.",
     "un turno de conversación, que vive en `turnos`"),
]

HARDWARE = [
    ("soberano (Beelink)", "Cerebro y forja",
     "Ryzen 7 255 · 64 GB · 915 GB de disco (421 libres). Ollama, API Guía :9001, "
     "PWA :8740, Ojo :8790. torch instalado es +cpu: sin ruta GPU para entrenar.",
     HOY, "auditoría de metal"),
    ("la-torre (Jetson Orin Nano)", "Entrenamiento LoRA y enjambre",
     "Alcanzable por SSH con clave, por MagicDNS y por IP. Alias `jetson` también.",
     HOY, "ssh -o BatchMode=yes"),
    ("la-fragua (Orange Pi 5)", "Ágora, registro, cola de trabajos",
     "RK3588 aarch64. Lexar SSD NM790 4TB MONTADO y confirmado por lsblk. "
     "Auth por clave sin password. Fase 4 desbloqueada.", HOY, "ssh + lsblk"),
    ("el-vigía (Raspberry Pi)", "Fachada y sensores RF (ADS-B, RTL-SDR)",
     "En línea en la red superpuesta. No sondeado en detalle.", HOY, "status de la red"),
    ("Doogee S110", "Edge real de pruebas (Android/Termux)",
     "adb en estado `device` (conectado y autorizado). OJO: el serial que circula en "
     "los documentos tiene un cero de más — usar el que devuelve `adb devices`.",
     HOY, "adb devices"),
    ("musculo-hp-01", "INHABILITADO desde 2026-08-04",
     "Offline. Aloja OSIRIS. No recuperable por vía remota: requiere acceso físico.",
     HOY, "status de la red (concuerda con el canon)"),
]

ESCALABILIDAD = [
    ("gates del recolector", "coste de CPU por corrida", "~10 s cada una",
     "En el timer se usa --rapido y se arrastran con su edad. Cada 15 min con gates "
     "serían 96 pytest al día quemando la CPU del entrenamiento.", HOY),
    ("previsualizaciones de la web", "procesos http.server huérfanos", "> 0",
     "Medidos 10 el 2026-08-30, el más viejo con 7 h. Usar un script de preview que "
     "se apague solo; el recolector los cuenta en cada corrida.", HOY),
    ("memory.db", "engramas frente a turnos", "engramas <= 1 con turnos > 1",
     "Medido: 1 engrama frente a 101 turnos. La memoria no está vacía, está SIN "
     "DESTILAR. Causa sin investigar — y NO puede ser el curador, cuya unidad se "
     "declara «higiene de la memoria, solo lectura (L3)».", HOY),
    ("forja en el nodo soberano", "ruta de entrenamiento", "torch == +cpu",
     "No hay ruta GPU en Beelink. Condiciona LoRA v8: entrenar en la-torre o asumir CPU.", HOY),
]

LORAS = [
    ("preceptor-v7", "Qwen3-4B", "sft_cot_v7.jsonl (109 líneas)", "NO_DATA",
     "servido en Ollama", "2026-08-29", "línea A"),
    ("preceptor-v7-linea-b", "Qwen3-4B", "sft_cot_v7.jsonl", "NO_DATA",
     "servido en Ollama", "2026-08-29", "línea B"),
]

FASES = [
    ("Sprint 0 · pulido", "en curso",
     "favicon, og tags, botón visible, badge con latencia, cifra real del gate",
     "6 de las 8 tareas originales ya estaban hechas o no aplicaban", HOY),
    ("Fase 1 · cerrar lo abierto", "pendiente",
     "migración ~/.aurelius→~/.preceptoros, siembra de memory.db", None, HOY),
    ("Fase 2 · modo libre", "pendiente", "sliders, selector de modelo, window.ai", None, HOY),
    ("Fase 3 · recuperación", "pendiente", "3 niveles de identidad, Sello cifrado", None, HOY),
    ("Fase 4 · Ágora", "pendiente", "backend en la-fragua, DSL, marketplace",
     "desbloqueada: SSH y Lexar 4TB verificados", HOY),
]


def sembrar(con):
    for i, regla, alcance, motivo in DOCTRINA:
        C._upsert(con, "doctrina", "id", {
            "id": i, "regla": regla, "alcance": alcance,
            "firmada_en": HOY, "motivo": motivo})

    for asunto, dec, mot in FALSOS_ROJOS:
        clave = f"falso rojo · {asunto}"
        ya = con.execute("SELECT 1 FROM decisiones WHERE asunto=?", (clave,)).fetchone()
        if not ya:
            con.execute("INSERT INTO decisiones (fecha, asunto, decision, motivo, "
                        "firmada_por) VALUES (?,?,?,?,?)",
                        (HOY, clave, dec, mot, "medición"))

    for fecha, asunto, dec, mot, quien in DECISIONES:
        ya = con.execute("SELECT 1 FROM decisiones WHERE asunto=?", (asunto,)).fetchone()
        if not ya:
            con.execute("INSERT INTO decisiones (fecha, asunto, decision, motivo, "
                        "firmada_por) VALUES (?,?,?,?,?)", (fecha, asunto, dec, mot, quien))

    for t, d, nc in GLOSARIO:
        C._upsert(con, "glosario", "termino",
                  {"termino": t, "definicion": d, "no_confundir_con": nc})
    for n, rol, det, med, fue in HARDWARE:
        C._upsert(con, "hardware", "nodo",
                  {"nodo": n, "rol": rol, "detalle": det, "medido_en": med, "fuente": fue})
    for n, est, ent, nota, act in FASES:
        C._upsert(con, "fases", "nombre",
                  {"nombre": n, "estado": est, "entrega": ent, "nota": nota,
                   "actualizada_en": act})
    for n, base, ds, vl, est, ent, nota in LORAS:
        C._upsert(con, "loras", "nombre",
                  {"nombre": n, "base": base, "dataset": ds, "val_loss": vl,
                   "estado": est, "entrenado_en": ent, "nota": nota})
    for comp, met, umb, acc, med in ESCALABILIDAD:
        ya = con.execute("SELECT 1 FROM escalabilidad WHERE componente=? AND metrica=?",
                         (comp, met)).fetchone()
        if not ya:
            con.execute("INSERT INTO escalabilidad (componente, metrica, umbral, "
                        "accion, medido_en) VALUES (?,?,?,?,?)", (comp, met, umb, acc, med))
    con.commit()


def main():
    con = C.abrir()
    C.init(con)
    sembrar(con)
    for t in sorted(C.ESQUEMA):
        n = con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        if n:
            print(f"  {t:16} {n}")
    con.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
