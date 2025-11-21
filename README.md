# Budenkiln

Web-enabled hardening and tempering kiln for the forge.

## Requirements
SPI:  
On RasPi:  
`sudo raspi-config`  
select: interfacing options > SPI > enable  
Python dependencies:  
See requirements.txt, or:  
`pip install -r requirements.txt`
The core dependencies are:
- django - Hosting the web-interface
- djangorestframework - Providing web-interface API
- pyzmq - IPC between server and controller
- Adafruit-Blinka - Provides circuitpython environment for embedded capability
- adafruit-circuitpython-max31855 - Lib for talking to the max31855 chip

## WiFi Hotspot
Useful for usage of Kiln without connection to existing Network:  
Follow official RaspberryPi documentation on hosting an AP, except simply use the provided config files:  
Move files from WiFiConfig-folder as required:  
- `dnsmasq.conf.*` and `dhcpcd.conf.*` into `/etc/`
- `hostapd.conf` into `/etc/hostapd/`

DHCPCD - Ignore if using the provided files:  
Add `noarp` to `/etc/dhcpcd.conf` (optional, only required if WiFi dies when specific devices - like OnePlus Phones - connect)  
### AP Switching
See Scripts in WiFiConfig-Folder

## Using python venv
Create the virtual environment:  
`python3 -m venv .pyvenv`  
Environment names other than `.pyvenv` are possible, but are not yet covered by `.gitignore`.  
Activate the venv (linux - command will vary based on OS):  
`source .pyvenv/bin/activate`  
Then work like normal (i.e. pip install)  
Deactivate the venv:  
`deactivate`

## Django
Start server:  
`python3 manage.py runserver`

Setup Database:  
`python3 .\manage.py makemigrations budenkiln` (if required)  
`python3 .\manage.py migrate`

## Remote RasPi Development (VS Code)
1. Install `Remote - SSH` extension
2. Install `Python/Pylance` extension on remote host  
(open extension explorer, should show "Install in SSH: \<Host IP>")  

## Local Development without RasPi
Hardware IO for the RasPi has been abstracted to allow for development on regular desktops.  
To do so, just set `_developmentMode = True` in `hardware_controller.py`, otherwise `False`.  
This will generate fake sensor input and void GPIO output.  
Otherwise works as usual, though the start script `start.sh` only works in the appropriate shell as expected.  

## Systemd for Autostart
Add the `budenkiln.service` file from the ServiceSetup directory into `/etc/systemd/system`.  
See `ServiceSetup/setup.txt` for additional info on systemd setup and commands.  

## TODO
- watchdog ?
