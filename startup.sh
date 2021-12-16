#!/bin/bash
echo "Starting Soundboard.."

echo "Turning on numlock"
# Turn numlock on for the TTYs:
for tty in /dev/tty[1-6]; do
    /usr/bin/setleds -D +num < "$tty";
done

echo "Checking for updates..."
git pull
echo "Updating dependings, sorry this is sloooooooooo"
python -m pip install -r requirements.txt
echo "Finally starting!  You should hear the startup sound."
python themes.py