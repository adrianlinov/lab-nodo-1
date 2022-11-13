

from payload import Payload
from time import sleep
import _thread
import payload_processor as PayloadProcessor


payload_to_send = []
payload_waiting_ack1 = []
payload_received = []
payload_sending_ack1 = []
payload_to_process = []

def start():
    _thread.start_new_thread(receiver_loop, ())
    _thread.start_new_thread(send_ack1_loop, ())
    _thread.start_new_thread(processing_loop, ())
    _thread.start_new_thread(no_ack1_received_loop, ())

def process_payload(payload):
    """Inserta un payload a la lista de recibidos y para su procesamiento"""
    payload_received.append(payload)

def payload_in_queue_to_send():
    """Consulta si hay un payload en la cola de envio"""
    return len(payload_to_send) > 0

def payload_in_queue_to_process():
    """Consulta si hay un payload en la cola de envio"""
    return len(payload_to_process) > 0

def payload_waiting_ack1_in_queue():
    """Consulta si hay un payload en la cola de envio"""
    return len(payload_waiting_ack1) > 0

def payload_in_queue_to_send_ack1():
    """Consulta si hay un payload en la cola de envio"""
    return len(payload_sending_ack1) > 0

def payload_in_queue_received():
    """Consulta si hay un payload en la cola de procesamiento"""
    return len(payload_received) > 0

def add_payload_to_sending_queue(payload):
    payload_to_send.append(payload)
    payload_waiting_ack1.append(payload)

def get_payload_to_send():
    """Obtiene el primer payload de la cola de envio"""
    # PUEDE HABER UN ERROR AQUI AL HACER POP SI NO HAY ELEMENTOS EN LA LISTA
    if len(payload_to_send) > 0:
        return payload_to_send.pop(0)
    else:
        return None

# ===================== Processing Methods =====================

# CORREGIR: SE DEBE ENVIAR UN ACK1 CADA 5 SEGUNDO SI ES QUE NO SE HA RECIBIDO EL ACK2
def register_process(payload):
    payload_sending_ack1.append(payload)
    

def process_ping(payload):
    pass

def process_set_state(payload):
    pass

def process_read(payload):
    pass

def process_read_all(payload):
    pass

def process_ack_1(payload):
    # find in packets waiting ACK
    payload_command = next((x for x in payload_sending_ack1 if x.p_id == payload.data["ack_1"]))
    if payload_command != None:
        ack2_payload = Payload()
        ack2_payload.action = "ack_2"
        ack2_payload.data["ack_2"] = payload.data["ack_1"]
        ack2_payload.receiver = payload.sender
        payload_command.number_of_ack1_received = payload_command.number_of_ack1_received + 1
        payload_to_send.append(ack2_payload)

def dummmy_action():
    payload = Payload()
    payload.action = "action"
    payload.data["led_1"] = "on"
    payload.receiver = "nodo_a"
    payload_to_send.append(payload)
    return True


def receive_ack1(ack1_payload):
    payload = next((x for x in payload_waiting_ack1 if x.p_id == ack1_payload.data["ack_1"]))
    payload_waiting_ack1.remove(payload)


def receive_ack2(ack2_payload):
    print("Received ACK2 for:" + ack2_payload.data["ack_2"])
    payload = next((x for x in payload_sending_ack1 if x.p_id == ack2_payload.data["ack_2"]))
    if payload != None:
        payload_sending_ack1.remove(payload)
        payload_to_process.append(payload)
#     
# ======================= Loops ======================    

def receiver_loop():
    """Procesa los payloads en la cola de procesamiento"""
    while True:
        # En caso de payloads recibidos se procesan
        if payload_in_queue_received():
            payload = payload_received.pop(0)
            # print(payload.to_dic())
            if payload.action == ("set_state" or "read" or "read_all"):
                print("Payload Received: " + payload.p_id)
                register_process(payload)

            if payload.action == "ack_1":
                receive_ack1(payload)

            if payload.action == "ack_2":
                receive_ack2(payload)


def no_ack1_received_loop():
    while True:
        if (payload_waiting_ack1_in_queue()):
            try:
                sleep(5)
                payload = payload_waiting_ack1.pop(0)
                payload_to_send.append(payload)
                payload_waiting_ack1.append(payload)
            except:
                continue

def send_ack1_loop():
    while True:
        if (payload_in_queue_to_send_ack1()):
            try:
                sleep(2)
                payload = payload_sending_ack1.pop(0)
                print("Sending ACK1: " + payload.p_id)
                payload_to_send.append(payload.generate_ack1())
                payload_sending_ack1.append(payload)
            except Exception as e:
                print(e)
                continue


def processing_loop():
    while True:
        if (payload_in_queue_to_process()):
            PayloadProcessor.process_payload(payload_to_process.pop(0))


def transmitter_loop():
    while True:
        dummmy_action()
        sleep(5)