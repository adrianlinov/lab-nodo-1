import time
import _thread

security_rules = []
security_rules_activated = []

def start():
    if len(security_rules) > 0:
        _thread.start_new_thread(security_loop, ())


def add_security_rule(rule):
    security_rules.append(rule)


def validate_actuator_security_rules(actuator_id):
    for rule in security_rules:
        if rule.actuator_id == actuator_id:
            if rule.is_violated() == True:
                return False
    return True


def security_loop():
    while True:
        # filter with high priority
        for rule in security_rules:
            if rule.is_violated(take_action=True) == True:
                if rule not in security_rules_activated:
                    security_rules_activated.append(rule)
                    # avisar al gateway
                # Regla de seguridad violada, avisar al gateway
                pass
            else:
                if rule in security_rules_activated:
                    security_rules_activated.remove(rule)
                pass
        time.sleep(60)

