from components.sensor import Sensor
import machine, onewire, ds18x20, time

class TemperatureSensor(Sensor):
    
    def __init__(self, id, pool, pin_number):
        super().__init__(id, pool)
        self.sensor = ds18x20.DS18X20(onewire.OneWire(machine.Pin(pin_number)))
        self.rom = self.sensor.scan()[0]
        self.last_value = None
        
    def read(self):
        '''Lee el valor del sensor'''
        self.sensor.convert_temp()
        time.sleep_ms(750)
        return round(self.sensor.read_temp(self.rom), 1)

    def get_last_value(self):
        return self.last_value