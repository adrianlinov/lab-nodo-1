import utime
from components.sensors.temperature_sensor import TemperatureSensor
from components.sensors.oxygen_sensor import OxygenSensor
from components.sensors.ph_sensor import PhSensor
from components.sensors.conductivity_sensor import ConductivitySensor
from components.sensors.sampler import Sampler
from lora import LoRa
import time
import _thread
from payload import Payload
import payload_manager as PayloadManager
import constants as constant
import sys
import machine, onewire
from machine import UART
from components.actuators.relay_actuator import RelayActuator
import ds18x20
import sx127x


actuators = []
available_to_rx = False
pulses_actual = 0
flowing = False

wait_for_message_should_exit = False
tx_loop_should_exit = False


def try_ds18b20():
    while True:
        sensor = ds18x20.DS18X20(onewire.OneWire(machine.Pin(16)))
        roms = sensor.scan()
        sensor.convert_temp()
        time.sleep_ms(750)
        # print(roms)
        for rom in roms:
            print(''.join('{:02x}'.format(byte) for byte in rom))
            print(round(sensor.read_temp(rom), 1))
            # print("")
        time.sleep(5)
        # print("====================================")

def try_releys():
    pins = [2, 5, 4, 22, 23, 12, 25, 33, 32]
    pm = [machine.Pin(2, machine.Pin.OUT), machine.Pin(5, machine.Pin.OUT), machine.Pin(4, machine.Pin.OUT), machine.Pin(22, machine.Pin.OUT), machine.Pin(23, machine.Pin.OUT), machine.Pin(12, machine.Pin.OUT), machine.Pin(25, machine.Pin.OUT), machine.Pin(33, machine.Pin.OUT), machine.Pin(32, machine.Pin.OUT)]
    # Turn pins on for 5 seconds, then off for 5 seconds, repeat.
    
    while True:
        print("OFF")
        for p in pm:
            p.off()
        time.sleep(5)
        print("ON")
        for p in pm:
            p.off()
        time.sleep(5)

def sumar_vuelta(pin):
    global pulses_actual, flowing
    pulses_actual += 1
    flowing = True

def read():
    machine.Pin(35, machine.Pin.IN).irq(trigger=machine.Pin.IRQ_FALLING, handler=sumar_vuelta)
    global pulses_actual
    global flowing
    while True:
        while (flowing == False):
            time.sleep(0.1)
            print("Esperando...")
        pulses_inicio = 0
        pulses_actual = 0
        time_inicio = time.time()
        prev_pulses = pulses_actual
        while (pulses_actual > prev_pulses):
            prev_pulses = pulses_actual
            time.sleep(0.2)
            print("Midiendo...")

        flowing = False
        
            
        current_time = time.time()
        # Calcular el tiempo transcurrido desde el inicio
        time_elapsed = current_time - time_inicio

        # Calcular la cantidad de pulsos desde el inicio
        pulses_delta = pulses_actual - pulses_inicio

        # Calcular el caudal en pulsos por segundo
        if time_elapsed > 0:
            pulsos_por_segundo = pulses_delta / (time_elapsed)  # convertir a segundos
            
            # Calcular el caudal en litros por segudo (suponiendo 7.5 pulsos por litro)
            caudal = pulsos_por_segundo / (7.5 * 60)
            litros_por_minuto = caudal * 60

            # Calcular la cantidad total de litros
            litros_total = caudal * time_elapsed
            if time_elapsed > 0:
                print("Litros por segundo:", caudal)
                print("Litros por minuto:", litros_por_minuto)
                print("Litros totales:", litros_total)
                print("Tiempo transcurrido (s):", time_elapsed)
                flowing = False

def read_chatgpt():
    # Configurar el pin para la interrupción
    machine.Pin(35, machine.Pin.IN).irq(trigger=machine.Pin.IRQ_FALLING, handler=sumar_vuelta)
    global flowing
    while True:
        if flowing:
            time_inicio = time.ticks_ms()
            pulses_inicio = pulses_actual
            flowing = False

        time_actual = time.ticks_ms()
        pulses_actual = pulses_actual

        # Calcular el tiempo transcurrido desde el inicio
        time_elapsed = time_actual - time_inicio

        # Calcular la cantidad de pulsos desde el inicio
        pulses_delta = pulses_actual - pulses_inicio

        # Calcular el caudal en pulsos por segundo
        caudal = pulses_delta / (time_elapsed / 1000)  # convertir a segundos

        # Calcular el caudal en litros por minuto (suponiendo 7.5 pulsos por litro)
        litros_por_minuto = caudal / 7.5

        # Calcular la cantidad total de litros
        litros_total = (pulses_actual / 7.5)

        if time_elapsed > 0:
            print("Caudal (pulsos por segundo):", caudal)
            print("Litros por minuto:", litros_por_minuto)
            print("Litros totales:", litros_total)
            print("Tiempo transcurrido (ms):", time_elapsed)
            
