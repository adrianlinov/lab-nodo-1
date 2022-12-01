import time
import _thread
import payload_manager_v2 as PayloadManager
from payload import Payload
from components.node import node as Node



def start():
    # _thread.start_new_thread(local_security_loop, ())
    _thread.start_new_thread(local_processing_loop, ())


def process_payload(payload):
    """
    Ejecuta el procesamiento de un payload recibido
    """
    if payload.action == "read":
        return _process_read(payload)

    if payload.action == "read_all":
        return _process_read_all(payload)

    if payload.action == "set_state":
        return _process_set_state(payload)
            
    if payload.action == "ping":
        return _process_ping(payload)
        # Enviar los datos solicitados

def _process_read(payload):
    response_payload = Payload()
    response_payload.action = "read_res"
    response_payload.receiver = payload.sender

    if "s" in payload.data.keys():
        if payload.data["s"] != None and len(payload.data["s"]) > 0:
                for sensor_id in payload.data["s"]:
                    response_payload.data[sensor_id] = "19"
                    # Identificar el sensor
                    # Leer el valor del sensor
                    # Colocar el dato del sensor en un payload
                    # Enviar el payload al Gateway
                    # pass
    if "a" in payload.data.keys():
        if payload.data["a"] != None and len(payload.data["a"]) > 0:
            for actuator_id in payload.data["a"]:
                response_payload.data[actuator_id] = "ON"
                # Identificar el sensor
                # Leer el valor del sensor
                # Colocar el dato del sensor en un payload
                # Enviar el payload al Gateway
                # pass
    return response_payload

def _process_ping(payload):
    response_payload = Payload()
    response_payload.action = "ping_res"
    response_payload.receiver = payload.sender
    return response_payload

def _process_read_all(payload):
    response_payload = Payload()
    response_payload.action = "read_all_res"
    response_payload.receiver = payload.sender
    # LA DATA TIENE QUE SER CONSULTADA A LOS SENSORES
    response_payload.data["s"] = {"sensor_1": "19", "sensor_2": "19"}
    response_payload.data["a"] = {"actuator_1": "ON", "actuator_2": "OFF"}
    return response_payload

def _process_set_state(payload):
    response_payload = Payload()
    response_payload.action = "set_state_res"
    response_payload.receiver = payload.sender
    # LA DATA TIENE QUE SER CONSULTADA A LOS SENSORES
    response_payload.data["a"] = {"actuator_1": "ON", "actuator_2": "OFF"}
    return response_payload

# def local_security_loop():
#     '''
#     Loop de seguridad local, nada puede activarse si no se cumple con las condiciones de seguridad local
#     '''
#     while True:
#         if PayloadManager.last_received_time + 30 < time.time():
#             # Si no se ha recibido un payload en 30 segundos, se apagan todos los componentes
#             pass
        
        # Leer estado de componentes de prioridad alta (Sensores de Nivel, Electrovalvulas, etc) [Diferente para cada nodo]

        # Aplicar medidas de seguridad en caso de ser necesario

        # Notificar al Gateway de los cambios de estado

def local_processing_loop():
    while True:
        pass
        # Leer estado de componentes

        # Aplicar medidas de seguridad en caso de ser necesario

        # Notificar al Gateway de los cambios de estado