import random
import portion as I
from portion import Interval

NUMBER_INITIAL_BITS = 256

def get_bit(value: int, bit_position: int) -> int:
    """Get the bit at the specified position."""
    return (value >> bit_position) & 1

# NOTE: This is for compilation, figure out a better way to do this
class pointer:
    pass
class data:
    pass

class data:
    # records the data
    # IMPORTANT TODO: Add in a way to track which bits have been contaminated
    def __init__(self, value: int | None = None, number_initial_bits: int = NUMBER_INITIAL_BITS, contamination_track: Interval | None = None):
        #  Contamination index
        if contamination_track is not None:
            self.contamination_track = contamination_track
        else:
            self.contamination_track = I.empty()
        
        # This is the value stored in the data
        self.value: int = 1 if value is None else value
        self.add_value_into_contamination(0)

        # This is the range of bits that can be used for initial pointers
        self.allowed_initial_bits_start = 1
        self.allowed_initial_bits_end = number_initial_bits - 1

    def _set_bit(self, bit_position: int, bit_value: int):
        if bit_value not in (0, 1):
            raise ValueError("bit_value must be 0 or 1")
        if bit_value == 1:
            self.value |= (1 << bit_position)
        else:
            self.value &= ~(1 << bit_position)

        # Keep track of the contamination
        self.add_value_into_contamination(bit_position)

    def generate_pointer(self, pointer_address: int | None = None) -> pointer:

        # Set the pointer to a random value between allowed_initial_bits_start and allowed_initial_bits_end inclusive
        if pointer_address is None:
            pointer_address = random.randint(self.allowed_initial_bits_start, self.allowed_initial_bits_end)

        return pointer(pointer_address, self)
    
    def get_value(self):
        return self.value
    
    def add_value_into_contamination(self, index: int) -> None:
        # This function adds the index into the contamination checker recursively
        if index in self.contamination_track:
            self.add_value_into_contamination(index + 1)
        else:
            self.contamination_track = self.contamination_track | I.singleton(index)

    # This is a stupid way to iterate through intevals
    def stupid_interval_iterateor(self):
        for interval in self.contamination_track:
            for i in range(interval.lower, interval.upper + 1):  # +1 to include upper bound
                yield i

    def combine_contamination(self, other: data, is_and: bool = True) -> Interval | None:
        new_contamination = I.empty()

        temp_dict = {}
        # Special check for the NOT to make sure there is not more than 2 overlap
        for i in self.stupid_interval_iterateor():
            if i in temp_dict:
                temp_dict[i] += 1
            else:
                temp_dict[i] = 1
        for _, value in temp_dict.items():
            if value > 2:
                return None

        for i in self.stupid_interval_iterateor():
            for j in other.stupid_interval_iterateor():
                # Make sure there is no overlap
                if is_and and i + j in new_contamination:
                    return None

                new_contamination = new_contamination | I.singleton(i + j)

        return new_contamination

class pointer:
    # records the position of the pointer
    def __init__(self, position: int, data_pointer: data):
        self.position = position
        self.data_pointer = data_pointer

    def get_value(self) -> int:
        return get_bit(self.data_pointer.value, self.position)
    
    def set_value(self, bit_value: int):
        self.data_pointer._set_bit(self.position, bit_value)
    
    def get_address(self) -> int:
        return self.position

def AND(a: pointer, b: pointer) -> pointer | None:

    # Needs to add the pointer addresses to get the address of the new pointer
    new_address = a.get_address() + b.get_address()

    # Needs to multiply the values to get the value of the data
    new_value = a.data_pointer.get_value() * b.data_pointer.get_value()

    # Generate the new contamination
    new_contamination = a.data_pointer.combine_contamination(b.data_pointer)
    if new_contamination is None:
        # There was overlap
        return None

    # Make data and pointer then return the pointer
    new_data = data(new_value, contamination_track=new_contamination)
    return new_data.generate_pointer(new_address)

def NOT(a: pointer) -> pointer | None:
    
    # Needs to copy the pointer address to get the address of the new pointer
    new_address = a.get_address()

    # Needs to multiply the value by a data with bit value 1 at address 0 and bit value 1 at the pointer address
    temp_data: data = data(1)
    temp_data._set_bit(new_address, 1)
    new_value = a.data_pointer.get_value() * temp_data.get_value()

    # Generate the new contamination
    new_contamination = a.data_pointer.combine_contamination(temp_data, is_and=False)
    if new_contamination is None:
        # There was overlap too much overlap
        return None

    # Make data and pointer then return the pointer
    # new_data = data(new_value, contamination_track=new_contamination)
    new_data = data(new_value)
    return new_data.generate_pointer(new_address)