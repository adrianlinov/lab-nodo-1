from components.sensor import Sensor
import machine, onewire, ds18x20, time

class TemperatureSensor(Sensor):
    
    def __init__(self, id, pin_number):
        super().__init__(id)
        self.sensor = ds18x20.DS18X20(onewire.OneWire(machine.Pin(pin_number)))
        self.rom = self.ds_sensor.scan()[0]
        
    def read(self):
        '''Lee el valor del sensor'''
        self.sensor.convert_temp()
        time.sleep_ms(750)
        return round(self.ds_sensor.read_temp(self.rom), 1)