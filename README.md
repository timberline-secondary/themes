
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