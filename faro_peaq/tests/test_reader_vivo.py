"""
Tests del lector contra agung EN VIVO.

Se saltan solos si no hay red (`FARO_PEAQ_LIVE=0` o fallo de conexión): un test
de red que revienta el CI no aporta, pero uno que MIENTE es peor. Por eso, si el
RPC no responde, esto marca `skip` con el motivo, no `pass`.
"""

import os

import pytest

from faro_peaq.models import AGUNG_ONFINALITY
from faro_peaq.reader import KNOWN_PREFIXES, PeaqKeylessReader, storage_prefix
from faro_peaq.rpc import RpcError

LIVE = os.environ.get("FARO_PEAQ_LIVE", "1") != "0"


@pytest.fixture(scope="module")
def reader():
    if not LIVE:
        pytest.skip("FARO_PEAQ_LIVE=0")
    r = PeaqKeylessReader(AGUNG_ONFINALITY, timeout=25)
    try:
        r.assert_testnet()
    except RpcError as exc:
        pytest.skip(f"agung inalcanzable desde este nodo: {exc}")
    return r


def test_prefijos_calculados_coinciden_con_los_verificados():
    """Si xxhash no está, cae a la tabla; si está, debe reproducirla exactamente."""
    for clave, esperado in KNOWN_PREFIXES.items():
        pallet, item = clave.split(".")
        assert storage_prefix(pallet, item) == esperado


def test_es_agung_y_no_mainnet(reader):
    info = reader.chain_info()
    assert info.chain == "Agung network"
    assert info.eth_chain_id == 9990
    assert info.block_number > 10_000_000


def test_hay_dids_reales_y_decodifican(reader):
    muestras = reader.sample_dids(limit=5)
    assert muestras, "agung debería tener DIDs; si no, es hallazgo, no fallo de test"
    decodificados = [m for m in muestras if m.document is not None]
    assert decodificados, [m.decode_error for m in muestras]
    assert any(m.document.id.startswith("did:peaq:") for m in decodificados)
    # Los dos envoltorios conviven en cadena: se documenta, no se asume uno.
    assert {m.document.wrapper for m in decodificados} <= {"hex-ascii", "raw-proto"}


def test_hay_items_de_storage_reales(reader):
    items = reader.sample_storage_items(limit=5)
    assert items
    assert all(i.raw_hex.startswith("0x") for i in items)


def test_did_inexistente_devuelve_none_sin_romper(reader):
    ausente = reader.read_did(
        "5Df42mkztLtkksgQuLy4YV6hmhzdjYvDknoxHv1QBkaY12Pg",
        "no-existe-este-did-hexelion",
    )
    assert ausente is None
