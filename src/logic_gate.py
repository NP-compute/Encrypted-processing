
def get_bit(value: int, bit_position: int) -> int:
    """Get the bit at the specified position."""
    return (value >> bit_position) & 1

def perform_not_example(value: int) -> int:
    # This is an example function to demonstrate a not operation

    # Make sure the value is 0 or 1
    assert value in (0, 1), "Value must be 0 or 1"

    # Get the first number we have to multiply to negate
    left = 3

    # Get the second number we have to multiply to negate
    right = (value << 1) + 1

    # Perform the operation
    answer = left * right

    # Extract the bit we want
    return get_bit(answer, 1)

def perform_nand_example(value1: int, value2: int) -> int:
    # This is an example function to demonstrate an and operation

    # Make sure the values are 0 or 1
    assert value1 in (0, 1), "Value1 must be 0 or 1"
    assert value2 in (0, 1), "Value2 must be 0 or 1"

    # Get the first number we have to multiply to negate
    left = (value1 << 1) + 1

    # Get the second number we have to multiply to negate
    right = (1 << 1) + value2

    # Perform the operation
    answer = left * right

    # Extract the bit we want
    return get_bit(answer, 1)