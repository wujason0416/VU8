#!/usr/bin/env python

import glob
import time
import ConfigParser
import requests

# DS18B20.py
# 2016-04-25
# Public Domain

# Typical reading
# 73 01 4b 46 7f ff 0d 10 41 : crc=41 YES
# 73 01 4b 46 7f ff 0d 10 41 t=23187

### your API key here
API_KEY = "c95cf268e66b36c78511a576f02ab7a2"
###remote url
CEMS_URL= "http://220.135.99.159/cems/input/post.json?node="
NODE_NAME = "DS18B20_"

while True:

#    try:
#        str = open('/sys/class/net/%s/address' %interface).read()
#    except:
#        str = "00:00:00:00:00:00"
    #return str[0:17]

    MAC_ADD = "20190226"


    print(str)
    #MAC_ADD = getMAC(interface='wlan0')

    for sensor in glob.glob("/sys/bus/w1/devices/28-00*/w1_slave"):
        id = sensor.split("/")[5]

        try:
            f = open(sensor, "r")
            data = f.read()
            f.close()
            if "YES" in data:
                (discard, sep, reading) = data.partition(' t=')
                t = float(reading) / 1000.0
                print("{} {:.1f}".format(id, t))

                API_ENDPOINT = CEMS_URL + NODE_NAME + MAC_ADD + "&json={"\
                + str("{}".format(id))+":"+str("{:.1f}".format(t))\
                +"}&apikey="+API_KEY

                r = requests.post(url = API_ENDPOINT)
            else:
                print("999.9")

        except:
            pass

    time.sleep(1.0)

