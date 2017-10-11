#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 詮能科技 中科院雷物組 VU8 <-> RPi <-> PC 專案
 RPi 作為Modbus RTU master 向 VU8要資料，再扮演Modbus TCP slave 等待 Modbus TCP Master讀表
 
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

import logging
import threading

import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus as modbus
import modbus_tk.modbus_tcp as modbus_tcp
from modbus_tk import modbus_rtu
import random

#RPi only
#PORT = '/dev/ttyAMA0'
#RPi
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

                #print 'aa: ', aa, 'size', len(aa)
                #aa = random.random()


                slave_1.set_values('0', 0, distance)
            
        """
            cmd = sys.stdin.readline()
            #这里是进入程序以后，读取每次输入的命令：以回车来判断命令是否输入完毕
            args = cmd.split(' ')
            if cmd.find('quit')==0:
                #当输入的只有quit，程序就会退出
                sys.stdout.write('bye-bye\r\n')
                break
            elif args[0]=='add_slave':
                slave_id = int(args[1])
                #slave id只能为int?是的
                server.add_slave(slave_id)
                sys.stdout.write('done: slave %d added\r\n' % (slave_id))
                #write到哪里去了？屏幕输出去了~~
            elif args[0]=='add_block':
                slave_id = int(args[1])
                name = args[2]
                block_type = int(args[3])
                starting_address = int(args[4])
                length = int(args[5])
                slave = server.get_slave(slave_id)
                slave.add_block(name, block_type, starting_address, length)
                sys.stdout.write('done: block %s added\r\n' % (name))
            elif args[0]=='set_values':
                slave_id = int(args[1])
                name = args[2]
                #这个name是slave_id对应的block的名字
                address = int(args[3])
                values = []
                #这里的values只可少设不可多设，否则就报错退出程序
                for v in args[4:]:
                    #value只能是int，就算是其他数字类型也报错
                    #囧 好奇怪，明明平时int（0.1）也是可以的
                    values.append(int(v))
                slave = server.get_slave(slave_id)
                slave.set_values(name, address, values)
                values = slave.get_values(name, address, len(values))
                sys.stdout.write('done: values written: %s\r\n' % (str(values)))
            elif args[0]=='get_values':
                slave_id = int(args[1])
                name = args[2]
                address = int(args[3])
                length = int(args[4])
                slave = server.get_slave(slave_id)
                values = slave.get_values(name, address, length)
                sys.stdout.write('done: values read: %s\r\n' % (str(values)))
            else:
                sys.stdout.write("unknown command %s\r\n" % (args[0]))
"""                
    finally:
        server.stop()

