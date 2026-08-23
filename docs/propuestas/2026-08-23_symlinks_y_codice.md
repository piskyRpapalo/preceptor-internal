# PROPUESTA · symlinks rotos y el Códice que miente sobre la máquina

**Fecha:** 2026-08-23 · **Repositorio afectado:** `~/p0x` (privado del rack)
**Estado:** PROPUESTA. **No aplicada.** La aplica y empuja el Soberano.

---

## 1 · El problema, medido

### 1.1 · Dos symlinks rotos, versionados en git

```
$ git ls-files -s mente/codice/CODICE_david.md mente/tecnicas
120000 6657228960d91a4e654d2fbef78fffef57c4dfa6 0    mente/codice/CODICE_david.md
120000 356cdb996d326aabf844be8fff7b92efd7debfc6 0    mente/tecnicas
```

El modo `120000` confirma que git los guarda **como enlaces simbólicos**, no como
ficheros. Apuntan a:

```
mente/codice/CODICE_david.md -> /mnt/nvme/p0x/codice/CODICE_david.md
mente/tecnicas               -> /mnt/nvme/p0x/registro_tecnicas/tecnicas
```

```
$ ls -d /mnt/nvme
ls: no se puede acceder a '/mnt/nvme': No existe el archivo o directorio
```

En este nodo **no existe `/mnt/nvme`**. Los dos enlaces apuntan a la nada. El Códice real
vive en `~/p0x/codice/CODICE_david.md`, y el registro de técnicas en
`~/p0x/registro_tecnicas/`, que hoy solo contiene `models.py` sin datos.

Consecuencia práctica: cualquier herramienta que siga la ruta que la propia doctrina
documenta lee la nada. Y lo hace **en silencio**, porque un symlink roto no da error hasta
que alguien intenta abrirlo.

### 1.2 · El Códice declara una máquina que ya no es la suya

`~/p0x/codice/CODICE_david.md`, línea 40:

> **Recursos reales (verificado 2026-06-27)** — Cómputo: la-fragua (RK3588, CPU, ~15 GiB,
> sin CUDA → `qwen3:8b` batch + nomic-embed + Qdrant) · la-torre (Jetson Orin Nano 8 GB →
> `qwen3:4b` interactivo + Sínodo) · proxy LiteLLM enruta · **El Oráculo para lo pesado
> (a mano)**.

Y su cabecera declara `Ruta: /mnt/nvme/p0x/codice/CODICE_david.md`, que tampoco existe.

Este fichero es el **filtro de realidad** del sistema: lo que se consulta para saber qué es
viable. Hoy el cómputo pesado vive en `soberano` con 64 GB y un 30B residente, y «El
Oráculo» era un PC Windows que ya no está en el rack. **Un sistema que lo consulte le dirá
al Soberano que no puede hacer lo que ya hace todos los días.**

Y es **byte a byte idéntico** a la copia arqueológica de junio que está en el archivo
disperso: nunca se actualizó desde que se escribió.

---

## 2 · Lo que se propone hacer

Dos cosas separadas, que se pueden firmar por separado.

### 2.1 · Los symlinks

```bash
cd ~/p0x
git rm --cached mente/codice/CODICE_david.md mente/tecnicas
rm mente/codice/CODICE_david.md mente/tecnicas
ln -s ../../codice/CODICE_david.md mente/codice/CODICE_david.md
ln -s ../registro_tecnicas/tecnicas mente/tecnicas
git add mente/codice/CODICE_david.md mente/tecnicas
```

**Enlaces relativos, no absolutos.** Un enlace absoluto vuelve a romperse el día que el
repositorio se clone en otra ruta o en otro nodo — que es exactamente lo que pasó aquí.
Con enlaces relativos, el repositorio es autocontenido.

**Aviso:** `mente/tecnicas` apuntaría a `~/p0x/registro_tecnicas/tecnicas`, que **hoy no
existe** — la carpeta `registro_tecnicas/` solo tiene `models.py`. Hay dos salidas honestas
y la decisión es del Soberano:

- **(a)** Crear `registro_tecnicas/tecnicas/` vacío con un `LEEME.md` que diga que es el
  encargo y no el resultado — es el mismo patrón que ya usa `mente/corpus/_INDICE.md`.
