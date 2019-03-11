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

SLAVE_IP = '192.168.1.173'
TCP_PORT = 1502
UART_PORT = 'COM7'
BAUD_RATE = 9600

def main():


        try:
            while 1:
##                config = ConfigParser.ConfigParser()
##                config.read('/boot/CDC_Config.ini')
##                CEMS_URL = config.get('CEMS', 'CEMS_URL')
##                API_KEY = config.get('CEMS', 'API_KEY')
##                NODE_NAME = config.get('CEMS', 'NODE_NAME')
##                Meter_IP = config.get('CEMS', 'Meter_IP')
##                Port = config.get('CEMS', 'Port')
##                TCM3001_ID = config.get('CEMS', 'TCM3001_ID')
###                print getMAC(interface='wlan0')
##                MAC_ADD = getMAC(interface='wlan0')
##
##                time.sleep(3)

                print "** TCM3003 Power Meter **"
                #Connect to the Serial RTU slave
                master = modbus_rtu.RtuMaster(
                    serial.Serial(port=UART_PORT, baudrate=BAUD_RATE, bytesize=8, parity='N', stopbits=1, xonxoff=0)
                )
                master.set_timeout(5.0)
                master.set_verbose(True)
##        
##                MAC_ADD = getMAC(interface='wlan0')
##
##                #BCM2835 core temperature
##                file = open("/sys/class/thermal/thermal_zone0/temp")
##                temp = float(file.read())/1000
##                file.close()
##                print "CPU temperatre: %0.1f" %temp
##                #API_ENDPOINT = CEMS_URL+MAC_ADD+"&json={"\
##                API_ENDPOINT = CEMS_URL + "input/post.json?node=" + NODE_NAME + "_" + MAC_ADD + "&json={"\
##                +'CPU_Temperature: '+str(temp)\
##                +"}&apikey="+API_KEY
###                r = requests.post(url = API_ENDPOINT)


                # 設定電表ID及封包起始位址與長度 (母表ID=1, 子表#1 ID=172, 子表#2 ID=172, ...)
                print '[ID=172]'
                Meter_Value_172 = master.execute(172, cst.READ_INPUT_REGISTERS, 100, 30)
                print  Meter_Value_172

                time.sleep(2)
                print '[ID=173]'
                Meter_Value_173 = master.execute(173, cst.READ_INPUT_REGISTERS, 100, 30)
                print Meter_Value_173                
                time.sleep(2)
                ##                PhA_ActEnergy=str(Meter_Value[8])+str(Meter_Value[7])
##                PhA_ReactEnergy=str(Meter_Value[10])+str(Meter_Value[9])
##                PhA_ApparEnergy=str(Meter_Value[12])+str(Meter_Value[11])
##
##                PhB_ActEnergy=str(Meter_Value[21])+str(Meter_Value[20])
##                PhB_ReactEnergy=str(Meter_Value[23])+str(Meter_Value[22])
##                PhB_ApparEnergy=str(Meter_Value[25])+str(Meter_Value[24])
##
##                PhC_ActEnergy=str(Meter_Value[34])+str(Meter_Value[33])
##                PhC_ReactEnergy=str(Meter_Value[36])+str(Meter_Value[35])
##                PhC_ApparEnergy=str(Meter_Value[38])+str(Meter_Value[37])
##
##                # defining the api-endpoint
##                API_ENDPOINT = CEMS_URL + "input/post.json?node=" + NODE_NAME + "_" + TCM3001_ID + "_" + MAC_ADD + "&json={"\
##                +'PhA_Irms: '+str(Meter_Value[0]*0.01) +','\
##                +'PhA_Vrms: '+str(Meter_Value[1]*0.1) +','\
##                +'PhA_Pf: '+str(Meter_Value[2]*0.0001) +','\
##                +'PhA_LineFreq: '+str(Meter_Value[3]*0.01) +','\
##                +'PhA_ActPower: '+str(Meter_Value[4]*0.01) +','\
##                +'PhA_ReactPower: '+str(Meter_Value[5]*0.01) +','\
##                +'PhA_ApparPower: '+str(Meter_Value[6]*0.01) +','\
##                +'PhA_ActEnergy: '+PhA_ActEnergy+','\
##                +'PhA_ReactEnergy: '+PhA_ReactEnergy+','\
##                +'PhA_ApparEnergy: '+PhA_ApparEnergy+','\
##                +'PhB_Irms: '+str(Meter_Value[14]*0.01) +','\
##                +'PhB_Vrms: '+str(Meter_Value[15]*0.1) +','\
##                +'PhB_Pf: '+str(Meter_Value[16]*0.0001) +','\
##                +'PhB_LineFreq: '+str(Meter_Value[17]*0.01) +','\
##                +'PhB_ActPower: '+str(Meter_Value[17]*0.01) +','\
##                +'PhB_ReactPower: '+str(Meter_Value[18]*0.01) +','\
##                +'PhB_ApparPower: '+str(Meter_Value[19]*0.01) +','\
##                +'PhB_ActEnergy: '+PhB_ActEnergy +','\
##                +'PhB_ReactEnergy: '+PhB_ReactEnergy +','\
##                +'PhB_ApparEnergy: '+PhB_ApparEnergy +','\
##                +'PhC_Irms: '+str(Meter_Value[26]*0.01) +','\
##                +'PhC_Vrms: '+str(Meter_Value[27]*0.1) +','\
##                +'PhC_Pf: '+str(Meter_Value[28]*0.001) +','\
##                +'PhC_LineFreq: '+str(Meter_Value[29]*0.001) +','\
##                +'PhC_ActPower: '+str(Meter_Value[30]*0.001) +','\
##                +'PhC_ReactPower: '+str(Meter_Value[31]*0.001) +','\
##                +'PhC_ApparPower: '+str(Meter_Value[32]*0.001) +','\
##                +'PhC_ActEnergy: '+PhC_ActEnergy  +','\
##                +'PhC_ReactEnergy: '+PhC_ReactEnergy +','\
##                +'PhC_ApparEnergy: '+PhC_ApparEnergy +','\
##                +'Irms_avg: '+str(Meter_Value[39]*0.01) +','\
##                +'Pf_avg: '+str(Meter_Value[40]*0.0001) +','\
##                +'KW_tot: '+str(Meter_Value[41]*0.01) +','\
##                +'KVar_tot: '+str(Meter_Value[42]*0.01) +','\
##                +'KVa_tot: '+str(Meter_Value[43]*0.01) +','\
##                +'KWh_tot: '+str(Meter_Value[45])+str(Meter_Value[44])  +','\
##                +'KVarh_tot: '+str(Meter_Value[47])+str(Meter_Value[46])  +','\
##                +'KVah_tot: '+str(Meter_Value[49])+str(Meter_Value[48])  \
##                +"}&apikey="+API_KEY
##                print "checked"
##
##                r = requests.post(url = API_ENDPOINT)
##                print API_ENDPOINT
                time.sleep(2)




        except modbus_tk.modbus.ModbusError, e:
            print "Modbus error", e.get_exception_code()
            pass
        ##    except Exception, e2:
        ##        #print "Error", str(e2)
        ##        pass
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
