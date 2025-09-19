from src.logic_gate import data, pointer, NAND, UNITARY

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

def test_NAND_into_NAND():
    data_a = data()
    data_b = data()
    output = data()

    # Make a pointer we can set
    pointer_b1 = data_b.generate_pointer()

    # Build the NAND gate
    pointer_a1, output_pointer1 = NAND(pointer_b1, data_a, output)

    # Set the values for the first NAND
    pointer_a1.set_value(1)
    pointer_b1.set_value(1)

    # Perform the multiplication process
    output.value = data_a.value * data_b.value

    assert output_pointer1.get_value() == 0, f'Expected 0 but got {output_pointer1.get_value()}'

    data_c = data()
    output2 = data()

    # Build a NAND gate with output of first NAND and data_c
    pointer_a2, output_pointer2 = NAND(output_pointer1, data_c, output2)

    # Make a pointer we can set for data_c
    pointer_c = data_c.generate_pointer()

    # Set the value for data_c
    pointer_c.set_value(1)

    # Perform the multiplication process
    output2.value = output.value * data_c.value

    assert output_pointer2.get_value() == 1, f'Expected 1 but got {output_pointer2.get_value()}'

def test_UNITARY():
    data_a = data()
    data_b = data()
    output = data()

    # Make a pointer we can set
    pointer_a = data_a.generate_pointer()

    # Set the values
    pointer_a.set_value(1)

    # Perform the UNITARY operation to copy data from data_a to data_b
    output_pointer = UNITARY(pointer_a, data_b, output)

    # Perform the multiplication process
    output.value = data_a.value * data_b.value

    assert output_pointer.get_value() == 1, f'1. Expected 1 but got {output_pointer.get_value()} with the data values {data_a.value=}, {data_b.value=} and {output.value=}'

    # NOTE: This is going through the process a few times to make sure the value is kept between clock cycles
    output2 = data()
    data_c = data()

    # Perform the UNITARY operation to copy data from output to data_c
    output_pointer2 = UNITARY(output_pointer, data_c, output2)

    # Perform the multiplication process
    output2.value = output.value * data_c.value

    assert output_pointer2.get_value() == 1, f'2. Expected 1 but got {output_pointer2.get_value()} with the data values {data_c.value=}, {output.value=}, and {output2.value=}'

    # NOTE: This is going through the process a few times to make sure the value is kept between clock cycles
    output3 = data()
    data_d = data()

    # Perform the UNITARY operation to copy data from output2 to data_d
    output_pointer3 = UNITARY(output_pointer2, data_d, output3)

    # Perform the multiplication process
    output3.value = output2.value * data_d.value

    assert output_pointer3.get_value() == 1, f'3. Expected 1 but got {output_pointer3.get_value()} with the data values {data_d.value=}, {output2.value=}, and {output3.value=}'

if __name__ == "__main__":
    test_NAND_all()
    test_two_NANDS()
    test_three_NANDS()
    test_NAND_into_NAND()
    test_UNITARY()
    print("All tests passed for logic_gate.py")