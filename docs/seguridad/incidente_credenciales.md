# INCIDENTE · CREDENCIALES EN CLARO EN EL ARCHIVO DISPERSO

**Fecha del hallazgo:** 2026-08-23 · **Estado:** ABIERTO
**Quién rota:** el Soberano, despierto. **Esta sesión no ha tocado ninguna credencial.**

---

## 1 · Qué se hizo y qué no

Se **clasificó** el contenido por patrones, con los valores enmascarados en todo momento.
No se ha copiado, movido, editado ni versionado el fichero. No se ha abierto ninguna
cuenta, ni se ha probado ninguna credencial, ni se ha tocado ningún fichero de claves.

Una nota de honestidad: al buscar la contraseña, el primer patrón (`clave:` / `password=`)
**no la encontró**, porque está dentro de una celda de tabla Markdown sin separador. Se dio
con ella al segundo intento, y en ese momento el valor apareció en la salida del comando.
No se ha vuelto a escribir en ningún sitio y no aparece en este documento. Se dice porque
un informe de seguridad que oculta cómo se obtuvo el dato no es un informe de seguridad.

---

## 2 · Dónde está

**Un solo fichero**, fuera de todo repositorio git:

```
~/pre-bee/p0x/MD 3/HEXELION_LEGION_DEPIN_20260514.md
```

9.965 bytes, 266 líneas. Es el registro de una sesión de despliegue DePIN del 14 de mayo de
2026 sobre `musculo-hp-01` y `musculo-hp-02`.

**No está en ningún repositorio.** Verificado contra los 18 repositorios git del disco. No
se ha publicado nunca.

Un segundo fichero, sin credenciales pero con exposición de identidad:

```
~/pre-bee/p0x/MD 3/hexelion_m2m_manifest_yaml__1_.txt
```

Declara `hexelion.near` de **mainnet** como identidad M2M pública, con
`no_human_required: true`. La auditoría del 30 de mayo ya ordenó retirarlo; sigue ahí.

---

## 3 · Qué hay, por severidad

| Sev. | Qué | Dónde | Nota |
|---|---|---|---|
| **ALTA** | **Una contraseña de servicio en texto plano** (servicio de *earning* Pawns) | línea 39 | Es la única credencial de acceso reutilizable del fichero |
| **MEDIA** | Mención de una **frase mnemónica de 24 palabras** para la cuenta POKT | líneas 215-217 | **La frase NO está en el fichero.** Solo se dice que existe y qué se haría con ella. El riesgo es que apunta a dónde buscarla |
| **BAJA** | **2 direcciones EVM** operativas (Rivalz, Meson; una asociada a MetaMask) | líneas 35, 232 | Son direcciones públicas, no claves. El daño es de correlación: enlazan identidad, nodos y actividad |
| **BAJA** | **2 direcciones base58** (cuenta SOL de Grass, cuenta POKT) | líneas 36, 41, 215, 236 | Ídem. La cuenta POKT declara saldo 0 |

**Lo que NO hay, y es la mejor noticia del informe:** cero claves privadas. Ni en formato
hexadecimal de 64 caracteres, ni PEM, ni OpenSSH. Cero frases semilla escritas. Cero
ficheros de credenciales adjuntos.

---

## 4 · Orden de rotación propuesto

De más urgente a menos. **Lo hace el carbono.**

**1 · La contraseña del servicio (línea 39).** Es lo único reutilizable. Si esa contraseña
se repite en otro sitio, el alcance no es un servicio de *earning*: es todo lo que comparta
esa contraseña. **Primera pregunta antes de rotar: ¿está reutilizada?** Si la respuesta es
sí, la rotación deja de ser una tarea y pasa a ser una lista.

**2 · La cuenta POKT y su mnemónica.** La frase no está en el fichero, pero el documento
dice exactamente qué es y para qué sirve. Decidir: rotar, o cerrar la cuenta. Declara 0
POKT en cadena Morse, así que cerrar puede ser más barato que rotar.

**3 · Las cuentas EVM y SOL.** No hay claves expuestas, luego no hay urgencia técnica. La
decisión es de correlación: si esas direcciones van a seguir usándose, conviene que no
estén enlazadas por escrito a los nodos del rack. Si ya no se usan, no hay nada que hacer.

**4 · `hexelion.near` en el manifiesto.** No es rotación: es retirar el fichero, que ya se
ordenó en mayo y no se hizo. Una cuenta de mainnet declarada como identidad de máquina con
`no_human_required: true` contradice de frente la doctrina de hoy.

---

## 5 · Destino del fichero

**No entra en ningún repositorio, ni público ni privado.** Está fuera de git y ahí se
queda. La `PROPUESTA_CONSERJERIA` lo recoge en la lista de «no se mueve».

Si algún día se necesita su contenido —el registro de despliegue tiene valor histórico—,
lo correcto es **extraer a mano el texto útil sin las credenciales** y archivar eso, dejando
el original fuera. No al revés.

---

## 6 · La lección, que ya estaba escrita

Este fichero es un registro de sesión: alguien anotó lo que hacía mientras lo hacía, y las
credenciales entraron en la nota porque en ese momento eran parte del trabajo. No fue
descuido de seguridad: fue **ausencia de una frontera entre el cuaderno y el almacén de
secretos**.

El propio archivo ya tiene la regla que lo habría impedido, y nunca llegó al repositorio:
*«cero claves en la embajada»* y el patrón de clave de alcance limitado, de
`00_CONSTITUCION_Y_ADN.md`. La `REVISION_CRUZADA` la propone como doctrina ausente. Este
incidente es el argumento para firmarla.
