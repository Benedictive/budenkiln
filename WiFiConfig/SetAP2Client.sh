#!/bin/bash
# This script will stop Hotspot (AP+DHCP) and will Switch your Raspberry to a WIFI Client 
# Run : bash SetAP2Client.sh
# Source: RPi-Forums: https://forums.raspberrypi.com/viewtopic.php?t=307221
# Required setup:
# Have client-configs for dnsmasq and dhcpcd saved as *.conf.orig
# Have AP-Configs for dnsmasq and dhcpcd saved as *.conf.ap
# The latter is not required for deactivating, but would disable revertability
# Maybe rework for use of properly named temp files ?
# Result: Worked manually so far

echo "========================================"
echo " Switch from Hotspot (AP+DHP) to Client "
echo "========================================"
echo " "
echo "Reconfiguring dnsmasq"
sudo cp /etc/dnsmasq.conf.orig /etc/dnsmasq.conf

echo "Reconfiguring dhcpcd"
sudo cp /etc/dhcpcd.conf.orig /etc/dhcpcd.conf

echo "Stopping hostapd, dnsmasq "
sudo service dnsmasq stop
sudo service hostapd stop

echo "Reloading Daemon"
sudo systemctl daemon-reload

echo "Restaring dhcpcd"
sudo systemctl restart dhcpcd

echo "Done. System should connect to known WiFi in range."
exit