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
flag1 = "Flag1:56901cf4584b7841ec3cdbe1dba23caa47a79eb1\n-> Sending critical alert..."
flag2 = "Flag2:9c7406a76dd8958ea0026e4756dca4346d1452b8\n-> Sending critical alert...\n\nThe Oil Plant has been compromised!!"
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
	if rr.registers[0] == 1 and rr.registers[2] == 0:
            # Flag1: pumping too much oil in the oil storage unit
            counter = 0
            while counter < 30:
                rr = client.read_holding_registers(0x1, 0x10)
	        if rr.registers[0] == 1 and rr.registers[2] == 0:
                    log.info("feeding with oil, valve is closed ({})".format(counter))
                    counter = counter + 1
                else:
                    break
                time.sleep(1)
            if counter == 30:
	        log.info("got flag1")
                with open('/app/noVNC/flag1.txt', 'w') as f:
                    f.write(flag1)
                    f.close()
	elif rr.registers[6] > 1000 and rr.registers[5] < 2:
            # Flag2: crude oil flows trough the separator vessel valve
            log.info("got flag2")
            with open('/app/noVNC/flag2.txt', 'w') as f:
                f.write(flag2)
                f.close()
        time.sleep(5)
except KeyboardInterrupt:
    client.close()
except ConnectionException:
    log.error("Unable to connect / Connection lost")
