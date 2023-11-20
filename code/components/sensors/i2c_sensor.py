from components.sensor import Sensor
import machine
import time

class I2CSensor(Sensor):
    
    def __init__(self, id, pool, i2c, hidden=True, address=None):
        super().__init__(id, pool, hidden=hidden)
        # USAR UART2
        self.i2c = i2c
        self.device_address = address
        self.last_value = None
            
    def read(self):
        '''Lee el valor del sensor'''
        self.i2c.writeto(self.device_address, b"R")
        time.sleep(1)
        response = self.i2c.readfrom(self.device_address, 7)
        response = response.decode("utf-8")[1:5]
        self.last_value = response
        return float(response)
