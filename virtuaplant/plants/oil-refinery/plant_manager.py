#!/usr/bin/env python

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException
import logging
import time

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

#####################################
# Code
#####################################
client = ModbusClient('localhost', port=5020)

while True:
    try:
        client.connect()
        break
    except KeyboardInterrupt:
        client.close()
        break
    except ConnectionException:
        log.error("Unable to connect")
        time.sleep(1)

try:
    while True:
        rr = client.read_holding_registers(0x1, 0x10)
        if not rr:
            continue
        if rr.registers[0] == 0 and rr.registers[1] == 0 and rr.registers[2] == 0 and rr.registers[3] == 0 and rr.registers[4] == 0 and rr.registers[7] == 0 and rr.registers[8] == 0:
	    # Oil storage is empty, all valves are closed
            log.info("Opening the feed pump")
            rq = client.write_register(0x1, 1)
        elif rr.registers[0] == 1 and rr.registers[1] == 0 and rr.registers[2] == 0 and rr.registers[3] == 0 and rr.registers[4] == 0 and rr.registers[7] == 0 and rr.registers[8] == 0:
	    log.info("Plant is working fine")
        elif rr.registers[0] == 0 and rr.registers[1] == 1 and rr.registers[2] == 0 and rr.registers[3] == 0 and rr.registers[4] == 0 and rr.registers[7] == 0 and rr.registers[8] == 0:
	    # Oil storage is full, all valves are closed
            log.info("Opening the outlet valve")
            rq = client.write_register(0x3, 1)
            log.info("Waiting a few")
	    time.sleep(15)
            log.info("Closing the outlet valve")
            rq = client.write_register(0x3, 0)
            log.info("Resetting the tank level sensor")
            rq = client.write_register(0x2, 0)
            log.info("Opening the waste water valve")
            rq = client.write_register(0x8, 1)
            log.info("Waiting a few")
	    time.sleep(20)
            log.info("Opening the separator vessel valve")
            rq = client.write_register(0x4, 1)
            log.info("Waiting a few")
	    time.sleep(20)
            log.info("Closing the waste water valve")
            rq = client.write_register(0x8, 0)
            log.info("Closing the separator vessel valve")
            rq = client.write_register(0x4, 0)
        else:
	    log.error("Abnormal condition #1")
            log.info("Cleaning the plant")
            log.info("Closing the feed pump")
            rq = client.write_register(0x1, 0)
            log.info("Opening the outlet valve")
            rq = client.write_register(0x3, 1)
            log.info("Opening the waste water valve")
            rq = client.write_register(0x8, 1)
            log.info("Opening the separator vessel valve")
            rq = client.write_register(0x4, 1)
            log.info("Waiting a few")
	    time.sleep(30)
            log.info("Resetting the tank level sensor")
            rq = client.write_register(0x2, 0)
            log.info("Closing the outlet valve")
            rq = client.write_register(0x3, 0)
            log.info("Closing the waste water valve")
            rq = client.write_register(0x8, 0)
            log.info("Closing the separator vessel valve")
            rq = client.write_register(0x4, 0)
        time.sleep(5)
except KeyboardInterrupt:
    client.close()
except ConnectionException:
    log.error("Unable to connect / Connection lost")
