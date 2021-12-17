#!/bin/bash
echo "Starting Entrance Theme Machine."

echo "Turning on numlock"
# Turn numlock on for the TTYs:
for tty in /dev/tty[1-6]; do
    /usr/bin/setleds -D +num < "$tty";
done

echo "Checking for updates..."
git pull

# only pip install if changes to requirements
# startup is too slow otherwise!
# https://stackoverflow.com/questions/17797740/check-if-specific-file-in-git-repository-has-changed
if ! git diff --exit-code --quiet requirements.txt; then
  echo "Updating dependings, sorry this is sloooooooooow....."
  python -m pip install -r requirements.txt
fi

echo "Finally starting!  You should hear the startup sound."
python themes.py