"""mse_lib_sgx.conversion module."""

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey)
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.serialization import (Encoding,
                                                          NoEncryption,
                                                          PrivateFormat,
                                                          PublicFormat)
from nacl.bindings import (crypto_sign_ed25519_pk_to_curve25519,
                           crypto_sign_ed25519_sk_to_curve25519)


def ed25519_to_x25519_sk(private_key: Ed25519PrivateKey) -> X25519PrivateKey:
    """Map an edwards25519 private key to x25519 private key.

    Parameters
    ----------
    private_key : Ed25519PrivateKey
        Ed25519 private key.

    Returns
    -------
    X25519PrivateKey
        X25519 private key corresponding to `private_key`.

    """
    pk = private_key.public_key().public_bytes(encoding=Encoding.Raw,
                                               format=PublicFormat.Raw)
    seed = private_key.private_bytes(encoding=Encoding.Raw,
                                     format=PrivateFormat.Raw,
                                     encryption_algorithm=NoEncryption())
    x25519_sk: bytes = crypto_sign_ed25519_sk_to_curve25519(seed + pk)

    return X25519PrivateKey.from_private_bytes(x25519_sk)


def ed25519_to_x25519_pk(public_key: Ed25519PublicKey) -> bytes:
    """Map an edwards25519 public key to a curve25519 public key.

    Parameters
    ----------
    public_key: Ed25519PublicKey
        Ed25519 public key.

    Returns
    -------
    bytes
        Bytes of the X25519 public key corresponding to `public_key`.

    """
    return crypto_sign_ed25519_pk_to_curve25519(
        public_key.public_bytes(encoding=Encoding.Raw, format=PublicFormat.Raw))
