from machine import UART
import time

# SE REQUIRE USAR UART 2 YA QUE UART 1 TRAE PROBLEMAS DE CONEXION
# PROBAR SOFTWARE SERIAL
    
serial = UART(2, 9600)
def read():
    '''Lee el valor del sensor'''
    serial.read()
    _awake()
    serial.write("R\r")
    response = serial.read().decode("utf-8").split("\r")[0]
    _sleep()
    return response

def _awake():
    serial.read()
    serial.write("K\r")
    return serial.read().decode("utf-8").split("\r")[0]

def _sleep():
    serial.read()
    serial.write("SLEEP\r")
    return serial.read().decode("utf-8").split("\r")[0]


while True:
    # print(read())
    _awake()
    print(".")
    time.sleep(1)