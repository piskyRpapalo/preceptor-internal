"""
models.py — Modelos Pydantic estrictos para el lector keyless y el constructor en seco.

`model_config = ConfigDict(extra="forbid", strict=True, frozen=True)` en todo lo
que cruza la frontera de la red: si peaq cambia el shape de una respuesta, esto
revienta en la cara en vez de propagar un None silencioso.
"""

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

_STRICT = ConfigDict(extra="forbid", strict=True, frozen=True)


# ── Red ──────────────────────────────────────────────────────────────────────

class PeaqEndpoint(BaseModel):
    """Un endpoint RPC público de peaq. Verificado a mano, no adivinado."""

    model_config = _STRICT

    name: str
    url: str
    network: Literal["agung", "peaq"]
    chain_id: int
    verified_on: str = Field(description="Fecha ISO en que este nodo lo probó vivo")


# Endpoints documentados por peaq y PROBADOS desde `soberano` el 2026-08-23.
# Fuente: https://docs.peaq.xyz/peaqchain/build/getting-started/connecting-to-peaq
AGUNG_ONFINALITY = PeaqEndpoint(
    name="onfinality-public",
    url="https://peaq-agung.api.onfinality.io/public",
    network="agung",
    chain_id=9990,
    verified_on="2026-08-23",
)
AGUNG_PEAQ_ASYNC = PeaqEndpoint(
    name="peaq-async",
    url="https://wss-async-agung.peaq.xyz",
    network="agung",
    chain_id=9990,
    verified_on="2026-08-23",
)
AGUNG_ENDPOINTS = (AGUNG_ONFINALITY, AGUNG_PEAQ_ASYNC)


class ChainInfo(BaseModel):
    """Identidad de la cadena leída en vivo. Sirve de aserción anti-red-equivocada."""

    model_config = _STRICT

    chain: str
    node_version: str
    eth_chain_id: int
    block_number: int
    endpoint: str


# ── DID ──────────────────────────────────────────────────────────────────────

class VerificationMethod(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    id: str = ""
    type: str = ""
    controller: str = ""
    public_key_multibase: str = ""


class DidSignature(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    type: str = ""
    issuer: str = ""
    hash: str = ""


class DidService(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    id: str = ""
    type: str = ""
    service_endpoint: str = ""
    data: str = ""


class PeaqDidDocument(BaseModel):
    """`document.Document` de peaq, decodificado."""

    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    id: str
    controller: str
    verification_methods: tuple[VerificationMethod, ...] = ()
    signature: Optional[DidSignature] = None
    services: tuple[DidService, ...] = ()
    authentications: tuple[str, ...] = ()
    wrapper: Literal["hex-ascii", "raw-proto"]


class DidAttribute(BaseModel):
    """Entrada de `PeaqDid::AttributeStore` tal y como vive en cadena."""

    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    storage_key: str
    name: str
    validity: int
    created_ms: int
    raw_value_hex: str
    document: Optional[PeaqDidDocument] = None
    decode_error: Optional[str] = None


class StorageItem(BaseModel):
    """Entrada de `PeaqStorage::ItemStore` (clave 64B : valor 256B)."""

    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    storage_key: str
    raw_hex: str
    as_text: Optional[str] = None


# ── El lado del Faro (formato REAL, leído de proofs/epoch_*.json) ────────────

class FaroAisData(BaseModel):
    """
    Campo `data` de la atestación v1 del Faro. Enteros escalados, cero floats,
    exactamente como los firma `main.py::_attest_v1`.
    """

    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    mmsi: int
    lat_e7: int
    lon_e7: int
    sog_e2: int
    cog_e2: int
    heading: Optional[int] = None


class FaroAttestationPayload(BaseModel):
    """
    Payload firmado del Faro v1. Es EXACTAMENTE lo que va bajo el dominio
    `hexelion-faro-attestation-v1\\n` + JCS antes de la firma Ed25519.
    """

    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    v: int
    kind: str
    node: str
    kid: str
    seq: int
    t: int
    prev: str
    data: FaroAisData


class FaroMerkleStep(BaseModel):
    model_config = _STRICT

    sibling: str
    side: Literal["left", "right"]


class FaroReceipt(BaseModel):
    """
    Una recepción AIS del Faro con todo lo que la hace verificable por un tercero:
    payload firmado + firma + (si ya fue anclada) su prueba Merkle y la tx del ancla.
    """

    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    payload: FaroAttestationPayload
    sig_b64url: Optional[str] = None
    leaf_hash: Optional[str] = None
    merkle_root: Optional[str] = None
    merkle_path: tuple[FaroMerkleStep, ...] = ()
    anchor_network: Optional[str] = None
    anchor_tx: Optional[str] = None
    epoch: Optional[int] = None


# ── El artefacto PREPARADO (Paso 2, nunca enviado aquí) ──────────────────────

class PreparedDidDocument(BaseModel):
    """DID de máquina PREPARADO. `submitted` es False por construcción."""

    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    did_name: str
    did_id: str
    controller: str
    document_proto_hex: str
    add_attribute_call: dict[str, Any]
    prepared: Literal[True] = True
    submitted: Literal[False] = False


class PreparedAttestation(BaseModel):
    """
    Atestación de recepción PREPARADA en formato peaq.

    Vocabulario: **atestación de recepción**, jamás "prueba de realidad física".
    El artefacto acredita que un receptor concreto, identificado por un DID, dice
    haber recibido una trama AIS en un instante. No acredita que el barco exista.
    """

    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    schema_id: Literal["hexelion/faro-peaq-attestation/v1"] = (
        "hexelion/faro-peaq-attestation/v1"
    )
    claim: Literal["attestation-of-reception"] = "attestation-of-reception"
    did_id: str
    item_type: str = Field(description="Clave de PeaqStorage::ItemStore (<=64 bytes)")
    item: str = Field(description="Valor de PeaqStorage::ItemStore (<=256 bytes)")
    item_bytes: int
    item_type_bytes: int
    within_storage_bounds: bool
    faro_seq: int
    faro_kid: str
    faro_sig_b64url: Optional[str]
    faro_merkle_root: Optional[str]
    faro_anchor_tx: Optional[str]
    trust_tier: Literal[1] = 1
    carbon_signature_required: Literal[True] = True
    add_item_call: dict[str, Any]
    prepared: Literal[True] = True
    submitted: Literal[False] = False
    network_target: Literal["agung"] = "agung"
