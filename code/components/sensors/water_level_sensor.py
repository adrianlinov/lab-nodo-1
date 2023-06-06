from components.sensor import Sensor
import machine


class WaterLevelSensor(Sensor):
    
    def __init__(self, id, pool, pin_numbers_list):
        super().__init__(id, pool)
        self.levels = []
        for pin_number in pin_numbers_list:
            self.levels.append(machine.Pin(pin_number, machine.Pin.IN, machine.Pin.PULL_UP))

    def read(self):
        '''
        Lee el valor del sensor
        '''
        sum = 0
        switch_state_list = list(map(lambda x: 1 - x.value(), self.levels))
        for i in switch_state_list:
            sum += i
        
        if sum == 0:
            return 0
        else:
            return round((sum) / len(switch_state_list), 2)

    def get_last_value(self):
        return self.read()
        

        