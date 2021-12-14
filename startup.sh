#!/bin/bash

screen -dm bash -c 'cd /home/pi/themes && git pull && pip install -r requirements.txt && python theme.py'