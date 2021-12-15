#!/bin/bash

export DISPLAY=:0

git pull
pip3 install -r requirements.txt
lxterminal -e "cd /home/pi/themes && python themes.py"