import time
import machine
from payload_manager import tx_waiting_ack1


def save_restart(last_message = None):
    global tx_waiting_ack1
    f = open('/data.txt', 'w')
    if last_message != None:
        f.write(f"{last_message}/n")
    for payload in tx_waiting_ack1:
        payload_str = payload.to_json_with_checksum()
        if payload_str != last_message:
            f.write(f"{payload_str}/n")
    f.close()
    print("PAYLOADS GUARDADOS")
    print("REINICIANDO EN 3...")
    time.sleep(1)
    print("REINICIANDO EN 2...")
    time.sleep(1)
    print("REINICIANDO EN 1...")
    time.sleep(1)
    machine.reset()