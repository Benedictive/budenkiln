#!/bin/bash
# This script will start Hotspot (AP+DHCP) and will Switch your Raspberry to a WIFI AP 
# Run : bash SetClient2AP.sh
# Required setup:
# Set ifname name, wifi ssid and password in line 17

echo "========================================"
echo " Switch from Client to Hotspot "
echo "========================================"
echo " "
echo "Shutting down wifi client"
sudo nmcli device disconnect wlan0
sudo nmcli radio wifi off

echo "Starting wifi in hotspot mode"
sudo nmcli radio wifi on
sudo nmcli device wifi hotspot ifname wlan0 ssid HotspotSSID password password

echo "Done. System should create WiFi AP."
exit