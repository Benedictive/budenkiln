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

## Systemd for Autostart
Add the `budenkiln.service` file from the ServiceSetup directory into `/etc/systemd/system`.  
See `ServiceSetup/setup.txt` for additional info on systemd setup and commands.  

## TODO
- watchdog ?
