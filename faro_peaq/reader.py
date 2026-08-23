"""
reader.py — Lector keyless de peaq agung. Cero claves, cero escritura.

Qué sabe hacer:
  · identificar la cadena y exigir que sea agung (`assert_testnet`);
  · leer un atributo DID por (dirección, nombre) vía `peaqdid_readAttribute`;
  · recorrer los mapas de estado `PeaqDid::AttributeStore`, `PeaqStorage::ItemStore`
    y `PeaqMor::MachineRegister` vía `state_getKeysPaged` + `state_getStorage`;
  · decodificar el documento DID (SCALE + protobuf) sin el SDK oficial.

Por qué no se usa `peaq-sdk` (PyPI 1.0.1): arrastra `web3`, `substrate-interface`,
`protobuf` y `base58` — es decir, toda la maquinaria de firmar — para un paso cuyo
requisito es no poder firmar. El prefijo twox128 de los mapas se calcula con
`xxhash` si está disponible; si no, se usan los prefijos precalculados y
verificados contra la cadena el 2026-08-23 (constantes `KNOWN_PREFIXES`).
"""

from __future__ import annotations

from typing import Iterator, Optional

from . import did_codec
from .models import (
    AGUNG_ONFINALITY,
    DidAttribute,
    DidService,
    DidSignature,
    PeaqDidDocument,
    PeaqEndpoint,
    StorageItem,
    VerificationMethod,
)
from .rpc import KeylessRpc, RpcError

# Prefijos twox128(pallet) ++ twox128(storage_item), verificados contra
# agung el 2026-08-23 desde `soberano` (devolvieron 16.895 / 41.955 / 8 claves).
KNOWN_PREFIXES: dict[str, str] = {
    "PeaqDid.AttributeStore":
        "0x50b1bab256dbd966f3aa4c23d3a7a20177fe881efb890ea5c9aede80c0d3a143",
    "PeaqStorage.ItemStore":
        "0xa94f76f4d854c6324f9c16806bea637ae7384cf5bc10e08366e9e0df10d163d6",
    "PeaqMor.MachineRegister":
        "0x43d0ee7e90e2ba8356552afbf18589e6c521f65e1a76f1ef96730fa9fdef14f1",
}


def storage_prefix(pallet: str, item: str) -> str:
    """twox128(pallet)++twox128(item). Usa xxhash si está; si no, la tabla verificada."""
    key = f"{pallet}.{item}"
    try:
        import xxhash  # type: ignore
    except ImportError:
        if key in KNOWN_PREFIXES:
            return KNOWN_PREFIXES[key]
        raise RuntimeError(
            f"Sin xxhash y sin prefijo precalculado para {key}. "
            "Instala xxhash o añade el prefijo verificado a KNOWN_PREFIXES."
        ) from None

    def t128(text: str) -> str:
        raw = text.encode()
        return (xxhash.xxh64(raw, 0).intdigest().to_bytes(8, "little")
                + xxhash.xxh64(raw, 1).intdigest().to_bytes(8, "little")).hex()

    computed = "0x" + t128(pallet) + t128(item)
    known = KNOWN_PREFIXES.get(key)
    if known and known != computed:
        raise RuntimeError(
            f"Prefijo calculado para {key} ({computed}) no coincide con el "
            f"verificado en cadena ({known}). PARO."
        )
    return computed


def _to_document(decoded: dict) -> PeaqDidDocument:
    sig = decoded.get("signature")
    return PeaqDidDocument(
        id=decoded["id"],
        controller=decoded["controller"],
        verification_methods=tuple(
            VerificationMethod(**vm) for vm in decoded["verification_methods"]
        ),
        signature=DidSignature(**sig) if sig else None,
        services=tuple(DidService(**s) for s in decoded["services"]),
        authentications=tuple(decoded["authentications"]),
        wrapper=decoded["_wrapper"],
    )


