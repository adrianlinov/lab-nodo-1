import _thread
import sys

# import components.node as Node
from logger import logger

security_groups = []

def start():
    if len(security_groups) > 0:
        _thread.start_new_thread(security_loop, ())


def add_security_group(rule):
    security_groups.append(rule)

def reset():
    global security_groups
    security_groups = []


def validate_security_rules():
    for group in security_groups:
        if group.is_violated() == True:
            # avisar al gateway
            pass
    return True

def validate_actuator_security_rules(id_actuator):
    for group in security_groups:
        if group.id_output_actuator == id_actuator:
            if group.is_violated() == True:
                # avisar al gateway
                return False
    return True


def security_loop():
    while True:
        try:
            # if Node.registered_by_gateway == True:
            if True == True:
                for group in security_groups:
                    group.is_violated()
                    if group.violated == False:
                        if group.is_violated() == True:
                            pass
                            # avisar al gateway que se vulnero una regla de seguridad local de alta prioridad

                    if group.violated == True:
                        if group.is_violated() == False:
                            pass
                            # avisar al gateway
        except Exception as e:
            logger.logException(e)
            continue
        