def read_caudal():
        machine.Pin(25, machine.Pin.IN).irq(trigger=machine.Pin.IRQ_FALLING, handler=sumar_vuelta)
        
        while True:
            global pulses_actual
            pulses_actual = 0  # Reinicia el contador de pulsos
            last_time = time.ticks_ms()
            time.sleep(2)
                
            # Detiene la interrupción
            current_time = time.ticks_ms()
            time_elapsed = current_time - last_time
            pulsos_por_segundo = (pulses_actual / time_elapsed) * 1000  # Caudal en pulsos por segundo
            caudal = pulsos_por_segundo / (7.5 * 60)  # Caudal en litros por segundo
            print(caudal)
            print(pulses_actual)
            print("===")

def read_caudal_automatico():
    while True:
        machine.Pin(35, machine.Pin.IN).irq(trigger=machine.Pin.IRQ_FALLING, handler=sumar_vuelta)
        machine.Pin(4, machine.Pin.OUT).value(0)
        global pulses_actual
        pulses_actual = 0  # Reinicia el contador de pulsos
        last_time = time.ticks_ms()
        time.sleep(3)
            
        # Detiene la interrupción
        current_time = time.ticks_ms()
        machine.Pin(4, machine.Pin.OUT).value(1)
        time_elapsed = current_time - last_time
        pulsos_por_segundo = (pulses_actual / time_elapsed) * 1000.0  # Caudal en pulsos por segundo
        caudal = (pulsos_por_segundo / (7.5 * 60)) * 1.30  # Caudal en litros por segundo
        print("Caudal (L/s): ", str(caudal))
        print("Pulsos: ", str(pulses_actual))
        print("Litros Totales: ", (caudal * time_elapsed / 1000))
        print("===")
        time.sleep(10)

