#!/bin/bash

# Turn numlock on for the TTYs:
for tty in /dev/tty[1-6]; do
    /usr/bin/setleds -D +num < "$tty";
done

git pull
python -m pip install -r requirements.txt
python themes.py