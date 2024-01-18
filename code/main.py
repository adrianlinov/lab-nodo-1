
import random
from lora import LoRa
import time
# import _thread
from payload import Payload
import payload_manager as PayloadManager
import constants as constant
import machine
from machine import UART
import ds18x20_new as ds18x20_new
from logger import logger
import utils
from components.actuators.relay_actuator import RelayActuator


actuators = []
available_to_rx = False
pulses_actual = 0
flowing = False
reset = False



def test_i2c():
    while True:
        try:
            i2c = machine.SoftI2C(scl=machine.Pin(25), sda=machine.Pin(22), freq=100000)
            # inpu = input("Ingrese comando: ")
            inpu = "R"
            command = inpu.encode('utf-8')
            i2c.writeto(0x63, command)
            time.sleep(1)
            
            response = i2c.readfrom(0x63, 8)
            print(response.decode("utf-8"))
            time.sleep(1)
        except Exception as e:
            logger.logException(e)

class LoRaTransceiver:
    def __init__(self):
        try:
            self.lora = LoRa()
            self.lora.set_callback(self.receive_callback)
        except Exception as e:
            logger.logException(e)
            machine.reset()

    def verify_payload(self, payload):
        try:
            validate = payload.split("}-")
            validate[0] = str(validate[0]) + "}"
            if sum(bytearray(validate[0],'utf8')) == int(validate[1]):
                payload_obj = Payload(payload)
                # print(payload)
                # print(payload_obj.receiver)
                # print(constant.node_id)
                
                if payload_obj.receiver in [constant.node_id, constant.node_id_prev]:
                    logger.log("=======")
                    logger.log(payload)
                    logger.log(f"RECIBIDO: node_id: {constant.node_id} - receiver: {payload_obj.receiver}")
                    logger.log("=======")
                    return True
                else:    
                    logger.log("=======")
                    logger.log(payload)
                    logger.log(f"ERROR: node_id: {constant.node_id} - receiver: {payload_obj.receiver}")
                    logger.log("=======")
                    return False
            else:
                logger.log("=======")
                logger.log(payload)
                logger.log("ERROR: Payload no cumple el formato deseado")
                logger.log("=======")
                return False
        except Exception as e:
            logger.logException(e)
            return False


    def wait_for_message(self):
        global reset
        while reset == False:
            try:
                # if available_to_rx:
                self.lora.receive_msg()
            except Exception as e:
                logger.logException(e)
                continue

    def receive_callback(self, payload_str):
        try:
            if self.verify_payload(payload_str) == True:
                payload = Payload(payload_str)
                payload.print()
                PayloadManager.payload_received(payload)
            else:
                # print(payload_str)
                logger.log("Payload Received: N/A")
        except Exception as e:
            logger.logException(e)



    def send_message(self, msg):
        # TOA = 390ms
        try:
            self.lora.send(msg)
        except Exception as e:
            logger.logException(e)

    def tx_loop(self):
        # global available_to_rx
        global reset
        while reset == False:
            try:
                # available_to_rx = True
                payload = PayloadManager.get_payload_to_send()
                if payload != None:
                    # available_to_rx = False
                    payload.print()
                    # print(payload.to_json_with_checksum())
                    # print("INICIO ENVIO")
                    self.send_message(payload.to_json_with_checksum())
                    # print("FIN ENVIO")
                    # available_to_rx = True
                    time.sleep(random.randint(2,5) * 2)
            except Exception as e:
                logger.logException(e)
                continue


    def lora_loop(self):
        # global available_to_rx
        global reset
        time_inicio = time.ticks_ms()
        # print("starting LoRa Loop")
        
        while True:
            # print(utils.free())
            # print(utils.df())
            if (time.ticks_ms() - time_inicio > 1000 * 60 * 10):
                break
            # print(time.ticks_ms() - time_inicio)
            try:
                # PARTE RECEPCION
                rx_time = time.ticks_ms()
                while time.ticks_ms() - rx_time < 4000:
                    try:
                        self.lora.receive_msg()
                    except:
                        continue
                # PARTE RECEPCION
                # PARTE ENVIO
                payload = PayloadManager.get_payload_to_send()
                if payload != None:
                    # available_to_rx = False
                    payload.print()
                    # print(payload.to_json_with_checksum())
                    # print("INICIO ENVIO")
                    self.send_message(payload.to_json_with_checksum())
                    # print("FIN ENVIO")
                    # available_to_rx = True
                # PARTE ENVIO
            except Exception as e:
                logger.logException(e)
                continue
            
            
def test_flowmeter():
    
    ae1 = RelayActuator("AE1", "1", 16, flowmeter_pin=36)   # AMARILLO
    ae2 = RelayActuator("AE2", "2", 33, flowmeter_pin=22)   # MARRON
    ae3 = RelayActuator("AE3", "3", 0, flowmeter_pin=34)    # AZUL
    ae4 = RelayActuator("AE4", "4", 13, flowmeter_pin=35)   # BLANCO
    ae5 = RelayActuator("AE5", "5", 21, flowmeter_pin=15)   # VERDE
    ae6 = RelayActuator("AE6", "6", 17, flowmeter_pin=12)   # NARANJA
    # ae7 = RelayActuator("AE7", "7", 23,flowmeter_pin= 3)  # ROJO
    # ae8 = RelayActuator("AE8", "8", 1, flowmeter_pin=10)  # NEGRO
    ae9 = RelayActuator("AE9", "9", 4, flowmeter_pin=25)   # TIRRA
    
    # EL CAUDALIMETRO DE 7 RALLAS ES EL 9
    time.sleep(5)

    ae1.set_state(0)
    ae2.set_state(0)
    ae3.set_state(0)
    ae4.set_state(0)
    ae5.set_state(0)
    ae6.set_state(0)
    # ae7.set_state(0)
    # ae8.set_state(0)
    ae9.set_state(0)

    time.sleep(1)

    # actuators.append(ae1)
    # actuators.append(ae2)
    # actuators.append(ae3)
    # actuators.append(ae4)
    actuators.append(ae5)
    # actuators.append(ae6)
    # actuators.append(ae7)
    # actuators.append(ae8)
    # actuators.append(ae9)

    while True:
        for actuator in actuators:
            # print(actuator.id)
            actuator.set_state_flowmetter(11.25)
            time.sleep(10)


def main():
    global reset
    # global available_to_rx
    print("starting Payload Manager")

    PayloadManager.start()
    while True:
        # print("starting LoRa")
        lora = LoRaTransceiver()
        
        # _thread.start_new_thread(lora.lora_loop, ())
        # _thread.start_new_thread(lora.wait_for_message, ())
        # _thread.start_new_thread(lora.tx_loop, ())
        lora.lora_loop()
        # while 1000 * 60 * 5 < (time.ticks_ms - time_inicio):
        #     time.sleep(1)
        #     # print(".")
        # reset = True
        # available_to_rx = False
        
        # print("Reset Lora")
        time.sleep(10)
        reset = False



if __name__ == '__main__':
    try:
        # print("started")
        time.sleep(5)

        # test_i2c()
        # try_ds18b20()
        # test_flowmeter()
        main()
    except Exception as e:
        logger.logException(e)