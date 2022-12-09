from components.actuators.relay_actuator import RelayActuator
from components.actuators.valve_actuator import ValveActuator
from components.sensors.temperature_sensor import TemperatureSensor
from components.sensors.water_level_sensor import WaterLevelSensor
import security.global_security_rules as GlobalSecurityRules
from security.security_rule import SecurityRule
import constants as Constants
import time

sensors = []
actuators = []
last_received_time = time.time()

def init():
    print("init executed sensor and actuators executed")
    global sensors
    global actuators

    sensors = []
    actuators = []

    if Constants.NODE_NAME == "n_a":
        ls1 = WaterLevelSensor("LS1", [36,39,34,35,32])
        sensors.append(ls1)

        ea1 = RelayActuator("EA1", 4)
        actuators.append(ea1)

        # Si el nivel de agua es LOW, entonces el electrovalvula debe estar cerrada
        GlobalSecurityRules.add_security_rule(SecurityRule("GR1", ea1, ls1, "==", "L", 0, None))
        # Si el nivel de agua es HIGH, entonces el electrovalvula debe estar cerrada
        GlobalSecurityRules.add_security_rule(SecurityRule("GR2", ea1, ls1, "==", "H", 0, None))

    GlobalSecurityRules.start()
    
    
def get_sensor(sensor_id):
    for sensor in sensors:
        if sensor.get_id() == sensor_id:
            return sensor
    return None

def get_actuator(actuator_id):
    for actuator in actuators:
        if actuator.get_id() == actuator_id:
            return actuator
    return None

def get_sensor_list():
    return sensors

def get_actuator_list():
    return actuators

def reset():
    Constants.reset_id()
    # TODO Enter safe mode
    
