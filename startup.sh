#!/bin/bash

export DISPLAY=:0

git pull
pip install -r requirements.txt
lxterminal -e "cd /home/pi/themes && python3.9 themes.py"