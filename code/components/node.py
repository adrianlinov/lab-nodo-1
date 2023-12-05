from components.sensors.i2c_sensor import I2CSensor
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
from machine import Pin
import machine

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

        # machine.Pin(14).value(0)
        # time.sleep(1)
        # machine.Pin(14).value(1)

        ae1 = RelayActuator("AE1", "1", 16, flowmeter_pin=36)   # AMARILLO
        ae2 = RelayActuator("AE2", "2", 33, flowmeter_pin=22)   # MARRON
        ae3 = RelayActuator("AE3", "3", 0, flowmeter_pin=34)    # AZUL
        ae4 = RelayActuator("AE4", "4", 13, flowmeter_pin=35)   # BLANCO
        ae5 = RelayActuator("AE5", "5", 21, flowmeter_pin=15)   # VERDE
        ae6 = RelayActuator("AE6", "6", 17, flowmeter_pin=12)   # NARANJA
        ae7 = RelayActuator("AE7", "7", 23,flowmeter_pin= 3)  # ROJO
        ae8 = RelayActuator("AE8", "8", 1, flowmeter_pin=10)  # NEGRO
        ae9 = RelayActuator("AE9", "9", 4, flowmeter_pin=25)   # TIRRA

        ae1.set_state(0)
        ae2.set_state(0)
        ae3.set_state(0)
        ae4.set_state(0)
        ae5.set_state(0)
        ae6.set_state(0)
        ae7.set_state(0)
        ae8.set_state(0)
        ae9.set_state(0)

        actuators.append(ae1)
        actuators.append(ae2)
        actuators.append(ae3)
        actuators.append(ae4)
        actuators.append(ae5)
        actuators.append(ae6)
        actuators.append(ae7)
        actuators.append(ae8)
        actuators.append(ae9)


    if Constants.NODE_NAME == "n_b":

        # Actuadores de Temperatura

        at1 = RelayActuator("AT1", "1", 17) #2)
        at2 = RelayActuator("AT2", "2", 33)  #0)
        at3 = RelayActuator("AT3", "3", 15)  #4)
        at4 = RelayActuator("AT4", "4", 4)  #22)
        at5 = RelayActuator("AT5", "5", 21) #23)
        at6 = RelayActuator("AT6", "6", 22) #12)
        at7 = RelayActuator("AT7", "7", 23) #25)
        at8 = RelayActuator("AT8", "8", 25) #33)
        at9 = RelayActuator("AT9", "9", 32) #32)

        at1.set_state(0, validate_rule=False)
        at2.set_state(0, validate_rule=False)
        at3.set_state(0, validate_rule=False)
        at4.set_state(0, validate_rule=False)
        at5.set_state(0, validate_rule=False)
        at6.set_state(0, validate_rule=False)
        at7.set_state(0, validate_rule=False)
        at8.set_state(0, validate_rule=False)
        at9.set_state(0, validate_rule=False)


        # Sensores de Temperatura de Agua
        stw1 = TemperatureSensor("STW1", "1", 16, "283dd45704a13c0f") # CAMBIADO CON STW5 
        stw2 = TemperatureSensor("STW2", "2", 16, "28111a5704433ca0")
        stw3 = TemperatureSensor("STW3", "3", 16, "28338b5704cc3c35")
        stw4 = TemperatureSensor("STW4", "4", 16, "28ebc65704f13cf1")
        stw5 = TemperatureSensor("STW5", "5", 16, "282d925704053cf4")
        stw6 = TemperatureSensor("STW6", "6", 16, "286f1d76e0013cd6")
        stw7 = TemperatureSensor("STW7", "7", 16, "28a2715704103cbd")
        stw8 = TemperatureSensor("STW8", "8", 16, "28ea6657044a3cd4")
        stw9 = TemperatureSensor("STW9", "9", 16, "2891e276e0013c7e") #28831676e0013cf2 EL COMENTADO ES DE STW9
        sta1 = TemperatureSensor("STA1", None, 16, "288adf57047c3c2c")

       
        
        
        sensors.append(stw1)
        sensors.append(stw2)
        sensors.append(stw3)
        sensors.append(stw4)
        sensors.append(stw5)
        sensors.append(stw6)
        sensors.append(stw7)
        sensors.append(stw8)
        sensors.append(stw9)
        sensors.append(sta1)

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

        lg01.security_rules.append(SecurityRule("L01", None, "STW1","<", 24))
        lg02.security_rules.append(SecurityRule("L02", None, "STW1",">", 32))
        lg03.security_rules.append(SecurityRule("L03", None, "STW2","<", 24))
        lg04.security_rules.append(SecurityRule("L04", None, "STW2",">", 32))
        lg05.security_rules.append(SecurityRule("L05", None, "STW3","<", 24))
        lg06.security_rules.append(SecurityRule("L06", None, "STW3",">", 32))
        lg07.security_rules.append(SecurityRule("L07", None, "STW4","<", 24))
        lg08.security_rules.append(SecurityRule("L08", None, "STW4",">", 32))
        lg09.security_rules.append(SecurityRule("L09", None, "STW5","<", 24))
        lg10.security_rules.append(SecurityRule("L10", None, "STW5",">", 32))
        lg11.security_rules.append(SecurityRule("L11", None, "STW6","<", 24))
        lg12.security_rules.append(SecurityRule("L12", None, "STW6",">", 32))
        lg13.security_rules.append(SecurityRule("L13", None, "STW7","<", 24))
        lg14.security_rules.append(SecurityRule("L14", None, "STW7",">", 32))
        lg15.security_rules.append(SecurityRule("L15", None, "STW8","<", 24))
        lg16.security_rules.append(SecurityRule("L16", None, "STW8",">", 32))
        lg17.security_rules.append(SecurityRule("L17", None, "STW9","<", 24))
        lg18.security_rules.append(SecurityRule("L18", None, "STW9",">", 32))


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

        

    if Constants.NODE_NAME == "n_c":
        # Actuadores de Bombas para Sistema de muestreo
        # ae10 = RelayActuator("AE10", "*", 15, hidden=True) # AMARILLO CHECK
        # ae11 = RelayActuator("AE11", "1", 16, hidden=True) # AMARILLO CHECK
        # ae12 = RelayActuator("AE12", "2", 33, hidden=True)  # MARRON CHECK
        # ae13 = RelayActuator("AE13", "3", 0, hidden=True)  # AZUL  Se reinicia el Nodo al apagar relay
        # ae14 = RelayActuator("AE14", "4", 13, hidden=True)  # BLANCO CHECK
        # ae15 = RelayActuator("AE15", "5", 21, hidden=True) # VERDE · No usar Pin 12 para FM
        # ae16 = RelayActuator("AE16", "6", 17, hidden=True) # NARANJA CHECK 
        # ae17 = RelayActuator("AE17", "7", 23, hidden=True) # ROJO CUENTA SOLO CON RELAY
        # ae18 = RelayActuator("AE18", "8", 1, hidden=True) # NEGRO
        # ae19 = RelayActuator("AE19", "9", 4, hidden=True) # TIRRA

        ae10 = RelayActuator("AE10", "*", 1, hidden=True) # AMARILLO CHECK
        ae11 = RelayActuator("AE11", "1", 16, hidden=True) # AMARILLO CHECK
        ae12 = RelayActuator("AE12", "2", 17, hidden=True)  # MARRON CHECK
        ae13 = RelayActuator("AE13", "3", 4, hidden=True)  # AZUL  Se reinicia el Nodo al apagar relay
        ae14 = RelayActuator("AE14", "4", 13, hidden=True)  # BLANCO CHECK
        ae15 = RelayActuator("AE15", "5", 21, hidden=True) # VERDE · No usar Pin 12 para FM
        ae16 = RelayActuator("AE16", "6", 32, hidden=True) # NARANJA CHECK 
        ae17 = RelayActuator("AE17", "7", 23, hidden=True) # ROJO CUENTA SOLO CON RELAY
        ae18 = RelayActuator("AE18", "8", 15, hidden=True) # NEGRO
        ae19 = RelayActuator("AE19", "9", 15, hidden=True) # TIRRA

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

        
        stw10 = TemperatureSensor("STW10", "*", 33, "28128579a2000352", hidden=True)
        
        i2c = machine.SoftI2C(scl=machine.Pin(25), sda=machine.Pin(22),freq=100000)  # Cambia los pines y la frecuencia según tu configuración
        so1 = I2CSensor("SO1", "*", i2c=i2c, address=0x61,hidden=True)
        sph1 = I2CSensor("SPH1", "*", i2c=i2c, address=0x63, hidden=True)
        sc1 = I2CSensor("SC1", "*", i2c=i2c, address=0x64, hidden=True)
        # sph1 = PhSensor("SPH1", "*", tx=33, rx=34, hidden=True)
        # sc1 = ConductivitySensor("SC1", "*", tx=25, rx=39, hidden=True)



        sensors.append(so1)
        sensors.append(sph1)
        sensors.append(sc1)
        sensors.append(stw10)

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

        sampler = Sampler("SS1",
                          [
            ae11, ae12, ae13, ae14, ae15, ae16, ae17, ae18, ae19
        ],
        ae10,
        so1,
        sph1,
        sc1,
        stw10
        )

        sensors.append(sampler)


    # GlobalSecurityRules.start()
    
