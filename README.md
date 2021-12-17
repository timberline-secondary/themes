
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
1. `cd themes && pip install -r requirements.txt`
1. Setup environment variables:  
   `cp .env.example .env`
1. Edit the `.env` file with desired values
1. Run the Entrance Theme Machine on startup by adding this code to the bottom of `/home/pi/.bashrc`:  
    ```
    # if not an ssh connection, then run the Entrance Theme Machine!
    if [ ! -n "$SSH_CLIENT" ] && [ ! -n "$SSH_TTY" ]; then
    cd /home/pi/themes && sh startup.sh
    fi
    ```
1. Reboot the pi and listen for the startup sound!