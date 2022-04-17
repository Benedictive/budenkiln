# Budenkiln

Web-enabled hardening and tempering kiln for the forge.

## Requirements
DBus:  
Gnome Desktop Environment  
Dbus-Python uses GLib for its main loop, so it will not work headless...  
Various packages to set up Dbus/Glib:  
APT: `sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0`  
SPI:  
On RasPi:  
`sudo raspi-config`  
select: interfacing options > SPI > enable  
Python dependencies:  
See requirements.txt, or:  
`pip install -r requirements.txt`
### WiFi Hotspot (using RaspAP)
Install RaspAP (quick setup)
DHCPCD:
After RaspAP install add `noarp` to `/etc/dhcpcd.conf` (optional, only required if WiFi dies when specific devices - like OnePlus Phones - connect)  

### Using python venv
Create the virtual environment:  
`python3 -m venv .pyvenv`  
Environment names other than `.pyvenv` are possible, are not yet covered by `.gitignore` though.     
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

## TODO
- maybe replace Dbus with something else
- handle curve submit with existing name
- watchdog ?
- switch relay based on actual temp vs target temp