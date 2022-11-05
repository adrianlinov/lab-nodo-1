from lora import LoRa
import machine
import time
import json
import _thread
from payload import Payload

payloads_received_waiting_for_processing = []
payloads_waiting_for_sending = []
class LoraManager:
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



    def receive_callback(self, payload):
        print("payload recived")
        print(payload)
        if payload != None:
            if self.verify_payload(payload) == True:
                payload = Payload(payload)
                if payload.run() == "success":
                    print("success")
                    response_payload = payload.response().to_json_with_checksum()
                    payloads_waiting_for_sending.append(response_payload)
                    self.send_message(response_payload)
                    # Send status_payload
                else:
                    print("error")
                    # status_payload = payload.response_status()
                    # payloads_waiting_for_sending.append(status_payload)
                    # Send status_payload
                    # respond with error and error_message
    def process_payload(self, payload):
        pass
    def send_message(self, msg):
        self.lora.send(msg)
    def tx_loop(self):
        while True:
            # leer data de sensores
            # enviar data
            msg = 'ESP->RPI: '
            print(msg)
            self.lora.send(msg)
            time.sleep(1)
            # get number of threads
def main():
    print("starting")
    lora = LoraManager()
    print("starting thread")
    _thread.start_new_thread(lora.wait_for_message, ())
    while True:
        print(" ")
        time.sleep(5)
    # lora.wait_msg()
    # Colocar todo en modo seguro
    # Entablar comunicaci�n con el gateway hasta obtener respuesta
    # Ejecutar proceso de inicio
    # Colocar todo a como indique el Gateway
    # Iniciar loop de transmisi�n
        # Si el no se obtiene respuesta de confirmaci�n del gateway en 5 intentos colocar en modo seguro
    # lora.tx_loop()
if __name__ == '__main__':
    main()
