from time import sleep
import config_lora
from sx127x import SX127x
from controller_esp32 import ESP32Controller
import _thread
import time
import machine
from payload_manager import tx_waiting_ack1
import utils
import sys
from logger import logger


start_time = None
listen_time = None

last_message = "None"

def reset_loop():
    global start_time
    global last_message
    global tx_waiting_ack1
    global listen_time
    while True:
        try:
            time.sleep(1)
            # FALTA GUARDAR LOS DEMAS PAYLOADS [READ, READ_RES, SET_STATE, SET_STATE_RES]
            if start_time != None:
                print("Tiempo Para Reinicio por envio: " + str(time.ticks_ms() - start_time))
                if time.ticks_ms() - start_time > 10000:
                    if "register" in last_message:
                        utils.save_restart()
                    else:
                        utils.save_restart(last_message)

            if listen_time != None:
                print("Tiempo Para Reinicio por escucha: " + str(time.ticks_ms() - listen_time))
                if time.ticks_ms() - listen_time > 10000:
                    if "register" in last_message:
                        utils.save_restart()
                    else:
                        utils.save_restart(last_message)
        except Exception as e:
            logger.logException(e)
            continue


class LoRa:

    #Iniciamos el objeto de lora de acuerdo a los pines establecidos para las placas
    #TTGO y Heltec con el chip sx127x
    def __init__(self, header=None, period=0):
        #Se especifica la cabecera en caso de que solo se quiera procesar algo en especifico
        #y tambien un periodo por si se quiere hacer cierta accion de manera periodica

        self.header = header
        self.period = float(period)
        self.status = 1
        self.cb = None
        # _thread.start_new_thread(reset_loop,())

        self.controller = ESP32Controller()
        self.lora = self.controller.add_transceiver(SX127x(name = 'LoRa'),
                                pin_id_ss = ESP32Controller.PIN_ID_FOR_LORA_SS,
                                pin_id_RxDone = ESP32Controller.PIN_ID_FOR_LORA_DIO0)



    def __del__(self):
        print("LoRa object deleted")

    def stop(self):
        self.status = 0

    def go_on(self):
        self.status = 1

    #permite enviar un dato con el header especificado en la construccion del objeto
    #o con un header distinto
    def send(self, data, spheader=None):
        global start_time
        global last_message
        last_message = data
        start_time = time.ticks_ms()

        if spheader is not None:
            self.lora.println(str(spheader)+'@'+str(data))
        elif self.header is not None:
            self.lora.println(str(self.header)+'@'+str(data))
        else:
            self.lora.println(str(data))
        start_time = None
        

    #metodo para escuchar algun mensaje y ejecutar el callback
    def wait_msg(self):
        assert self.cb is not None, "Subscribe callback is not set"
        # def inc_msg():
        while 1:
            if self.status:
                if self.lora.receivedPacket():
                    try:
                        payload = self.lora.read_payload().decode()
                        data = payload.split('@')
                        if len(data)==2:
                            if self.header is not None:
                                payload = payload.split('@')
                                if payload[0] == str(self.header):
                                    self.cb(payload[1])
                            else:
                                pass
                        elif self.header is None:
                            self.cb(payload)
                        sleep(self.period)
                    except Exception as e:
                        logger.logException(e)
        # _thread.start_new_thread(inc_msg, ())

    def set_callback(self, f):
        self.cb = f

    #metodo para el recibimiento de paquetes
    def receive_msg(self):
        global listen_time
        assert self.cb is not None, "Subscribe callback is not set"
        listen_time = time.ticks_ms()
        if self.lora.receivedPacket():
            try:
                payload = self.lora.read_payload().decode()
                data = payload.split('@')
                if len(data)==2:
                    if self.header is not None:
                        payload = payload.split('@')
                        if payload[0] == str(self.header):
                            listen_time = None
                            self.cb(payload[1])
                    else:
                        pass
                elif self.header is None:
                    listen_time = None
                    self.cb(payload)
            except Exception as e:
                print(sys.print_exception(e))
                logger.logException(e)
                listen_time = None
                self.cb(payload)
        listen_time = None

