from components.sensor import Sensor

class PhSensor(Sensor):
    
    def __init__(self, id):
        super().__init__(id)
        

    def read(self):
        '''Lee el valor del sensor'''
        pass