__author__ = 'Harold'
# ---------------- Begin Raspberry report IP address --------------------- #

import socket
import fcntl
import struct
from instapush import Instapush, App
import urllib2
import time
import re

# Initialization

Exist_wlan = 0
Exist_Eth = 0
string_internet = 'Internet address not exist, werid, check it'

#Test if the Raspberry can connect the internet

# def check_internet():

Url_instapush = 'https://instapush.im/'
while 1:
    try:
        response_test = urllib2.urlopen(Url_instapush)
        string_instapush = response_test.read()
        length = len(string_instapush)
        if length > 0:
            break
    except :
        time.sleep(5)

# Get IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    Ip_address_Eth0 = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', 'eth0'))[20:24])
    Exist_Eth = 1
except:
    Ip_address_Eth0 = 'Not exist'

try:
    Ip_address_wlan0 = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', 'wlan0'))[20:24])
    Exist_wlan = 1
except:
    Ip_address_wlan0 = 'Not exist'

# Get internet Ip address
try:
    pattern_for_ip = re.compile('(\d{1,3}\.){3}\d{1,3}')
    url_get_internet_address = "http://www.ip138.com/ip2city.asp"
    opener = urllib2.urlopen(url_get_internet_address)
    string_ip = opener.read()
    Ip_address_internet = re.search(pattern_for_ip,string_ip).group()
    string_internet = 'Internet Ip address : ' + Ip_address_internet
except:
    pass

string_Eth0 = 'Eth Ip address : ' + Ip_address_Eth0
string_wlan0 = 'Wlan Ip address : ' + Ip_address_wlan0

# Push information to Mobile phone via Instapush

app = App(appid = '561bac12a4c48a31793792b5', secret = '5b3446093d50511955f95b589988c541')

if Exist_wlan:
    app.notify(event_name = 'Report_IP_address_of_raspberry_pi', trackers ={'Message': string_wlan0})

if Exist_Eth:
    app.notify(event_name = 'Report_IP_address_of_raspberry_pi', trackers ={'Message': string_Eth0})

try:
    app.notify(event_name = 'Report_IP_address_of_raspberry_pi', trackers ={'Message': string_internet})
except :
    pass



# Application ID :
# 561bac12a4c48a31793792b5

# Application Secret :
# 5b3446093d50511955f95b589988c541