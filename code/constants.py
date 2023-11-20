# !!! ESTE ARCHIVO CAMBIA CON CADA NODO !!!
import uuid
import ubinascii
import machine

def _get_node_name():
    if ubinascii.hexlify(machine.unique_id()).decode('utf-8') == "0cb815c43bc8":
        return "n_a"
    elif ubinascii.hexlify(machine.unique_id()).decode('utf-8') == "0cb815c4983c":
        return "n_b"
    elif ubinascii.hexlify(machine.unique_id()).decode('utf-8') == "ccdba71cf5dc":
        return "n_c"
    return "n_d"
    

NODE_NAME = _get_node_name()
NODE_ID = str(uuid.uuid4())[:8]

NODE_ID_PREV = None


start_time = None

def reset_id():
    global NODE_ID
    NODE_ID = str(uuid.uuid4())[:8]
