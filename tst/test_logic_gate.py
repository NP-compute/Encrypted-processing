from src.logic_gate import data, pointer, NAND

def test_NAND(x: int, y: int, expected: int):
    data_a = data()
    data_b = data()
    output = data()

    # Make a pointer we can set
    pointer_b = data_b.generate_pointer()

    # Build the NAND gate
    pointer_a, output_pointer = NAND(pointer_b, data_a, output)

    # Set the values
    pointer_a.set_value(x)
    pointer_b.set_value(y)

    # Perform the multiplication process
    output.value = data_a.value * data_b.value

    assert output_pointer.get_value() == expected, f'Expected {expected} but got {output_pointer.get_value()}\n for data values {data_a.value=}, {data_b.value=}'

def test_NAND_all():
    test_NAND(0, 0, 1)
    test_NAND(0, 1, 1)
    test_NAND(1, 0, 1)
    test_NAND(1, 1, 0)

def test_two_NANDS():
    data_a = data()
    data_b = data()
    output = data()

    # Make a pointer we can set
    pointer_b1 = data_b.generate_pointer()
    pointer_b2 = data_b.generate_pointer()

    # Build the NAND gate
    pointer_a1, output_pointer1 = NAND(pointer_b1, data_a, output)
    pointer_a2, output_pointer2 = NAND(pointer_b2, data_a, output)

    # Set the values for the first NAND
    pointer_a1.set_value(1)
    pointer_b1.set_value(1)

    # Set the values for the second NAND
    pointer_a2.set_value(0)
    pointer_b2.set_value(1)

    # Perform the multiplication process
    output.value = data_a.value * data_b.value

    assert output_pointer1.get_value() == 0, f'Expected 0 but got {output_pointer1.get_value()}'
    assert output_pointer2.get_value() == 1, f'Expected 1 but got {output_pointer2.get_value()}'

def test_three_NANDS():
    data_a = data()
    data_b = data()
    output = data()

    # Make a pointer we can set
    pointer_b1 = data_b.generate_pointer()
    pointer_b2 = data_b.generate_pointer()
    pointer_b3 = data_b.generate_pointer()

    # Build the NAND gate
    pointer_a1, output_pointer1 = NAND(pointer_b1, data_a, output)
    pointer_a2, output_pointer2 = NAND(pointer_b2, data_a, output)
    pointer_a3, output_pointer3 = NAND(pointer_b3, data_a, output)

    # Set the values for the first NAND
    pointer_a1.set_value(1)
    pointer_b1.set_value(1)

    # Set the values for the second NAND
    pointer_a2.set_value(0)
    pointer_b2.set_value(1)

    # Set the values for the third NAND
    pointer_a3.set_value(1)
    pointer_b3.set_value(0)

    # Perform the multiplication process
    output.value = data_a.value * data_b.value

    assert output_pointer1.get_value() == 0, f'Expected 0 but got {output_pointer1.get_value()}'
    assert output_pointer2.get_value() == 1, f'Expected 1 but got {output_pointer2.get_value()}'
    assert output_pointer3.get_value() == 1, f'Expected 1 but got {output_pointer3.get_value()}'

if __name__ == "__main__":
    test_NAND_all()
    test_two_NANDS()
    test_three_NANDS()
    print("All tests passed for logic_gate.py")