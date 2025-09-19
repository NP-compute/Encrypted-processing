from typing import Tuple
from Crypto.PublicKey import RSA
from Crypto.Util import number
import random

# Standalone functions as requested
def encrypt_int(message: int, key_size: int = 2048, key: Tuple[int, int, int] | None = None) -> Tuple[int, Tuple[int, int, int]]:
    """
    Encrypt an integer using RSA.
    
    Args:
        message: Integer to encrypt
        key_size: Size of RSA key to generate
        key: Optional pre-generated RSA key (n, e, d)

    Returns:
        Tuple of (encrypted_message, decrypt_key)
    """
    if key is None:
        key = RSA.generate(key_size)
        n, e, d = key.n, key.e, key.d
    else:
        n, e, d = key

    if message >= n:
        raise ValueError(f"Message must be less than n ({n})")
    
    encrypted = pow(message, e, n)
    decrypt_key = (n, e, d)
    
    return encrypted, decrypt_key

def decrypt_int(encrypted_message: int, key: Tuple[int, int, int]) -> int:
    """
    Decrypt an RSA-encrypted message.
    
    Args:
        encrypted_message: The encrypted integer
        decrypt_key: Tuple of (n, d) - the private key
    
    Returns:
        The decrypted integer
    """
    n, e, d = key
    decrypted = pow(encrypted_message, d, n)
    return decrypted

def multiply_encrypted(enc_a: int, enc_b: int, key: Tuple[int, int, int]) -> int:
    """
    Multiply two RSA-encrypted integers.
    """
    n, e, d = key
    return (enc_a * enc_b) % n
