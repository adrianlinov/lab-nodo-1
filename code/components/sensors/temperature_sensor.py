import sys
from components.sensor import Sensor
import machine, onewire_new, time
import ds18x20_new as ds18x20_new
from logger import logger

class TemperatureSensor(Sensor):
    
    def __init__(self, id, pool, pin_number, identifier, hidden=False):
        super().__init__(id, pool, hidden=hidden)
        self.sensor = ds18x20_new.DS18X20(onewire_new.OneWire(machine.Pin(pin_number)))
        self.roms = self.sensor.scan()
        self.rom = None
        for rom in self.roms:
            if ''.join('{:02x}'.format(byte) for byte in rom) == identifier:
                self.rom = rom
                print(f"sensor identificado: {identifier}")
                break
        if self.rom == None:
            logger.log("No se encontro el sensor: " + str(identifier))
            machine.reset()
        self.last_value = None
        
    def read(self):
        '''Lee el valor del sensor'''
        contador = 0
        # IMPLEMENTAR https://github.com/robert-hh/Onewire_DS18X20/tree/master
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
                logger.logException(e)
                contador = contador + 1
                continue
        return 0.0
                

    def get_last_value(self):
        return self.last_value