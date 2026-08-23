"""
Tests del BLINDAJE del cliente RPC. Ninguno toca la red: el veto ocurre antes
del socket, que es justo lo que hay que demostrar.
"""

import pytest

from faro_peaq import rpc


@pytest.mark.parametrize("method", sorted(rpc.WRITE_METHODS))
def test_todo_metodo_de_escritura_es_vetado(method):
    client = rpc.KeylessRpc()
    with pytest.raises(rpc.WriteAttemptError):
        client.call(method, [])
    assert client.calls == 0, "el veto debe ocurrir antes de tocar el socket"


def test_metodo_desconocido_tambien_es_vetado():
    client = rpc.KeylessRpc()
    with pytest.raises(rpc.WriteAttemptError):
        client.call("author_unsafeMagicThing", [])
    assert client.calls == 0


def test_allowlist_y_veto_no_se_solapan():
    assert not (rpc.READ_METHODS & rpc.WRITE_METHODS)


def test_allowlist_no_contiene_nada_que_huela_a_firma():
    prohibido = ("submit", "sign", "sendtransaction", "sendraw",
                 "insertkey", "rotatekeys", "unlock", "additem", "addattribute")
    for method in rpc.READ_METHODS:
        low = method.lower()
        assert not any(p in low for p in prohibido), f"{method} no pinta de lectura"


def test_el_paquete_no_importa_maquinaria_de_firma():
    """
    Regla de suelo: si algún día alguien mete `nacl`, `web3`, `substrateinterface`
    o `peaq_sdk` en este paquete, este test lo delata.
    """
    import pathlib

    raiz = pathlib.Path(__file__).resolve().parent.parent
    prohibidos = ("import nacl", "from nacl", "import web3", "from web3",
                  "substrateinterface", "peaq_sdk", "SigningKey", "PrivateKey")
    for fichero in raiz.glob("*.py"):
        texto = fichero.read_text(encoding="utf-8")
        for aguja in prohibidos:
            assert aguja not in texto, f"{fichero.name} contiene {aguja!r}"
