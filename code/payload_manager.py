

import sys
from payload import Payload
import time
import _thread
import payload_processor as PayloadProcessor
import constants
import random
import components.node as Node
import math
import os


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
    # _thread.start_new_thread(connection_timeout_loop, ())
    # _thread.start_new_thread(keep_alive_loop, ())
    try:
        if os.stat("/data.txt")[6] > 0:
            print("HAY DATA PARA MANDAR")
            lines = open("/data.txt").readlines()
            for line in lines:
                payload = Payload(str(line).replace("/n", ""))
                if payload.action in ["read","read_res","set_state","set_state_res"]:
                    constants.node_id_prev = payload.sender
                    send_payload(payload)
            os.remove("/data.txt")
    except Exception as e:
        sys.print_exception(e)
        pass
    contador = 0
    while True:
        if (len(payload_to_send) + len(rx_to_process) + len(rx_sending_ack1) + len(tx_timeout_ack2) + len(tx_waiting_ack1)) == 0:
            contador = contador + 1
        else:
            contador = 0
        if contador > 10:
            break
        time.sleep(0.3)
    print("REGISTRANDO EN RED")
    
    Node.register_in_network()

def payload_received(p_received):
    """
    Inserta un payload a la lista de recibidos y para su procesamiento, se utiliza en el Main y 
    se realiza todo el proceso de ACK

    Se debe usar cada vez que se reciben datos nuevos
    """
    Node.last_received_time = time.time()
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
            send_payload(payload)
            time.sleep(random.randint(1, 3) * 2)

def payload_sending_ack1_loop():
    '''Envía los ACK1 de los payloads recibidos'''
    while True:
        if len(rx_sending_ack1) > 0:
            payload = rx_sending_ack1.pop(0)
            payload_to_send.append(payload.generate_ack1())
            rx_sending_ack1.append(payload)
            time.sleep(random.randint(1, 3) * 2)

def on_ack1_received(ack1_payload):
    '''Al recibir un ACK1 se envía el ACK2'''
    payload = None
    for x in tx_waiting_ack1:
        if x.p_id == ack1_payload.data["ack_1"]:
            payload = x
            break
    if payload != None:
        if (payload.action == "register" and not Node.registered_by_gateway) or (Node.register_in_network):
            tx_waiting_ack1.remove(payload)            
            tx_timeout_ack2.append(payload)
            payload_to_send.append(payload.generate_ack2())

    for x in tx_timeout_ack2:
        if x.p_id == ack1_payload.data["ack_1"]:
            payload = x
            break
    
    if payload != None:
        if (payload.action == "register" and not Node.registered_by_gateway) or (Node.register_in_network):
            tx_timeout_ack2.remove(payload)
            payload_to_send.append(payload.generate_ack2())
            payload.tx_last_ack1_time = time.time()
            tx_timeout_ack2.append(payload)

def _dividir_diccionario(diccionario, num_divisiones):
    resultado = []
    print("=====")
    print(diccionario)
    print("=====")

    for i in range(num_divisiones):
        division = {}
        for clave_padre, valores_hijos in diccionario.items():
            division[clave_padre] = {}
            for clave_hijo, valor_hijo in valores_hijos.items():
                print()
                if int(clave_hijo) % num_divisiones == i:
                    division[clave_padre][clave_hijo] = valor_hijo
        resultado.append(division)
    return resultado

def rx_to_process_loop():
    '''Envía los payloads a ser procesados'''
    while True:
        try:
            if len(rx_to_process) > 0:
                payload = rx_to_process.pop(0)
                response = PayloadProcessor.process_payload(payload)
                cantidad_bytes_payload = len(response.to_json_with_checksum())
                if response != None and cantidad_bytes_payload <= 255:
                    payload_to_send.append(response)
                    tx_waiting_ack1.append(response)
                if response != None and cantidad_bytes_payload > 255:
                    cantidad_de_payloads_necesarios = math.ceil((cantidad_bytes_payload - 90) / (255 - 90))
                    print("cantidad_de_payloads_necesarios: " + str(cantidad_de_payloads_necesarios))
                    divisiones_s = _dividir_diccionario(response.data["s"]["SS1"], cantidad_de_payloads_necesarios)
                    divisiones_a = _dividir_diccionario(response.data["a"], cantidad_de_payloads_necesarios)
                    for payload_index in range(0, cantidad_de_payloads_necesarios):
                        new_payload = Payload()
                        new_payload.receiver = response.receiver
                        try:
                            new_payload.data["s"] = {"SS1" : divisiones_s[payload_index]}
                        except Exception as e:
                            sys.print_exception(e)
                            continue
                        try:
                            new_payload.data["a"] = divisiones_a[payload_index]
                        except Exception as e:
                            sys.print_exception(e)
                            continue
                        new_payload.action = response.action
                        
                        
                        payload_to_send.append(new_payload)
                        tx_waiting_ack1.append(new_payload)
                    len(response.to_json_with_checksum())
        except Exception as e:
            sys.print_exception(e)
            continue

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
                    Node.registered_by_gateway = True
                # PAYLOAD FUE SATISFACTORIAMENTE ENVIADO, SE ACABA EL PROCESO DE TX

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
    
def send_payload(payload):
    payload_to_send.append(payload)
    tx_waiting_ack1.append(payload)


def connection_timeout_loop():
    '''Verifica si no se recibió un paquete por mas de 60 segundos'''
    while True:
        if time.time() - Node.last_received_time > 240 and Node.register_in_network:
            global tx_waiting_ack1
            global tx_timeout_ack2
            global rx_sending_ack1
            global rx_to_process
            global payload_to_send

            Node.registered_by_gateway = False
            tx_waiting_ack1 = []
            tx_timeout_ack2 = []
            rx_sending_ack1 = []
            rx_to_process = []
            payload_to_send = []
            Node.reset()
