from machine import UART, Pin
import time

# SE REQUIRE USAR UART 2 YA QUE UART 1 TRAE PROBLEMAS DE CONEXION
# PROBAR SOFTWARE SERIAL
    

pin = Pin(13, Pin.OUT)
print(pin.value())

while True:
    time.sleep(1)
    pin.value(1)
    time.sleep(1)
    pin.value(0)
    time.sleep(1)