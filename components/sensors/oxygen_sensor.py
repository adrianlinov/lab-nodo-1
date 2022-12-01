from components.sensor import Sensor
from machine import UART

class OxygenSensor(Sensor):
    
    def __init__(self, id):
        super().__init__(id)
        self.serial = UART(1, 115200)
        
    def read(self):
        '''Lee el valor del sensor'''
        _awake()
        self.serial.write("R")
        self.serial.write('\r')
        response = self.serial.read()
        _sleep()
        return response

    def _awake(self):
        self.serial.write("K")
        self.serial.write('\r')
        return self.serial.read()

    def _sleep(self):
        self.serial.write("SLEEP")
        self.serial.write('\r')
        return self.serial.read()