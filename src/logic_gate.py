import random

NUMBER_INITIAL_BITS = 256

def get_bit(value: int, bit_position: int) -> int:
    """Get the bit at the specified position."""
    return (value >> bit_position) & 1

# NOTE: This is for compilation, figure out a better way to do this
class pointer:
    pass

class data:
    # records the data
    # IMPORTANT TODO: Add in a way to track which bits have been contaminated
    def __init__(self, value: int | None = None, allowed_initial_bits_start: int = 1, allowed_initial_bits_end: int = NUMBER_INITIAL_BITS - 1):
        # This is the value stored in the data
        self.value: int = 1 if value is None else value

        # This is the range of bits that can be used for initial pointers
        self.allowed_initial_bits_start = allowed_initial_bits_start
        self.allowed_initial_bits_end = allowed_initial_bits_end

    def _set_bit(self, bit_position: int, bit_value: int):
        if bit_value not in (0, 1):
            raise ValueError("bit_value must be 0 or 1")
        if bit_value == 1:
            self.value |= (1 << bit_position)
        else:
            self.value &= ~(1 << bit_position)

    def generate_pointer(self, pointer_address: int | None = None) -> pointer:

        # Set the pointer to a random value between allowed_initial_bits_start and allowed_initial_bits_end inclusive
        if pointer_address is None:
            pointer_address = random.randint(self.allowed_initial_bits_start, self.allowed_initial_bits_end)

        return pointer(pointer_address, self)
    
    def get_value(self):
        return self.value

class pointer:
    # records the position of the pointer
    def __init__(self, position: int, data_pointer: data):
        self.position = position
        self.data_pointer = data_pointer

    def get_value(self) -> int:
        return get_bit(self.data_pointer.value, self.position)
    
    def set_value(self, bit_value: int):
        self.data_pointer._set_bit(self.position, bit_value)
    
    def get_address(self) -> int:
        return self.position

def AND(a: pointer, b: pointer) -> pointer:

    # Needs to add the pointer addresses to get the address of the new pointer
    new_address = a.get_address() + b.get_address()

    # Needs to multiply the values to get the value of the data
    new_value = a.data_pointer.get_value() * b.data_pointer.get_value()

    # Make data and pointer then return the pointer
    new_data = data(new_value)
    return new_data.generate_pointer(new_address)

def NOT(a: pointer) -> pointer:
    
    # Needs to copy the pointer address to get the address of the new pointer
    new_address = a.get_address()

    # Needs to multiply the value by a data with bit value 1 at address 0 and bit value 1 at the pointer address
    temp_data: data = data(1)
    temp_data._set_bit(new_address, 1)
    new_value = a.data_pointer.get_value() * temp_data.get_value()

    # Make data and pointer then return the pointer
    new_data = data(new_value)
    return new_data.generate_pointer(new_address)