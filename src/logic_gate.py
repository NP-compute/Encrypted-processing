from src.constants import COMPUTE_SIZE, CONTAMINATION_SIZE

class Data:
    # records the data
    def __init__(self):
        self.value: int = 1
        # NOTE: This pointer points to the MSB contaiminated bit
        self.contaminated_pointer: int = COMPUTE_SIZE

    def set_bit(self, bit_position: int, bit_value: int):
        assert self.contaminated_pointer < bit_position, "Cannot set a bit in the contaminated region"

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

    def make_pointer(self, value: int, total_buffer: int = 1) -> 'Pointer':
        assert value in (0, 1), f'must be 0 or 1 but got {value=}'

        # Add buffer to make sure there is no carry error
        self.add_buffer(total_buffer)

        address: int = self.get_contaminated_len()
        self.set_bit(address, value)
        self.set_contaminated_pointer(address)

        # Add a buffer on the other side too
        self.add_buffer(total_buffer)

        return Pointer(address, self)
    
    def add_buffer(self, buffer_size: int = 1):
        assert buffer_size > 0, "Buffer size must be positive"
        self.set_contaminated_pointer(self.get_contaminated_pointer() + buffer_size)

    def contamination_ok(self) -> bool:
        return (1 << self.get_contaminated_len()) > self.value

class Pointer:
    def __init__(self, address: int, data_pointer: Data):
        self.address = address
        self.data_pointer = data_pointer

    def set_value(self, value: int):
        self.data_pointer.set_bit(self.address, value)

    def get_value(self) -> int:
        return self.data_pointer.get_bit(self.address)
    
    def __str__(self):
        return f'Pointer(address={self.address}, value={self.get_value()})'

def contamination_check_output(value_wrapper_before_operation: int, value_wrapper_after_operation: int):
    # Make sure adding an operation does not change the operation before
    
    a: int = value_wrapper_before_operation
    b: int = value_wrapper_after_operation

    assert b > a

    temp: int = a ^ b
    temp = temp & a

    assert temp == 0, f'Need to make sure not contamination the earlier process'

def output_check(data_pointer: Pointer):
    # Make sure there is a buffer of at least 1 around the output pointer

    assert Pointer(data_pointer.address - 1, data_pointer.data_pointer).get_value() == 0, "There must be a 0 bit below the output pointer to avoid carry issues"
    assert Pointer(data_pointer.address + 1, data_pointer.data_pointer).get_value() == 0, "There must be a 0 bit above the output pointer to avoid carry issues"

# IMPORTANT TODO: Check if contamination occurs when the operations are multiplied together

def UNITARY(data_pointer_a: Pointer, operation_wrapper: Data, output_wrapper: Data, buffer: int = 1) -> Pointer:

    data_wrapper: Data = data_pointer_a.data_pointer
    data_wrapper.add_buffer(buffer)
    operation_wrapper.add_buffer(buffer)

    a: int = data_wrapper.value * operation_wrapper.value

    assert data_wrapper.contamination_ok(), f'The contamination for data_wrapper is not ok'
    assert operation_wrapper.contamination_ok(), f'The contamination for operation_wrapper is not ok'
    assert output_wrapper.contamination_ok(), f'The contamination for output_wrapper is not ok'

    # Set operation wrapper value to 1
    operation_address = max(operation_wrapper.get_contaminated_len(), data_wrapper.get_contaminated_len(), output_wrapper.get_contaminated_len())
    operation_wrapper.set_bit(operation_address, 1)
    operation_wrapper.set_contaminated_pointer(operation_address)
    
    # Calculate the contamination for all 3 Data wrappers
    assert data_pointer_a.address <= data_pointer_a.data_pointer.get_contaminated_pointer(), "Data should be in the contaminated region for now"
    new_contamination_len: int = data_wrapper.get_contaminated_len() + operation_wrapper.get_contaminated_len()
    operation_wrapper.set_contaminated_len(new_contamination_len)
    data_wrapper.set_contaminated_len(new_contamination_len)
    output_wrapper.set_contaminated_len(2 * new_contamination_len)

    b: int = data_wrapper.value * operation_wrapper.value
    contamination_check_output(a, b)

    # Return resulting pointer
    return Pointer(operation_address + data_pointer_a.address, output_wrapper)

