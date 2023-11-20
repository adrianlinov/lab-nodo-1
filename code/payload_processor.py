import time
import _thread
import payload_manager as PayloadManager
from payload import Payload
import components.node as Node
import machine

payload_p_id_processing_no_repeate = []

def process_payload(payload):
    """
    Ejecuta el procesamiento de un payload recibido
    """
    if len(payload_p_id_processing_no_repeate) > 10:
        payload_p_id_processing_no_repeate.remove(payload_p_id_processing_no_repeate[0])
    if payload.p_id not in payload_p_id_processing_no_repeate:
        payload_p_id_processing_no_repeate.append(payload.p_id)
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
    response_payload.data["s"] = {}
    response_payload.data["a"] = {}

    if "s" in payload.data.keys():
        if payload.data["s"] != None and len(payload.data["s"]) > 0:
            for sensor_id in payload.data["s"]:
                sensor = Node.get_sensor(sensor_id)
                if sensor != None:
                    response_payload.data["s"][sensor_id] = sensor.read()

    if "a" in payload.data.keys():
        if payload.data["a"] != None and len(payload.data["a"]) > 0:
            for actuator_id in payload.data["a"]:
                actuator = Node.get_actuator(actuator_id)
                if actuator != None:
                    response_payload.data["a"][actuator_id] = actuator.read()
    return response_payload

def _process_ping(payload):
    response_payload = Payload()
    response_payload.action = "ping_res"
    response_payload.receiver = payload.sender
    return response_payload

def _process_read_all(payload):
    response_payload = Payload()
    response_payload.action = "read_res"
    response_payload.receiver = payload.sender
    response_payload.data["s"] = {}
    response_payload.data["a"] = {}
    Node.get_sensor_list()

    for sensor in Node.get_sensor_list():
        response_payload.data["s"][sensor.get_id()] = sensor.read()
    
    for actuator in Node.get_actuator_list():
        response_payload.data["a"][actuator.get_id()] = actuator.read()

    return response_payload

def _process_set_state(payload):
    response_payload = Payload()
    response_payload.action = "set_state_res"
    response_payload.receiver = payload.sender
    response_payload.data["a"] = {}
    if "a" in payload.data.keys(): 
        if payload.data["a"] != None and len(payload.data["a"]) > 0:
            for actuator_id in payload.data["a"].keys():
                # if actuator_id in ["AE2"]:
                #     response_payload.data["a"][actuator_id] = Node.set_actuator_state(actuator_id, payload.data["a"][actuator_id], validate_rule=False)
                # else:
                #     response_payload.data["a"][actuator_id] = 1.123
                response_payload.data["a"][actuator_id] = Node.set_actuator_state(actuator_id, payload.data["a"][actuator_id], validate_rule=False)
    # machine.Pin(14).value(0)
    # time.sleep(1)
    # machine.Pin(14).value(1)
    return response_payload

