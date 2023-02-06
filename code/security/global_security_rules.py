import _thread

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


def security_loop():
    while security_groups > 0:
        # filter with high priority
        for group in security_groups:
            if group.violated == False:
                if group.is_violated() == True:
                    pass
                    # avisar al gateway que se vulnero una regla de seguridad local de alta prioridad

            if group.violated == True:
                if group.is_violated() == False:
                    pass
                    # avisar al gateway

