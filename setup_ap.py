#!/usr/bin/env python

import subprocess
import time
import os

def start_access_point():
    # Stop network services
    stop_network_services()

    # Configure static IP for wlan0
    configure_static_ip()

    # Configure hostapd
    configure_hostapd()

    # Restart network services
    restart_network_services()

def stop_access_point():
    # Stop network services
    stop_network_services()

    # Restore original network configuration
    restore_original_config()

    # Restart network services
    restart_network_services()

def stop_network_services():
    # Stop existing network services
    subprocess.run(["sudo", "systemctl", "stop", "hostapd"])
    subprocess.run(["sudo", "systemctl", "stop", "dnsmasq"])
    subprocess.run(["sudo", "systemctl", "stop", "wpa_supplicant"])

def configure_static_ip():
    # Set static IP for wlan0
    subprocess.run(["sudo", "ifconfig", "wlan0", "192.168.4.1", "netmask", "255.255.255.0"])

def configure_hostapd():
    # Configure hostapd
    hostapd_conf = """
    interface=wlan0
    driver=nl80211
    ssid=RaspberryPi_AP
    hw_mode=g
    channel=7
    wmm_enabled=0
    macaddr_acl=0
    auth_algs=1
    ignore_broadcast_ssid=0
    wpa=2
    wpa_passphrase=password123
    wpa_key_mgmt=WPA-PSK
    wpa_pairwise=TKIP
    rsn_pairwise=CCMP
    """

    with open("/tmp/hostapd.conf", "w") as f:
        f.write(hostapd_conf)

    subprocess.run(["sudo", "mv", "/tmp/hostapd.conf", "/etc/hostapd/hostapd.conf"])
    subprocess.run(["sudo", "systemctl", "unmask", "hostapd"])
    subprocess.run(["sudo", "systemctl", "enable", "hostapd"])
    subprocess.run(["sudo", "systemctl", "start", "hostapd"])

    # Explicitly specify the dnsmasq configuration file and port
    subprocess.run(["sudo", "systemctl", "unmask", "dnsmasq"])
    subprocess.run(["sudo", "systemctl", "enable", "dnsmasq"])
    subprocess.run(["sudo", "systemctl", "start", "dnsmasq", "--conf-file=/etc/dnsmasq.conf"])

def restore_original_config():
    # Restore original configuration for wlan0
    subprocess.run(["sudo", "ifconfig", "wlan0", "0.0.0.0"])

def restart_network_services():
    # Restart network services
    subprocess.run(["sudo", "systemctl", "start", "dnsmasq"])
    subprocess.run(["sudo", "systemctl", "start", "wpa_supplicant"])

if __name__ == "__main__":
    try:
        print("Starting Access Point...")
        start_access_point()
        input("Access Point is running. Press Enter to stop.")
    except KeyboardInterrupt:
        print("\nStopping Access Point...")
        stop_access_point()
    except Exception as e:
        print(f"Error: {e}")