class PeaqKeylessReader:
    """Lector de sólo lectura. No tiene constructor de transacciones. A propósito."""

    def __init__(self, endpoint: PeaqEndpoint = AGUNG_ONFINALITY, timeout: int = 30) -> None:
        self.rpc = KeylessRpc(endpoint, timeout=timeout)

    # ── identidad de cadena ─────────────────────────────────────────────────

    def chain_info(self):
        return self.rpc.chain_info()

    def assert_testnet(self):
        return self.rpc.assert_testnet()

    # ── DID ─────────────────────────────────────────────────────────────────

    def read_did(self, address: str, name: str) -> Optional[DidAttribute]:
        """
        `peaqdid_readAttribute(address, 0x<hex(name)>)`.
        Devuelve None si el DID no existe (el nodo responde `null`).
        """
        name_hex = "0x" + name.encode("utf-8").hex()
        result = self.rpc.call("peaqdid_readAttribute", [address, name_hex])
        if result is None:
            return None
        raw_name = bytes.fromhex(result["name"][2:]).decode("utf-8", errors="replace")
        raw_value = bytes.fromhex(result["value"][2:])
        return self._build_attribute(
            storage_key=f"rpc:peaqdid_readAttribute({address},{name})",
            name=raw_name,
            value=raw_value,
            validity=int(result.get("validity", 0)),
            created_ms=int(result.get("created", 0)),
        )

    def _build_attribute(self, storage_key: str, name: str, value: bytes,
                         validity: int, created_ms: int) -> DidAttribute:
        document = None
        error = None
        try:
            document = _to_document(did_codec.decode_did_document(value))
        except Exception as exc:  # decodificar nunca debe tumbar el barrido
            error = f"{type(exc).__name__}: {exc}"
        return DidAttribute(
            storage_key=storage_key,
            name=name,
            validity=validity,
            created_ms=created_ms,
            raw_value_hex="0x" + value.hex(),
            document=document,
            decode_error=error,
        )

    # ── barrido de mapas de estado ──────────────────────────────────────────

    def iter_storage_keys(self, pallet: str, item: str, limit: int = 100,
                          page: int = 100) -> Iterator[str]:
        prefix = storage_prefix(pallet, item)
        start = prefix
        emitted = 0
        while emitted < limit:
            batch = min(page, limit - emitted)
            keys = self.rpc.call("state_getKeysPaged", [prefix, batch, start])
            if not keys:
                return
            for key in keys:
                yield key
                emitted += 1
            if len(keys) < batch:
                return
            start = keys[-1]

    def count_entries(self, pallet: str, item: str, hard_cap: int = 200_000) -> int:
        """Cuenta claves del mapa. Barato: sólo pide claves, no valores."""
        prefix = storage_prefix(pallet, item)
        start = prefix
        total = 0
        while total < hard_cap:
            keys = self.rpc.call("state_getKeysPaged", [prefix, 1000, start])
            total += len(keys)
            if len(keys) < 1000:
                return total
            start = keys[-1]
        return total

    def sample_dids(self, limit: int = 5) -> list[DidAttribute]:
        """Lee N atributos DID reales de la cadena y los decodifica."""
        out: list[DidAttribute] = []
        for key in self.iter_storage_keys("PeaqDid", "AttributeStore", limit=limit):
            raw_hex = self.rpc.call("state_getStorage", [key])
            if raw_hex is None:
                continue
            attr = did_codec.decode_attribute(bytes.fromhex(raw_hex[2:]))
            out.append(self._build_attribute(
                storage_key=key,
                name=attr["name"].decode("utf-8", errors="replace"),
                value=attr["value"],
                validity=attr["validity"],
                created_ms=attr["created_ms"],
            ))
        return out

    def sample_storage_items(self, limit: int = 5) -> list[StorageItem]:
        out: list[StorageItem] = []
        for key in self.iter_storage_keys("PeaqStorage", "ItemStore", limit=limit):
            raw_hex = self.rpc.call("state_getStorage", [key])
            if raw_hex is None:
                continue
            raw = bytes.fromhex(raw_hex[2:])
            try:
                body, _ = did_codec.scale_bytes(raw, 0)
            except did_codec.DecodeError:
                body = raw
            try:
                text = body.decode("utf-8")
            except UnicodeDecodeError:
                text = None
            out.append(StorageItem(storage_key=key, raw_hex=raw_hex, as_text=text))
        return out


def main() -> int:
    """Sonda manual: `python -m faro_peaq.reader`. Sólo imprime; no escribe nada."""
    import json

    reader = PeaqKeylessReader()
    try:
        info = reader.assert_testnet()
    except RpcError as exc:
        print(f"FALLO DE LECTURA (documentado, no simulado): {exc}")
        return 1
    print(json.dumps(info.model_dump(), indent=2, ensure_ascii=False))
    for pallet, item in (("PeaqDid", "AttributeStore"),
                         ("PeaqStorage", "ItemStore"),
                         ("PeaqMor", "MachineRegister")):
        try:
            print(f"{pallet}.{item}: {reader.count_entries(pallet, item)} entradas")
        except Exception as exc:
            print(f"{pallet}.{item}: NO_DATA ({exc})")
    for attr in reader.sample_dids(limit=3):
        print("—", attr.name, "|", attr.document.id if attr.document else attr.decode_error)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
