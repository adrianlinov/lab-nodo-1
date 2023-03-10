from components.sensor import Sensor
import machine

# OFF | ON
# PIN 17: LOW LEVEL ->   25%
# PIN 16: 25%       ->   50% 
# PIN  4: 50%       ->   75%
# PIN  0: 75%       ->   100%
# PIN  2: 100%      ->   OVERFLOW

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
        # TODO Revisar lectura
        sum = 0
        switch_state_list = list(map(lambda x: 1 - x.value(), self.levels))
        for i in switch_state_list:
            sum += i
        
        if sum == 0:
            return "L"
        elif sum == len(switch_state_list):
            return "H"
        else:
            return round((sum - 1) / (len(switch_state_list) - 1), 2)

    def get_last_value(self):
        return self.read()
        

        