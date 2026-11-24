#!/bin/bash
# Run by themes-updater.service (as root) when the Pi starts, alongside themes.service (the
# player). The player usually starts before this has finished updating, so it would keep
# running the old version: if anything changed, the player is restarted at the end.
echo "Starting Entrance Theme Machine."

echo "Turning on numlock"
# Turn numlock on for the TTYs:
for tty in /dev/tty[1-6]; do
    /usr/bin/setleds -D +num < "$tty";
done

echo "Checking for updates..."
before=$(git rev-parse HEAD)
git pull
after=$(git rev-parse HEAD)

# only pip install if changes to requirements
# startup is too slow otherwise!
if [ "$before" != "$after" ] && ! git diff --quiet "$before" "$after" -- requirements.txt; then
  echo "Updating dependings, sorry this is sloooooooooow....."
  python -m pip install -r requirements.txt
fi

if [ "$before" != "$after" ]; then
  echo "The player was updated, so restarting it to run the new version."
  echo "(You'll hear the startup sound again.)"
  systemctl restart themes
fi

echo "Finally starting!  You should hear the startup sound."
