"""
faro_peaq — El Faro sobre peaq · Paso 1 (spec + lectura keyless + atestación PREPARADA).

BLINDAJE (invariante de todo el paquete):
  · CERO escritura en cadena. Ni testnet. `rpc.KeylessRpc` sólo admite métodos
    de una allowlist de lectura; cualquier otro método levanta `WriteAttemptError`.
  · CERO claves. Este paquete no genera, no lee y no importa material de firma.
    No hay dependencia de `nacl`, `substrate-interface`, `web3` ni keystore alguno.
  · El constructor de atestación produce un objeto PREPARADO (`prepared=True`,
    `submitted=False`). Nadie en este paquete sabe cómo enviar una extrínseca.

El punto de firma es del carbono, fuera de este paquete y fuera de este nodo.
"""

__version__ = "0.1.0"
__all__ = ["models", "rpc", "reader", "did_codec", "attestation"]
