#!/bin/bash
# This script will start Hotspot (AP+DHCP) and will Switch your Raspberry to a WIFI AP 
# Run : bash SetClient2AP.sh
# Source: RPi-Forums: https://forums.raspberrypi.com/viewtopic.php?t=307221
# Required setup:
# Have client-configs for dnsmasq and dhcpcd saved as *.conf.orig
# Have AP-Configs for dnsmasq and dhcpcd saved as *.conf.ap
# The former is not required for activating, but would disable revertability
# Maybe rework for use of properly named temp files ?
# Result: Worked manually so far

echo "========================================"
echo " Switch from Client to Hotspot (AP+DHP) "
echo "========================================"
echo " "
echo "Reconfiguring dnsmasq"
sudo cp /etc/dnsmasq.conf.ap /etc/dnsmasq.conf

echo "Reconfiguring dhcpcd"
sudo cp /etc/dhcpcd.conf.ap /etc/dhcpcd.conf

echo "Reloading Daemon"
sudo systemctl daemon-reload

echo "Restaring dhcpcd"
sudo systemctl restart dhcpcd

echo "Starting hostapd, dnsmasq "
sudo service dnsmasq start
sudo service hostapd start

echo "Done. System should create WiFi AP."
exit