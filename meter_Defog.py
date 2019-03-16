#!/usr/bin/env python
# -*- coding: utf_8 -*-
# 詮能科技 TCM3001電能管理系統讀表

"""
 Modbus TestKit: Implementation of Modbus protocol in python

 (C)2009 - Luc Jean - luc.jean@gmail.com
 (C)2009 - Apidev - http://www.apidev.fr

 This is distributed under GNU LGPL license, see license.txt
"""
import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus as modbus
import modbus_tk.modbus_tcp as modbus_tcp
from modbus_tk import modbus_rtu
from modbus_tk import modbus_tcp, hooks
import time
import ConfigParser
import glob
import requests
import math

def main():
    try:
        while 1:
            config = ConfigParser.ConfigParser()
            config.read('/boot/CDC_Config.ini')
            CEMS_URL = config.get('CEMS', 'CEMS_URL')
            EmonPi_URL = config.get('CEMS', 'EmonPi_URL')
            API_KEY = config.get('CEMS', 'API_KEY')
            API_KEY2 = config.get('CEMS', 'API_KEY2')
            API_KEY_EmonPi = config.get('CEMS', 'API_KEY_EmonPi')
#            NODE_NAME = config.get('CEMS', 'NODE_NAME')
            Meter_IP = config.get('CEMS', 'Meter_IP_1')
            Port = config.get('CEMS', 'Port')
            UART_PORT = config.get('CEMS', 'UART_PORT')
            BAUD_RATE = config.get('CEMS', 'BAUD_RATE')

            time.sleep(1)

#            master = modbus_rtu.RtuMaster(
#            serial.Serial(port=UART_PORT, baudrate=BAUD_RATE, bytesize=8, parity='N', stopbits=1, xonxoff=0)
#            )
            master = modbus_tcp.TcpMaster(Meter_IP)

            master.set_timeout(5.0)
            master.set_verbose(True)

            print '[TCM3001, ID=1]'
            NODE_NAME = 'HiLife_BlueSea_TCM3001'
            Meter_Value =  master.execute(1, cst.READ_INPUT_REGISTERS, 61696, 64)
            print  Meter_Value
            CEMS_Input(CEMS_URL, API_KEY, API_KEY2, NODE_NAME, 'Defog', Meter_Value, EmonPi_URL, API_KEY_EmonPi)
            time.sleep(5)

    except modbus_tk.modbus.ModbusError, e:
        print "Modbus error", e.get_exception_code()
        pass
    except Exception, e2:
        print "Error", str(e2)
        s.shutdown(socket.SHUT_RDWR)
        s.close()
    ##    pass
#    finally:
#        main()

def CEMS_Input(CEMS_URL, API_KEY, API_KEY2, NODE_NAME, TCM3003_ID, Meter_Value, EmonPi_URL, API_KEY_EmonPi):

    # defining the api-endpoint
    API_ENDPOINT = "input/post.json?node=" + NODE_NAME + "_" + str(TCM3003_ID) + "&json={"\
    +'PhA_Irms: '+str(Meter_Value[0]*0.01) \
    +"}&apikey="
#    print "checked"

    r = requests.post(url = CEMS_URL + API_ENDPOINT + API_KEY)
    r = requests.post(url = CEMS_URL + API_ENDPOINT + API_KEY2)
    r = requests.post(url = EmonPi_URL + API_ENDPOINT + API_KEY_EmonPi)
#    print API_ENDPOINT



if __name__ == "__main__":
    main()
