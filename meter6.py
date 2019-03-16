#!/usr/bin/env python
# -*- coding: utf_8 -*-
# 詮能科技 TCM3001電能管理系統讀表

"""
 Implementation of UDP protocol in python

"""
import requests
import logging
import time
import ConfigParser
import netifaces as ni
import socket
import ast
import json
import time
#import ijson
#from itertools import islice

# Read Configeration setting
config = ConfigParser.ConfigParser()
config.read('/boot/CDC_Config.ini')
Gateway_Port = config.get ('Gateway','Gateway_Port')
CEMS_URL = config.get('CEMS', 'CEMS_URL')
API_KEY = config.get('CEMS', 'API_KEY')
API_KEY2 = config.get('CEMS', 'API_KEY2')
API_KEY_EmonPi = config.get('CEMS', 'API_KEY_EmonPi')
NODE_NAME = config.get('CEMS', 'NODE_NAME')
Meter_IP = config.get('CEMS', 'Meter_IP')
Port = config.get('CEMS', 'Port')
TCM3001_ID = config.get('CEMS', 'TCM3001_ID')

# Get its IP address
ni.ifaddresses('enxb827eb64c50d')
Gateway_IP = ni.ifaddresses('enxb827eb64c50d')[ni.AF_INET][0]['addr']

# Act as UDP Server to receive data
address = ('192.168.20.152', 56841)
#address = (Gateway_IP, int(Gateway_Port))
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)

def main():

    try:
        while 1:

            #receive TCM3001 Periodical UDP Report
            json_string, addr = s.recvfrom(2048)

            #Method 1: PYTHON中将STRING转化为DICT的方法
#            d = ast.literal_eval(json_string)
#            print type(d)
#            print d

            #Method 2: PYTHON中将STRING转化为DICT的方法
            UDP_Report = json.loads(json_string)
