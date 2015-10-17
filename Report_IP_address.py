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

# Deifine these constant at the beginning of the program
IP_ADDRESS_ETH_TEMP = '0.0.0.0'
IP_ADDRESS_WLAN_TEMP = '0.0.0.0'
IP_ADDRESS_INTERNET_TEMP = '0.0.0.0'

EXIST_ETH = 0
EXIST_WLAN = 0
EXIST_INTERNET = 0
string_internet = 'Internet address not exist, werid, check it'

def Check_internet() :
# This function is to check if Raspbery pi can connect to Internet

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
def Get_Ip_address() :
    # This funciton can get IP address.
    global EXIST_ETH
    global EXIST_WLAN
    global EXIST_INTERNET

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        Ip_address_Eth0 = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', 'eth0'))[20:24])
        EXIST_ETH = 1
    except:
        EXIST_ETH = 0
        Ip_address_Eth0 = 'Not exist'

    try:
        Ip_address_wlan0 = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', 'wlan0'))[20:24])
        EXIST_WLAN = 1
    except:
        EXIST_WLAN = 0
        Ip_address_wlan0 = 'Not exist'

    # Get internet Ip address
    try:
        pattern_for_ip = re.compile('(\d{1,3}\.){3}\d{1,3}')
        url_get_internet_address = "http://www.ip138.com/ip2city.asp"
        opener = urllib2.urlopen(url_get_internet_address)
        string_ip = opener.read()
        Ip_address_internet = re.search(pattern_for_ip,string_ip).group()
        EXIST_INTERNET = 1;
    except:
        EXIST_INTERNET = 0
        Ip_address_internet = 'Not exist'

    return (Ip_address_Eth0,Ip_address_wlan0,Ip_address_internet,EXIST_ETH,EXIST_WLAN,EXIST_INTERNET)

# Push information to Mobile phone via Instapush

def Pushinformation(Ip_address_Eth0,Ip_address_wlan0,Ip_address_internet,Exist_Eth,Exist_wlan,Exist_Internet) :
    # This function can push information to mobile phone.
    # Note the app tag, It need to be changed to your own tag before you use it, or I will receive your Ip address...

    app = App(appid = '561bac12a4c48a31793792b5', secret = '5b3446093d50511955f95b589988c541')

    if Exist_Eth:
        string_Eth0 = 'Eth Ip address : ' + Ip_address_Eth0
        app.notify(event_name = 'Report_IP_address_of_raspberry_pi', trackers ={'Message': string_Eth0})

    if Exist_wlan:
        string_wlan0 = 'Wlan Ip address : ' + Ip_address_wlan0
        app.notify(event_name = 'Report_IP_address_of_raspberry_pi', trackers ={'Message': string_wlan0})

    if Exist_Internet:
        string_internet = 'Internet Ip address : ' + Ip_address_internet
        app.notify(event_name = 'Report_IP_address_of_raspberry_pi', trackers ={'Message': string_internet})

def Check_Ip_change() :
    # This function can detect if there is any changes in Ip address, if any, will send new Ip address to mobile phone.

    global IP_ADDRESS_ETH_TEMP
    global IP_ADDRESS_WLAN_TEMP
    global IP_ADDRESS_INTERNET_TEMP

    (Ip_address_Eth0,Ip_address_wlan0,Ip_address_internet,Exist_Eth,Exist_wlan,Exist_Internet) = Get_Ip_address()

    if (Ip_address_Eth0 <> IP_ADDRESS_ETH_TEMP) | (Ip_address_wlan0 <> IP_ADDRESS_WLAN_TEMP) | (Ip_address_internet <> IP_ADDRESS_INTERNET_TEMP):
        Pushinformation(Ip_address_Eth0,Ip_address_wlan0,Ip_address_internet,Exist_Eth,Exist_wlan,Exist_Internet)

    IP_ADDRESS_ETH_TEMP = Ip_address_Eth0
    IP_ADDRESS_WLAN_TEMP = Ip_address_wlan0
    IP_ADDRESS_INTERNET_TEMP = Ip_address_internet



if __name__ == '__main__':

    Check_internet()

    while 1 :
        Check_Ip_change()
        time.sleep(900)


# Application ID :
# 561bac12a4c48a31793792b5

# Application Secret :
# 5b3446093d50511955f95b589988c541