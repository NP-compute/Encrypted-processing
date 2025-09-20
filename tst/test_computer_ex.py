
from src.logic_gate import Data, Pointer
from src.logic_gate import NOT, AND, UNITARY

def computer_helper(a: int, b: int, c: int, d: int):
    data_wrapper = Data()
    operation_wrapper1 = Data()
    output_wrapper1 = Data()
    operation_wrapper2 = Data()
    output_wrapper2 = Data()
    operation_wrapper3 = Data()
    output_wrapper3 = Data()

    # Generate the constant for the data wrapper
    pointer_a: Pointer = data_wrapper.make_pointer(a, total_buffer=8)
    pointer_b: Pointer = data_wrapper.make_pointer(b, total_buffer=8)
    pointer_c: Pointer = data_wrapper.make_pointer(c, total_buffer=8)
    pointer_d: Pointer = data_wrapper.make_pointer(d, total_buffer=8)

    # Perform the first computation, a and b, not c, unitary d
    and_pointer1 = AND(pointer_a, pointer_b, operation_wrapper1, output_wrapper1, buffer=8)
    not_pointer1 = NOT(pointer_c, operation_wrapper1, output_wrapper1, buffer=8)
    unitary_pointer1 = UNITARY(pointer_d, operation_wrapper1, output_wrapper1, buffer=8)

    output_wrapper1.value = data_wrapper.value * operation_wrapper1.value

    assert and_pointer1.get_value() == (a and b), f'1. Expected {a and b} but got {and_pointer1.get_value()} at an address of {and_pointer1.address} with the data values {data_wrapper.value=}, {operation_wrapper1.value=} and {output_wrapper1.value=}'
    assert not_pointer1.get_value() == (1 - c), f'1. Expected {1 - c} but got {not_pointer1.get_value()} at an address of {not_pointer1.address} with the data values {data_wrapper.value=}, {operation_wrapper1.value=} and {output_wrapper1.value=}'
    assert unitary_pointer1.get_value() == d, f'1. Expected {d} but got {unitary_pointer1.get_value()} at an address of {unitary_pointer1.address} with the data values {data_wrapper.value=}, {operation_wrapper1.value=} and {output_wrapper1.value=}'

    # Perform the second computation, and_pointer1 and not_pointer1, not unitary_pointer1
    and_pointer2 = AND(and_pointer1, not_pointer1, operation_wrapper2, output_wrapper2, buffer=8)
    not_pointer2 = NOT(unitary_pointer1, operation_wrapper2, output_wrapper2, buffer=8)

    output_wrapper2.value = output_wrapper1.value * operation_wrapper2.value

    assert and_pointer2.get_value() == ((a and b) and (1 - c)), f'2. Expected {(a and b) and (1 - c)} but got {and_pointer2.get_value()} at an address of {and_pointer2.address} with the data values {data_wrapper.value=}, {operation_wrapper2.value=} and {output_wrapper2.value=}'
    assert not_pointer2.get_value() == (1 - d), f'2. Expected {1 - d} but got {not_pointer2.get_value()} at an address of {not_pointer2.address} with the data values {data_wrapper.value=}, {operation_wrapper2.value=} and {output_wrapper2.value=}'

    # IMPORTANT TODO: There is some contamination issue happening here!!!

    # Make sure the contamination lengths are correct
    assert operation_wrapper3.contamination_ok(), f'The contamination for operation_wrapper3 is not ok'
    assert output_wrapper3.contamination_ok(), f'The contamination for output_wrapper3 is not ok'

    # IMPORTANT TODO: There is some contamination issue happening here!!!

    final_pointer = AND(and_pointer2, not_pointer2, operation_wrapper3, output_wrapper3, buffer=8)

    output_wrapper3.value = output_wrapper2.value * operation_wrapper3.value

    assert final_pointer.get_value() == ((a and b) and (not c) and (not d)), f'3. Expected {(a and b) and (not c) and (not d)} but got {final_pointer.get_value()} at an address of {final_pointer.address} with the data inputs of {and_pointer2} with 1 value less than {Pointer(and_pointer2.address - 1, and_pointer2.data_pointer)} and {not_pointer2} with 1 value less than {Pointer(not_pointer2.address - 1, not_pointer2.data_pointer)}'

    return final_pointer.get_value()

def test_computer():
    for a in [0, 1]:
        for b in [0, 1]:
            for c in [0, 1]:
                for d in [0, 1]:
                    assert computer_helper(a, b, c, d) == ((a and b) and (not c) and not d), f'Failed for {a=}, {b=}, {c=}, {d=} with final value {computer_helper(a, b, c, d)}'

if __name__ == '__main__':
    test_computer()
    print("All computer tests passed.")