from src.rsa import encrypt_int, decrypt_int
from src.generate_data import generate_adding_data

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

def test_enc_zero():
    # This is an edge test to make sure that encrypting 0 doesnt result in 1
    DATA_SIZE = 32
    wrapped_data, data_pointer, data_size = generate_adding_data(0, DATA_SIZE)
    enc_data, key = encrypt_int(wrapped_data)
    
    assert enc_data != 1 or enc_data != 0, f'this isnt really encrypted, need to add a bit or something to prevent this'

if __name__ == "__main__":
    test_rsa_encryption_decryption()
    print("RSA encryption/decryption test passed.")
    
    test_rsa_homomorphic_multiplication()
    print("RSA homomorphic multiplication test passed.")

    test_enc_zero()
    print(f'edge cases passed')