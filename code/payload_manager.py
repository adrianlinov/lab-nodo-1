

from payload import Payload
import time
import _thread
import payload_processor as PayloadProcessor
import constants
import random
import components.node as Node

registered_by_gateway = False

tx_waiting_ack1 = []
tx_timeout_ack2 = []
rx_sending_ack1 = []
rx_to_process = []
payload_to_send = []

def start():
    _thread.start_new_thread(payload_waiting_ack1_loop, ())
    _thread.start_new_thread(payload_sending_ack1_loop, ())
    _thread.start_new_thread(timeout_for_processing, ())
    _thread.start_new_thread(rx_to_process_loop, ())
    _thread.start_new_thread(connection_timeout_loop, ())
    # _thread.start_new_thread(no_ack1_received_loop, ())
    # _thread.start_new_thread(keep_alive_loop, ())
    register_in_network()


def register_in_network():
    global registered_by_gateway
    registered_by_gateway = False
    payload = Payload()
    payload.receiver = "gw"
    payload.action = "register"
    payload.data["n_n"] = constants.NODE_NAME
    payload.data["n_id"] = constants.NODE_ID
    Node.init()

    payload.data["s"] = []
    sensors = Node.get_sensor_list()
    for sensor in sensors:
        payload.data["s"].append(sensor.get_id())

    payload.data["a"] = []
    actuators = Node.get_actuator_list()
    for actuator in actuators:
        payload.data["a"].append(actuator.get_id())

    tx_waiting_ack1.append(payload)

def payload_received(p_received):
    """
    Inserta un payload a la lista de recibidos y para su procesamiento, se utiliza en el Main y 
    se realiza todo el proceso de ACK

    Se debe usar cada vez que se reciben datos nuevos
    """
    if p_received.action == "ack_1":
        on_ack1_received(p_received)
    elif p_received.action == "ack_2":
        on_ack2_received(p_received)
    else:
        payload = None
        for x in rx_sending_ack1:
            if x.p_id == p_received.p_id:
                payload = x
                break
        for x in rx_to_process:
            if x.p_id == p_received.p_id:
                payload = x
                break
        if payload == None:
            rx_sending_ack1.append(p_received)

def payload_waiting_ack1_loop():
    '''Envía los payloads que están en la lista de espera de ACK1'''
    while True:
        if len(tx_waiting_ack1) > 0:
            payload = tx_waiting_ack1.pop(0)
            payload.tx_payload_send_count += 1
            if payload.tx_payload_send_count > 3:
                payload.priority = 1
            payload_to_send.append(payload)
            tx_waiting_ack1.append(payload)
            time.sleep(random.randint(1, 5))

def payload_sending_ack1_loop():
    '''Envía los ACK1 de los payloads recibidos'''
    while True:
        if len(rx_sending_ack1) > 0:
            payload = rx_sending_ack1.pop(0)
            payload_to_send.append(payload.generate_ack1())
            rx_sending_ack1.append(payload)
            time.sleep(random.randint(1, 5))

def on_ack1_received(ack1_payload):
    '''Al recibir un ACK1 se envía el ACK2'''
    payload = None
    for x in tx_waiting_ack1:
        if x.p_id == ack1_payload.data["ack_1"]:
            payload = x
            break
    if payload != None:
        if (payload.action == "register" and not registered_by_gateway) or (register_in_network):
            tx_waiting_ack1.remove(payload)
            # TODO: SUMAR 1 AL CONTADOR DE ACK2 ENVIADOS y ACTUALIZAR LAST_ACK1_RECEIVED_TIME
            
            tx_timeout_ack2.append(payload)
            payload_to_send.append(payload.generate_ack2())

    for x in tx_timeout_ack2:
        if x.p_id == ack1_payload.data["ack_1"]:
            payload = x
            break
    
    if payload != None:
        if (payload.action == "register" and not registered_by_gateway) or (register_in_network):
            tx_timeout_ack2.remove(payload)
            payload_to_send.append(payload.generate_ack2())
            payload.tx_last_ack1_time = time.time()
            # TODO: SUMAR 1 AL CONTADOR DE ACK2 ENVIADOS y ACTUALIZAR LAST_ACK1_RECEIVED_TIME
            tx_timeout_ack2.append(payload)

def rx_to_process_loop():
    '''Envía los payloads a ser procesados'''
    while True:
        if len(rx_to_process) > 0:
            payload = rx_to_process.pop(0)
            response = PayloadProcessor.process_payload(payload)
            if response != None:
                payload_to_send.append(response)
                tx_waiting_ack1.append(response)

def on_ack2_received(ack2_payload):
    '''Al recibir un ACK2 se envía el payload a ser procesado'''
    payload = None
    for x in rx_sending_ack1:
        if x.p_id == ack2_payload.data["ack_2"]:
            payload = x
            break
    if payload != None:
        rx_sending_ack1.remove(payload)
        rx_to_process.append(payload)
        # PAYLOAD FUE SATISFACTORIAMENTE RECIBIDO, SE ACABA EL PROCESO DE RX
    

def timeout_for_processing():
    '''Verifica si no se recibió un ACK1 por mas de 60 segundos'''
    while True:
        for payload in tx_timeout_ack2:
            if time.time() - payload.tx_last_ack1_time > 60:
                tx_timeout_ack2.remove(payload)
                if payload.action == "register":
                    global registered_by_gateway
                    registered_by_gateway = True
                # PAYLOAD FUE SATISFACTORIAMENTE ENVIADO
                # !!! SE ACABA EL PROCESO DE TX !!!

def get_payload_to_send():
    """
    Obtiene el primer payload de la cola de envío
    """
    if len(payload_to_send) > 0:
        # order payload by priority
        payload_to_send.sort(key=lambda x: x.priority, reverse=True)
        return payload_to_send.pop(0)
    else:
        return None


def connection_timeout_loop():
    '''Verifica si no se recibió un paquete por mas de 60 segundos'''
    while True:
        if time.time() - Node.last_received_time > 60 and register_in_network:
            global registered_by_gateway
            global tx_waiting_ack1
            global tx_timeout_ack2
            global rx_sending_ack1
            global rx_to_process
            global payload_to_send

            registered_by_gateway = False
            tx_waiting_ack1 = []
            tx_timeout_ack2 = []
            rx_sending_ack1 = []
            rx_to_process = []
            payload_to_send = []
            Node.reset()
