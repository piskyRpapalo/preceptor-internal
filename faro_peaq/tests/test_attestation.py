"""
Tests del constructor EN SECO.

La entrada es el fichero REAL `faro_epoch_23.json`, copia literal de
`hexelion/faro/proofs/epoch_23.json` — un lote ya anclado en NEAR testnet
(tx LD4MQTo41V9eXf5uTMDXUofujzpUMhEoqr3gF3bmF6d). No hay payload inventado.
"""

import json
import pathlib

import pytest
from pydantic import ValidationError

from faro_peaq import attestation
from faro_peaq.models import PreparedAttestation

FIXTURE = pathlib.Path(__file__).resolve().parent.parent / "fixtures" / "faro_epoch_23.json"

# 32 bytes públicos de prueba. NO es la clave del Faro: la real vive en
# la-fragua (`keys/attest_ed25519.pub`) y este paso no lee ficheros de claves.
PUBKEY_DE_PRUEBA = bytes(range(32))
MACHINE_ADDR = "0x122db40F59B9B669e46c712192Aea952cc0e57fe"


@pytest.fixture()
def bundle():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


@pytest.fixture()
def receipt(bundle):
    return attestation.load_receipt_from_proof_bundle(bundle, seq=23)


# ── la recepción real se parsea sin perder nada ─────────────────────────────

def test_recepcion_real_se_carga(receipt):
    assert receipt.payload.seq == 23
    assert receipt.payload.kind == "ais.position"
    assert receipt.payload.kid == "hxl-attest-1"
    assert receipt.payload.node == "hexelion.near"
    assert receipt.payload.data.mmsi == 263701460
    assert receipt.payload.data.lat_e7 == 386511000
    assert receipt.anchor_network == "testnet"
    assert receipt.anchor_tx == "LD4MQTo41V9eXf5uTMDXUofujzpUMhEoqr3gF3bmF6d"


def test_seq_inexistente_falla_ruidosamente(bundle):
    with pytest.raises(ValueError, match="no está en el epoch"):
        attestation.load_receipt_from_proof_bundle(bundle, seq=999)


def test_payload_es_estricto_sin_floats(receipt):
    """El Faro firma enteros escalados. Si alguien mete un float, revienta."""
    crudo = receipt.payload.model_dump(exclude_none=True)
    assert all(isinstance(v, int) for v in crudo["data"].values())
    with pytest.raises(ValidationError):
        type(receipt.payload.data)(**{**crudo["data"], "lat_e7": 38.6511})


# ── la pieza que ata todo: reproducimos la hoja Merkle del Faro ─────────────

def test_recomputamos_la_hoja_merkle_del_faro(receipt):
    """
    Si nuestra canonicalización JCS no fuese byte a byte la del Faro, este hash
    no coincidiría. Coincide contra un valor ya anclado en NEAR: prueba de que
    el mapeo a peaq parte del artefacto real y no de una reinterpretación.
    """
    recomputado = attestation.faro_leaf_hash(receipt.payload.model_dump(exclude_none=True))
    assert recomputado == receipt.leaf_hash
    assert recomputado == "5a2b1597038ab0daaf89efa269c148eef7913d49f1d51fcc7f469f45c078efdc"


def test_preimagen_de_firma_lleva_el_dominio(receipt):
    pre = attestation.faro_signing_preimage(receipt.payload.model_dump(exclude_none=True))
    assert pre.startswith(b"hexelion-faro-attestation-v1\n")
    assert b'"mmsi":263701460' in pre


# ── DID de máquina PREPARADO ───────────────────────────────────────────────

def test_did_preparado_declara_ed25519(receipt):
    did = attestation.build_prepared_did(
        machine_name="hexelion-vigia-01",
        machine_address=MACHINE_ADDR,
        ed25519_public_key=PUBKEY_DE_PRUEBA,
        faro_verify_endpoint="http://100.82.94.83:8100/v1/attested",
    )
    assert did.did_id == f"did:peaq:{MACHINE_ADDR}"
    assert did.prepared is True
    assert did.submitted is False
    assert did.add_attribute_call["status"] == "NO ENVIADO (Paso 1 es seco)"
    assert "CARBONO" in did.add_attribute_call["signer"]

    from faro_peaq import did_codec
    doc = did_codec.decode_did_document(bytes.fromhex(did.document_proto_hex[2:]))
    vm = doc["verification_methods"][0]
    assert vm["type"] == "Ed25519VerificationKey2020"
    assert vm["public_key_multibase"].startswith("z")
    assert doc["authentications"] == ["#hxl-attest-1"]
    assert any(s["type"] == "SignaturePreimageDomain" for s in doc["services"])


def test_multibase_rechaza_longitud_incorrecta():
    with pytest.raises(ValueError, match="32 bytes"):
        attestation.ed25519_multibase(b"corta")


def test_base58btc_ceros_a_la_izquierda():
    assert attestation.base58btc(b"\x00\x00\x01") == "112"


# ── atestación PREPARADA ───────────────────────────────────────────────────

def test_atestacion_preparada_cabe_en_el_pallet(receipt):
    prep = attestation.build_prepared_attestation(
        receipt, did_id=f"did:peaq:{MACHINE_ADDR}", machine_address=MACHINE_ADDR,
    )
    assert prep.within_storage_bounds is True
    assert prep.item_bytes <= attestation.STORAGE_VALUE_MAX_BYTES
    assert prep.item_type_bytes <= attestation.STORAGE_KEY_MAX_BYTES
    cuerpo = json.loads(prep.item)
    assert cuerpo["s"] == 23
    assert cuerpo["l"] == receipt.leaf_hash
    assert cuerpo["r"] == receipt.merkle_root
    assert cuerpo["x"] == receipt.anchor_tx


def test_atestacion_es_de_recepcion_y_esta_en_seco(receipt):
    prep = attestation.build_prepared_attestation(
        receipt, did_id=f"did:peaq:{MACHINE_ADDR}", machine_address=MACHINE_ADDR,
    )
    assert prep.claim == "attestation-of-reception"
    assert prep.prepared is True
    assert prep.submitted is False
    assert prep.carbon_signature_required is True
    assert prep.network_target == "agung"
    assert prep.trust_tier == 1
    assert prep.add_item_call["status"] == "NO ENVIADO (Paso 1 es seco)"


def test_el_tipo_prohibe_marcar_enviado(receipt):
    """`submitted` es Literal[False]. No hay forma legítima de construir un enviado."""
    prep = attestation.build_prepared_attestation(
        receipt, did_id=f"did:peaq:{MACHINE_ADDR}", machine_address=MACHINE_ADDR,
    )
    datos = prep.model_dump()
    datos["submitted"] = True
    with pytest.raises(ValidationError):
        PreparedAttestation(**datos)


def test_objeto_preparado_es_inmutable(receipt):
    prep = attestation.build_prepared_attestation(
        receipt, did_id=f"did:peaq:{MACHINE_ADDR}", machine_address=MACHINE_ADDR,
    )
    with pytest.raises(ValidationError):
        prep.submitted = True  # type: ignore[misc]


def test_todas_las_recepciones_del_epoch_se_preparan(bundle):
    for leaf in bundle["leaves"]:
        rec = attestation.load_receipt_from_proof_bundle(bundle, seq=leaf["seq"])
        prep = attestation.build_prepared_attestation(
            rec, did_id=f"did:peaq:{MACHINE_ADDR}", machine_address=MACHINE_ADDR,
        )
        assert prep.within_storage_bounds
        assert attestation.faro_leaf_hash(
            rec.payload.model_dump(exclude_none=True)) == leaf["leaf_hash"]
