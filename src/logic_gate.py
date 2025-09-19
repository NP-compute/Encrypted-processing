
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
        self.contaminated_pointer: int = 1 # This points to the highest bit that is contaminated

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