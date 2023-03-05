from components.peripheral import Peripheral


class Sensor(Peripheral):
    
    def __init__(self, id, pool):
        super().__init__(pool)
        self.id = id

    def read(self):
        '''Lee el valor del sensor'''
        pass

    def get_id(self):
        '''Devuelve el id del sensor'''
        return self.id 
