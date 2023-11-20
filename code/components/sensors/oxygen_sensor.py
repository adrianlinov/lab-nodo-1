from components.sensor import Sensor
from machine import UART
import time

class OxygenSensor(Sensor):
    
    def __init__(self, id, pool, uart_id=1, tx=None, rx=None, hidden=True):
        super().__init__(id, pool, hidden=hidden)
        # USAR UART2
        self.serial = UART(uart_id, baudrate=9600, tx=tx, rx=rx)
        self.last_value = None
        
    def read(self):
        '''Lee el valor del sensor'''
        self.serial.read()
        self._awake()
        self.serial.write("R\r")
        time.sleep(1)
        response = self.serial.read().decode("utf-8").split("\r")[0]
        self.last_value = float(response)
        self._sleep()
        return float(response)

    def get_last_value(self):
        return self.last_value

    def _awake(self):
        try:
            self.serial.read()
            self.serial.write("K\r")
            time.sleep(1)
            return self.serial.read().decode("utf-8").split("\r")[0]
        except:
            self.serial.read()
            return None
            
    def _sleep(self):
        try:
            self.serial.read()
            self.serial.write("SLEEP\r")
            time.sleep(1)
            return self.serial.read().decode("utf-8").split("\r")[0]
        except:
            self.serial.read()
            return None
