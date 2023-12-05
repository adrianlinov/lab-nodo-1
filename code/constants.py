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
node_id = str(uuid.uuid4())[:8]

node_id_prev = None


start_time = None

def reset_id():
    global node_id
    node_id = str(uuid.uuid4())[:8]
