#!/bin/bash

cd ~/spotmicroai
export PYTHONPATH=.

python3 integration_tests/test_motion/test_motion.py
