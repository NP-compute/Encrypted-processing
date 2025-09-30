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

def test_contamination():
    # AND
    data_a = data(number_initial_bits=2)
    data_b = data(number_initial_bits=2)

    # Make pointers, set the pointer values to the start_bit_values
    pointer_a = data_a.generate_pointer()
    pointer_a.set_value(1)
    pointer_b = data_b.generate_pointer()
    pointer_b.set_value(1)

    # Perform the AND operation
    # NOTE: this should return None due to contamination overlap
    output_pointer = AND(pointer_a, pointer_b)

    assert output_pointer is None, f'Expected None due to contamination overlap but got {output_pointer} with contamination {data_a.contamination_track=} and {data_b.contamination_track} and {output_pointer.data_pointer.contamination_track=}'

    # NOT
    data_c = data(number_initial_bits=2)

    # Make a pointer, set the pointer value to the start_bit_value
    pointer_c = data_c.generate_pointer()
    pointer_c.set_value(0)

    # Perform the NOT operation
    output_pointer = NOT(pointer_c)

    # Check the output value
    assert output_pointer.get_value() == 1, f'Expected 1 but got {output_pointer.get_value()} with contamination {data_a.contamination_track=} and {output_pointer.data_pointer.contamination_track=}'

def test_AND():
    _test_helper_AND(0, 0)
    _test_helper_AND(0, 1)
    _test_helper_AND(1, 0)
    _test_helper_AND(1, 1)

if __name__ == "__main__":
    # IMPORTANT NOTE: If AND and NOT fails randomly, it is likely due to contamination issues, which is expected behavior, this is checked later in the integration tests
    test_NOT()
    test_AND()
    test_contamination()
    print("Unit logic gates tests passed")