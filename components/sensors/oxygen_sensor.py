from components.sensor import Sensor
from machine import UART
import time

class OxygenSensor(Sensor):
    
    def __init__(self, id, uart_id):
        super().__init__(id)
        # USAR UART2
        self.serial = UART(uart_id, 9600)
        
def read(self):
    '''Lee el valor del sensor'''
    self.serial.read()
    _awake()
    self.serial.write("R\r")
    time.sleep(1)
    response = self.serial.read().decode("utf-8").split("\r")[0]
    _sleep()
    return response

def _awake(self):
    try:
        self.serial.read()
        self.serial.write("K\r")
        return self.serial.read().decode("utf-8").split("\r")[0]
    except:
        self.serial.read()
        return None
def _sleep(self):
    try:
        self.serial.read()
        self.serial.write("SLEEP\r")
        return self.serial.read().decode("utf-8").split("\r")[0]
    except:
        self.serial.read()
        return None
