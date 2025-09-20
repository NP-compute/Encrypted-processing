class Data:
    # records the data
    def __init__(self):
        self.value: int = 1
        # NOTE: This pointer points to the MSB contaiminated bit
        self.contaminated_pointer: int = 0

    def set_bit(self, bit_position: int, bit_value: int):
        if bit_value not in (0, 1):
            raise ValueError("bit_value must be 0 or 1")
        if bit_value == 1:
            self.value |= (1 << bit_position)
        else:
            self.value &= ~(1 << bit_position)

    def get_bit(self, bit_position: int) -> int:
        """Get the bit at the specified position."""
        return (self.value >> bit_position) & 1

    def get_contaminated_len(self) -> int:
        return self.contaminated_pointer + 1
    
    def get_contaminated_pointer(self) -> int:
        return self.contaminated_pointer
    
    def set_contaminated_pointer(self, new_pointer: int):
        assert new_pointer >= self.contaminated_pointer
        self.contaminated_pointer = new_pointer

    def set_contaminated_len(self, new_len: int):
        self.set_contaminated_pointer(new_len - 1)

    def make_pointer(self, value: int) -> 'Pointer':
        assert value in (0, 1), f'must be 0 or 1 but got {value=}'

        address: int = self.get_contaminated_len()
        self.set_bit(address, value)
        self.set_contaminated_pointer(address)

        return Pointer(address, self)
    
    def add_buffer(self, buffer_size: int = 1):
        assert buffer_size > 0, "Buffer size must be positive"
        self.set_contaminated_pointer(self.get_contaminated_pointer() + buffer_size)

class Pointer:
    def __init__(self, address: int, data_pointer: Data):
        self.address = address
        self.data_pointer = data_pointer

    def set_value(self, value: int):
        self.data_pointer.set_bit(self.address, value)

    def get_value(self) -> int:
        return self.data_pointer.get_bit(self.address)

def UNITARY(data_pointer_a: Pointer, operation_wrapper: Data, output_wrapper: Data) -> Pointer:

    data_wrapper: Data = data_pointer_a.data_pointer
    data_wrapper.add_buffer()
    operation_wrapper.add_buffer()

    # Set operation wrapper value to 1
    operation_address = operation_wrapper.get_contaminated_len()
    operation_wrapper.set_bit(operation_address, 1)
    operation_wrapper.set_contaminated_pointer(operation_address)
    
    # Calculate the contamination for all 3 Data wrappers
    assert data_pointer_a.address <= data_pointer_a.data_pointer.get_contaminated_pointer(), "Data should be in the contaminated region for now"
    new_contamination_len: int = data_wrapper.get_contaminated_len() + operation_wrapper.get_contaminated_len()
    output_wrapper.set_contaminated_len(new_contamination_len)
    operation_wrapper.set_contaminated_len(new_contamination_len)
    data_wrapper.set_contaminated_len(new_contamination_len)

    # Return resulting pointer
    return Pointer(operation_address + data_pointer_a.address, output_wrapper)

def AND(data_pointer_a: Pointer, data_pointer_b: Pointer, operation_wrapper:Data, output_wrapper: Data) -> Pointer:
    pass

def NOT(data_pointer_a: Pointer, operation_wrapper: Data, output_wrapper: Data) -> Pointer:
    pass