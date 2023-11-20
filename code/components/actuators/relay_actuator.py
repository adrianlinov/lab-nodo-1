from components.actuator import Actuator
from machine import Pin
from security import global_security_rules as GlobalSecurityRules
import time

class RelayActuator(Actuator):
    
    def __init__(self, id, pool, pin, flowmeter_pin=None, hidden=False):
        self.pin = Pin(pin, Pin.OUT)
        self.pin.value(1)
        if flowmeter_pin != None:
            self.flowmeter_pin = Pin(flowmeter_pin, Pin.IN)
            self.pulses = 0
            self.flowmeter_pin.irq(trigger=Pin.IRQ_FALLING, handler=self._count_pulse)
        super().__init__(id, pool, hidden)

    def _count_pulse(self, pin):
        self.pulses += 1

    def _reset_pulses(self):
        self.pulses = 0

    def _get_compensation(self):
        if self.id in ["AE4","AE5"]:
            return -0.300
        if self.id in ["AE7"]:
            return -0.5
        if self.id in ["AE9"]:
            return +0.6
        else:
            return 0

    def set_state(self, newState, validate_rule=True):
        if validate_rule == True:
            if GlobalSecurityRules.validate_actuator_security_rules(self.get_id()) == True:
                if newState == True or newState == "ON" or newState == "on" or newState == "1" or newState == 1:
                    self.pin.value(0)
                    print(f"{self.id}: ON")
                    return 1
                elif newState == False or newState == "OFF" or newState == "off" or newState == "0" or newState == 0:
                    self.pin.value(1)
                    print(f"{self.id}: OFF")
                    return 0
                else:
                    print("Invalid state")
            else:
                # informar que no se cumplen las reglas de seguridad para activar el actuador
                print("Security rules not validated")
        else:
            if newState == True or newState == "ON" or newState == "on" or newState == "1" or newState == 1:
                self.pin.value(0)
                print(f"{self.id}: ON")
                return 1
            elif newState == False or newState == "OFF" or newState == "off" or newState == "0" or newState == 0:
                self.pin.value(1)
                print(f"{self.id}: OFF")
                return 0
            else:
                print("Invalid state")

        
    def set_state_until(self, start_callback, callback, value, newState, timeout=120):        
        previous_value = self.pin.value()
        start_time = time.time()
        if GlobalSecurityRules.validate_actuator_security_rules(self.get_id()) == True:
            if newState == True or newState == "ON" or newState == "on" or newState == "1" or newState == 1:
                self.pin.value(1)
                time.sleep(0.5)
                start_callback()
                while callback() <= value and timeout > (time.time() - start_time):
                    time.sleep(0.5)
                self.pin.value(previous_value)
            elif newState == False or newState == "OFF" or newState == "off" or newState == "0" or newState == 0:
                self.pin.value(0)
                time.sleep(0.5)
                start_callback()
                while callback() <= value and timeout > (time.time() - start_time):
                    time.sleep(0.5)
                self.pin.value(previous_value)
            else:
                raise print("Invalid state")
        else:
            # informar que no se cumplen las reglas de seguridad para activar el actuador
            raise print("Security rules not validated")
        
    def set_state_flowmetter(self, litters, validate_rule=True):
        litters = litters + self._get_compensation()
        self._reset_pulses()
        self.pin.value(0)
        litros_dispensados = 0
        contador = 0
        litros_dispensados_prev = 0
        while litros_dispensados < litters and contador < 10:
            self._reset_pulses()
            time_inicio_bucle = time.ticks_ms()
            time.sleep(0.1)
            time_fin_bucle = time.ticks_ms()
            time_elapsed_bucle = time_fin_bucle - time_inicio_bucle
            pulsos_por_segundo = (self.pulses / time_elapsed_bucle) * 1000.0  # Caudal en pulsos por segundo
            caudal = (pulsos_por_segundo / (7.5 * 60))
            litros_en_medida_de_tiempo = caudal * (time_elapsed_bucle / 1000)
            litros_dispensados += litros_en_medida_de_tiempo
            print(str(litros_en_medida_de_tiempo) + " - " + str(litros_dispensados))
            if litros_dispensados == 0 or litros_dispensados == litros_dispensados_prev:
                contador+=1
            litros_dispensados_prev = litros_dispensados
            # if round(litros_en_medida_de_tiempo,3) >= 0.016:
            #     break       
        self.pin.value(1)
        return litros_dispensados


    def read(self):
        if self.pin.value():
            return 0
        else:
            return 1

    def safe_mode(self):
        '''Pone el actuador en modo seguro'''
        self.pin.value(1)
