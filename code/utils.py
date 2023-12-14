import time
import machine
from payload_manager import tx_waiting_ack1


def save_restart(last_message = None):
    global tx_waiting_ack1
    try:
        # g = open('/prev_id.txt', 'w')
        # g.write(f"{constants.node_id}")
        # g.close()

        f = open('/data.txt', 'w')
        lista_de_pids = []
        for payload in tx_waiting_ack1:
            try:
                payload_str = payload.to_json_with_checksum()
                if payload_str != last_message and payload.action not in ["register", "ack_1", "ack_2"] and payload.p_id not in lista_de_pids:
                    lista_de_pids.append(payload.p_id)
                    f.write(f"{payload_str}\n")
            except:
                continue
        for payload in tx_waiting_ack1:
            try:
                payload_str = payload.to_json_with_checksum()
                if payload_str != last_message and payload.action not in ["register", "ack_1", "ack_2"] and payload.p_id not in lista_de_pids:
                    lista_de_pids.append(payload.p_id)
                    f.write(f"{payload_str}\n")
            except:
                continue
        guardar = True
        if last_message != None:
            for pid in lista_de_pids:
                if pid in last_message:
                    guardar = False
            if guardar:
                f.write(f"{last_message}\n")
        f.close()
        # print("PAYLOADS GUARDADOS")
        # print("REINICIANDO EN 3...")
        time.sleep(1)
        # print("REINICIANDO EN 2...")
        # time.sleep(1)
        # print("REINICIANDO EN 1...")
        # time.sleep(1)
        machine.reset()
    except:
        machine.reset()

import gc
import os

def df():
    s = os.statvfs('//')
    return ('{0} MB'.format((s[0]*s[3])/1048576))

def free(full=False):
    F = gc.mem_free()
    A = gc.mem_alloc()
    T = F+A
    P = '{0:.2f}%'.format(F/T*100)
    if not full: return P
    else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P))