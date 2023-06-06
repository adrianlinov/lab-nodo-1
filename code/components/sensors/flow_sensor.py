from components.sensor import Sensor
import machine, time

class FlowSensor(Sensor):
    
    def __init__(self, pin_number):
        super().__init__(id, None)
        self.last_value = False
        self.pin_number = pin_number
        self.pin = machine.Pin(pin_number, machine.Pin.IN)
        machine.disable_irq()
        self.counter = 0
        self.factor = 7.5
        
    def read(self):
        '''Lee el valor del sensor'''
        try:
            self.counter = 0
            self.pin.irq(trigger=machine.Pin.IRQ_RISING, handler=self.handle_interrupt)
            time.sleep(1)
            self.pin.irq(None)
            if self.counter > 0:
                self.last_value = round(self.counter / self.factor, 1)
                if self.last_value > 3:
                    return True
                return False
            else:
                return False
        except Exception as e:
            print(e)
            return False
        
    def handle_interrupt(self, pin):
        if pin == self.pin_number:
            self.counter += 1
        

    def get_last_value(self):
        return self.last_value