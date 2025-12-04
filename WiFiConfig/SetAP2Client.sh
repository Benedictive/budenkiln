#!/bin/bash
# This script will stop Hotspot (AP+DHCP) and will Switch your Raspberry to a WIFI Client 
# Run : bash SetAP2Client.sh
# Required setup:
# Replace 'ConnectionName' with the actual name of your WiFi connection profile and ifname as desired.

echo "========================================"
echo " Switch from Hotspot to Client "
echo "========================================"
echo " "
echo "Shutting down wifi"
sudo nmcli device disconnect wlan0
sudo nmcli radio wifi off

echo "Starting wifi in client mode"
sudo nmcli radio wifi on
sudo nmcli connection up id ConnectionName ifname wlan0

echo "Done. System should connect to Wifi."
exit