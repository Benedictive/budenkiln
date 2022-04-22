#!/bin/bash
# This script will stop Hotspot (AP+DHCP) and will Switch your Raspberry to a WIFI Client (Temporarily) 
# Effect is dynamic --> Next start will be as AP
# Run : bash sap2cl.sh
# Source: Stackoverflow
# Result: Doesn't work

echo "========================================"
echo " Switch from Hotspot (AP+DHP) to Client "
echo "  Next start will be : AP mode "
echo "========================================"
echo " "
echo "Stopping hostapd, dnsmasq "
sudo systemctl stop hostapd.service
sudo systemctl stop dnsmasq.service

echo "Configure Client to recover dhcp"
sudo cp  /etc/dhcpcd-dynamic.conf /etc/dhcpcd.conf
sudo systemctl daemon-reload

echo "Restart wpa_supplicant"
sudo pkill wpa_supplicant
sleep 2
sudo wpa_supplicant -c/etc/wpa_supplicant/wpa_supplicant.conf -iwlan0 -B -Dnl80211,wext

echo "Prepare for next start as AP"
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq.service
sudo cp  /etc/dhcpcd-static.conf /etc/dhcpcd.conf

echo "Done."
exit