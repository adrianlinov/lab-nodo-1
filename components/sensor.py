class Sensor():
    
    def __init__(self, id):
        self.id = id

    def read(self):
        '''Lee el valor del sensor'''
        pass

    def get_id(self):
        '''Devuelve el id del sensor'''
        return self.id 
