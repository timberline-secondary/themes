
# Entrance Theme Machine!
## Operating System and Dependancies

1. Raspberry Pi OS Lite (no desktop)
1. Config the pi: `sudo raspi-config`:
   - set hostname to `pi-themes`, 
   - turn on ssh server, 
   - etc.
1. Dependancies: `sudo apt install ntp git espeak python3-pip neofetch`
1. Ensure that the pi is running at least v3.9 Python: `python -V`

## Installing the Entrance Theme Player:

1. Clone the repo:  
`git clone https://github.com/timberline-secondary/themes.git`
2. `cd themes && pip install -r requirements.txt`
3. Setup environment variables:  
   `cp .env.example .env`
4. Edit the `.env` file with desired values
5. Create a systemd service @ `/lib/systemd/system/themes.service` with the contents of:
   ```bash
   [Unit]
   Description=Theme Player
   After=multi-user.target
   Conflicts=getty@tty1.service
   
   [Service]
   Type=simple
   # Restart=on-failure
   # RestartSec=30
   WorkingDirectory=/home/pi/themes
   User=pi
   ExecStart=/usr/bin/python themes.py
   StandardInput=tty-force
   
   [Install]
   WantedBy=multi-user.target
   ```
6. Update the permissions for the file with `sudo chmod 644 /lib/systemd/system/themes.service`
7. Create the updater service @ `/lib/systemd/system/themes-updater.service` with the contents of:
    ```bash
    [Unit]
   Description=Updater for Theme Player
   Wants=network-online.target
   After=network-online.target
   
   [Service]
   Type=simple
   ExecStart=/usr/bin/bash -c "cd /home/pi/themes && sh startup.sh"
   
   [Install]
   WantedBy=multi-user.target
    ```
8. Update the permissions for the file with `sudo chmod 644 /lib/systemd/system/themes-updater.service`
9. Enable both service with the following commands: `systemctl enable themes` and `systemctl enable themes-updater`
10. Reboot the pi and listen for the startup sound!

## Updates

Each time the Pi starts, `themes-updater` runs `startup.sh`, which gets the latest version from
GitHub (`git pull`). The player (`themes`) starts at the same time and is usually already
running by then, so if anything was updated, `startup.sh` restarts it to run the new version
(you'll hear the startup sound twice). If `requirements.txt` changed, it also reinstalls the
Python packages first. So after merging a change here, rebooting pi-themes is enough.

To restart just the player by hand: `sudo systemctl restart themes`.

## Keypad log

Every code typed is added to `keypad.log` next to `themes.py`, with the time and what happened:

```
2026-11-27 10:31:02  keypad  2*2           played 2x2.mp3
2026-11-27 10:31:40  keypad  2*2           spam-blocked (5 more minutes)
2026-11-27 10:32:15  keypad  9/9           not found (there's no 9d9.mp3)
2026-11-27 10:35:00  keypad  (admin)       spam block set to 7 minutes
```

`keypad` is the entrance keypad; `ssh` is a copy of the player started over ssh (e.g. the
control panel's *Play a theme*). Admin codes are never written down (they're the passwords in
`.env`), only what they did. When it reaches 1 MB it's moved to `keypad.log.1`. Watch it live
with `tail -f keypad.log`, or the control panel's *Watch the keypad*.

## Codes and file names

A code plays the file with that name in `THEME_PATH`: typing `0027` plays `0027.mp3`, and
`2+2` plays `2+2.mp3`. Codes can use every key on the number pad (`0-9 . + - * /`), but `*`
and `/` can't be in a file name (`/` is a folder, and USB sticks formatted for Windows don't
allow `*`), so those are letters in the file name instead:

| Key | In the file name | Example |
| --- | --- | --- |
| `*` | `x` | typing `2*2` plays `2x2.mp3` |
| `/` | `d` | typing `3/4` plays `3d4.mp3` |

Codes starting with `*` are admin codes, so they never play a theme. The Hackerspace control
panel names new themes this way, and explains it when a code has `*` or `/` in it.

## Disabling the NumLock Key:

1. SSH into the Raspberry Pi
2. Make sure console-setup is installed:
   ```
   sudo apt update
   sudo apt install console-setup
   ```
3. Create a systemd service @ `/etc/systemd/system/disable-numlock.service` with the contents of:
   ```bash
   [Unit]
   Description=Disable Num Lock key
   After=local-fs.target

   [Service]
   Type=oneshot
   ExecStart=/bin/sh -c 'echo "keycode 69 = VoidSymbol" | /usr/bin/loadkeys -'
   RemainAfterExit=yes

   [Install]
   WantedBy = multi-user.target
   ```
4. Restart and confirm with:
   ```
   sudo systemctl daemon-reload
   sudo systemctl restart disable-numlock.service
   sudo systemctl status disable-numlock.service --no-pager
   ```
5. Feel free to reboot the pi and test but if `sudo systemctl status disable-numlock.service --no-pager` returns `active (exited)` it works.
