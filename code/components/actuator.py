from components.peripheral import Peripheral


class Actuator(Peripheral):

    def __init__(self, id_actuator, pool):
        self.id = id_actuator
        super().__init__(pool)


    def set_state(self, newState):
        pass

    def read(self):
        pass

    def get_id(self):
        '''Devuelve el id del actuador'''
        return self.id 

    def safe_mode(self):
        '''Pone el actuador en modo seguro'''
        pass
