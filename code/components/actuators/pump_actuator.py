from components.actuator import Actuator
from machine import Pin


class PumpActuator(Actuator):
    
    def __init__(self, id, pin):
        super().__init__(id)
        self.pin = Pin(pin, Pin.OUT)
        self.pin.value(1)

    def set_state(self, newState):
        if newState == True or newState == "ON" or newState == "on" or newState == "1" or newState == 1:
            return self.pin.value(1)
        elif newState == False or newState == "OFF" or newState == "off" or newState == "0" or newState == 0:
            return self.pin.value(0)
        else:
            raise ValueError("Invalid state")

    def get_state(self):
        return self.pin.value()
