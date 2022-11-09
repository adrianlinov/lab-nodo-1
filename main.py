from lora import LoRa
import machine
import time
import json
import _thread
from payload import Payload
import payload_manager as PayloadManager

payloads_received_waiting_for_processing = []
payloads_waiting_for_sending = []

class LoRaTransceiver:
    def __init__(self):
        self.lora = LoRa()
        self.lora.set_callback(self.receive_callback)

    def verify_payload(self, payload):
        validate = payload.split("}-")
        validate[0] = str(validate[0]) + "}"
        print(sum(bytearray(validate[0],'utf8')), " - ",
              int(validate[1]))
        if sum(bytearray(validate[0],'utf8')) == int(validate[1]):
            return True
        else:
            return False

    def listen_for_messages(self):
        while True:
            while len(payloads_waiting_for_sending) == 0:
                self.lora.receive_msg()

    def wait_for_message(self):
        self.lora.wait_msg()

    def receive_callback(self, payload_str):
        print("payload recived")
        if self.verify_payload(payload_str) == True:
            payload = Payload(payload_str)
            PayloadManager.process_payload(payload)
            print("Payload received:" + str(payload.p_id))

    def process_payload(self, payload):
        pass

    def send_message(self, msg):
        self.lora.send(msg)

    def tx_loop(self):
        while True:
            if PayloadManager.payload_in_queue_to_send() > 0:
                payload = PayloadManager.get_payload_to_send()
                self.send_message(payload.to_json_with_checksum())
            # get number of threads

def main():
    print("starting")
    lora = LoRaTransceiver()
    print("starting thread")
    _thread.start_new_thread(lora.wait_for_message, ())
    # PayloadManager.start()
    while True:
        print(" ")
        time.sleep(5)

if __name__ == '__main__':
    main()
