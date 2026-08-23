"""
did_codec.py — Decodificadores puros (cero dependencias, cero red, cero claves).

Dos codificaciones hay que entender para leer peaq sin SDK:

1. SCALE (Substrate). El valor de `PeaqDid::AttributeStore` es la struct
   `Attribute { name: Vec<u8>, value: Vec<u8>, validity: BlockNumber(u32),
   created: Moment(u64) }` codificada en SCALE.

2. Protobuf `document.Document` (esquema de peaq, fichero
   `did_document_format.proto` del SDK oficial):

       message VerificationMethod { string id=1; string type=2;
                                    string controller=3;
                                    string public_key_multibase=4; }
       message Signature          { string type=1; string issuer=2; string hash=3; }
       message Services           { string id=1; string type=2;
                                    optional string service_endpoint=3;
                                    optional string data=4; }
       message Document { string id=1; string controller=2;
                          repeated VerificationMethod verification_methods=3;
                          Signature signature=4;
                          repeated Services services=5;
                          repeated string authentications=6; }
       enum VerificationType { Ed25519VerificationKey2020=0;
                               Sr25519VerificationKey2020=1; }

DESVIACIÓN OBSERVADA EN CADENA (agung, 2026-08-23): el campo `value` aparece con
DOS envoltorios distintos según quién escribió el DID:
  · hex-ascii  — bytes ASCII que son a su vez el hex del protobuf (lo que asume
                 el SDK oficial de Python en `did.py::_read`).
  · raw-proto  — el protobuf directamente, sin envoltorio hex.
El SDK oficial revienta con los segundos. Aquí se prueban ambos, en ese orden.
"""

from __future__ import annotations

from typing import Any, Optional

# El protobuf de peaq no numera el enum en el campo `type` del
# VerificationMethod: escribe la cadena literal. Se mantiene el enum por
# fidelidad al .proto y porque el mapeo del Faro depende de que Ed25519 exista.
VERIFICATION_TYPES = (
    "Ed25519VerificationKey2020",
    "Sr25519VerificationKey2020",
    "EcdsaSecp256k1RecoveryMethod2020",
)


class DecodeError(ValueError):
    """El buffer no decodifica como lo que se esperaba."""


# ── SCALE ────────────────────────────────────────────────────────────────────

def scale_compact(buf: bytes, i: int = 0) -> tuple[int, int]:
    """Lee un entero SCALE compact. Devuelve (valor, siguiente_offset)."""
    if i >= len(buf):
        raise DecodeError("compact: buffer agotado")
    flag = buf[i] & 0b11
    if flag == 0:
        return buf[i] >> 2, i + 1
    if flag == 1:
        if i + 2 > len(buf):
            raise DecodeError("compact: buffer corto (2 bytes)")
        return int.from_bytes(buf[i:i + 2], "little") >> 2, i + 2
    if flag == 2:
        if i + 4 > len(buf):
            raise DecodeError("compact: buffer corto (4 bytes)")
        return int.from_bytes(buf[i:i + 4], "little") >> 2, i + 4
    n = (buf[i] >> 2) + 4
    if i + 1 + n > len(buf):
        raise DecodeError("compact: buffer corto (big-int)")
    return int.from_bytes(buf[i + 1:i + 1 + n], "little"), i + 1 + n


def scale_bytes(buf: bytes, i: int = 0) -> tuple[bytes, int]:
    """Lee un `Vec<u8>` SCALE (compact-len + bytes)."""
    n, i = scale_compact(buf, i)
    if i + n > len(buf):
        raise DecodeError(f"vec<u8>: se piden {n} bytes y sólo hay {len(buf) - i}")
    return buf[i:i + n], i + n


def decode_attribute(raw: bytes) -> dict[str, Any]:
    """
    Decodifica `PeaqDid::Attribute` (SCALE) tal y como sale de
    `state_getStorage` sobre el mapa `AttributeStore`.

    Devuelve {"name": bytes, "value": bytes, "validity": int, "created_ms": int}.
    `created` es un `Moment` de Substrate: milisegundos unix.
    """
    name, i = scale_bytes(raw, 0)
    value, i = scale_bytes(raw, i)
    if i + 12 > len(raw):
        raise DecodeError("attribute: faltan validity(u32)+created(u64)")
    validity = int.from_bytes(raw[i:i + 4], "little")
    created_ms = int.from_bytes(raw[i + 4:i + 12], "little")
    return {"name": name, "value": value, "validity": validity,
            "created_ms": created_ms}


# ── Protobuf (subconjunto: sólo lo que el .proto de peaq usa) ───────────────

def _varint(buf: bytes, i: int) -> tuple[int, int]:
    result = 0
    shift = 0
    while True:
        if i >= len(buf):
            raise DecodeError("varint: buffer agotado")
        byte = buf[i]
        result |= (byte & 0x7F) << shift
        i += 1
        if not byte & 0x80:
            return result, i
        shift += 7
        if shift > 63:
            raise DecodeError("varint: demasiado largo")


