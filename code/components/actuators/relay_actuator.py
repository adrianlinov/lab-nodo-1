from components.actuator import Actuator
from machine import Pin
from security import global_security_rules as GlobalSecurityRules


class RelayActuator(Actuator):
    
    def __init__(self, id, pool, pin):
        super().__init__(id, pool)
        self.pin = Pin(pin, Pin.OUT)
        self.pin.value(1)

    def set_state(self, newState):
        if GlobalSecurityRules.validate_actuator_security_rules(self.get_id()) == True:
            if newState == True or newState == "ON" or newState == "on" or newState == "1" or newState == 1:
                return self.pin.value(1)
            elif newState == False or newState == "OFF" or newState == "off" or newState == "0" or newState == 0:
                return self.pin.value(0)
            else:
                raise ValueError("Invalid state")
        else:
            # informar que no se cumplen las reglas de seguridad para activar el actuador
            raise ValueError("Security rules not validated")

    def get_state(self):
        return self.pin.value()

    def safe_mode(self):
        '''Pone el actuador en modo seguro'''
        self.pin.value(0)
