from components.actuators.relay_actuator import RelayActuator
from components.actuators.valve_actuator import ValveActuator
from components.sensors.temperature_sensor import TemperatureSensor
from components.sensors.water_level_sensor import WaterLevelSensor


sensors = []
actuators = []

def init():
    print("init executed sensor and actuators executed")
    global sensors
    global actuators
    sensors = []
    actuators = []
    sensors.append(WaterLevelSensor("LS1", [36,39,34,35,32]))
    actuators.append(ValveActuator("EA1", 4))
    
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