def litros_contados():
    machine.Pin(39, machine.Pin.IN).irq(trigger=machine.Pin.IRQ_FALLING, handler=sumar_vuelta)
    while True:
        litros = float(input("Ingresa litros: "))
        time.sleep(1)
        print("3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        machine.Pin(33, machine.Pin.OUT).value(0)
        global pulses_actual
        pulses_actual = 0  # Reinicia el contador de pulsos
        time_inicio_general = time.ticks_ms()
        litros_dispensados = 0
        
        while litros_dispensados < litros:
            time_inicio_bucle = time.ticks_ms()
            time.sleep(0.2)
            time_fin_bucle = time.ticks_ms()
            time_elapsed_bucle = time_fin_bucle - time_inicio_bucle
            pulsos_por_segundo = (pulses_actual / time_elapsed_bucle) * 1000.0  # Caudal en pulsos por segundo
            caudal = (pulsos_por_segundo / (7.5 * 60))
            litros_dispensados += caudal * (time_elapsed_bucle / 1000)
            print(litros_dispensados)
            
            
        machine.Pin(33, machine.Pin.OUT).value(1)

        time_elapsed = time.ticks_ms() - time_inicio_general
        print("Time: ", time_elapsed)        
        print("Litros Totales: ", litros_dispensados)
        print("===")

def test_sensor_serial(sensor):
    # 35, 32 O2
    # 34, 33 ph
    #39, 25 COND
    if sensor == "ph":
        tx=32
        rx=35
    if sensor == "cond":
        tx=33
        rx=34
    if sensor == "o2":
        tx=25
        rx=39
    # SOFTWARE SERIAL
    serial = UART(1, baudrate=9600, tx=tx, rx=rx)
    while True:
        serial.read()
        comando = str(input("Ingrese Comando: "))
        serial.write(f"{comando}\r")
        time.sleep(1)
        response = serial.read().decode("utf-8").split("\r")[0]
        print(response)

def test_flowmeter():
    
    # ae1 = RelayActuator("AE1", "1", 16, flowmeter_pin=36) # AMARILLO CHECK
    # ae2 = RelayActuator("AE2", "2", 33, flowmeter_pin=39)  # MARRON CHECK
    # ae3 = RelayActuator("AE3", "3", 4, flowmeter_pin=34)  # AZUL  Se reinicia el Nodo al apagar relay
    # ae4 = RelayActuator("AE4", "4", 13, flowmeter_pin=35)  # BLANCO CHECK DA COMO 6L
    # ae5 = RelayActuator("AE5", "5", 21, flowmeter_pin=15) # VERDE · No usar Pin 12 para FM
    # ae6 = RelayActuator("AE6", "6", 22, flowmeter_pin=17) # NARANJA CHECK 
    # ae7 = RelayActuator("AE7", "7", 23,flowmeter_pin= 3) # ROJO CUENTA SOLO CON RELAY
    # ae8 = RelayActuator("AE8", "8", 1, flowmeter_pin=10) # NEGRO
    # ae9 = RelayActuator("AE9", "9", 32, flowmeter_pin=25) # TIRRA ORIGINAL PIN 2

    ae1 = RelayActuator("AE1", "1", 16, flowmeter_pin=36)   # AMARILLO
    ae2 = RelayActuator("AE2", "2", 33, flowmeter_pin=22)   # MARRON
    ae3 = RelayActuator("AE3", "3", 0, flowmeter_pin=34)    # AZUL
    ae4 = RelayActuator("AE4", "4", 13, flowmeter_pin=35)   # BLANCO
    ae5 = RelayActuator("AE5", "5", 21, flowmeter_pin=15)   # VERDE
    ae6 = RelayActuator("AE6", "6", 17, flowmeter_pin=2)   # NARANJA
    # ae7 = RelayActuator("AE7", "7", 23,flowmeter_pin= 3)  # ROJO
    # ae8 = RelayActuator("AE8", "8", 1, flowmeter_pin=10)  # NEGRO
    ae9 = RelayActuator("AE9", "9", 4, flowmeter_pin=25)   # TIRRA
    
    # EL CAUDALIMETRO DE 7 RALLAS ES EL 9
    time.sleep(5)

    ae1.set_state(0)
    ae2.set_state(0)
    ae3.set_state(0)
    ae4.set_state(0)
    ae5.set_state(0)
    ae6.set_state(0)
    # ae7.set_state(0)
    # ae8.set_state(0)
    ae9.set_state(0)

    time.sleep(1)

    actuators.append(ae1)
    actuators.append(ae2)
    actuators.append(ae3)
    actuators.append(ae4)
    actuators.append(ae5)
    actuators.append(ae6)
    # actuators.append(ae7)
    # actuators.append(ae8)
    actuators.append(ae9)

    while True:
        for actuator in actuators:
            # print(actuator.id)
            actuator.set_state_flowmetter(4)
            time.sleep(1)

def test_i2c():
    while True:
        try:
            i2c = machine.SoftI2C(scl=machine.Pin(25), sda=machine.Pin(22), freq=100000)
            command = b"R"
            i2c.writeto(0x61, command)
            time.sleep(1)
            response = i2c.readfrom(0x61, 7)
            print("1: " + response.decode("utf-8")[1:5])
            print(type(response.decode("utf-8")[1:5]))
            print(float(response.decode("utf-8")[1:5]))
            i2c.writeto(0x63, command)
            time.sleep(1)
            response = i2c.readfrom(0x63, 7)
            print("2: " + response.decode("utf-8")[1:5])
            print(type(response.decode("utf-8")[1:5]))
            print(float(response.decode("utf-8")[1:5]))
            i2c.writeto(0x64, command)
            time.sleep(1)
            response = i2c.readfrom(0x64, 7)
            print("3: " + response.decode("utf-8")[1:5])
            print(type(response.decode("utf-8")[1:5]))
            print(float(response.decode("utf-8")[1:5]))
            time.sleep(1)
        except Exception as e:
            sys.print_exception(e)

def test_electrovalvulas_muestreo():
    
    ae10 = RelayActuator("AE10", "*", 3) # AMARILLO CHECK
    ae11 = RelayActuator("AE11", "1", 16) # AMARILLO CHECK
    ae12 = RelayActuator("AE12", "2", 17)  # MARRON CHECK
    ae13 = RelayActuator("AE13", "3", 4)  # AZUL  Se reinicia el Nodo al apagar relay
    ae14 = RelayActuator("AE14", "4", 13)  # BLANCO CHECK
    ae15 = RelayActuator("AE15", "5", 21) # VERDE · No usar Pin 12 para FM
    ae16 = RelayActuator("AE16", "6", 22) # NARANJA CHECK 
    ae17 = RelayActuator("AE17", "7", 23) # ROJO CUENTA SOLO CON RELAY
    ae18 = RelayActuator("AE18", "8", 15) # NEGRO
    ae19 = RelayActuator("AE19", "9", 2) # TIRRA
    # EL CAUDALIMETRO DE 7 RALLAS ES EL 9
    time.sleep(5)
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

    time.sleep(1)

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

    while True:
        ae10.set_state(1)
        ae11.set_state(1)
        ae12.set_state(1)
        ae13.set_state(1)
        ae14.set_state(1)
        ae15.set_state(1)
        ae16.set_state(1)
        ae17.set_state(1)
        ae18.set_state(1)
        ae19.set_state(1)

        time.sleep(1)

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

        time.sleep(1)

    # time.sleep(1)
    #     for actuator in actuators:
    #         time.sleep(10)
    #         actuator.set_state(True)
    #         time.sleep(1)
    #         actuator.set_state(False)
    #         time.sleep(1)
    #         actuator.set_state(True)
    #         time.sleep(1)
    #         actuator.set_state(False)
    #         time.sleep(1)
    #         actuator.set_state(True)
    #         time.sleep(1)
    #         actuator.set_state(False)

def test_sampler():
    ae10 = RelayActuator("AE10", "*", 3) # AMARILLO CHECK
    ae11 = RelayActuator("AE11", "1", 16) # AMARILLO CHECK
    ae12 = RelayActuator("AE12", "2", 17)  # MARRON CHECK
    ae13 = RelayActuator("AE13", "3", 4)  # AZUL  Se reinicia el Nodo al apagar relay
    ae14 = RelayActuator("AE14", "4", 13)  # BLANCO CHECK
    ae15 = RelayActuator("AE15", "5", 21) # VERDE · No usar Pin 12 para FM
    ae16 = RelayActuator("AE16", "6", 22) # NARANJA CHECK 
    ae17 = RelayActuator("AE17", "7", 23) # ROJO CUENTA SOLO CON RELAY
    ae18 = RelayActuator("AE18", "8", 15) # NEGRO
    ae19 = RelayActuator("AE19", "9", 2) # TIRRA

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

    # sta1 = TemperatureSensor("STA1", "*", 4, "COMPLETAR")
    # stw10 = TemperatureSensor("STW10", "*", 4, "COMPLETAR", hidden=True)
    so1 = OxygenSensor("SO1", "*", tx=32, rx=35)
    sph1 = PhSensor("SPH1", "*", tx=33, rx=34)
    sc1 = ConductivitySensor("SC1", "*", tx=25, rx=39)



    sampler = Sampler("SAMPLER",
                        [
        ae11, ae12, ae13, ae14, ae15, ae16, ae17, ae18, ae19
    ],
    ae10,
    so1,
    sph1,
    sc1,
    )
    sampler.read_all()


class LoRaTransceiver:
    def __init__(self):
        try:
            self.lora = LoRa()
            self.lora.set_callback(self.receive_callback)
        except Exception as e:
            sys.print_exception(e)
            machine.reset()

    def verify_payload(self, payload):
        validate = payload.split("}-")
        validate[0] = str(validate[0]) + "}"
        if sum(bytearray(validate[0],'utf8')) == int(validate[1]):
            payload_obj = Payload(payload)
            print(payload)
            print(payload_obj.receiver)
            print(constant.NODE_ID)
            if payload_obj.receiver in [constant.NODE_ID, constant.node_id_prev]:
                return True
            else:    
                print("Error de validacion por ID")
                return False
        else:
            print("Error de validacion por checksum")
            return False


    def wait_for_message(self):
        while wait_for_message_should_exit == False:
            if available_to_rx:
                self.lora.receive_msg()
            

    def receive_callback(self, payload_str):
        if self.verify_payload(payload_str) == True:
            payload = Payload(payload_str)
            payload.print()
            PayloadManager.payload_received(payload)
        else:
            print("Payload Received: N/A")
            print(payload_str)

    def send_message(self, msg):
        # TOA = 390ms
        try:
            self.lora.send(msg)
        except Exception as e:
            sys.print_exception(e)

    def tx_loop(self):
        global available_to_rx
        while tx_loop_should_exit == False:
            available_to_rx = True
            payload = PayloadManager.get_payload_to_send()
            if payload != None:
                try:
                    available_to_rx = False
                    payload.print()
                    print(payload.to_json_with_checksum())
                    time.sleep(1)
                    print("INICIO ENVIO")
                    self.send_message(payload.to_json_with_checksum())
                    print("FIN ENVIO")
                except Exception as e:
                    sys.print_exception(e)




def main():
    print("starting")
    # _thread.start_new_thread(loop_bloqueo_spi, ())
    lora = LoRaTransceiver()
    print("starting threads")
    _thread.start_new_thread(lora.wait_for_message, ())
    _thread.start_new_thread(lora.tx_loop, ())
    PayloadManager.start()
    while True:
        pass
# def main2():
#     print("starting")
#     while True:
#         lora = LoRaTransceiver()
#         print("starting threads")
#         _thread.start_new_thread(lora.wait_for_message, ())
#         _thread.start_new_thread(lora.tx_loop, ())
#         PayloadManager.start()
#         while True:
#             # print(".")
#             time.sleep(.5)



if __name__ == '__main__':
    try:
        print("started")
        time.sleep(10)


        # try_ds18b20()
        # test_flowmeter()
        main()
    except Exception as e:
        sys.print_exception(e)