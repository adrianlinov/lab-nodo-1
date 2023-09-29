import time

from components.sensor import Sensor


class Sampler(Sensor):

    def __init__(self, tank_valves, release_valve, oxygen_sensor, ph_sensor, conductivity_sensor, temperature_sensor):
        self.tank_valves = tank_valves
        self.oxygen_sensor = oxygen_sensor
        self.ph_sensor = ph_sensor
        self.conductivity_sensor = conductivity_sensor
        self.temperature_sensor = temperature_sensor
        self.release_valve = release_valve

    def read_from_tank(self, tank_number):
        '''Lee el valor de un tanque'''
        try:
            self.tank_valves[tank_number + 1].set_state(True)
            time.sleep(1) # TODO Establecer tiempo de llenado
            self.tank_valves[tank_number + 1].set_state(False)
            o2 = self.oxygen_sensor.read()
            ph = self.ph_sensor.read()
            cond = self.conductivity_sensor.read()
            temp = self.temperature_sensor.read()
            self.release_valve.set_state(True)
            time.sleep(1) # TODO Establecer tiempo de desfogue
            self.release_valve.set_state(False)
            return str(o2)+ "-" + str(ph) + "-" + str(cond) + "-" + str(temp)
        except Exception as e:
            print(e)
            return False
    def read(self):
        '''Lee el valor del sensor'''
        return self.read_all()
        
    def read_all(self):
        '''Lee el valor de un tanque'''
        results = []
        for tank_number in range(9):
            try:
                self.tank_valves[tank_number + 1].set_state(True)
                time.sleep(1)
                self.tank_valves[tank_number + 1].set_state(False)
                time.sleep(1)
                o2 = self.oxygen_sensor.read()
                ph = self.ph_sensor.read()
                cond = self.conductivity_sensor.read()
                temp = self.temperature_sensor.read()
                self.release_valve.set_state(True)
                time.sleep(1)
                self.release_valve.set_state(False)
                results.append(str(o2)+ "-" + str(ph) + "-" + str(cond) + "-" + str(temp))
            except Exception as e:
                print(e)
                return False
        return results
