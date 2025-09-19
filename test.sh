#!/bin/bash

# Set the bash script to exit immediately if any command fails
set -e

python3 -m tst.test_rsa
python3 -m tst.test_generate_data