- **(b)** No enlazar `mente/tecnicas` todavía, y dejarlo fuera hasta que haya datos. Un
  enlace a una carpeta vacía es honesto; un enlace a una carpeta inexistente, no.

Recomiendo **(a)**: mantiene la ruta documentada viva y declara la ausencia en vez de
esconderla.

### 2.2 · El Códice, marcado `@sleeping`

No se borra la línea de recursos ni se reescribe a mano con datos que caducarán otra vez.
Se aplica el patrón que el Soberano firmó: **retirar sin borrar, con condición de despertar
escrita.**

Parche propuesto sobre `~/p0x/codice/CODICE_david.md`:

```diff
 <!--
   EL CODICE — david · P0X
-  Ruta: /mnt/nvme/p0x/codice/CODICE_david.md
+  Ruta: ~/p0x/codice/CODICE_david.md
   Curador: el Preceptor · Autoridad final: el Soberano (lee/corrige/exporta/borra)
```

```diff
-### Recursos reales (verificado 2026-06-27)
-- **Computo**: la-fragua (RK3588, CPU, ~15 GiB, sin CUDA -> qwen3:8b batch + nomic-embed
-  + Qdrant + Codice en NVMe 3.7 TiB) · la-torre (Jetson Orin Nano 8 GB, memoria unificada,
-  CUDA -> qwen3:4b interactivo + Sinodo) · proxy LiteLLM enruta · El Oraculo para lo
-  pesado (a mano).
+### Recursos reales — @sleeping desde 2026-08-23
+
+> **Este apartado esta dormido, no borrado.**
+>
+> **Motivo:** describe el rack de 2026-06-27, que ya no existe. Nombraba «El Oraculo»
+> (un PC Windows fuera del rack actual) como host de lo pesado, daba `qwen3:8b` en
+> la-fragua y `qwen3:4b` en la-torre como techo de computo, y enrutaba por un proxy
+> LiteLLM que hoy no manda. Desde el 2026-08-04 `musculo-hp-01` esta inhabilitado.
+> Leido como vigente, este apartado le dice al Soberano que NO puede hacer cosas que
+> hace todos los dias.
+>
+> **Condicion de despertar:** un inventario de hardware real, medido y fechado — no
+> recordado. Cada nodo con su modelo cargado, su RAM libre con el modelo dentro, y su
+> backend (`ollama ps` primero, como manda el canon). Cuando exista ese inventario,
+> este apartado se reescribe con el y se despierta.
+>
+> **Mientras duerma:** el techo de computo no se deduce de aqui. Se mide.
+
+- **Tiempo**: *[franjas reales — noches / fines de semana]*
+- **Ubicacion**: Lisboa (Beato). Migracion planificada: Castelo Branco.
```

*(Las líneas de Tiempo y Ubicación se conservan tal cual: no han caducado.)*

---

## 3 · Por qué `@sleeping` y no una corrección directa

Porque escribir hoy el inventario correcto **a ojo** repetiría el error exacto que este
documento denuncia: un apartado que dice «verificado» sin que nadie lo verificara ese día.
La cabecera del propio Códice lo pide —«solo se cita lo LITERAL de este archivo, cero falsos
recuerdos»— y el canon del nodo lo repite: `ollama ps` primero, `num_ctx` demostrado por
dato, backend registrado al arranque.

Dormirlo con la llave puesta es la única salida que no crea una tercera versión del mismo
dato.

---

## 4 · Comprobación después de aplicar

```bash
cd ~/p0x
# 1 · los enlaces resuelven
readlink -f mente/codice/CODICE_david.md
test -e mente/codice/CODICE_david.md && echo "enlace OK"
# 2 · no queda ninguna referencia viva a /mnt/nvme fuera de citas historicas
grep -rn "/mnt/nvme" --include="*.md" . | grep -v "aurelius-internal"
# 3 · git guarda enlaces relativos
git ls-files -s mente/codice/CODICE_david.md
```

---

## 5 · Lo que esta sesión NO ha hecho

No se ha aplicado nada. No se ha tocado `~/p0x/codice/`, ni `mente/`, ni ningún symlink. El
único fichero escrito es este, dentro de `aurelius-internal`.
