#!/usr/bin/python
# -*- coding: utf-8 -*-
# filename: master_example.py
# 詮能科技 VU8 讀表

# ------------------------------------------------------------------------------
# 导入外部模块
# ------------------------------------------------------------------------------
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp


# ------------------------------------------------------------------------------
# 主程序
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        #Connect to the slave
        #Connect to the slave
		# 設定 TCM3001 IP address
        master = modbus_tcp.TcpMaster('127.0.0.1',1152)
        master.set_timeout(5.0)
        while True:
		
	    # 設定ID及封包起始位址與長度 (母表ID=1, 子表#1 ID=172, 子表#2 ID=172, ...)
            print master.execute(1, cst.READ_INPUT_REGISTERS, 0, 8)
            #master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 200, output_value=xrange(12))
            #print master.execute(1, cst.READ_HOLDING_REGISTERS, 10, 3)

    except modbus_tk.modbus.ModbusError, e:
        print "Modbus error", e.get_exception_code()
    except Exception, e2:
        print "Error", str(e2)
