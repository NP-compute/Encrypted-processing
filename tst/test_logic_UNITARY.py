from src.logic_gate import Data, Pointer
from src.logic_gate import UNITARY

def test_UNITARY_helper(value: int):
    data_wrapper = Data()
    operation_wrapper = Data()
    output_wrapper = Data()

    # Make a pointer we can set
    pointer_a: Pointer = data_wrapper.make_pointer(value)

    # Perform the UNITARY operation to copy data from data_wrapper to operation_wrapper
    output_pointer = UNITARY(pointer_a, operation_wrapper, output_wrapper)

    # Perform the multiplication process
    output_wrapper.value = data_wrapper.value * operation_wrapper.value

    assert output_pointer.get_value() == value, f'1. Expected 1 but got {output_pointer.get_value()} at an address of {output_pointer.address} with the data values {data_wrapper.value=}, {operation_wrapper.value=} and {output_wrapper.value=}'

def test_UNITARY():
    test_UNITARY_helper(0)
    test_UNITARY_helper(1)

if __name__ == '__main__':
    test_UNITARY()
    print("All UNITARY tests passed.")