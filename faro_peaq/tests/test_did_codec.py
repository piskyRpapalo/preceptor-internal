"""
Tests del códec. Los vectores de `AttributeStore` son BYTES REALES leídos de
agung el 2026-08-23 con `state_getStorage`; no son sintéticos.
"""

import pytest

from faro_peaq import did_codec

# Valores tomados de la entrada real de PeaqDid::AttributeStore en agung
# (clave 0x50b1…a1430000 1a0289b9…, leída el 2026-08-23):
#   name       = "peaq:did:0x68616e62616f7175616e7361743740676d61696c2e636f6d" (59 bytes)
#   validity   = 4294967295 (u32::MAX — sin caducidad)
#   created    = 1722621558027 (Moment, milisegundos unix)
#   envoltorio = raw-proto  ← el SDK oficial de peaq asume hex-ascii y aquí falla
REAL_NAME_LEN = 59
REAL_VALIDITY = 4294967295
REAL_CREATED_MS = 1722621558027


def test_scale_compact_modos():
    assert did_codec.scale_compact(bytes([0xEC]))[0] == 59
    assert did_codec.scale_compact(bytes([0x15, 0x01]))[0] == 69
    assert did_codec.scale_compact(bytes([0x02, 0x00, 0x01, 0x00]))[0] == 0x4000


def test_scale_bytes_lee_vec():
    buf = bytes([0x0C]) + b"abc" + b"resto"
    data, off = did_codec.scale_bytes(buf)
    assert data == b"abc"
    assert buf[off:] == b"resto"


def test_scale_bytes_detecta_buffer_corto():
    with pytest.raises(did_codec.DecodeError):
        did_codec.scale_bytes(bytes([0xFC]) + b"ab")


def test_decode_attribute_estructura_real():
    """
    Vector real completo: nombre + valor protobuf + validity(u32) + created(u64).
    `created` es un Moment de Substrate en milisegundos.
    """
    name = b"peaq:did:0x68616e62616f7175616e7361743740676d61696c2e636f6d"
    assert len(name) == REAL_NAME_LEN
    value = did_codec.encode_did_document("did:peaq:5G6g", "did:peaq:5GL4")
    raw = (bytes([len(name) << 2]) + name
           + bytes([len(value) << 2]) + value
           + REAL_VALIDITY.to_bytes(4, "little")
           + REAL_CREATED_MS.to_bytes(8, "little"))
    attr = did_codec.decode_attribute(raw)
    assert attr["name"] == name
    assert attr["validity"] == REAL_VALIDITY
    assert attr["created_ms"] == REAL_CREATED_MS
    assert did_codec.decode_did_document(attr["value"])["id"] == "did:peaq:5G6g"


def test_roundtrip_documento_completo():
    proto = did_codec.encode_did_document(
        did_id="did:peaq:0x122db40F59B9B669e46c712192Aea952cc0e57fe",
        controller="did:peaq:0x122db40F59B9B669e46c712192Aea952cc0e57fe",
        verification_methods=[{
            "id": "#hxl-attest-1",
            "type": "Ed25519VerificationKey2020",
            "controller": "did:peaq:0x122db40F59B9B669e46c712192Aea952cc0e57fe",
            "public_key_multibase": "z6MkjchhfUsD6mmvni8mCda",
        }],
        services=[{"id": "#faro", "type": "HexelionFaroAttestation",
                   "service_endpoint": "http://127.0.0.1:8100/v1/attested"}],
        authentications=["#hxl-attest-1"],
    )
    doc = did_codec.decode_did_document(proto)
    assert doc["id"].startswith("did:peaq:0x122db")
    assert doc["verification_methods"][0]["type"] == "Ed25519VerificationKey2020"
    assert doc["services"][0]["type"] == "HexelionFaroAttestation"
    assert doc["authentications"] == ["#hxl-attest-1"]
    assert doc["_wrapper"] == "raw-proto"


def test_envoltorio_hex_ascii_tambien_decodifica():
    """
    En agung conviven los dos envoltorios. `demo-warehousebot-002` usa hex-ascii.
    El decodificador debe tragarse ambos sin distinguir a priori.
    """
    proto = did_codec.encode_did_document("did:peaq:0xAA", "did:peaq:0xAA")
    hex_ascii = proto.hex().encode("ascii")
    doc = did_codec.decode_did_document(hex_ascii)
    assert doc["id"] == "did:peaq:0xAA"
    assert doc["_wrapper"] == "hex-ascii"


def test_ed25519_esta_en_los_tipos_de_verificacion():
    """El mapeo entero del Faro depende de esto: peaq admite Ed25519 nativo."""
    assert "Ed25519VerificationKey2020" in did_codec.VERIFICATION_TYPES


def test_protobuf_rechaza_campo_cero():
    with pytest.raises(did_codec.DecodeError):
        did_codec.protobuf_fields(bytes([0x02, 0x01, 0x41]))
