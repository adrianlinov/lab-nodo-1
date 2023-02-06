from components.sensors.oxygen_sensor import OxygenSensor
from components.sensors.ph_sensor import PhSensor
from components.actuators.relay_actuator import RelayActuator
from components.sensors.temperature_sensor import TemperatureSensor
from components.sensors.water_level_sensor import WaterLevelSensor
import security.global_security_rules as GlobalSecurityRules
from security.security_rule import SecurityRule
from security.security_rule_group import SecurityRuleGroup
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

    # Registrar sensores, actuadores y reglas de seguridad
    if Constants.NODE_NAME == "n_a":
        ae1 = RelayActuator("AE1", 15)
        ae2 = RelayActuator("AE2", 22)
        ae3 = RelayActuator("AE3", 23)
        ae4 = RelayActuator("AE4", 13)
        ae5 = RelayActuator("AE5", 12)
        ae6 = RelayActuator("AE6", 25)
        ae7 = RelayActuator("AE7", 33)
        ae8 = RelayActuator("AE8", 32)
        ae9 = RelayActuator("AE9", 0)
        ae10 = RelayActuator("AE10", 21)

        so1 = OxygenSensor("SO1", 0)
        sph1 = PhSensor("SPH1", 2)

        sensors.append(so1)
        sensors.append(sph1)

        actuators.append(ae1)
        actuators.append(ae2)
        actuators.append(ae3)
        actuators.append(ae4)
        actuators.append(ae5)
        actuators.append(ae6)
        actuators.append(ae7)
        actuators.append(ae8)
        actuators.append(ae9)
        actuators.append(ae10)

    if Constants.NODE_NAME == "n_b":
        aa1 = RelayActuator("AA1", 15)
        aa2 = RelayActuator("AA2", 2)
        aa3 = RelayActuator("AA3", 0)
        aa4 = RelayActuator("AA4", 4)
        aa5 = RelayActuator("AA5", 25)
        aa6 = RelayActuator("AA6", 33)
        aa7 = RelayActuator("AA7", 21)
        aa8 = RelayActuator("AA8", 22)
        aa9 = RelayActuator("AA9", 23)
        aag1 = RelayActuator("AAG1", 13)
        ap1 = RelayActuator("AP1", 12)

        sl1 = WaterLevelSensor("SL1", [17,16])

        sensors.append(sl1)

        actuators.append(aa1)
        actuators.append(aa2)
        actuators.append(aa3)
        actuators.append(aa4)
        actuators.append(aa5)
        actuators.append(aa6)
        actuators.append(aa7)
        actuators.append(aa8)
        actuators.append(aa9)
        actuators.append(aag1)     
        actuators.append(ap1)

        # Reglas de seguridad
        lsrg1 = SecurityRuleGroup("LSRG1", "AAG1", 0, 1, "all", True)
        lsrg1.security_rules.append(SecurityRule("LSR1", "AA1", None,"==", 0))
        lsrg1.security_rules.append(SecurityRule("LSR2", "AA2", None,"==", 0))
        lsrg1.security_rules.append(SecurityRule("LSR3", "AA3", None,"==", 0))
        lsrg1.security_rules.append(SecurityRule("LSR4", "AA4", None,"==", 0))
        lsrg1.security_rules.append(SecurityRule("LSR5", "AA5", None,"==", 0))
        lsrg1.security_rules.append(SecurityRule("LSR6", "AA6", None,"==", 0))
        lsrg1.security_rules.append(SecurityRule("LSR7", "AA7", None,"==", 0))
        lsrg1.security_rules.append(SecurityRule("LSR8", "AA8", None,"==", 0))
        lsrg1.security_rules.append(SecurityRule("LSR9", "AA9", None,"==", 0))

        lsrg1 = SecurityRuleGroup("LSRG1", "AAG1", 0, 1, "all", True)

        lsrg20 = SecurityRuleGroup("LSRG20", "AP1", 0, None, "all", True)
        lsrg20.security_rules.append(SecurityRule("LSR21", "LS1", None,"==", "L"))

        GlobalSecurityRules.add_security_group(lsrg1)
        GlobalSecurityRules.add_security_group(lsrg20)


    if Constants.NODE_NAME == "n_c":
        at1 = RelayActuator("AT1", 23)
        at2 = RelayActuator("AT2", 22)
        at3 = RelayActuator("AT3", 21)
        at4 = RelayActuator("AT4", 4)
        at5 = RelayActuator("AT5", 0)
        at6 = RelayActuator("AT6", 17)
        at7 = RelayActuator("AT7", 16)
        at8 = RelayActuator("AT8", 2)
        at9 = RelayActuator("AT9", 15)

        stw1 = TemperatureSensor("STW1", 36)
        stw2 = TemperatureSensor("STW2", 29)
        stw3 = TemperatureSensor("STW3", 34)
        stw4 = TemperatureSensor("STW4", 35)
        stw5 = TemperatureSensor("STW5", 32)
        stw6 = TemperatureSensor("STW6", 33)
        stw7 = TemperatureSensor("STW7", 25)
        stw8 = TemperatureSensor("STW8", 12)
        stw9 = TemperatureSensor("STW9", 13)

        sensors.append(stw1)
        sensors.append(stw2)
        sensors.append(stw3)
        sensors.append(stw4)
        sensors.append(stw5)
        sensors.append(stw6)
        sensors.append(stw7)
        sensors.append(stw8)
        sensors.append(stw9)

        actuators.append(at1)
        actuators.append(at2)
        actuators.append(at3)
        actuators.append(at4)
        actuators.append(at5)
        actuators.append(at6)
        actuators.append(at7)
        actuators.append(at8)
        actuators.append(at9)

        lsrg2 = SecurityRuleGroup("LSRG2", "AT1", 0, None, "all", True)
        lsrg2.security_rules.append(SecurityRule("LSR2", "STW1", None,">", 35))

        lsrg3 = SecurityRuleGroup("LSRG3", "AT2", 0, None, "all", True)
        lsrg3.security_rules.append(SecurityRule("LSR3", "STW2", None,">", 35))

        lsrg4 = SecurityRuleGroup("LSRG4", "AT3", 0, None, "all", True)
        lsrg4.security_rules.append(SecurityRule("LSR4", "STW3", None,">", 35))

        lsrg5 = SecurityRuleGroup("LSRG5", "AT4", 0, None, "all", True)
        lsrg5.security_rules.append(SecurityRule("LSR5", "STW4", None,">", 35))

        lsrg6 = SecurityRuleGroup("LSRG6", "AT5", 0, None, "all", True)
        lsrg6.security_rules.append(SecurityRule("LSR6", "STW5", None,">", 35))

        lsrg7 = SecurityRuleGroup("LSRG7", "AT6", 0, None, "all", True)
        lsrg7.security_rules.append(SecurityRule("LSR7", "STW6", None,">", 35))

        lsrg8 = SecurityRuleGroup("LSRG8", "AT7", 0, None, "all", True)
        lsrg8.security_rules.append(SecurityRule("LSR8", "STW7", None,">", 35))

        lsrg9 = SecurityRuleGroup("LSRG9", "AT8", 0, None, "all", True)
        lsrg9.security_rules.append(SecurityRule("LSR9", "STW8", None,">", 35))

        lsrg10 = SecurityRuleGroup("LSRG10", "AT9", 0, None, "all", True)
        lsrg10.security_rules.append(SecurityRule("LSR10", "STW9", None,">", 35))

        lsrg11 = SecurityRuleGroup("LSRG11", "AT1", 1, None, "all", True)
        lsrg11.security_rules.append(SecurityRule("LSR11", "STW1", None,"<", 20))

        lsrg12 = SecurityRuleGroup("LSRG12", "AT2", 1, None, "all", True)
        lsrg12.security_rules.append(SecurityRule("LSR12", "STW2", None,"<", 20))

        lsrg13 = SecurityRuleGroup("LSRG13", "AT3", 1, None, "all", True)
        lsrg13.security_rules.append(SecurityRule("LSR13", "STW3", None,"<", 20))

        lsrg14 = SecurityRuleGroup("LSRG14", "AT4", 1, None, "all", True)
        lsrg14.security_rules.append(SecurityRule("LSR14", "STW4", None,"<", 20))

        lsrg15 = SecurityRuleGroup("LSRG15", "AT5", 1, None, "all", True)
        lsrg15.security_rules.append(SecurityRule("LSR15", "STW5", None,"<", 20))

        lsrg16 = SecurityRuleGroup("LSRG16", "AT6", 1, None, "all", True)
        lsrg16.security_rules.append(SecurityRule("LSR16", "STW6", None,"<", 20))

        lsrg17 = SecurityRuleGroup("LSRG17", "AT7", 1, None, "all", True)
        lsrg17.security_rules.append(SecurityRule("LSR17", "STW7", None,"<", 20))

        lsrg18 = SecurityRuleGroup("LSRG18", "AT8", 1, None, "all", True)
        lsrg18.security_rules.append(SecurityRule("LSR18", "STW8", None,"<", 20))

        lsrg19 = SecurityRuleGroup("LSRG19", "AT9", 1, None, "all", True)
        lsrg19.security_rules.append(SecurityRule("LSR19", "STW9", None,"<", 20))



        GlobalSecurityRules.add_security_group(lsrg2)
        GlobalSecurityRules.add_security_group(lsrg3)
        GlobalSecurityRules.add_security_group(lsrg4)
        GlobalSecurityRules.add_security_group(lsrg5)
        GlobalSecurityRules.add_security_group(lsrg6)
        GlobalSecurityRules.add_security_group(lsrg7)
        GlobalSecurityRules.add_security_group(lsrg8)
        GlobalSecurityRules.add_security_group(lsrg9)
        GlobalSecurityRules.add_security_group(lsrg10)
        GlobalSecurityRules.add_security_group(lsrg11)
        GlobalSecurityRules.add_security_group(lsrg12)
        GlobalSecurityRules.add_security_group(lsrg13)
        GlobalSecurityRules.add_security_group(lsrg14)
        GlobalSecurityRules.add_security_group(lsrg15)
        GlobalSecurityRules.add_security_group(lsrg16)
        GlobalSecurityRules.add_security_group(lsrg17)
        GlobalSecurityRules.add_security_group(lsrg18)
        GlobalSecurityRules.add_security_group(lsrg19)
        

    if Constants.NODE_NAME == "n_d":
        ae11 = RelayActuator("AE11", 15)
        sl2 = WaterLevelSensor("SL2", [17,16,4,0,2])

        sensors.append(sl2)
        actuators.append(ae11)

        set_actuator_state("AE11", 1)

    

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

def get_sensor(sensor_id):
    for sensor in sensors:
        if sensor.get_id() == sensor_id:
            return sensor
    return None

def set_actuator_state(actuator_id, state):
    for i in range(len(actuators)):
        if actuators[i].get_id() == actuator_id:
            actuators[i].set_state(state)
            return True
    return None

def get_sensor_list():
    return sensors

def get_actuator_list():
    return actuators

def reset():
    Constants.reset_id()
    for actuator in actuators:
        actuator.safe_mode()
    global sensors
    global actuators
    sensors = []
    actuators = []
    GlobalSecurityRules.reset()
    # TODO Enter safe mode

