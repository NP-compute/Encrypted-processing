
# This is the core of the repo, this file converts data into ints that can be multiplied together for processing
# It also offers the ability to take an int and convert it back to the original data
# This allows two encrypted messages, one being data, one being operation, to be combined and processed together
# This allows encrypted processing

# Generate ints to allow adding by 1
def generate_adding_data(unencrypted_data: int, data_size: int) -> tuple[int, int, int]:
    """
    This function generates an UNENCRYPTED int for the data to exist in along with the necessary pointers and sizes.

    Args:
        unencrypted_data: The data to be wrapped
        data_size: The size of the data in bits

    Returns:
        A tuple of (wrapped_data, data_pointer, data_size)
    """

    assert unencrypted_data < (1 << data_size) - 1 , "Data too large for data size"
    
    # This is the UNENCRTPED data wrapper
    # It contains the data and allows the addition property
    wrapped_data: int = unencrypted_data
    wrapped_data = wrapped_data << data_size
    wrapped_data += 1

    # NOTE: If it returns 1 this will bug out the encryption and it wont actually be encrypted, this bit prevents one return
    wrapped_data += 1 << (data_size * 2)
    assert wrapped_data != 1, f'Wrapped data should not be 1, but is {wrapped_data}'

    # This is the pointer to the data
    # NOTE: This is zero indexed, I want to differentiate between size and pointer for later operations
    data_pointer: int = data_size

    return wrapped_data, data_pointer, data_size

# Decompose the UNENCRYPTED int back into the original data
def decompose_adding_data(wrapped_data: int, data_pointer: int, data_size: int) -> int:
    """
    This function extracts the original data from the wrapped data.

    Args:
        wrapped_data: The wrapped data
        data_pointer: The pointer to the data
        data_size: The size of the data in bits

    Returns:
        The original unencrypted data
    """
    return (wrapped_data >> data_pointer) & ((1 << data_size) - 1)