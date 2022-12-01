from components.sensor import Sensor
import machine

# OFF | ON
# PIN 17: LOW LEVEL ->   25%
# PIN 16: 25%       ->   50% 
# PIN  4: 50%       ->   75%
# PIN  0: 75%       ->   100%
# PIN  2: 100%      ->   OVERFLOW

class WaterLevelSensor(Sensor):
    
    def __init__(self, id, pin_numbers_list):
        super().__init__(id)
        for pin_number in pin_numbers_list:
            self.levels.append(machine.Pin(pin_number, machine.Pin.IN, machine.Pin.PULL_UP))

    def read(self):
        '''Lee el valor del sensor
        125 = OVERFLOW
        100 = 100%
        75 = 75%
        50 = 50%
        25 = 25%
        0 = LOW LEVEL
        '''
        sum = 0
        switch_state_list = list(map(lambda x: x.value(), self.levels))
        
        for switch_state in switch_state_list:
            sum += int(switch_state)
        
        return round(sum * (100 / len(switch_state_list)), 1)

        