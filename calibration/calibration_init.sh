#!/bin/bash

cd ~/spotmicroai || exit
export PYTHONPATH=.

python3 calibration/calibration/calibration_init.py
