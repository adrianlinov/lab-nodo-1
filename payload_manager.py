

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
    _thread.start_new_thread(print_arrays, ())
    PayloadProcessor.start()

def process_payload(payload):
    """
    Inserta un payload a la lista de recibidos y para su procesamiento, se utiliza en el Main y 
    se realiza todo el proceso de ACK

    Se debe usar cada vez que se reciben datos nuevos
    """
    payload_received.append(payload)

def payload_in_queue_to_send():
    """
    Consulta si hay un payload en la cola de envio de paquetes raw, se utiliza para paquetes que no requieren ACK

    Lista de paquetes raw (Payload, ACK1, ACK2)	
    """
    return len(payload_to_send) > 0

def payload_in_queue_to_process():
    """
    Consulta si hay un payload en la cola de procesamiento, que ya cumplio con el proceso de ACK para ser procesado
    """
    return len(payload_to_process) > 0

def payload_waiting_ack1_in_queue():
    """
    Para datos emitidos del Nodo

    Consulta si hay un payload esperando ACK1
    """
    return len(payload_waiting_ack1) > 0

def payload_in_queue_to_send_ack1():
    """
    Consulta si hay un payload en la cola de envio
    """
    return len(payload_sending_ack1) > 0

def payload_in_queue_received():
    """
    Consulta si hay un payload en la cola de recibidos para iniciar con el proceso de ACK
    """
    return len(payload_received) > 0

def add_payload_to_sending_queue(payload):
    """
    Añade un payload a la cola de envio de datos, se utiliza para paquetes que requieren ACK
    """
    payload_to_send.append(payload)
    payload_waiting_ack1.append(payload)

def get_payload_to_send():
    """
    Obtiene el primer payload de la cola de envio
    """
    if len(payload_to_send) > 0:
        return payload_to_send.pop(0)
    else:
        return None

def get_payload_sending_ack1():
    """
    Obtiene el primer payload de la cola de paquetes que se envian ACK1 y esperan ACK2
    """
    if len(payload_sending_ack1) > 0:
        return payload_sending_ack1.pop(0)
    else:
        return None

def get_payload_received():
    """
     Obtiene el primer payload de la cola de paquetes raw que se reciben
    """
    if len(payload_received) > 0:
        return payload_received.pop(0)
    else:
        return None


# CORREGIR: SE DEBE ENVIAR UN ACK1 CADA 5 SEGUNDO SI ES QUE NO SE HA RECIBIDO EL ACK2
def register_process(payload):
    """
    Al recibir un paquete que no es un ACK, se debe registrar el proceso para iniciar el proceso de ACK
    """
    payload_sending_ack1.append(payload)
    
# def process_ack_1(payload):
#     """
#     Procesa el ACK1 recibido de un paquete emitido
#     """
#     payload_command = None
#     for x in payload_sending_ack1:
#         if x.p_id == payload.data["ack_1"]:
#             payload_command = x
#             break
#     if payload_command != None:
#         ack2_payload = Payload()
#         ack2_payload.action = "ack_2"
#         ack2_payload.data["ack_2"] = payload.data["ack_1"]
#         ack2_payload.receiver = payload.sender
#         payload_command.number_of_ack1_received = payload_command.number_of_ack1_received + 1
#         payload_to_send.append(ack2_payload)


def receive_ack1(ack1_payload):
    payload = None
    for x in payload_waiting_ack1:
        if x.p_id == ack1_payload.data["ack_1"]:
            payload = x
            break
    if payload != None:
        payload_waiting_ack1.remove(payload)


def receive_ack2(ack2_payload):
    payload = None
    for x in payload_sending_ack1:
        if x.p_id == ack2_payload.data["ack_2"]:
            payload = x
            break
    if payload != None:
        payload_sending_ack1.remove(payload)
        payload_to_process.append(payload)
#     
# ======================= Loops ======================    

def receiver_loop():
    """
    Procesa los payloads en la cola de procesamiento
    """
    while True:
        # En caso de payloads recibidos se procesan
        if payload_in_queue_received():
            payload = get_payload_received()
            if payload != None:
                if payload.action == ("set_state" or "read" or "read_all"):
                    register_process(payload)

                elif payload.action == "ack_1":
                    receive_ack1(payload)

                elif payload.action == "ack_2":
                    receive_ack2(payload)


def no_ack1_received_loop():
    """
    Renvia los paquetes que no recibieron el ACK1
    """
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
    """
    Envia los ACK1
    """
    while True:
        sleep(2)
        if (payload_in_queue_to_send_ack1()):
            try:
                payload = get_payload_sending_ack1()
                # print("Sending ACK1: " + payload.p_id)
                payload_to_send.append(payload.generate_ack1())
                payload_sending_ack1.append(payload)
            except Exception as e:
                print(e)
                continue


def processing_loop():
    """
    Procesa los payloads que fueron verificados con ACK
    """
    while True:
        if (payload_in_queue_to_process()):
            PayloadProcessor.process_payload(payload_to_process.pop(0))


def transmitter_loop():
    while True:
        sleep(5)

def print_arrays():
    '''
    Imprime los arrays de la cola de envio, recepcion y procesamiento
    '''
    while True:
        print("=================================")
        print("payload_to_send: " + str(len(payload_to_send)))
        print("payload_to_process: " + str(len(payload_to_process)))
        print("payload_waiting_ack1: " + str(len(payload_waiting_ack1)))
        print("payload_sending_ack1: " + str(len(payload_sending_ack1)))
        print("payload_received: " + str(len(payload_received)))
        print("=================================")
        sleep(1)