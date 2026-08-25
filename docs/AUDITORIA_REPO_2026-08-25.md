# AUDITORÍA DEL REPOSITORIO PÚBLICO · PreceptorOS

**Fecha:** 2026-08-25 · **Commit auditado:** `87ea1cc` + `1dce87c` · **Tag:** `v1.1`
**Método:** clon limpio desde GitHub en `/tmp`, no el árbol de trabajo. Auditar el árbol
donde se desarrolla es auditar lo que uno cree que subió.

---

## Veredicto

**Se puede compartir.** Cinco comprobaciones, cinco en verde, y tres notas que no bloquean.

---

## 1 · Instalación limpia · ✅

```
git clone https://github.com/piskyRpapalo/PreceptorOS.git
python3 preceptoros.py --view --db /tmp/nueva.db
```

Arranca y dice lo correcto sobre una memoria que no existe: *«Todavía no hay memoria en esta
máquina […] Ejecuta esto y la creamos juntos»*. No revienta, no inventa, no crea nada sin
permiso.

**La tanda en el clon recién hecho: `VERDE · 337/337`**, sabotajes 4/4 y 6/6. Lo que está
publicado pasa sus propias pruebas en una máquina que no es la de desarrollo.

## 2 · Licencia · ✅ consistente

| fichero | declara |
|---|---|
| `LICENSE` | Apache License, Version 2.0 |
| `LICENSE-PROSE` | Attribution-ShareAlike 4.0 International |
| `README.md` | Apache-2.0 + CC BY-SA 4.0 |
| `pyproject.toml` | Apache-2.0 |
| `MANIFIESTO.md` | Apache-2.0 + CC BY-SA 4.0 |
| `CHANGELOG.md` | Apache-2.0 + CC BY-SA 4.0 |

Código Apache-2.0, prosa CC BY-SA 4.0, **en los seis sitios sin contradecirse**.

*Nota de método:* el primer barrido dio «MIT» en cinco ficheros. Era falso positivo — `grep`
casando dentro de «per**mit**e» y «lí**mit**e». Se repitió con límites de palabra. Una
auditoría que no comprueba su propia herramienta produce hallazgos inventados.

## 3 · Secretos · ✅ ninguno

`corpus/muestras.json` contiene cadenas como `OPENAI_API_KEY=sk-proj-Xk29...`, y **son
falsas a propósito**: es el corpus con el que se prueba que el redactor de la frontera las
caza. El propio fichero lo declara en su primera línea:

> *«Datos inventados: ninguna credencial de aquí es real, ninguna máquina de aquí existe.»*

Ningún otro fichero del árbol contiene material que parezca credencial.

⚠️ **Nota, no hallazgo:** el escaneo automático de secretos de GitHub puede marcar ese fichero
y mandarte un aviso. Y alguien que llegue al repo a decidir si se fía verá
`OPENAI_API_KEY=sk-proj-…` en un repositorio público antes de leer la nota. **Sugerencia (S):**
renombrar el fichero a `corpus/muestras_falsas.json` o partir las cadenas
(`"sk-" + "proj-Xk29…"`). No cambia nada técnico; cambia el primer segundo de quien mira.

## 4 · Blobs grandes · ✅ limpio de sorpresas

`.git` pesa **16 MB**. Los cinco objetos por encima de 1 MB son las láminas del filósofo
(`laminas/*.png`, 1,8–2,5 MB), que son contenido legítimo y **doctrina explícita de no
tocar**.

**No queda rastro de `ashly_zhao.md`** (3,54 MB) en el clon público: `git log --all` sobre esa
ruta no devuelve nada. La reescritura funcionó.

## 5 · Promesas del README · ✅ todas ciertas

Comprobadas una a una contra el clon:

| promesa | comprobación | |
|---|---|---|
| «nada más allá de Python 3» / stdlib | El Guardián sobre el clon: **66 ficheros, 0 hallazgos** | ✅ |
| «no necesita red» | Solo `descarga.py` (`urllib`) y `empaquetado/lanzador.py` (`socket`) importan red. La descarga del cerebro es **opcional y a petición**; el producto funciona sin ella. La promesa dice *necesita*, y es exacta | ✅ |
| «busca» (nuevo en v1.1) | FTS5 sobre `engrams`, con su limitación declarada: busca palabras, no significado | ✅ |
| Cifras del prompt-cache | Las del README son las medidas el 24-ago, con su máquina al lado | ✅ |

**Corregida en esta ronda:** el README decía *«No busca — todavía»*, falso desde B.1a. Un
README que promete de menos es tan poco fiable como uno que promete de más.

## 6 · CHANGELOG · ✅ al día

`v1.1` con su entrada y `RELEASE_v1.1.md` enlazado. `RELEASE_v1.0.md` conserva sus URL viejas
**a propósito**, con una nota que lo explica: reescribir una nota de versión pasada para que
parezca que siempre se llamó PreceptorOS es falsear el registro.

## 7 · LORE.md y ARQUETIPO.md · revisados, **no tocados**

Ninguno miente tras el renombrado. Los dos usan «Aurelius» como **personaje**, que es
exactamente la doctrina: el producto es PreceptorOS, el personaje es Aurelius, y el nombre
sigue honrando a Marco Aurelio.

Un hallazgo que sirve para otra cosa: **`LORE.md` enuncia D68 en el propio Lore** —
*«Aurelius habla con su voz igual: por tubería, no por socket»*. La regla que gobierna
`FRONTERA_D68.md` no es solo una decisión técnica: tiene respaldo narrativo. Eso la hace más
difícil de erosionar por comodidad.

---

## Lo que queda pendiente, y no bloquea compartir

| # | Qué | Coste |
|---|---|---|
| A1 | `corpus/muestras.json` puede disparar el escáner de secretos de GitHub y asusta al primer vistazo | S |
| A2 | El logo dice «Aurelius» y el producto es PreceptorOS. **Decisión del Soberano** (ver abajo) | M |
| A3 | Los dos paths de fábrica están solo en español; el producto es bilingüe | M |

### Sobre A2 · el logo

La orden dice cambiarlo a «Aurelius × PreceptorOS». Es imagen, no código: hay que **rehacer
los PNG** (`assets/titulo-aurelius.png`, `assets/social-preview.png`, `assets/avatar-github.png`)
y eso no lo puede hacer esta sesión sin herramientas de imagen.

Y merece pensarse antes de hacerlo: *«Aurelius × PreceptorOS»* pone al mismo nivel dos cosas
que la doctrina separa a propósito — el personaje y el producto. `MARCA.md` ya fija que el
avatar lleva el busto sobre violeta de la casa. **Sugerencia:** el nombre del producto en el
título y el personaje en el sprite, que es como ya está en el `manifest.json` de la PWA
(`name: "PreceptorOS"`, sprite de Aurelius). Sin la «×».
