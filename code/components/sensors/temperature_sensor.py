import sys
from components.sensor import Sensor
import machine, onewire, ds18x20, time

class TemperatureSensor(Sensor):
    
    def __init__(self, id, pool, pin_number, identifier, hidden=False):
        super().__init__(id, pool, hidden=hidden)
        self.sensor = ds18x20.DS18X20(onewire.OneWire(machine.Pin(pin_number)))
        self.roms = self.sensor.scan()
        self.rom = None
        for rom in self.roms:
            print(''.join('{:02x}'.format(byte) for byte in rom))
        print("======")
        for rom in self.roms:
            print(''.join('{:02x}'.format(byte) for byte in rom))
            if ''.join('{:02x}'.format(byte) for byte in rom) == identifier:
                self.rom = rom
                print("sensor identificado")
                break
        if self.rom == None:
            print("No se encontro" + str(identifier))
            machine.reset()
        self.last_value = None
        
    def read(self):
        '''Lee el valor del sensor'''
        contador = 0
        while contador < 10:
            try:
                self.sensor.convert_temp()
                time.sleep_ms(750)
                res = round(self.sensor.read_temp(self.rom), 1)
                if res <= 0:
                    contador = contador + 1
                else:
                    return res
            except Exception as e:
                sys.print_exception(e)
                contador = contador + 1
        
        return 0.0
                

    def get_last_value(self):
        return self.last_value