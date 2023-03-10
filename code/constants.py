# !!! ESTE ARCHIVO CAMBIA CON CADA NODO !!!
import uuid

NODE_NAME = "n_c"
NODE_ID = str(uuid.uuid4())[:8]

def reset_id():
    global NODE_ID
    NODE_ID = str(uuid.uuid4())[:8]
