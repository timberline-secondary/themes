#!/bin/bash

export DISPLAY=:0

git pull
pip install -r requirements.txt
bash cd /home/pi/themes && python themes.py