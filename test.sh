#!/bin/bash

# Set the bash script to exit immediately if any command fails
set -e

# IMPORTANT NOTE: Not all the test_logic_gates are gauranteed to pass due to contamination issues (this is resolved in the integration tests)

python3 -m tst.test_rsa
python3 -m tst.test_encrypted_data
python3 -m tst.test_logic_gate
python3 -m tst.test_logic_gate_integration