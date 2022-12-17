from components.sensors.oxygen_sensor import OxygenSensor
from components.sensors.ph_sensor import PhSensor
from components.actuators.relay_actuator import RelayActuator
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
        ea1 = RelayActuator("EA1", 4)
        
        sensors.append(ls1)
        actuators.append(ea1)


    if Constants.NODE_NAME == "n_b":
        ls2 = WaterLevelSensor("LS2", [36,39])
        pa1 = RelayActuator("PA1", 4)
        
        sensors.append(ls2)
        actuators.append(pa1)

        GlobalSecurityRules.add_security_rule(SecurityRule("GR1", pa1, ls2, "==", "L", 0, None))
        

    if Constants.NODE_NAME == "n_c":
        tws1 = TemperatureSensor("TWS1", 4)
        tas1 = TemperatureSensor("TAS1", 5)
        os1 = OxygenSensor("OS1", 2)
        ph1 = PhSensor("PS1", 0)
        oa1 = RelayActuator("OA1", 6)
        ta1 = RelayActuator("TA1", 7)
        
        sensors.append(tws1)
        sensors.append(tas1)
        sensors.append(os1)
        sensors.append(ph1)
        actuators.append(oa1)
        actuators.append(ta1)

        GlobalSecurityRules.add_security_rule(SecurityRule("GR2", ta1, tws1, ">", 30, 0, None))
        GlobalSecurityRules.add_security_rule(SecurityRule("GR3", ta1, tws1, "<", 15, 1, None))
        GlobalSecurityRules.add_security_rule(SecurityRule("GR4", oa1, os1, "<", 8, 1, None))


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
    for actuator in actuators:
        actuator.safe_mode()
    # TODO Enter safe mode

