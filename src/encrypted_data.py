# This is a class that will allow numbers to be encrypted with a private key
# The numbers can be added together
# The numbers can also be multiplied by a known amount
# There will be checks with public keys to make sure we can combine numbers safely

from src.generate_data import generate_adding_data, decompose_adding_data
from src.rsa import encrypt_int, decrypt_int, multiply_encrypted

DATA_SIZE = 32

def generate_encrypted_data(unencrypted_data: int, key: int) -> tuple[int, int]:
    wrapped_data, data_pointer, data_size = generate_adding_data(unencrypted_data, DATA_SIZE)
    enc_data, key = encrypt_int(wrapped_data, key=key)
    return enc_data, data_pointer

def decrypt_encrypted_data(enc_data: int, data_pointer: int, data_size: int, key: int) -> int:
    dec_data = decrypt_int(enc_data, key)
    unencrypted_data = decompose_adding_data(dec_data, data_pointer, data_size)
    return unencrypted_data

def seperate_bits(value: int) -> tuple[int, int]:
    """ This function takes an int and seperates into two non zero ints (if possible) that add to the original value

    Args:
        value (int): _description_

    Raises:
        ValueError: _description_

    Returns:
        tuple[int, int]: _description_
    """

    a = value // 2
    b = a + (value % 2)

    return a, b

class EncryptedNumber:
    def __init__(self, variables: dict[str, int], key: int|None=None):
        # Variables are the variables the user set
        # Premade variables are variables the user doesnt see for certain operations
        self.variables: dict[str, int] = {}
        self.premade_variables: dict[int, int] = {}

        # Add zero into the encryption
        wrapped_zero, self.data_pointer, data_size = generate_adding_data(0, DATA_SIZE)
        enc_zero, self.key = encrypt_int(wrapped_zero)
        self.premade_variables[0] = enc_zero

        # Loop through the bit shifted encodings for every bit
        for shift in range(0, DATA_SIZE):

            data: int = 1 << shift

            enc_data, data_pointer = generate_encrypted_data(data, self.key)
            self.premade_variables[data] = enc_data

        # Add in the variables the user wanted
        self.add_variables(variables)

    def add_variables(self, variables: dict[str, int]):
        for var, value in variables.items():
            if var in self.variables:
                raise ValueError(f"Variable '{var}' already exists.")
            else:
                enc_data, data_pointer = generate_encrypted_data(value, self.key)
                self.variables[var] = enc_data
    
    def _add_premade_variable_to_storage(self, value: int) -> int:
        # This function adds premade variables into storage for later usage

        # Make sure the variable is within the acceptable range
        assert value < (1 << DATA_SIZE), f'Value must be lower than {1 << DATA_SIZE} and it is {value}'
        assert value >= 0, f'Value must be non negative, but is {value}'

        # Also makes sure the variable doesnt already exist
        if value in self.premade_variables:
            return self.premade_variables[value]

        # TODO: Optimize this seperate bit function
        a, b = seperate_bits(value)

        # TODO: Add a memory for each variable we calculate, also use the memory for faster compute
        enc_a = self._add_premade_variable_to_storage(a)
        enc_b = self._add_premade_variable_to_storage(b)

        enc_value = multiply_encrypted(enc_a, enc_b, self.key)

        self.premade_variables[value] = enc_value
        return enc_value

    def _get_enc(self, name: str|int) -> int:
        """ Get the encrypted value with the requested name

        Args:
            name (str | int): A string in the variable dictionary or an integer.

        Returns:
            int: The encrypted value
        """

        return self.variables[name] if isinstance(name, str) else self._add_premade_variable_to_storage(name)

    def add(self, a: str, b: str|int, c: str|int) -> None:
        """

        Does the equation a=b+c but encrypted. Save in a, will override any existing value that is in a

        Args:
            a (str): The name of the variable to store the result.
            b (str | int): The first operand, either a variable name or an integer.
            c (str | int): The second operand, either a variable name or an integer.
        """

        b_enc: int = self._get_enc(b)
        c_enc: int = self._get_enc(c)

        assert b_enc is not None and c_enc is not None, f'{b_enc=} and {c_enc=} cannot be none'

        self.variables[a] = multiply_encrypted(b_enc, c_enc, self.key)

        return self.variables[a]
    
    def decrypt_all(self) -> dict[str, int]:
        # This function decrpyts everything in the variables

        variables_copy = dict()

        for var, value in self.variables.items():
            variables_copy[var] = decrypt_encrypted_data(value, self.data_pointer, DATA_SIZE, self.key)

        return variables_copy