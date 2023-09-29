from components.sensors.flowmeter_sensor import FlowMeterSensor
from components.sensors.conductivity_sensor import ConductivitySensor
from components.sensors.sampler import Sampler
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
import sys

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

        sf1 = FlowMeterSensor("SF1", "1", 13)
        sf2 = FlowMeterSensor("SF2", "2", 13)
        sf3 = FlowMeterSensor("SF3", "3", 13)
        sf4 = FlowMeterSensor("SF4", "4", 13)
        sf5 = FlowMeterSensor("SF5", "5", 13)


        ae1 = RelayActuator("AE1", "1", 15)
        ae2 = RelayActuator("AE2", "2", 2)
        ae3 = RelayActuator("AE3", "3", 0)
        ae4 = RelayActuator("AE4", "4", 4)
        ae5 = RelayActuator("AE5", "5", 21)

        ae1.set_state(0)
        ae2.set_state(0)
        ae3.set_state(0)
        ae4.set_state(0)
        ae5.set_state(0)

        sensors.append(sf1)
        sensors.append(sf2)
        sensors.append(sf3)
        sensors.append(sf4)
        sensors.append(sf5)

        actuators.append(ae1)
        actuators.append(ae2)
        actuators.append(ae3)
        actuators.append(ae4)
        actuators.append(ae5)

        # TODO COLOCAR REGLAS DE SEGURODAD







    if Constants.NODE_NAME == "n_b":

        sf6 = FlowMeterSensor("SF6", "6", 13)
        sf7 = FlowMeterSensor("SF7", "7", 13)
        sf8 = FlowMeterSensor("SF8", "8", 13)
        sf9 = FlowMeterSensor("SF9", "9", 13)


        ae6 = RelayActuator("AE6", "6", 15)
        ae7 = RelayActuator("AE7", "7", 2)
        ae8 = RelayActuator("AE8", "8", 0)
        ae9 = RelayActuator("AE9", "9", 4)

        ae6.set_state(0)
        ae7.set_state(0)
        ae8.set_state(0)
        ae9.set_state(0)

        sensors.append(sf6)
        sensors.append(sf7)
        sensors.append(sf8)
        sensors.append(sf9)

        actuators.append(ae6)
        actuators.append(ae7)
        actuators.append(ae8)
        actuators.append(ae9)

        # TODO COLOCAR REGLAS DE SEGURODAD

        

    if Constants.NODE_NAME == "n_c":

        
        # Actuadores de Temperatura
        at1 = RelayActuator("AT1", "1", 2)
        at2 = RelayActuator("AT2", "2", 0)
        at3 = RelayActuator("AT3", "3", 4)
        at4 = RelayActuator("AT4", "4", 22)
        at5 = RelayActuator("AT5", "5", 23)
        at6 = RelayActuator("AT6", "6", 12)
        at7 = RelayActuator("AT7", "7", 25)
        at8 = RelayActuator("AT8", "8", 33)
        at9 = RelayActuator("AT9", "9", 32)

        # Sensores de Temperatura de Agua
        stw1 = TemperatureSensor("STW1", "1", 13, "282d925704053cf4")
        stw2 = TemperatureSensor("STW2", "2", 13, "28111a5704433ca0")
        stw3 = TemperatureSensor("STW3", "3", 13, "28338b5704cc3c35")
        stw4 = TemperatureSensor("STW4", "4", 13, "28ebc65704f13cf1")
        stw5 = TemperatureSensor("STW5", "5", 13, "283dd45704a13c0f")
        stw6 = TemperatureSensor("STW6", "6", 13, "286f1d76e0013cd6")
        stw7 = TemperatureSensor("STW7", "7", 13, "28a2715704103cbd")
        stw8 = TemperatureSensor("STW8", "8", 13, "28831676e0013cf2")
        stw9 = TemperatureSensor("STW9", "9", 13, "28ea6657044a3cd4")

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


        # Actuadores de Bombas para Sistema de muestreo
        ae10 = RelayActuator("AE10", "1", 33)
        ae11 = RelayActuator("AE11", "1", 15)
        ae12 = RelayActuator("AE12", "2", 2)
        ae13 = RelayActuator("AE13", "3", 0)
        ae14 = RelayActuator("AE14", "4", 4)
        ae15 = RelayActuator("AE15", "5", 21)
        ae16 = RelayActuator("AE16", "6", 22)
        ae17 = RelayActuator("AE17", "7", 23)
        ae18 = RelayActuator("AE18", "8", 25)
        ae19 = RelayActuator("AE19", "9", 32)

        ae10.set_state(0)
        ae11.set_state(0)
        ae12.set_state(0)
        ae13.set_state(0)
        ae14.set_state(0)
        ae15.set_state(0)
        ae16.set_state(0)
        ae17.set_state(0)
        ae18.set_state(0)
        ae19.set_state(0)

        sta1 = TemperatureSensor("STA1", "*", 4, "COMPLETAR")
        stw10 = TemperatureSensor("STW10", "*", 4, "COMPLETAR")
        
        # Sensores de Oxigeno y PH
        so1 = OxygenSensor("SO1", "*", 0)
        sph1 = PhSensor("SPH1", "*", 2)
        sc1 = ConductivitySensor("SC1", "*", 2)

        sensors.append(so1)
        sensors.append(sph1)
        sensors.append(sc1)
        sensors.append(stw10)
        sensors.append(sta1)

        actuators.append(ae10)
        actuators.append(ae11)
        actuators.append(ae12)
        actuators.append(ae13)
        actuators.append(ae14)
        actuators.append(ae15)
        actuators.append(ae16)
        actuators.append(ae17)
        actuators.append(ae18)
        actuators.append(ae19)

        sampler = Sampler([
            ae11, ae12, ae13, ae14, ae15, ae16, ae17, ae18, ae19
        ],
        ae10,
        so1,
        sph1,
        sc1,
        stw10
        )


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