def AND(data_pointer_a: Pointer, data_pointer_b: Pointer, operation_wrapper:Data, output_wrapper: Data, buffer: int = 1) -> Pointer:

    data_wrapper: Data = data_pointer_a.data_pointer
    assert data_wrapper is data_pointer_b.data_pointer, "Data pointers must point to the same Data instance"
    data_wrapper.add_buffer(buffer)
    operation_wrapper.add_buffer(buffer)

    a: int = data_wrapper.value * operation_wrapper.value

    assert data_wrapper.contamination_ok(), f'The contamination for data_wrapper is not ok'
    assert operation_wrapper.contamination_ok(), f'The contamination for operation_wrapper is not ok'
    assert output_wrapper.contamination_ok(), f'The contamination for output_wrapper is not ok'

    # Set lower operation wrapper value to 1
    operation_address_lower = max(operation_wrapper.get_contaminated_len(), data_wrapper.get_contaminated_len(), output_wrapper.get_contaminated_len())
    operation_wrapper.set_bit(operation_address_lower, 1)

    print(f'lower address {Pointer(operation_address_lower, operation_wrapper)} 1 under as {Pointer(operation_address_lower - 1, operation_wrapper)} 1 over as {Pointer(operation_address_lower + 1, operation_wrapper)}')

    # Set upper operation wrapper value to 1
    operation_address_upper = operation_address_lower + abs(data_pointer_a.address - data_pointer_b.address)
    operation_wrapper.set_bit(operation_address_upper, 1)
    operation_wrapper.set_contaminated_pointer(operation_address_upper)

    print(f'upper address {Pointer(operation_address_upper, operation_wrapper)} 1 under as {Pointer(operation_address_upper - 1, operation_wrapper)} 1 over as {Pointer(operation_address_upper + 1, operation_wrapper)}')

    # Check to make sure there is a small buffer between the two addresses
    assert abs(data_pointer_a.address - data_pointer_b.address) > 1, "Data pointers must be at least 2 bits apart to avoid carry issues"

    # Calculate the contamination for all 3 Data wrappers
    new_contamination_len: int = data_wrapper.get_contaminated_len() + operation_wrapper.get_contaminated_len()
    operation_wrapper.set_contaminated_len(new_contamination_len)
    data_wrapper.set_contaminated_len(new_contamination_len)
    output_wrapper.set_contaminated_len(2 * new_contamination_len)

    # Return resulting pointer
    output_pointer_int: int = operation_address_lower + data_pointer_b.address
    assert output_pointer_int == operation_address_upper + data_pointer_a.address, "These should intersect at the same point"
    output_pointer_int += 1

    b: int = data_wrapper.value * operation_wrapper.value
    contamination_check_output(a, b)

    return Pointer(output_pointer_int, output_wrapper)

def NOT(data_pointer_a: Pointer, operation_wrapper: Data, output_wrapper: Data, buffer: int = 1) -> Pointer:
    
    data_wrapper: Data = data_pointer_a.data_pointer
    data_wrapper.add_buffer(buffer)
    operation_wrapper.add_buffer(buffer)

    a: int = data_wrapper.value * operation_wrapper.value

    assert data_wrapper.contamination_ok(), f'The contamination for data_wrapper is not ok'
    assert operation_wrapper.contamination_ok(), f'The contamination for operation_wrapper is not ok'
    assert output_wrapper.contamination_ok(), f'The contamination for output_wrapper is not ok'

    # Set lower operation wrapper value to 1
    operation_address_lower = max(operation_wrapper.get_contaminated_len(), data_wrapper.get_contaminated_len(), output_wrapper.get_contaminated_len())
    operation_wrapper.set_bit(operation_address_lower, 1)

    # Set upper operation wrapper value to 1
    operation_address_upper = operation_address_lower + data_pointer_a.address
    operation_wrapper.set_bit(operation_address_upper, 1)
    operation_wrapper.set_contaminated_pointer(operation_address_upper)

    # Check to make sure there is a small buffer between the two addresses
    assert data_pointer_a.address > 0, "Data pointer must be at least 1 bit away from 0 to avoid carry issues"

    # Calculate the contamination for all 3 Data wrappers
    new_contamination_len: int = data_wrapper.get_contaminated_len() + operation_wrapper.get_contaminated_len()
    operation_wrapper.set_contaminated_len(new_contamination_len)
    data_wrapper.set_contaminated_len(new_contamination_len)
    output_wrapper.set_contaminated_len(2 * new_contamination_len)

    # Return resulting pointer
    output_pointer_int: int = operation_address_lower + data_pointer_a.address
    assert output_pointer_int == operation_address_upper, "These should intersect at the same point"
    b: int = data_wrapper.value * operation_wrapper.value
    contamination_check_output(a, b)
    return Pointer(output_pointer_int, output_wrapper)