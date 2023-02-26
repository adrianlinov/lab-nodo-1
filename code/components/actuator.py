from code.components.peripheral import Peripheral


class Actuator(Peripheral):

    def __init__(self, id, pool):
        super().__init__(pool)
        self.id = id


    def set_state(self, newState):
        pass

    def get_state(self):
        pass

    def get_id(self):
        '''Devuelve el id del actuador'''
        return self.id 

    def safe_mode(self):
        '''Pone el actuador en modo seguro'''
        pass
