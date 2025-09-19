from src.generate_data import generate_adding_data,  decompose_adding_data
from src.rsa import encrypt_int, decrypt_int, multiply_encrypted

def test_generate_adding():
    unencrypted_data = 3
    data_size = 3
    increment_value = 2
    wrapped_data, data_pointer, data_size = generate_adding_data(unencrypted_data, data_size)
    wrapped_operation, data_pointer2, data_size2 = generate_adding_data(increment_value, data_size)
    
    assert data_pointer == data_pointer2, "Data pointers do not match"
    assert data_size == data_size2, "Data sizes do not match"

    # Make sure we can extract the data
    assert (wrapped_data >> data_size) & data_size == unencrypted_data, f'Failed to extract encrypted data, {wrapped_data} >> {data_size} != {unencrypted_data}'

    # Make sure we can perform the operation and extract the correct data
    answer: int = ((wrapped_data * wrapped_operation) >> data_size) & ((data_size << 1) - 1)
    assert answer == (unencrypted_data + increment_value), f'Failed to perform operation, {answer} != {unencrypted_data} + {increment_value}'
    print(f'more complex operation passed')

def test_decompose_adding():
    unencrypted_data = 5
    data_size = 4
    increment_value = 3
    wrapped_data, data_pointer, data_size = generate_adding_data(unencrypted_data, data_size)
    wrapped_operation, data_pointer2, data_size2 = generate_adding_data(increment_value, data_size)
    
    assert data_pointer == data_pointer2, "Data pointers do not match"
    assert data_size == data_size2, "Data sizes do not match"

    # Decompose the data
    decomposed_data = decompose_adding_data(wrapped_data, data_pointer, data_size)
    assert decomposed_data == unencrypted_data, f'Failed to decompose data, {decomposed_data} != {unencrypted_data}'
    
    # Perform the operation and decompose the result
    result = (wrapped_data * wrapped_operation)
    decomposed_result = decompose_adding_data(result, data_pointer, data_size)
    expected_result = unencrypted_data + increment_value
    assert decomposed_result == expected_result, f'Failed to decompose result, {decomposed_result} != {expected_result}'
    print(f'decomposition test passed')

def test_integration():
    # This test takes the typeical data, encrypts it, performs the operation, and decrypts it back
    unencrypted_data = 7
    data_size = 4
    increment_value = 5
    wrapped_data, data_pointer, data_size = generate_adding_data(unencrypted_data, data_size)
    wrapped_operation, data_pointer2, data_size2 = generate_adding_data(increment_value, data_size)
    
    assert data_pointer == data_pointer2, "Data pointers do not match"
    assert data_size == data_size2, "Data sizes do not match"

    # Encrypt the data
    enc_data, key = encrypt_int(wrapped_data)
    enc_operation, key2 = encrypt_int(wrapped_operation, key=key)

    assert key == key2, "Keys do not match for homomorphic operation"

    # Perform the ENCRYPTED operation on the ENCRYPTED data
    enc_result = multiply_encrypted(enc_data, enc_operation, key)

    # Decrypt the result
    dec_result = decrypt_int(enc_result, key)

    # Decompose the result
    decomposed_result = decompose_adding_data(dec_result, data_pointer, data_size)
    expected_result = unencrypted_data + increment_value
    assert decomposed_result == expected_result, f'Failed to decompose result, {decomposed_result} != {expected_result}'

if __name__ == "__main__":
    test_generate_adding()
    test_decompose_adding()
    test_integration()
    print("Data generation test passed.")