def register_in_network(new_id=True):
    global registered_by_gateway
    init()
    if new_id:
        registered_by_gateway = False
        payload = Payload()
        payload.receiver = "gw"
        payload.action = "register"
        payload.data["n_n"] = Constants.NODE_NAME
        payload.data["n_id"] = Constants.node_id
        

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
    print("ERROR Buscando actuador:" + str(actuator_id))
    time.sleep(5)
    return None

def get_sensor(sensor_id):
    for sensor in sensors:
        if sensor.get_id() == sensor_id:
            return sensor
    return None

def set_actuator_state(actuator_id, state, validate_rule=True):
    global actuators
    print("Actuators: ", str(actuators))
    for i in range(len(actuators)):
        print(actuators[i].get_id() + "==" + actuator_id)
        if actuators[i].get_id() == actuator_id:
            if state not in ["ON", "on", "1", 1, "OFF", "off", "0", 0, True, False, "True", "False", "TRUE", "FALSE"]:
                print(f"ACTUATOR: {actuator_id}: " + str(state))
                return round(float(actuators[i].set_state_flowmetter(state, False)),3)
            else:
                print(f"ACTUATOR: {actuator_id}: " + str(state))
                return actuators[i].set_state(state, False)
    return None


def set_state_flowmetter(actuator_id, litters, validate_rule=True):
    for i in range(len(actuators)):
        if actuators[i].get_id() == actuator_id:
            actuators[i].set_state_flowmetter(litters, validate_rule)
            return True
    return None

def get_sensor_list():
    return_sensors = []
    for sensor in sensors:
        try:
            if sensor.hidden == False:
                return_sensors.append(sensor)                
        except:
            return_sensors.append(sensor)
    return return_sensors

def get_actuator_list():
    return_actuators = []
    for actuator in actuators:
        try:
            if actuator.hidden == False:
                return_actuators.append(actuator)                
        except:
            return_actuators.append(actuator)
    return return_actuators

def reset():
    Constants.reset_id()
    for actuator in actuators:
        actuator.safe_mode()
    sensors.clear()
    actuators.clear()
    GlobalSecurityRules.reset()
    register_in_network()
    
    # TODO Enter safe mode

