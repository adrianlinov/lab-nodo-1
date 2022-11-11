from lora import LoRa
import machine
import time
import json
import _thread
from payload import Payload
import payload_manager as PayloadManager

payloads_received_waiting_for_processing = []
payloads_waiting_for_sending = []

available_to_rx = True

class LoRaTransceiver:
    def __init__(self):
        self.lora = LoRa()
        self.lora.set_callback(self.receive_callback)

    def verify_payload(self, payload):
        validate = payload.split("}-")
        validate[0] = str(validate[0]) + "}"
        if sum(bytearray(validate[0],'utf8')) == int(validate[1]):
            return True
        else:
            return False


    def wait_for_message(self):
        # while True:
        #     if available_to_rx:
        #         self.lora.receive_msg()
        self.lora.wait_msg()

    def receive_callback(self, payload_str):
        if self.verify_payload(payload_str) == True:
            payload = Payload(payload_str)
            PayloadManager.process_payload(payload)

    def process_payload(self, payload):
        pass

    def send_message(self, msg):
        self.lora.send(msg)

    def tx_loop(self):
        while True:
            available_to_rx = True
            if PayloadManager.payload_in_queue_to_send():
                try:
                    available_to_rx = False
                    time.sleep(0.5)
                    payload = PayloadManager.get_payload_to_send()
                    print("========== PAYLOAD SENT ============")
                    print(payload.to_dic())
                    self.send_message(payload.to_json_with_checksum())
                except Exception as e:
                    print("========================================")
                    print(e)

            # get number of threads

def main():
    print("starting")
    lora = LoRaTransceiver()
    print("starting thread")
    _thread.start_new_thread(lora.wait_for_message, ())
    _thread.start_new_thread(lora.tx_loop, ())
    PayloadManager.start()
    while True:
        time.sleep(.2)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
