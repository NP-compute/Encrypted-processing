from src.logic_gate import data, pointer, AND, NOT

def combined_logic_gate_test():
    # Test NOT gate
    data_a = data()
    pointer_a = data_a.generate_pointer()
    pointer_a.set_value(1)
    output_pointer = NOT(pointer_a)
    assert output_pointer.get_value() == 0, f'Expected 0 but got {output_pointer.get_value()}'

    # Test AND gate
    data_b = data()
    pointer_b = data_b.generate_pointer()
    pointer_b.set_value(1)
    output_pointer = AND(output_pointer, pointer_b)
    assert output_pointer.get_value() == 0, f'Expected 0 but got {output_pointer.get_value()}'

    # Test NOT gate again
    output_pointer = NOT(output_pointer)
    assert output_pointer.get_value() == 1, f'Expected 1 but got {output_pointer.get_value()}'

    # Test AND gate again
    data_c = data()
    pointer_c = data_c.generate_pointer()
    pointer_c.set_value(1)
    output_pointer = AND(output_pointer, pointer_c)
    assert output_pointer.get_value() == 1, f'Expected 1 but got {output_pointer.get_value()}'

if __name__ == "__main__":
    combined_logic_gate_test()
    print("Integration logic gates tests passed")