

from payload import Payload
import time
import _thread
import payload_processor as PayloadProcessor
import constants


payload_to_send = []
payload_waiting_ack1 = []
payload_received = []
payload_sending_ack1 = []
payload_to_process = []

last_received_time = None
registered_by_gateway = False

def start():
    _thread.start_new_thread(receiver_loop, ())
    _thread.start_new_thread(send_ack1_loop, ())
    _thread.start_new_thread(processing_loop, ())
    _thread.start_new_thread(no_ack1_received_loop, ())
    _thread.start_new_thread(dummy_sender_loop, ())
    PayloadProcessor.start()
    register_in_network()


def register_in_network():
    global registered_by_gateway
    registered_by_gateway = False
    payload = Payload()
    payload.receiver = "gw"
    payload.action = "register"
    payload.data["n_n"] = constants.NODE_NAME
    constants.reset_id()
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
            payload = get_payload_received()
            if payload != None:
                if payload.action == ("set_state" or "read" or "read_all") and registered_by_gateway:
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
                time.sleep(5)
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
        time.sleep(2)
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
            payload = payload_to_process.pop(0)
            if payload.action == "register":
                global registered_by_gateway
                registered_by_gateway = True
            if payload.action != "register" and registered_by_gateway:    
                PayloadProcessor.process_payload(payload)


def transmitter_loop():
    while True:
        time.sleep(5)

def dummy_sender_loop():
    while True:
        if registered_by_gateway:
            time.sleep(5)
            payload = Payload()
            payload.action = "important"
            payload.data["led"] = "ON"
            payload.receiver = "gw"
            payload_to_send.append(payload)


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
        time.sleep(1)