from payload import Payload
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
import payload_manager as PayloadManager

sensors = []
actuators = []
last_received_time = time.time()

registered_by_gateway = False

def init():
    print("init executed sensor and actuators executed")
    global sensors
    global actuators

    sensors = []
    actuators = []

    # Registrar sensores, actuadores y reglas de seguridad
    if Constants.NODE_NAME == "n_a":
        ae1 = RelayActuator("AE1", "1", 15)
        ae2 = RelayActuator("AE2", "2", 22)
        ae3 = RelayActuator("AE3", "3", 23)
        ae4 = RelayActuator("AE4", "4", 13)
        ae5 = RelayActuator("AE5", "5", 12)
        ae6 = RelayActuator("AE6", "6", 25)
        ae7 = RelayActuator("AE7", "7", 33)
        ae8 = RelayActuator("AE8", "8", 32)
        ae9 = RelayActuator("AE9", "9", 0)
        ae10 = RelayActuator("AE10", None, 21)

        ae1.set_state(0)
        ae2.set_state(0)
        ae3.set_state(0)
        ae4.set_state(0)
        ae5.set_state(0)
        ae6.set_state(0)
        ae7.set_state(0)
        ae8.set_state(0)
        ae9.set_state(0)
        ae10.set_state(0)
        
        so1 = OxygenSensor("SO1", "*", 0)
        sph1 = PhSensor("SPH1", "*", 2)

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
        aa1 = RelayActuator("AA1", "1", 15)
        aa2 = RelayActuator("AA2", "2", 2)
        aa3 = RelayActuator("AA3", "3", 0)
        aa4 = RelayActuator("AA4", "4", 4)
        aa5 = RelayActuator("AA5", "5", 25)
        aa6 = RelayActuator("AA6", "6", 33)
        aa7 = RelayActuator("AA7", "7", 21)
        aa8 = RelayActuator("AA8", "8", 22)
        aa9 = RelayActuator("AA9", "9", 23)
        aag1 = RelayActuator("AAG1", None, 13)
        ap1 = RelayActuator("AP1", None, 12)

        sl1 = WaterLevelSensor("SL1", None, [17,16])


        aa1.set_state(1)
        aa2.set_state(1)
        aa3.set_state(1)
        aa4.set_state(1)
        aa5.set_state(1)
        aa6.set_state(1)
        aa7.set_state(1)
        aa8.set_state(1)
        aa9.set_state(1)
        aag1.set_state(1)
        ap1.set_state(0)

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
        
        lg19 = SecurityRuleGroup("LG19", "AAG1", 1, None, "any", True)
        lg20 = SecurityRuleGroup("LG20", "AAG1", 0, None, "all", True)
        lg21 = SecurityRuleGroup("LG21", "AP1", 0, None, "all", True)
        
        
        
        lg19.security_rules.append(SecurityRule("L19", "AA1", None,"==", 1))
        lg19.security_rules.append(SecurityRule("L20", "AA2", None,"==", 1))
        lg19.security_rules.append(SecurityRule("L21", "AA3", None,"==", 1))
        lg19.security_rules.append(SecurityRule("L22", "AA4", None,"==", 1))
        lg19.security_rules.append(SecurityRule("L23", "AA5", None,"==", 1))
        lg19.security_rules.append(SecurityRule("L24", "AA6", None,"==", 1))
        lg19.security_rules.append(SecurityRule("L25", "AA7", None,"==", 1))
        lg19.security_rules.append(SecurityRule("L26", "AA8", None,"==", 1))
        lg19.security_rules.append(SecurityRule("L27", "AA9", None,"==", 1))
        lg20.security_rules.append(SecurityRule("L28", "AA1", None,"==", 0))
        lg20.security_rules.append(SecurityRule("L29", "AA2", None,"==", 0))
        lg20.security_rules.append(SecurityRule("L30", "AA3", None,"==", 0))
        lg20.security_rules.append(SecurityRule("L31", "AA4", None,"==", 0))
        lg20.security_rules.append(SecurityRule("L32", "AA5", None,"==", 0))
        lg20.security_rules.append(SecurityRule("L33", "AA6", None,"==", 0))
        lg20.security_rules.append(SecurityRule("L34", "AA7", None,"==", 0))
        lg20.security_rules.append(SecurityRule("L35", "AA8", None,"==", 0))
        lg20.security_rules.append(SecurityRule("L36", "AA9", None,"==", 0))
        lg21.security_rules.append(SecurityRule("L37", None, "SL1","==", 0))

        
        GlobalSecurityRules.add_security_group(lg19)
        GlobalSecurityRules.add_security_group(lg20)
        GlobalSecurityRules.add_security_group(lg21)



    if Constants.NODE_NAME == "n_c":
        at1 = RelayActuator("AT1", "1", 23)
        at2 = RelayActuator("AT2", "2", 22)
        at3 = RelayActuator("AT3", "3", 21)
        at4 = RelayActuator("AT4", "4", 4)
        at5 = RelayActuator("AT5", "5", 0)
        at6 = RelayActuator("AT6", "6", 17)
        at7 = RelayActuator("AT7", "7", 16)
        at8 = RelayActuator("AT8", "8", 2)
        at9 = RelayActuator("AT9", "9", 15)

        stw1 = TemperatureSensor("STW1", "1", 36)
        stw2 = TemperatureSensor("STW2", "2", 29)
        stw3 = TemperatureSensor("STW3", "3", 34)
        stw4 = TemperatureSensor("STW4", "4", 35)
        stw5 = TemperatureSensor("STW5", "5", 32)
        stw6 = TemperatureSensor("STW6", "6", 33)
        stw7 = TemperatureSensor("STW7", "7", 25)
        stw8 = TemperatureSensor("STW8", "8", 12)
        stw9 = TemperatureSensor("STW9", "9", 13)

        at1.set_state(0)
        at2.set_state(0)
        at3.set_state(0)
        at4.set_state(0)
        at5.set_state(0)
        at6.set_state(0)
        at7.set_state(0)
        at8.set_state(0)
        at9.set_state(0)
        
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

        lg01 = SecurityRuleGroup("LG01", "AT1", 1, None, "all", True)
        lg02 = SecurityRuleGroup("LG02", "AT1", 0, None, "all", True)
        lg03 = SecurityRuleGroup("LG03", "AT2", 1, None, "all", True)
        lg04 = SecurityRuleGroup("LG04", "AT2", 0, None, "all", True)
        lg05 = SecurityRuleGroup("LG05", "AT3", 1, None, "all", True)
        lg06 = SecurityRuleGroup("LG06", "AT3", 0, None, "all", True)
        lg07 = SecurityRuleGroup("LG07", "AT4", 1, None, "all", True)
        lg08 = SecurityRuleGroup("LG08", "AT4", 0, None, "all", True)
        lg09 = SecurityRuleGroup("LG09", "AT5", 1, None, "all", True)
        lg10 = SecurityRuleGroup("LG10", "AT5", 0, None, "all", True)
        lg11 = SecurityRuleGroup("LG11", "AT6", 1, None, "all", True)
        lg12 = SecurityRuleGroup("LG12", "AT6", 0, None, "all", True)
        lg13 = SecurityRuleGroup("LG13", "AT7", 1, None, "all", True)
        lg14 = SecurityRuleGroup("LG14", "AT7", 0, None, "all", True)
        lg15 = SecurityRuleGroup("LG15", "AT8", 1, None, "all", True)
        lg16 = SecurityRuleGroup("LG16", "AT8", 0, None, "all", True)
        lg17 = SecurityRuleGroup("LG17", "AT9", 1, None, "all", True)
        lg18 = SecurityRuleGroup("LG18", "AT9", 0, None, "all", True)

        lg01.security_rules.append(SecurityRule("L01", "STW1", None,"<", 21))
        lg02.security_rules.append(SecurityRule("L02", "STW1", None,">", 35))
        lg03.security_rules.append(SecurityRule("L03", "STW2", None,"<", 21))
        lg04.security_rules.append(SecurityRule("L04", "STW2", None,">", 35))
        lg05.security_rules.append(SecurityRule("L05", "STW3", None,"<", 21))
        lg06.security_rules.append(SecurityRule("L06", "STW3", None,">", 35))
        lg07.security_rules.append(SecurityRule("L07", "STW4", None,"<", 21))
        lg08.security_rules.append(SecurityRule("L08", "STW4", None,">", 35))
        lg09.security_rules.append(SecurityRule("L09", "STW5", None,"<", 21))
        lg10.security_rules.append(SecurityRule("L10", "STW5", None,">", 35))
        lg11.security_rules.append(SecurityRule("L11", "STW6", None,"<", 21))
        lg12.security_rules.append(SecurityRule("L12", "STW6", None,">", 35))
        lg13.security_rules.append(SecurityRule("L13", "STW7", None,"<", 21))
        lg14.security_rules.append(SecurityRule("L14", "STW7", None,">", 35))
        lg15.security_rules.append(SecurityRule("L15", "STW8", None,"<", 21))
        lg16.security_rules.append(SecurityRule("L16", "STW8", None,">", 35))
        lg17.security_rules.append(SecurityRule("L17", "STW9", None,"<", 21))
        lg18.security_rules.append(SecurityRule("L18", "STW9", None,">", 35))


        GlobalSecurityRules.add_security_group(lg01)
        GlobalSecurityRules.add_security_group(lg02)
        GlobalSecurityRules.add_security_group(lg03)
        GlobalSecurityRules.add_security_group(lg04)
        GlobalSecurityRules.add_security_group(lg05)
        GlobalSecurityRules.add_security_group(lg06)
        GlobalSecurityRules.add_security_group(lg07)
        GlobalSecurityRules.add_security_group(lg08)
        GlobalSecurityRules.add_security_group(lg09)
        GlobalSecurityRules.add_security_group(lg10)
        GlobalSecurityRules.add_security_group(lg11)
        GlobalSecurityRules.add_security_group(lg12)
        GlobalSecurityRules.add_security_group(lg13)
        GlobalSecurityRules.add_security_group(lg14)
        GlobalSecurityRules.add_security_group(lg15)
        GlobalSecurityRules.add_security_group(lg16)
        GlobalSecurityRules.add_security_group(lg17)
        GlobalSecurityRules.add_security_group(lg18)
        
        

    if Constants.NODE_NAME == "n_d":
        ae11 = RelayActuator("AE11", None, 15)
        sl2 = WaterLevelSensor("SL2", None, [17,16,4,0,2])

        ae11.set_state(1)

        sensors.append(sl2)
        actuators.append(ae11)


    GlobalSecurityRules.start()
    
def register_in_network():
    global registered_by_gateway
    registered_by_gateway = False
    payload = Payload()
    payload.receiver = "gw"
    payload.action = "register"
    payload.data["n_n"] = Constants.NODE_NAME
    payload.data["n_id"] = Constants.NODE_ID
    init()

    payload.data["s"] = list(map(lambda x: x.get_id(), get_sensor_list()))
    payload.data["a"] = list(map(lambda x: x.get_id(), get_actuator_list()))
    
    PayloadManager.send_payload(payload)

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
    sensors.clear()
    actuators.clear()
    GlobalSecurityRules.reset()
    register_in_network()
    
    # TODO Enter safe mode

