__author__ = 'Harold'
# ---------------- Begin Raspberry report IP address --------------------- #

import socket
import fcntl
import struct
from instapush import Instapush, App

# Get IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

Ip_address_Eth0 = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', 'eth0'))[20:24])

Ip_address_wlan0 = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', 'wlan0'))[20:24])

string_Eth0 = 'Eth Ip address : ' + Ip_address_Eth0
string_wlan0 = 'Wlan Ip address: ' + Ip_address_wlan0

# Push information to App

app = App(appid = '561bac12a4c48a31793792b5', secret = '5b3446093d50511955f95b589988c541')

app.notify(event_name = 'Report_IP_address_of_raspberry_pi', trackers ={'Message': string_Eth0})

app.notify(event_name = 'Report_IP_address_of_raspberry_pi', trackers ={'Message': string_wlan0})


# Application ID :
# 561bac12a4c48a31793792b5

# Application Secret :
# 5b3446093d50511955f95b589988c541