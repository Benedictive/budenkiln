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
- RPi.GPIO
- Adafruit-Blinka - Provides circuitpython environment for embedded capability
- adafruit-circuitpython-max31855 - Lib for talking to the max31855 chip

## WiFi Hotspot
Useful for usage of Kiln without connection to existing Network:  
Follow [official RaspberryPi](https://www.raspberrypi.com/documentation/computers/configuration.html#host-a-wireless-network-from-your-raspberry-pi) documentation on hosting an AP.

### AP Switching
Before any switching can happen, find the desired wifi interface using `nmcli device`, typically it'll be wifi0.

To host a WiFi hotspot:
`sudo nmcli device wifi hotspot ssid <desired-ssid> password <desired-pw> ifname <wifi-interface>`
Or just start the hotspot if it has been defined already:
`sudo nmcli connection up Hotspot`

To switch away from hotspot (i.e. to any other connection):
`sudo nmcli connection down Hotspot`

To turn off hotspot/disconnect from WiFi:
`sudo nmcli device disconnect <wifi-interface>`

To go back to connecting to a wifi:
`nmcli device wifi connect "<wifi-ssid>" ifname <wifi-interface>`

Sometimes the WiFi will randomly be unfindable. Restarting wifi usually fixes it:
`nmcli radio wifi off`
`nmcli radio wifi on`

See [Jeff Geerlings post](https://www.jeffgeerling.com/blog/2023/nmcli-wifi-on-raspberry-pi-os-12-bookworm) for more.

### DNS setup

To setup a custom nameserver, first install dnsmasq.
Disable the dnsmasq service if using it together with NetworkManager, as NW starts its own instance.

Create `/etc/NetworkManager/dnsmasq.d/budenkiln.conf`
and add `address=/buden.kiln/<Device IP>`

For Network manager to use that config, create `/etc/NetWorkManager/conf.d/budenkiln.conf`
and add
`[main]`
`dns=dnsmasq`

Then just restart Network manager, maybe kill and start the Hotspot.

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
If the start script has been copied over from a windows system, it might not be runnable because of incorrect line
endings. In that case, convert to unix (i.e. using `dos2unix <file>`) beforehand.  
See `ServiceSetup/setup.txt` for additional info on systemd setup and commands.  

## TODO
- watchdog ?
