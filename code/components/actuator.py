class Actuator():

    def __init__(self, id):
        self.id = id

    def set_state(self, newState):
        pass

    def get_state(self):
        pass

    def get_id(self):
        '''Devuelve el id del actuador'''
        return self.id 
