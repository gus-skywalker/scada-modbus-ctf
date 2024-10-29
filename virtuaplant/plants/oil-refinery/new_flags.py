#!/usr/bin/env python

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException
import logging
import time

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# Definições dos alertas de flags
flag1 = "Flag1:bdkf84hj4cfbd5ce3ae91ef7021flv04\n-> Sending critical alert..."
flag2 = "Flag2:0d348fuac66272769fghj3409smfh995\n-> Sending critical alert...\n\nThe Oil Plant has been compromised!!"
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

        # Flag1: Excesso de bombeamento de óleo no tanque
        if rr.registers[0] == 1 and rr.registers[2] == 0:
            counter = 0
            while counter < 30:
                rr = client.read_holding_registers(0x1, 0x10)
                if rr.registers[0] == 1 and rr.registers[2] == 0:
                    log.info("feeding with oil, valve is closed ({})".format(counter))
                    counter += 1
                else:
                    break
                time.sleep(1)
            if counter == 30:
                log.info("got flag1")
                with open('/home/plant/noVNC/flag1.txt', 'w') as f:
                    f.write(flag1)

        # Flag2: Fluxo de óleo bruto na válvula do vaso separador
        if rr.registers[6] > 1000 and rr.registers[5] < 2:
            log.info("got flag2")
            with open('/home/plant/noVNC/flag2.txt', 'w') as f:
                f.write(flag2)

        # Novo Alerta 1: Tanque no nível máximo por muito tempo
        if rr.registers[1] == 1:  # PLC_TANK_LEVEL = 1
            tank_counter = 0
            while tank_counter < 60:
                rr = client.read_holding_registers(0x1, 0x10)
                if rr.registers[1] == 1:
                    log.info("Tank level is at maximum ({})".format(tank_counter))
                    tank_counter += 1
                else:
                    break
                time.sleep(1)
            if tank_counter == 60:
                log.info("Critical Alert: Tank has been at maximum level for an extended time!")
                with open('/home/plant/noVNC/alert_tank_max.txt', 'w') as f:
                    f.write("Tank level critical for extended period.")

        # Novo Alerta 2: Vazamento significativo de óleo
        if rr.registers[6] > 50:  # PLC_OIL_SPILL
            log.info("Critical Alert: Significant oil spill detected!")
            with open('/home/plant/noVNC/alert_oil_spill.txt', 'w') as f:
                f.write("High volume of oil spilled detected.")

        # Novo Alerta 3: Separador em ciclo prolongado
        if rr.registers[3] == 1:  # PLC_SEP_VALVE = 1
            sep_counter = 0
            while sep_counter < 30:
                rr = client.read_holding_registers(0x1, 0x10)
                if rr.registers[3] == 1:
                    log.info("Separator valve open ({})".format(sep_counter))
                    sep_counter += 1
                else:
                    break
                time.sleep(1)
            if sep_counter == 30:
                log.info("Critical Alert: Separator valve open for extended period!")
                with open('/home/plant/noVNC/alert_sep_valve.txt', 'w') as f:
                    f.write("Separator valve open for extended time, check for blockages.")

        # Novo Alerta 4: Sobrecarga na bomba de alimentação
        if rr.registers[0] == 1:  # PLC_FEED_PUMP = 1
            pump_counter = 0
            while pump_counter < 100:
                rr = client.read_holding_registers(0x1, 0x10)
                if rr.registers[0] == 1:
                    log.info("Feed pump running ({})".format(pump_counter))
                    pump_counter += 1
                else:
                    break
                time.sleep(1)
            if pump_counter == 100:
                log.info("Critical Alert: Feed pump running for too long!")
                with open('/home/plant/noVNC/alert_feed_pump.txt', 'w') as f:
                    f.write("Feed pump running for an extended period, check for potential malfunction.")

        # Novo Alerta 5: Limite de processamento de óleo excedido
        if rr.registers[7] > 65000:  # PLC_OIL_PROCESSED
            log.info("Critical Alert: Oil processed limit exceeded!")
            with open('/home/plant/noVNC/alert_oil_processed.txt', 'w') as f:
                f.write("Total oil processed has exceeded safe capacity limits.")

        time.sleep(5)

except KeyboardInterrupt:
    client.close()
except ConnectionException:
    log.error("Unable to connect / Connection lost")
