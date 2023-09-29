from components.actuator import Actuator
from machine import Pin
from security import global_security_rules as GlobalSecurityRules
import time

class RelayActuator(Actuator):
    
    def __init__(self, id_actuator, pool, pin):
        self.pin = Pin(pin, Pin.OUT)
        self.pin.value(1)
        super().__init__(id_actuator, pool)

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
        
    def set_state_until(self, start_callback, callback, value, newState, timeout=120):        
        previous_value = self.pin.value()
        start_time = time.time()
        if GlobalSecurityRules.validate_actuator_security_rules(self.get_id()) == True:
            if newState == True or newState == "ON" or newState == "on" or newState == "1" or newState == 1:
                self.pin.value(1)
                time.sleep(0.5)
                start_callback()
                while callback() <= value and timeout > (time.time() - start_time):
                    time.sleep(0.5)
                self.pin.value(previous_value)
            elif newState == False or newState == "OFF" or newState == "off" or newState == "0" or newState == 0:
                self.pin.value(0)
                time.sleep(0.5)
                start_callback()
                while callback() <= value and timeout > (time.time() - start_time):
                    time.sleep(0.5)
                self.pin.value(previous_value)
            else:
                raise ValueError("Invalid state")
        else:
            # informar que no se cumplen las reglas de seguridad para activar el actuador
            raise ValueError("Security rules not validated")
        
     

    def read(self):
        return self.pin.value()

    def safe_mode(self):
        '''Pone el actuador en modo seguro'''
        self.pin.value(0)
