
def get_bit(value: int, bit_position: int) -> int:
    """Get the bit at the specified position."""
    return (value >> bit_position) & 1

# NOTE: This is for compilation, figure out a better way to do this
class pointer:
    pass

class data:
    # records the data
    def __init__(self):
        self.value: int = 1
        # NOTE: This was supposed to be 0, but it is crashing, may be a bug
        self.contaminated_pointer: int = 2 # This points to the highest bit that is contaminated

    def set_bit(self, bit_position: int, bit_value: int):
        if bit_value not in (0, 1):
            raise ValueError("bit_value must be 0 or 1")
        if bit_value == 1:
            self.value |= (1 << bit_position)
        else:
            self.value &= ~(1 << bit_position)

    def generate_pointer(self) -> pointer:
        # Generate a pointer to the next uncontaminated bit
        new_pointer = pointer(self.contaminated_pointer + 1, self)
        self.contaminated_pointer += 1
        return new_pointer
    
    def get_len_contaminated(self) -> int:
        return self.contaminated_pointer + 1

class pointer:
    # records the position of the pointer
    def __init__(self, position: int, data_pointer: data):
        self.position = position
        self.data_pointer = data_pointer

    def set_value(self, value: int):
        self.data_pointer.set_bit(self.position, value)

    def get_value(self) -> int:
        return get_bit(self.data_pointer.value, self.position)
    
def UNITARY(pointer_b: pointer, data_a: data, output: data) -> pointer:
    """ Performs the unitary operation to make a pointer to the data in the output

    Args:
        pointer_b (pointer): The value to save
        data_a (data): The other dataset that is to be modified
        output (data): The output data object

    Returns:
        pointer: A pointer to the output data object that will have the same value as pointer_b after multiplication
    """
    # Perform the NAND operation

    data_b: data = pointer_b.data_pointer

    # NOTE: To perform operations with the same data object there will need to be a unitary operation to load the data into another data object
    assert pointer_b.data_pointer != data_a, "Pointers must point to different data objects"

    # Update the contaminated pointers in the data
    new_contaminated_pointer = pointer_b.data_pointer.get_len_contaminated() + data_a.get_len_contaminated()
    pointer_b.data_pointer.contaminated_pointer = new_contaminated_pointer
    data_a.contaminated_pointer = new_contaminated_pointer

    # Make the new pointer a that is to be set to 1
    pointer_a: pointer = data_a.generate_pointer()
    pointer_a.set_value(1)

    # Make the output pointer
    output_int: int = pointer_a.position + pointer_b.position
    output_pointer: pointer = pointer(output_int, output)

    return output_pointer

def XOR(pointer_a1: pointer, pointer_a2: pointer, data_b: data, output: data) -> pointer:
    """ Performs the xor operation

    Args:
        pointer_a1 (pointer): The first value to XOR
        pointer_a2 (pointer): The second value to XOR
        data_b (data): The other dataset that is to be modified
        output (data): The output data object

    Returns:
        pointer: A pointer to the output data object that will have the same value as pointer_a XOR pointer_b after multiplication
    """
    
    assert pointer_a1.data_pointer == pointer_a2.data_pointer, "Pointers must point to the same data object"
    assert pointer_a1.data_pointer != data_b, "Pointers must point to different data objects"

    # Set the lower pointer to 1 for the XOR operation
    lower_pointer: pointer = data_b.generate_pointer()
    lower_pointer.set_value(1)

    # Set the upper pointer to 1 for the XOR operation
    upper_pointer_int: int = abs(pointer_a1.position - pointer_a2.position) + lower_pointer.position
    data_b.set_bit(upper_pointer_int, 1)
    upper_pointer: pointer = pointer(upper_pointer_int, data_b)

    # Add in the contaminated pointers
    new_contaminated_pointer: int = lower_pointer.position + upper_pointer.position + 1
    pointer_a1.data_pointer.contaminated_pointer = new_contaminated_pointer
    data_b.contaminated_pointer = new_contaminated_pointer

    # Make the output pointer
    output_int: int = lower_pointer.position + max(pointer_a1.position, pointer_a2.position)
    assert output_int == upper_pointer.position+min(pointer_a1.position, pointer_a2.position), "These should intersect"
    output_pointer: pointer = pointer(output_int, output)

    return output_pointer

def NAND(pointer_b: pointer, data_a: data, output: data) -> tuple[pointer, pointer]:
    """ Performs the nand operation

    Args:
        pointer_b (pointer): _description_
        data_a (data): _description_
        output (data): _description_

    Returns:
        tuple[pointer, pointer]: (pointer the user can set in a, pointer to the result in output data object)
    """
    # Perform the NAND operation

    data_b: data = pointer_b.data_pointer

    # NOTE: To perform operations with the same data object there will need to be a unitary operation to load the data into another data object
    assert pointer_b.data_pointer != data_a, "Pointers must point to different data objects"

    # Update the contaminated pointers in the data
    new_contaminated_pointer = pointer_b.data_pointer.get_len_contaminated() + 2 * data_a.get_len_contaminated()
    pointer_b.data_pointer.contaminated_pointer = new_contaminated_pointer
    data_a  .contaminated_pointer = new_contaminated_pointer

    # Make the new pointer a that is to be set
    pointer_a: pointer = data_a.generate_pointer()

    # Set the value for the 1 for the computation of the NAND
    output_int: int = pointer_a.position+pointer_b.position
    data_b.set_bit(output_int, 1)

    # Make the output pointer
    output_pointer: pointer = pointer(output_int, output)

    return (pointer_a, output_pointer)