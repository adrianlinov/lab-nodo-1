from components.peripheral import Peripheral


class Actuator(Peripheral):

    def __init__(self, id, pool, hidden):
        self.id = id
        self.hidden = hidden
        super().__init__(pool)


    def set_state(self, newState, validate_rule):
        pass

    def read(self):
        pass

    def get_id(self):
        '''Devuelve el id del actuador'''
        return self.id 

    def safe_mode(self):
        '''Pone el actuador en modo seguro'''
        pass
