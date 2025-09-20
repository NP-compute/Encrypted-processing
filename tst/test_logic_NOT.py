from src.logic_gate import Data, Pointer
from src.logic_gate import NOT

def test_NOT_helper(value: int):
    data_wrapper = Data()
    operation_wrapper = Data()
    output_wrapper = Data()

    # Make a pointer we can set
    pointer_a: Pointer = data_wrapper.make_pointer(value)

    # Perform the NOT operation
    output_pointer = NOT(pointer_a, operation_wrapper, output_wrapper)

    # Perform the NOT process
    output_wrapper.value = data_wrapper.value * operation_wrapper.value

    assert output_pointer.get_value() == (1 - value), f'1. Expected {1 - value} but got {output_pointer.get_value()} at an address of {output_pointer.address} with the data values {data_wrapper.value=}, {operation_wrapper.value=} and {output_wrapper.value=}'

def test_NOT():
    test_NOT_helper(0)
    test_NOT_helper(1)

if __name__ == '__main__':
    test_NOT()
    print("All NOT tests passed.")