def protobuf_fields(buf: bytes) -> list[tuple[int, Any]]:
    """
    Decodificador protobuf mínimo. Devuelve [(numero_campo, valor)] donde el
    valor es `bytes` para wire-type 2 e `int` para wire-type 0.
    Wire-types 1 y 5 se saltan; 3/4 (grupos, deprecados) abortan.
    """
    out: list[tuple[int, Any]] = []
    i = 0
    while i < len(buf):
        key, i = _varint(buf, i)
        field_no, wire = key >> 3, key & 0b111
        if field_no == 0:
            raise DecodeError("protobuf: número de campo 0")
        if wire == 0:
            val, i = _varint(buf, i)
            out.append((field_no, val))
        elif wire == 2:
            n, i = _varint(buf, i)
            if i + n > len(buf):
                raise DecodeError("protobuf: longitud fuera de rango")
            out.append((field_no, buf[i:i + n]))
            i += n
        elif wire == 1:
            i += 8
        elif wire == 5:
            i += 4
        else:
            raise DecodeError(f"protobuf: wire-type {wire} no soportado")
        if i > len(buf):
            raise DecodeError("protobuf: desbordamiento")
    return out


def _s(v: Any) -> str:
    return v.decode("utf-8", errors="replace") if isinstance(v, bytes) else str(v)


def _submessage(raw: bytes, mapping: dict[int, str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for field_no, val in protobuf_fields(raw):
        key = mapping.get(field_no)
        if key is not None:
            out[key] = _s(val)
    return out


_VM_FIELDS = {1: "id", 2: "type", 3: "controller", 4: "public_key_multibase"}
_SIG_FIELDS = {1: "type", 2: "issuer", 3: "hash"}
_SVC_FIELDS = {1: "id", 2: "type", 3: "service_endpoint", 4: "data"}


def unwrap_did_value(value: bytes) -> tuple[bytes, str]:
    """
    Devuelve (bytes_protobuf, envoltorio) donde envoltorio ∈
    {"hex-ascii", "raw-proto"}. Ver nota de desviación en el docstring del módulo.
    """
    try:
        text = value.decode("ascii")
    except UnicodeDecodeError:
        return value, "raw-proto"
    stripped = text[2:] if text[:2] in ("0x", "0X") else text
    if stripped and len(stripped) % 2 == 0:
        try:
            return bytes.fromhex(stripped), "hex-ascii"
        except ValueError:
            pass
    return value, "raw-proto"


def decode_did_document(value: bytes) -> dict[str, Any]:
    """
    Decodifica el `value` de un atributo DID a un documento peaq normalizado.

    Devuelve un dict con las claves del .proto: id, controller,
    verification_methods, signature, services, authentications, y además
    `_wrapper` con el envoltorio detectado.
    """
    raw, wrapper = unwrap_did_value(value)
    doc: dict[str, Any] = {
        "id": "",
        "controller": "",
        "verification_methods": [],
        "signature": None,
        "services": [],
        "authentications": [],
        "_wrapper": wrapper,
    }
    for field_no, val in protobuf_fields(raw):
        if field_no == 1:
            doc["id"] = _s(val)
        elif field_no == 2:
            doc["controller"] = _s(val)
        elif field_no == 3 and isinstance(val, bytes):
            doc["verification_methods"].append(_submessage(val, _VM_FIELDS))
        elif field_no == 4 and isinstance(val, bytes):
            doc["signature"] = _submessage(val, _SIG_FIELDS)
        elif field_no == 5 and isinstance(val, bytes):
            doc["services"].append(_submessage(val, _SVC_FIELDS))
        elif field_no == 6:
            doc["authentications"].append(_s(val))
    return doc


def encode_varint(n: int) -> bytes:
    if n < 0:
        raise ValueError("varint: sólo enteros no negativos")
    out = bytearray()
    while True:
        byte = n & 0x7F
        n >>= 7
        if n:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def encode_string_field(field_no: int, text: str) -> bytes:
    """Codifica un `string` protobuf (wire-type 2). Usado por el constructor en seco."""
    data = text.encode("utf-8")
    return encode_varint((field_no << 3) | 2) + encode_varint(len(data)) + data


def encode_submessage(field_no: int, body: bytes) -> bytes:
    return encode_varint((field_no << 3) | 2) + encode_varint(len(body)) + body


def encode_did_document(
    did_id: str,
    controller: str,
    verification_methods: Optional[list[dict[str, str]]] = None,
    services: Optional[list[dict[str, str]]] = None,
    authentications: Optional[list[str]] = None,
    signature: Optional[dict[str, str]] = None,
) -> bytes:
    """
    Serializa un `document.Document` de peaq. **Sólo construye bytes en memoria.**
    No firma, no envía, no toca red. Se usa para PREPARAR el artefacto del Paso 2.
    """
    out = bytearray()
    out += encode_string_field(1, did_id)
    out += encode_string_field(2, controller)
    for vm in verification_methods or []:
        body = bytearray()
        for no, key in sorted(_VM_FIELDS.items()):
            if vm.get(key):
                body += encode_string_field(no, vm[key])
        out += encode_submessage(3, bytes(body))
    if signature:
        body = bytearray()
        for no, key in sorted(_SIG_FIELDS.items()):
            if signature.get(key):
                body += encode_string_field(no, signature[key])
        out += encode_submessage(4, bytes(body))
    for svc in services or []:
        body = bytearray()
        for no, key in sorted(_SVC_FIELDS.items()):
            if svc.get(key):
                body += encode_string_field(no, svc[key])
        out += encode_submessage(5, bytes(body))
    for auth in authentications or []:
        out += encode_string_field(6, auth)
    return bytes(out)
