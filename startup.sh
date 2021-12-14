#!/bin/bash

screen -dm bash -c 'git pull && pip install -r requirements.txt && python3 themes.py'