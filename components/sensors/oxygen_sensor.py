from components.sensor import Sensor

class OxygenSensor(Sensor):
    
    def __init__(self, id):
        super().__init__(id)
        

    def read(self):
        '''Lee el valor del sensor'''
        pass

    