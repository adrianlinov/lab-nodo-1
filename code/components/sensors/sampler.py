import sys
import time

from components.sensor import Sensor
from logger import logger


class Sampler(Sensor):

    def __init__(self, id, tank_valves, release_valve, oxygen_sensor, ph_sensor, conductivity_sensor, temperature_sensor=None, hidden=False):
        super().__init__(id, None, hidden=hidden)
        self.tank_valves = tank_valves
        self.oxygen_sensor = oxygen_sensor
        self.ph_sensor = ph_sensor
        self.conductivity_sensor = conductivity_sensor
        self.temperature_sensor = temperature_sensor
        self.release_valve = release_valve

    def read_from_tank(self, tank_number):
        '''Lee el valor de un tanque'''
        try:
            index = tank_number-1
            self.tank_valves[index].set_state(True)
            self.release_valve.set_state(True)
            time.sleep(30)
            self.release_valve.set_state(False)
            time.sleep(100)
            o2 = self.oxygen_sensor.read()
            ph = self.ph_sensor.read()
            cond = self.conductivity_sensor.read()
            temp = self.temperature_sensor.read()
            self.tank_valves[index].set_state(False)
            self.release_valve.set_state(False)
            time.sleep(40)
            return str(o2)+ "-" + str(ph) + "-" + str(cond) + "-" + str(temp)
        except Exception as e:
            logger.logException(e)
            return False
    def read(self):
        '''Lee el valor del sensor'''
        return self.read_all()
        
    def read_all(self):
        '''Lee el valor de un tanque'''
        results = {
            "SO1" : {},
            "SPH1" : {},
            "SC1" : {},
            "STW10" : {},
        }
        for tank_number in range(1,10):
            temp = []
            o2 = []
            ph = []
            cond = []
            const = 10
            # const = 1
            index = tank_number-1
            # Desfoga el agua del sistema
            self.release_valve.set_state(True)
            time.sleep(4 * const)
            # Limpia el agua de la manguera
            self.tank_valves[index].set_state(True)
            self.release_valve.set_state(True)
            time.sleep(10 * const)
            # Llena el sistema de agua 1 vez
            self.release_valve.set_state(False)
            time.sleep(10 * const)
            self.tank_valves[index].set_state(False)
            self.release_valve.set_state(True)
            time.sleep(4 * const)
            # Llena el sistema de agua 2 vez
            self.tank_valves[index].set_state(True)
            self.release_valve.set_state(False)
            time.sleep(18 * const)
            for c in range(0,10):
                try:
                    temp.append(self.temperature_sensor.read())
                except Exception as e:
                    logger.logException(e) 
                try:
                    o2.append(self.oxygen_sensor.read())
                except Exception as e:
                    logger.logException(e) 
                try:
                    ph.append(self.ph_sensor.read(temperatureCompensation=temp))
                except Exception as e:
                    logger.logException(e) 
                try:
                    cond.append(self.conductivity_sensor.read(temperatureCompensation=temp))
                except Exception as e:
                    logger.logException(e) 
            time.sleep(1)
            if len(temp) == 0:
                temp = [0]
            if len(o2) == 0:
                o2 = [0]
            if len(ph) == 0:
                ph = [0]
            if len(cond) == 0:
                cond = [0]
            results["SO1"][f"{tank_number}"] = sum(o2)/len(o2)
            results["SPH1"][f"{tank_number}"] = sum(ph)/len(ph)
            results["SC1"][f"{tank_number}"] = sum(cond)/len(cond)
            results["STW10"][f"{tank_number}"] = sum(temp)/len(temp)
            self.tank_valves[index].set_state(False)
        return results
