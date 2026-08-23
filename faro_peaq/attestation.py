"""
attestation.py — Constructor EN SECO de atestación de recepción en formato peaq.

Toma una recepción AIS **real** del Faro (formato `faro-proof-bundle/v1`, el que
persiste `hexelion/faro/proof_store.py` en `proofs/epoch_*.json`) y construye:

  1. `PreparedDidDocument` — el DID de máquina del receptor, con el método de
     verificación **Ed25519VerificationKey2020** que ya usa el Faro. No se
     inventa una clave nueva: se declara la que ya firma.
  2. `PreparedAttestation` — el ítem de `PeaqStorage` que atestigua la recepción.

**NADA DE ESTO SE ENVÍA.** No hay cliente de escritura en este paquete. Los
campos `prepared=True` / `submitted=False` son literales del tipo: Pydantic
rechaza construir el objeto con otro valor.

Vocabulario: *atestación de recepción*. El artefacto dice «este receptor,
identificado por este DID, afirma haber recibido esta trama AIS en este
instante». No dice «este barco está ahí». Jamás «prueba de realidad física».
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Optional

from .did_codec import encode_did_document
from .models import (
    FaroReceipt,
    PreparedAttestation,
    PreparedDidDocument,
)

# Límites reales del pallet `peaq_pallet_storage`, según la doc de peaq:
# «peaq storage supports a simple structure: 64-byte key : 256-byte value».
# Fuente: https://docs.peaq.xyz/build/first-depin/store-machine-data
STORAGE_KEY_MAX_BYTES = 64
STORAGE_VALUE_MAX_BYTES = 256

# Multicodec de clave pública Ed25519 para multibase (did:key y peaq usan lo mismo).
_MULTICODEC_ED25519_PUB = b"\xed\x01"
_B58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

# Prefijo de dominio que el Faro antepone al payload ANTES de firmar con Ed25519.
# Constante `_ATTEST_DOMAIN` de hexelion/faro/main.py. La firma NO cubre el JSON
# a secas: cubre dominio+JSON. Quien verifique fuera del Faro debe saberlo.
FARO_ATTEST_DOMAIN = b"hexelion-faro-attestation-v1\n"

# Prefijo de hoja Merkle del Faro (RFC-6962), constante `_LEAF` de merkle.py.
MERKLE_LEAF_PREFIX = b"\x00"


def base58btc(data: bytes) -> str:
    """base58btc puro, sin dependencias. Sólo se usa para codificar claves PÚBLICAS."""
    n = int.from_bytes(data, "big")
    out = ""
    while n > 0:
        n, rem = divmod(n, 58)
        out = _B58_ALPHABET[rem] + out
    for byte in data:
        if byte == 0:
            out = _B58_ALPHABET[0] + out
        else:
            break
    return out or _B58_ALPHABET[0]


def ed25519_multibase(public_key: bytes) -> str:
    """
    Clave PÚBLICA Ed25519 (32 bytes) → multibase `z<base58btc(0xed01||pk)>`,
    que es lo que espera `VerificationMethod.public_key_multibase` de peaq.

    Sólo acepta material público. Aquí no entra ninguna clave privada ni semilla.
    """
    if len(public_key) != 32:
        raise ValueError(
            f"Una clave pública Ed25519 son 32 bytes, llegaron {len(public_key)}"
        )
    return "z" + base58btc(_MULTICODEC_ED25519_PUB + public_key)


def canonical_json(payload: dict[str, Any]) -> bytes:
    """
    JCS / RFC-8785 tal y como lo implementa el Faro (`_canonical_json` en main.py
    y `canonical_bytes` en merkle.py): claves ordenadas, sin espacios, UTF-8.
    """
    return json.dumps(payload, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def faro_leaf_hash(payload: dict[str, Any]) -> str:
    """Recomputa la hoja Merkle del Faro: sha256(0x00 || JCS(payload))."""
    return hashlib.sha256(MERKLE_LEAF_PREFIX + canonical_json(payload)).hexdigest()


def faro_signing_preimage(payload: dict[str, Any]) -> bytes:
    """Bytes exactos que el Faro firma con Ed25519. Se calculan; NO se firman aquí."""
    return FARO_ATTEST_DOMAIN + canonical_json(payload)


def load_receipt_from_proof_bundle(bundle: dict[str, Any], seq: int) -> FaroReceipt:
    """
    Extrae una recepción concreta de un `faro-proof-bundle/v1`
    (`hexelion/faro/proofs/epoch_NN.json`). Formato REAL, no inventado.
    """
    if bundle.get("format") != "faro-proof-bundle/v1":
        raise ValueError(f"formato no reconocido: {bundle.get('format')!r}")
    leaf = next((l for l in bundle["leaves"] if l["seq"] == seq), None)
    if leaf is None:
        raise ValueError(f"seq {seq} no está en el epoch {bundle.get('epoch')}")
    path = bundle.get("merkle_paths", {}).get(str(seq), [])
    return FaroReceipt(
        payload=leaf["payload"],
        leaf_hash=leaf["leaf_hash"],
        merkle_root=bundle.get("root"),
        merkle_path=tuple(path),
        anchor_network=bundle.get("network"),
        anchor_tx=bundle.get("anchor_tx"),
        epoch=bundle.get("epoch"),
    )


def build_prepared_did(
    machine_name: str,
    machine_address: str,
    ed25519_public_key: bytes,
    controller_address: Optional[str] = None,
    faro_verify_endpoint: Optional[str] = None,
) -> PreparedDidDocument:
    """
    PREPARA el DID de máquina del receptor (El Vigía) en formato peaq.

    `machine_address` y `controller_address` los aporta el CARBONO: sin clave no
    hay dirección, y este paquete no toca claves. Se pasan como dato de entrada.

    `ed25519_public_key` son los 32 bytes PÚBLICOS de la clave de atestación que
    el Faro ya usa (`kid=hxl-attest-1`). El fichero público vive en
    `hexelion/faro/keys/attest_ed25519.pub` en la-fragua; aquí no se lee ni se copia.
    """
    controller = controller_address or machine_address
    did_id = f"did:peaq:{machine_address}"
    controller_did = f"did:peaq:{controller}"
    vm_id = "#hxl-attest-1"

    verification_methods = [{
        "id": vm_id,
        "type": "Ed25519VerificationKey2020",
        "controller": controller_did,
        "public_key_multibase": ed25519_multibase(ed25519_public_key),
    }]
    services = []
    if faro_verify_endpoint:
        services.append({
            "id": "#faro-attested",
            "type": "HexelionFaroAttestation",
            "service_endpoint": faro_verify_endpoint,
        })
    services.append({
        "id": "#faro-domain",
        "type": "SignaturePreimageDomain",
        "data": FARO_ATTEST_DOMAIN.decode("utf-8").strip(),
    })

    proto = encode_did_document(
        did_id=did_id,
        controller=controller_did,
        verification_methods=verification_methods,
        services=services,
        authentications=[vm_id],
    )

    return PreparedDidDocument(
        did_name=machine_name,
        did_id=did_id,
        controller=controller_did,
        document_proto_hex="0x" + proto.hex(),
        add_attribute_call={
            "chain": "agung",
            "pallet": "peaq_did",
            "call": "add_attribute",
            "args": {
                "did_account": machine_address,
                "name": machine_name,
                "value": "0x" + proto.hex(),
                "valid_for": None,
            },
            "evm_alternative": {
                "precompile": "0x0000000000000000000000000000000000000800",
                "signature": "addAttribute(address,bytes,bytes,uint32)",
            },
            "signer": "CARBONO — fuera de este nodo, fuera de este paquete",
            "status": "NO ENVIADO (Paso 1 es seco)",
        },
    )


def build_prepared_attestation(
    receipt: FaroReceipt,
    did_id: str,
    machine_address: str,
    item_type: Optional[str] = None,
) -> PreparedAttestation:
    """
    PREPARA la atestación de recepción como ítem de `PeaqStorage`.

    El valor se comprime a propósito: el pallet impone 256 bytes y la firma
    Ed25519 en base64url ya son 86 caracteres. Se ancla el vínculo criptográfico
    (hoja Merkle + raíz + tx del ancla NEAR) y la firma completa queda tras el
    servicio declarado en el DID. Esto no es un atajo: es el límite real del
    pallet, medido, con `within_storage_bounds` como testigo.
    """
    payload = receipt.payload.model_dump(exclude_none=True)
    leaf = receipt.leaf_hash or faro_leaf_hash(payload)

    item_obj = {
        "v": 1,
        "s": receipt.payload.seq,
        "t": receipt.payload.t,
        "l": leaf,
        "r": receipt.merkle_root or "",
        "x": receipt.anchor_tx or "",
    }
    item = json.dumps(item_obj, sort_keys=True, separators=(",", ":"))
    key = item_type or f"hxl.faro.ais.v1.{receipt.payload.seq}"

    item_bytes = len(item.encode("utf-8"))
    key_bytes = len(key.encode("utf-8"))
    within = (item_bytes <= STORAGE_VALUE_MAX_BYTES
              and key_bytes <= STORAGE_KEY_MAX_BYTES)

    return PreparedAttestation(
        did_id=did_id,
        item_type=key,
        item=item,
        item_bytes=item_bytes,
        item_type_bytes=key_bytes,
        within_storage_bounds=within,
        faro_seq=receipt.payload.seq,
        faro_kid=receipt.payload.kid,
        faro_sig_b64url=receipt.sig_b64url,
        faro_merkle_root=receipt.merkle_root,
        faro_anchor_tx=receipt.anchor_tx,
        add_item_call={
            "chain": "agung",
            "pallet": "peaq_storage",
            "call": "add_item",
            "args": {
                "item_type": key,
                "item": item,
                "account": machine_address,
            },
            "trust_tier": 1,
            "tier_justification": (
                "Tier 1 de peaq verify = dato firmado por la propia máquina con "
                "su clave privada. El Faro ya cumple: Ed25519 sobre "
                "dominio+JCS(payload). Tier 2/3 de peaq no existen todavía."
            ),
            "signer": "CARBONO — fuera de este nodo, fuera de este paquete",
            "status": "NO ENVIADO (Paso 1 es seco)",
        },
    )
