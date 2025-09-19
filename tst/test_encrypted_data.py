from src.encrypted_data import EncryptedNumber

def test_encrypt_decrypt():
    variables = {'a': 1, 'b': 2, 'c': 3}

    temp = EncryptedNumber(variables)

    decrypted = temp.decrypt_all()
    assert decrypted == variables, f'the variables were not stored and retreived correctly, {decrypted} == {variables} is not true'

def test_adding_premade_storeage():
    variables = {'a': 1, 'b': 2, 'c': 3}

    temp = EncryptedNumber(variables)

    # Test add a variable into the premade storage
    temp._add_premade_variable_to_storage(5)
    assert 5 in temp.premade_variables, f'did not save to the storage correctly'

    # Try making a new variable d with value 3 using variables we set
    temp.add('d', 'a', 'b')
    expected = variables.copy()
    expected['d'] = 3

    decrypted = temp.decrypt_all()
    assert decrypted == expected, f'1. the variables were not changed correctly, {decrypted} == {expected} is not true'

    # Try making a new variable d with value 3 using variables we set
    temp.add('e', 'a', 2)
    expected['e'] = 3

    decrypted = temp.decrypt_all()
    assert decrypted == expected, f'2. the variables were not changed correctly, {decrypted} == {expected} is not true'

    # Try making a new variable d with value 3 using variables we set
    temp.add('f', 7, 11)
    expected['f'] = 18

    decrypted = temp.decrypt_all()
    assert decrypted == expected, f'3. the variables were not changed correctly, {decrypted} == {expected} is not true'

if __name__ == '__main__':
    test_encrypt_decrypt()
    test_adding_premade_storeage()
    print(f'Finished the encrypted data tests')