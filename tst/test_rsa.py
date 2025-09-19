from src.rsa import encrypt_int, decrypt_int

def test_rsa_encryption_decryption():
    original_message = 12345
    encrypted_message, decrypt_key = encrypt_int(original_message)
    decrypted_message = decrypt_int(encrypted_message, decrypt_key)
    assert original_message == decrypted_message, "Decrypted message does not match original"

def test_rsa_homomorphic_multiplication():
    original_msg = 123
    multiplier = 456
    
    # Encrypt original message
    enc_msg, key = encrypt_int(original_msg)
    
    # Encrypt multiplier
    enc_multiplier, key2 = encrypt_int(multiplier, key=key)

    assert key == key2, "Keys do not match for homomorphic operation"
    
    # Multiply encrypted values
    enc_result = (enc_msg * enc_multiplier) % key[0]
    
    # Decrypt result
    decrypted_result = decrypt_int(enc_result, key)
    expected_result = original_msg * multiplier
    
    assert decrypted_result == expected_result, "Homomorphic multiplication failed"

if __name__ == "__main__":
    test_rsa_encryption_decryption()
    print("RSA encryption/decryption test passed.")
    
    test_rsa_homomorphic_multiplication()
    print("RSA homomorphic multiplication test passed.")