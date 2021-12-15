#!/bin/bash

export DISPLAY=:0

git pull
python -m pip install -r requirements.txt
python themes.py