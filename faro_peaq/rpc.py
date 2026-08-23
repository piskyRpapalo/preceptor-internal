"""
rpc.py — Cliente JSON-RPC KEYLESS contra peaq.

Diseño deliberado (mismo patrón que `hexelion/faro/chain_verify.py`, que es
read-only y aislado): `urllib` de la stdlib, cero SDK, cero `web3`, cero
`substrate-interface`, cero keystore.

BLINDAJE MECÁNICO — no es una promesa en un comentario, es un `if`:
  · `READ_METHODS` es una allowlist cerrada. Todo método fuera de ella levanta
    `WriteAttemptError` ANTES de tocar el socket.
  · No hay ningún camino en este módulo que construya, firme o envíe una
    extrínseca. `author_submitExtrinsic` y familia están explícitamente vetados.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from .models import AGUNG_ONFINALITY, ChainInfo, PeaqEndpoint

# Allowlist cerrada. Todo lo de aquí es lectura pura de estado o metadatos.
READ_METHODS: frozenset[str] = frozenset({
    # Substrate — cadena y estado
    "system_chain",
    "system_name",
    "system_version",
    "system_properties",
    "system_health",
    "chain_getBlockHash",
    "chain_getHeader",
    "chain_getFinalizedHead",
    "state_getMetadata",
    "state_getRuntimeVersion",
    "state_getStorage",
    "state_getKeysPaged",
    "rpc_methods",
    # peaq — RPC propios de los pallets (todos de lectura)
    "peaqdid_readAttribute",
    "peaqstorage_readAttribute",
    "peaqrbac_fetchRole",
    "peaqrbac_fetchRoles",
    "peaqrbac_fetchGroup",
    "peaqrbac_fetchGroups",
    "peaqrbac_fetchPermission",
    "peaqrbac_fetchPermissions",
    "peaqrbac_fetchUserRoles",
    "peaqrbac_fetchUserGroups",
    "peaqrbac_fetchUserPermissions",
    # EVM — sólo lectura (eth_call incluido: es una llamada sin estado)
    "eth_chainId",
    "eth_blockNumber",
    "eth_getCode",
    "eth_call",
    "eth_getBalance",
    "net_version",
})

# Vetados de forma explícita para que el error sea legible, no un KeyError.
WRITE_METHODS: frozenset[str] = frozenset({
    "author_submitExtrinsic",
    "author_submitAndWatchExtrinsic",
    "author_insertKey",
    "author_rotateKeys",
    "author_hasKey",
    "author_hasSessionKeys",
    "eth_sendTransaction",
    "eth_sendRawTransaction",
    "eth_sign",
    "eth_signTransaction",
    "personal_sign",
    "personal_unlockAccount",
    "peaqdid_addAttribute",
    "peaqstorage_addItem",
})


class WriteAttemptError(RuntimeError):
    """Se intentó un método que no está en la allowlist de lectura. Paso 1 = seco."""


class RpcError(RuntimeError):
    """El nodo respondió con un error JSON-RPC, o la respuesta no es JSON-RPC."""


class KeylessRpc:
    """Cliente JSON-RPC de sólo lectura. No sabe firmar. No tiene dónde guardar una clave."""

    def __init__(self, endpoint: PeaqEndpoint = AGUNG_ONFINALITY, timeout: int = 30) -> None:
        self.endpoint = endpoint
        self.timeout = timeout
        self.calls = 0

    # ── núcleo ──────────────────────────────────────────────────────────────

    def call(self, method: str, params: list[Any] | None = None) -> Any:
        if method in WRITE_METHODS:
            raise WriteAttemptError(
                f"'{method}' es un método de escritura/firma. El Paso 1 es seco: "
                "cero escritura en cadena, ni en testnet."
            )
        if method not in READ_METHODS:
            raise WriteAttemptError(
                f"'{method}' no está en la allowlist de lectura de faro_peaq.rpc. "
                "Si de verdad es de lectura, añádelo a READ_METHODS con motivo declarado."
            )
        body = json.dumps({
            "jsonrpc": "2.0", "id": self.calls + 1,
            "method": method, "params": params or [],
        }).encode()
        req = urllib.request.Request(
            self.endpoint.url, data=body,
            headers={"Content-Type": "application/json",
                     "User-Agent": "hexelion-faro-peaq-keyless/0.1"},
            method="POST",
        )
        self.calls += 1
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                parsed = json.loads(resp.read())
        except urllib.error.URLError as exc:
            raise RpcError(f"{self.endpoint.url} inalcanzable: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise RpcError(f"{self.endpoint.url} no devolvió JSON: {exc}") from exc
        if "error" in parsed:
            raise RpcError(f"{method}: {parsed['error']}")
        if "result" not in parsed:
            raise RpcError(f"{method}: respuesta sin 'result': {parsed!r}")
        return parsed["result"]

    # ── conveniencias ───────────────────────────────────────────────────────

    def chain_info(self) -> ChainInfo:
        """Identidad de la cadena. Si esto no es 'Agung network', para y reporta."""
        return ChainInfo(
            chain=self.call("system_chain"),
            node_version=self.call("system_version"),
            eth_chain_id=int(self.call("eth_chainId"), 16),
            block_number=int(self.call("eth_blockNumber"), 16),
            endpoint=self.endpoint.url,
        )

    def assert_testnet(self) -> ChainInfo:
        """
        Falla ruidosamente si el endpoint no es agung. Barrera anti-mainnet:
        aunque este paquete no pueda escribir, tampoco debe LEER creyendo que
        lee testnet cuando está mirando mainnet.
        """
        info = self.chain_info()
        if info.eth_chain_id != 9990 or "agung" not in info.chain.lower():
            raise RpcError(
                f"Se esperaba agung (chain_id 9990) y se encontró "
                f"{info.chain!r} chain_id={info.eth_chain_id}. PARO."
            )
        return info
