from src.logic_gate import Data, Pointer
from src.logic_gate import AND

def test_AND_helper(value1: int, value2: int):
    data_wrapper = Data()
    operation_wrapper = Data()
    output_wrapper = Data()

    # Make pointers we can set
    pointer_a: Pointer = data_wrapper.make_pointer(value1)
    pointer_b: Pointer = data_wrapper.make_pointer(value2)

    # Perform the AND operation
    output_pointer = AND(pointer_a, pointer_b, operation_wrapper, output_wrapper)

    # Perform the AND process
    output_wrapper.value = data_wrapper.value * operation_wrapper.value

    assert output_pointer.get_value() == (value1 & value2), f'1. Expected {value1 & value2} but got {output_pointer.get_value()} at an address of {output_pointer.address} with the data values {data_wrapper.value=}, {operation_wrapper.value=} and {output_wrapper.value=}'

def test_AND():
    test_AND_helper(0, 0)
    test_AND_helper(0, 1)
    test_AND_helper(1, 0)
    test_AND_helper(1, 1)

if __name__ == '__main__':
    test_AND()
    print("All AND tests passed.")