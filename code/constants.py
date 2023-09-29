# !!! ESTE ARCHIVO CAMBIA CON CADA NODO !!!
import uuid
import ubinascii
import machine

def _get_node_name():
    if ubinascii.hexlify(machine.unique_id()).decode('utf-8') == "0cb815c49fa0":
        return "n_a"
    elif ubinascii.hexlify(machine.unique_id()).decode('utf-8') == "0cb815c4983c":
        return "n_c"
    return "n_c"
    

NODE_NAME = _get_node_name()
NODE_ID = str(uuid.uuid4())[:8]

def reset_id():
    global NODE_ID
    NODE_ID = str(uuid.uuid4())[:8]
