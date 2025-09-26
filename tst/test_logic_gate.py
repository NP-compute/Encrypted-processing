from src.logic_gate import data, pointer, AND, NOT

def _test_helper_NOT(start_bit_value: int):

    data_a = data()

    # Make a pointer, set the pointer value to the start_bit_value
    pointer_a = data_a.generate_pointer()
    pointer_a.set_value(start_bit_value)

    # Perform the NOT operation
    output_pointer = NOT(pointer_a)

    # Check the output value
    assert output_pointer.get_value() == (1 - start_bit_value), f'Expected {1 - start_bit_value} but got {output_pointer.get_value()}\n for data values {data_a.value=}'

def test_NOT():
    _test_helper_NOT(0)
    _test_helper_NOT(1)

def _test_helper_AND(start_bit_value_a: int, start_bit_value_b: int):

    data_a = data()
    data_b = data()

    # Make pointers, set the pointer values to the start_bit_values
    pointer_a = data_a.generate_pointer()
    pointer_a.set_value(start_bit_value_a)
    pointer_b = data_b.generate_pointer()
    pointer_b.set_value(start_bit_value_b)

    # Perform the AND operation
    output_pointer = AND(pointer_a, pointer_b)

    # Check the output value
    assert output_pointer.get_value() == (start_bit_value_a * start_bit_value_b), f'Expected {start_bit_value_a * start_bit_value_b} but got {output_pointer.get_value()}\n for data values {data_a.value=} and {data_b.value=}'

def test_AND():
    _test_helper_AND(0, 0)
    _test_helper_AND(0, 1)
    _test_helper_AND(1, 0)
    _test_helper_AND(1, 1)

if __name__ == "__main__":
    test_NOT()
    test_AND()
    print("Unit logic gates tests passed")