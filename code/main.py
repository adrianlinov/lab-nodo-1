# from lora import LoRa
import time
import json
import _thread
# from payload import Payload
# import payload_manager as PayloadManager
# import constants as constant
# import components.node as Node
import sys
import machine, onewire
# import ds18x20


available_to_rx = False

class LoRaTransceiver:
    def __init__(self):
        self.lora = LoRa()
        self.lora.set_callback(self.receive_callback)

    def verify_payload(self, payload):
        validate = payload.split("}-")
        validate[0] = str(validate[0]) + "}"
        if sum(bytearray(validate[0],'utf8')) == int(validate[1]):
            payload_obj = Payload(payload)
            print(payload)
            print(payload_obj.receiver)
            print(constant.NODE_ID)
            if payload_obj.receiver == constant.NODE_ID:
                return True
            else: 
                print(payload_obj.receiver) 
                print(constant.NODE_ID)
                print(len(payload_obj.receiver))
                print(len(constant.NODE_ID))
                print(type(payload_obj.receiver))
                print(type(constant.NODE_ID))
                print("Error de validacion por ID")
                return False
        else:
            print("Error de validacion por checksum")
            return False


    def wait_for_message(self):
        while True:
            if available_to_rx:
                self.lora.receive_msg()
            

    def receive_callback(self, payload_str):
        if self.verify_payload(payload_str) == True:
            payload = Payload(payload_str)
            payload.print()
            PayloadManager.payload_received(payload)
        else:
            print("Payload Received: N/A")
            print(payload_str)

    def send_message(self, msg):
        # TOA = 390ms
        self.lora.send(msg)

    def tx_loop(self):
        global available_to_rx
        while True:
            available_to_rx = True
            payload = PayloadManager.get_payload_to_send()
            if payload != None:
                try:
                    available_to_rx = False
                    # print("Payload Send: " + payload.to_json_with_checksum())
                    payload.print()
                    self.send_message(payload.to_json_with_checksum())
                except Exception as e:
                    print(e)


def main():
    print("starting")
    lora = LoRaTransceiver()
    print("starting threads")
    _thread.start_new_thread(lora.wait_for_message, ())
    _thread.start_new_thread(lora.tx_loop, ())
    PayloadManager.start()
    while True:
        time.sleep(.5)
        print(" ")

def try_ds18b20():
    while True:
        sensor = ds18x20.DS18X20(onewire.OneWire(machine.Pin(13)))
        roms = sensor.scan()
        sensor.convert_temp()
        time.sleep_ms(750)
        for rom in roms:
            print(type(rom))
            print(''.join('{:02x}'.format(byte) for byte in rom))
            print(sensor.read_temp(rom))
            print("")
        time.sleep(5)
        print("====================================")

def try_airvalves():
    pins = [2, 5, 4, 22, 23, 12, 25, 33, 32]
    pm = [machine.Pin(2, machine.Pin.OUT), machine.Pin(5, machine.Pin.OUT), machine.Pin(4, machine.Pin.OUT), machine.Pin(22, machine.Pin.OUT), machine.Pin(23, machine.Pin.OUT), machine.Pin(12, machine.Pin.OUT), machine.Pin(25, machine.Pin.OUT), machine.Pin(33, machine.Pin.OUT), machine.Pin(32, machine.Pin.OUT)]
    # Turn pins on for 5 seconds, then off for 5 seconds, repeat.
    
    while True:
        print("OFF")
        for p in pm:
            p.off()
        time.sleep(5)
        print("ON")
        for p in pm:
            p.off()
        time.sleep(5)

if __name__ == '__main__':
    try:
        main()
        print("started")
        # try_ds18b20()
        # try_airvalves()
    except Exception as e:
        sys.print_exception(e)
