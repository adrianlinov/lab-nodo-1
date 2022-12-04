

from payload import Payload
import time
import _thread
import payload_processor as PayloadProcessor
import constants
import random


payload_to_send = []
payload_waiting_ack1 = []
payload_received_from_ext = []
payload_sending_ack1 = []
payload_to_process = []

last_received_time = time.time()
registered_by_gateway = False

def start():
    _thread.start_new_thread(receiver_loop, ())
    _thread.start_new_thread(send_ack1_loop, ())
    _thread.start_new_thread(processing_loop, ())
    _thread.start_new_thread(no_ack1_received_loop, ())
    _thread.start_new_thread(keep_alive_loop, ())
    PayloadProcessor.start()
    register_in_network()


def register_in_network():
    global registered_by_gateway
    registered_by_gateway = False
    payload = Payload()
    payload.receiver = "gw"
    payload.action = "register"
    payload.data["n_n"] = constants.NODE_NAME
    payload.data["n_id"] = constants.NODE_ID
    payload.data["s"] = [
        "TEMP_1",
        "TEMP_2",
        "TEMP_3"
    ]
    payload.data["a"] = [
        "PUMP_1",
        "PUMP_2",
        "PUMP_3",
    ]
    

    add_payload_to_sending_queue(payload)


def payload_received(payload):
    """
    Inserta un payload a la lista de recibidos y para su procesamiento, se utiliza en el Main y 
    se realiza todo el proceso de ACK

    Se debe usar cada vez que se reciben datos nuevos
    """
    payload_received_from_ext.append(payload)

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
    return len(payload_received_from_ext) > 0

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

def get_payload_received_from_ext():
    """
     Obtiene el primer payload de la cola de paquetes raw que se reciben
    """
    if len(payload_received_from_ext) > 0:
        return payload_received_from_ext.pop(0)
    else:
        return None


# CORREGIR: SE DEBE ENVIAR UN ACK1 CADA 5 SEGUNDO SI ES QUE NO SE HA RECIBIDO EL ACK2
def register_process(payload):
    """                                                                                 
    Al recibir un paquete que no es un ACK, se debe registrar el proceso para iniciar el proceso de ACK
    """
    # AQUI DEBE IR VERIFICACION DE QUE EL NODO ESTA REGISTRADO
    payload_sending_ack1.append(payload)
    


def receive_ack1(ack1_payload):
    payload = None
    for x in payload_waiting_ack1:
        if x.p_id == ack1_payload.data["ack_1"]:
            payload = x
            break
    if payload != None:
        payload_waiting_ack1.remove(payload)
        payload_to_send.append(payload.generate_ack2())
        # AQUI DEBE IR APPEND A LA DE PROCESAMIENTO
        payload_to_process.append(payload)
    else:
        ack_2 = Payload()
        ack_2.receiver = ack1_payload.sender
        ack_2.action = "ack_2"
        ack_2.data["ack_2"] = ack1_payload.data["ack_1"]
        payload_to_send.append(ack_2)


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
            global last_received_time
            last_received_time = time.time()
            payload = get_payload_received_from_ext()
            if payload != None:
                if payload.action in ["set_state","read","read_all"] and registered_by_gateway:
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
                time.sleep(random.randint(1, 5))
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
        time.sleep(1)
        if (payload_in_queue_to_send_ack1()):
            try:
                payload = get_payload_sending_ack1()
                payload_to_send.append(payload.generate_ack1())
                payload_sending_ack1.append(payload)
                # if payload.action != "ping" and payload.number_of_ack1_send >= 10:
                #     # Colocar dispositivo en modo seguro
                #     pass
                    
                if payload.number_of_ack1_send >= 30:
                    # Colocar dispositivo en modo seguro
                    # Limpiar colas de todos las listas
                    payload_to_send.clear()
                    payload_waiting_ack1.clear()
                    payload_received_from_ext.clear()
                    payload_sending_ack1.clear()
                    payload_to_process.clear()
                    constants.reset_id()
                    register_in_network()


            except Exception as e:
                print(e)
                continue


def processing_loop():
    """
    Procesa los payloads que fueron verificados con ACK
    """
    while True:
        if (payload_in_queue_to_process()):
            payload = payload_to_process.pop(0)
            if payload.action == "register":
                global registered_by_gateway
                registered_by_gateway = True
            if payload.action != "register" and registered_by_gateway:    
                payloadResponse = PayloadProcessor.process_payload(payload)
                if payloadResponse != None:
                    add_payload_to_sending_queue(payloadResponse)
                
                


def transmitter_loop():
    while True:
        time.sleep(5)

def keep_alive_loop():
    while True:
        ping_in_queue = False
        for x in payload_to_send:
            if x.action == "ping":
                ping_in_queue = True
        for x in payload_waiting_ack1:
            if x.action == "ping":
                ping_in_queue = True
        for x in payload_to_process:
            if x.action == "ping":
                ping_in_queue = True
        

                
        if registered_by_gateway and time.time() - last_received_time > 30 and not ping_in_queue:
            payload = Payload()
            payload.action = "ping"
            payload.receiver = "gw"
            payload_to_send.append(payload)
            time.sleep(random.randint(5, 10))
            # REGISTRAR EL KEEPALIVE EN UNA VARIABLE


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
        print("payload_received: " + str(len(payload_received_from_ext)))
        print("=================================")
        time.sleep(1)