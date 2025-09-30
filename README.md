# Encrypted Processing

A cryptographic computation system that enables processing on encrypted data using RSA homomorphic properties and logic gate operations.

## Overview

This project demonstrates secure computation by performing operations on encrypted data without decryption. It leverages RSA's multiplicative homomorphic property: `E(m₁) × E(m₂) = E(m₁ × m₂)`, enabling multiplication on encrypted values in untrusted environments.

## Key Features

- **Homomorphic Addition**: Add encrypted numbers using RSA multiplication
- **Logic Gates**: Implement AND and NOT gates on encrypted data
- **Contamination Tracking**: Prevent bit collisions during operations
- **Universal Computation**: NAND-complete gate system for arbitrary logic

## Core Components

### 1. Encrypted Data (`src/encrypted_data.py`)

Provides encrypted number operations with automatic key management.

#### Example: Encrypted Addition

```python
from src.encrypted_data import EncryptedNumber

# Initialize with variables
enc = EncryptedNumber({'x': 10, 'y': 3})

# Perform encrypted addition: result = x + y
enc.add('result', 'x', 'y')

# Decrypt to verify
decrypted = enc.decrypt_all()
print(decrypted['result'])  # Output: 13
```

#### How It Works: Binary Addition

For 4-bit numbers, the encoding uses the format `a0001`:
- 'a' occupies 4 bits (data)
- '0001' acts as a separator/marker

Example: `1010_0001 × 0011_0001 = 00011110_11010001`

Extracting the lower bits: `1101_0001` → data = `1101` (13 in decimal)

### 2. Logic Gates (`src/logic_gate.py`)

Implements fundamental logic operations with contamination tracking to prevent bit conflicts.

#### Data and Pointer System

```python
from src.logic_gate import data, pointer, AND, NOT

# Create data with initial value
d1 = data(value=5)  # Binary: 101
d2 = data(value=3)  # Binary: 011

# Generate pointers to specific bit positions
p1 = d1.generate_pointer(1)  # Points to bit 1
p2 = d2.generate_pointer(2)  # Points to bit 2

# Get values at pointer positions
print(p1.get_value())  # Output: 0 (bit 1 of 101)
print(p2.get_value())  # Output: 0 (bit 2 of 011)
```

#### AND Gate

```python
from src.logic_gate import data, AND

# Create data objects
d1 = data(1)  # Initialize with value 1
d2 = data(1)

# Create pointers
p1 = d1.generate_pointer(2)  # Bit position 2
p2 = d2.generate_pointer(3)  # Bit position 3

# Set bit values
p1.set_value(1)  # Set bit 2 to 1
p2.set_value(1)  # Set bit 3 to 1

# Perform AND operation
result = AND(p1, p2)

if result:
    print(f"AND result: {result.get_value()}")  # Output: 1
    print(f"Result address: {result.get_address()}")  # Output: 5 (2+3)
```

#### NOT Gate

```python
from src.logic_gate import data, NOT

# Create data
d = data(1)
p = d.generate_pointer(4)
p.set_value(0)  # Set bit to 0

# Apply NOT operation
result = NOT(p)

if result:
    print(f"NOT result: {result.get_value()}")  # Output: 1
    print(f"Result address: {result.get_address()}")  # Output: 4 (same position)
```

## NAND Gate Construction

Since NAND is a universal gate, any logic circuit can be built. For 2-bit multiplication (a₁a₀ × b₁b₀):

- **Bit 0**: `out₀ = a₀ AND b₀`
- **Bit 1**: `out₁ = (a₀ AND b₁) XOR (a₁ AND b₀)`
- **Bit 2**: `out₂ = (a₁ AND b₁) XOR ((a₀ AND b₁) AND (a₁ AND b₀))`
- **Bit 3**: `out₃ = (a₁ AND b₁) AND ((a₀ AND b₁) OR (a₁ AND b₀))`

Example: 3 × 2 = 6
- Input: `a₁=11` (3), `b₁=10` (2)
- Output: `0110` (6) ✓

## Contamination Tracking

The system tracks which bits have been used to prevent collisions:

```python
from src.logic_gate import data, AND

data_a = data(number_initial_bits=2)
data_b = data(number_initial_bits=2)

# Make pointers, set the pointer values to the start_bit_values
pointer_a = data_a.generate_pointer()
pointer_a.set_value(1)
pointer_b = data_b.generate_pointer()
pointer_b.set_value(1)

# Perform the AND operation
# NOTE: this should return None due to contamination overlap with undesired bits
output_pointer = AND(pointer_a, pointer_b)

print(output_pointer)
```

## Installation

```bash
pip install portion
pip install cryptography
```

## Running Tests

```bash
./test.sh
```

## Limitations

- **Exponential Cost**: Each gate operation generates extra bits (3 unwanted bits per desired bit)
- **Contamination**: Strict bit usage tracking limits certain operations
- **Performance**: Encryption overhead for each operation

## Project Structure

```
encrypted_processing/
├── src/
│   ├── logic_gate.py       # AND/NOT gate implementations
│   ├── encrypted_data.py   # Homomorphic addition
│   ├── generate_data.py    # Data encoding utilities
│   └── rsa.py              # RSA encryption primitives
├── tst/
│   ├── test_logic_gate.py
│   └── test_encrypted_data.py
└── README.md
```

## License

Free to use.

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
