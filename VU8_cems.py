#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 詮能科技 中科院雷物組 VU8 <-> RPi <-> PC 專案
 RPi 作為Modbus RTU master 向 VU8要資料，send data to cems server
 
 (c) 2017 - Jason Wu - jason@mactronic.com.tw
 (c) 2017 - Mactronic Technology Ltd. - http://www.mactronic.com.tw
"""


"""
 Modbus TestKit: Implementation of Modbus protocol in python

 (C)2009 - Luc Jean - luc.jean@gmail.com
 (C)2009 - Apidev - http://www.apidev.fr

 This is distributed under GNU LGPL license, see license.txt
"""

import sys

#add logging capability
import serial
import requests
import logging
import threading
import time
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus as modbus
import modbus_tk.modbus_tcp as modbus_tcp
from modbus_tk import modbus_rtu
import random

# your API key here
API_KEY = "acd600359e6d1cc86b280480815670f1"
tim_API_KEY = "b66c94a03e6ab53d3f3ef4a09abee385"

PORT = '/dev/ttyS0'

logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")
    
if __name__ == "__main__":
        
    try:
        #Create the server
        server = modbus_tcp.TcpServer(port=1152)
        logger.info("running...VU8 Remote Server")


        server.start()
        #Connect to the Serial RTU slave
        rtumaster = modbus_rtu.RtuMaster(
            serial.Serial(port=PORT, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=0)
        )
        rtumaster.set_timeout(10.0)
        rtumaster.set_verbose(True)

        slave_1 = server.add_slave(1)
        slave_1.add_block('0', cst.READ_INPUT_REGISTERS, 0, 8)
        #range(100)为0-99的列表
        while True:
            while True:
                #logger.info(rtumaster.execute(1, cst.READ_INPUT_REGISTERS, 0, 36))
                distance= rtumaster.execute(1, cst.READ_INPUT_REGISTERS, 16, 8)

                API_ENDPOINT = "http://104.154.116.241/mactronic/input/post.json?node=LeddarVU8&json={"\
                +'Seg01: '+str(distance[0]) +','\
                +'Seg02: '+str(distance[1]) +','\
                +'Seg03: '+str(distance[2]) +','\
                +'Seg04: '+str(distance[3]) +','\
                +'Seg05: '+str(distance[4]) +','\
                +'Seg06: '+str(distance[5]) +','\
                +'Seg07: '+str(distance[6]) +','\
                +'Seg08: '+str(distance[7]) \
                 +"}&apikey="+tim_API_KEY 
                r = requests.post(url = API_ENDPOINT)
                time.sleep(1)

                slave_1.set_values('0', 0, distance)

                
    finally:
        server.stop()