#            print (type(UDP_Report))
#            print UDP_Report
#            print json_string
#            print (UDP_Report.get("sub"))


            if UDP_Report.get("cmd") == "NotifyEnergy" :
                """
                print "TCM3001"
                print("id : " + str(UDP_Report.get("id")) + " tm : " + str(UDP_Report.get("tm")))
                print("f0 : " + str(UDP_Report.get("f0")) + " ii0 : " + str(UDP_Report.get("ii0")) + " h0 : " + str(UDP_Report.get("h0")) + " vv0 : " + str(UDP_Report.get("vv0"))) 
                print("f1 : " + str(UDP_Report.get("f1")) + " ii1 : " + str(UDP_Report.get("ii1")) + " h1 : " + str(UDP_Report.get("h1")) + " vv1 : " + str(UDP_Report.get("vv1")))
                print("f2 : " + str(UDP_Report.get("f2")) + " ii2 : " + str(UDP_Report.get("ii2")) + " h2 : " + str(UDP_Report.get("h2")) + " vv2 : " + str(UDP_Report.get("vv2")))
                print("b0 : " + str(UDP_Report.get("b0")) + " r0 : " + str(UDP_Report.get("r0")) + " q0 : " + str(UDP_Report.get("q0")) + " s0 : " + str(UDP_Report.get("s0")))
                print("b1 : " + str(UDP_Report.get("b1")) + " r1 : " + str(UDP_Report.get("r1")) + " q1 : " + str(UDP_Report.get("q1")) + " s1 : " + str(UDP_Report.get("s1")))
                print("b2 : " + str(UDP_Report.get("b2")) + " r2 : " + str(UDP_Report.get("r2")) + " q2 : " + str(UDP_Report.get("q2")) + " s2 : " + str(UDP_Report.get("s2")))
                print("vq0 : " + str(UDP_Report.get("vq0")))
                print("vq1 : " + str(UDP_Report.get("vq1")))
                print("vq2 : " + str(UDP_Report.get("vq2")))
                print("v0 : " + str(UDP_Report.get("v0")) + " a0 : " + str(UDP_Report.get("a0")) + " i0 : " + str(UDP_Report.get("i0")))
                print("v1 : " + str(UDP_Report.get("v1")) + " a0 : " + str(UDP_Report.get("a1")) + " i1 : " + str(UDP_Report.get("i1")))
                print("v2 : " + str(UDP_Report.get("v2")) + " a0 : " + str(UDP_Report.get("a2")) + " i2 : " + str(UDP_Report.get("i2")))
                print("e0 : " + str(UDP_Report.get("e0")) + " p0 : " + str(UDP_Report.get("p0")) + " r0 : " + str(UDP_Report.get("r0")))
                print("e1 : " + str(UDP_Report.get("e1")) + " p1 : " + str(UDP_Report.get("p1")) + " r1 : " + str(UDP_Report.get("r1")))
                print("e2 : " + str(UDP_Report.get("e2")) + " p2 : " + str(UDP_Report.get("p2")) + " r2 : " + str(UDP_Report.get("r2")))
                """

                #Send Data to CEMS Servr (Admin account)
                API_ENDPOINT = CEMS_URL + "input/post.json?node=" + NODE_NAME + "_TCM3001_ID_"+str(UDP_Report.get("id")) + "&json={"\
                +'PhA_Irms :'+str(UDP_Report.get("i0"))+','+'PhB_Irms: '+str(UDP_Report.get("i1"))+','+'PhC_Irms: '+str(UDP_Report.get("i2"))\
                +"}&apikey="+API_KEY
                r = requests.post(url = API_ENDPOINT)

                #Send Data to CEMS Servr (ShangLuh account)
                API_ENDPOINT = CEMS_URL + "input/post.json?node=" + NODE_NAME + "_TCM3001_ID_"+str(UDP_Report.get("id")) + "&json={"\
                +'PhA_Irms :'+str(UDP_Report.get("i0"))+','+'PhB_Irms: '+str(UDP_Report.get("i1"))+','+'PhC_Irms: '+str(UDP_Report.get("i2"))\
                +"}&apikey="+API_KEY2
                r = requests.post(url = API_ENDPOINT)

                #Send Data to CEMS Servr ( EmonPi)
                API_ENDPOINT = CEMS_URL + "input/post.json?node=" + NODE_NAME + "_TCM3001_ID_"+str(UDP_Report.get("id")) + "&json={"\
                +'PhA_Irms :'+str(UDP_Report.get("i0"))+','+'PhB_Irms: '+str(UDP_Report.get("i1"))+','+'PhC_Irms: '+str(UDP_Report.get("i2"))\
                +"}&apikey="+API_KEY_EmonPi
                r = requests.post(url = API_ENDPOINT)

            elif UDP_Report.get("cmd") == "NotifySubEnergy":
                """
                print "TCM3003" + ", ID= " + str(UDP_Report.get("sub"))
                print("id : " + str(UDP_Report.get("id")) + " tm : " + str(UDP_Report.get("tm")))
                print("f0 : " + str(UDP_Report.get("f0")) + " ii0 : " + str(UDP_Report.get("ii0")) + " h0 : " + str(UDP_Report.get("h0")) + " vv0 : " + str(UDP_Report.get("vv0")))
                print("f1 : " + str(UDP_Report.get("f1")) + " ii1 : " + str(UDP_Report.get("ii1")) + " h1 : " + str(UDP_Report.get("h1")) + " vv1 : " + str(UDP_Report.get("vv1")))
                print("f2 : " + str(UDP_Report.get("f2")) + " ii2 : " + str(UDP_Report.get("ii2")) + " h2 : " + str(UDP_Report.get("h2")) + " vv2 : " + str(UDP_Report.get("vv2")))
                print("q0 : " + str(UDP_Report.get("q0")) + " s0 : " + str(UDP_Report.get("s0")) + " b0 : " + str(UDP_Report.get("b0")))
                print("q1 : " + str(UDP_Report.get("q1")) + " s1 : " + str(UDP_Report.get("s1")) + " b1 : " + str(UDP_Report.get("b1")))
                print("q2 : " + str(UDP_Report.get("q2")) + " s2 : " + str(UDP_Report.get("s2")) + " b2 : " + str(UDP_Report.get("b2")))
                print("v0 : " + str(UDP_Report.get("v0")) + " a0 : " + str(UDP_Report.get("a0")) + " i0 : " + str(UDP_Report.get("i0")))
                print("v1 : " + str(UDP_Report.get("v1")) + " a0 : " + str(UDP_Report.get("a1")) + " i1 : " + str(UDP_Report.get("i1")))
                print("v2 : " + str(UDP_Report.get("v2")) + " a0 : " + str(UDP_Report.get("a2")) + " i2 : " + str(UDP_Report.get("i2")))
                print("e0 : " + str(UDP_Report.get("e0")) + " p0 : " + str(UDP_Report.get("p0")) + " r0 : " + str(UDP_Report.get("r0")))
                print("e1 : " + str(UDP_Report.get("e1")) + " p1 : " + str(UDP_Report.get("p1")) + " r1 : " + str(UDP_Report.get("r1")))
                print("e2 : " + str(UDP_Report.get("e2")) + " p2 : " + str(UDP_Report.get("p2")) + " r2 : " + str(UDP_Report.get("r2")))
                """
               #Send Data to CEMS Servr
                API_ENDPOINT = CEMS_URL+"input/post.json?node="+ NODE_NAME + "_TCM3003_ID_"+str(UDP_Report.get("id")) + "_SubID_"+str(UDP_Report.get("sub")+172)+"&json={"\
                +'PhA_Irms :'+str(UDP_Report.get("i0"))+','+'PhB_Irms: '+str(UDP_Report.get("i1"))+','+'PhC_Irms: '+str(UDP_Report.get("i2"))\
                +"}&apikey="+API_KEY
                r = requests.post(url = API_ENDPOINT)

                #Send Data to CEMS Servr (Admin account)
                API_ENDPOINT = CEMS_URL+"input/post.json?node="+ NODE_NAME + "_TCM3003_ID_"+str(UDP_Report.get("id")) + "_SubID_"+str(UDP_Report.get("sub")+172)+"&json={"\
                +'PhA_Irms :'+str(UDP_Report.get("i0"))+','+'PhB_Irms: '+str(UDP_Report.get("i1"))+','+'PhC_Irms: '+str(UDP_Report.get("i2"))\
                +"}&apikey="+API_KEY_2
                r = requests.post(url = API_ENDPOINT)

                #Send Data to CEMS Servr (Admin account)
                API_ENDPOINT = CEMS_URL+"input/post.json?node="+ NODE_NAME + "_TCM3003_ID_"+str(UDP_Report.get("id")) + "_SubID_"+str(UDP_Report.get("sub")+172)+"&json={"\
                +'PhA_Irms :'+str(UDP_Report.get("i0"))+','+'PhB_Irms: '+str(UDP_Report.get("i1"))+','+'PhC_Irms: '+str(UDP_Report.get("i2"))\
                +"}&apikey="+API_KEY_EmonPi
                r = requests.post(url = API_ENDPOINT)


    ##except modbus_tk.modbus.ModbusError, e:
    ##    print "Modbus error", e.get_exception_code()
    ##    pass
    except Exception, e2:
        print "Error", str(e2)
        s.shutdown(socket.SHUT_RDWR)
        s.close()
    ##    pass
    finally:
        main()

def getMAC(interface='wlan0'):
  # Return the MAC address of the specified interface
    try:
        str = open('/sys/class/net/%s/address' %interface).read()
    except:
        str = "00:00:00:00:00:00"
    return str[0:17]
    MAC = str(getMAC('wlan0'))

if __name__ == "__main__":
    main()

