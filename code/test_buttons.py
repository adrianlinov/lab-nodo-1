from machine import Pin
import time

BUTTON_PINS = [17, 16, 25, 33]

# Configurar los pines de los botones como entradas con pull-up
buttons = []
for pin_num in BUTTON_PINS:
    pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
    buttons.append(pin)

# Función para imprimir el estado de los botones
def print_button_state():
    for i, button in enumerate(buttons):
        button_state = "ON" if button.value() == 0 else "OFF"
        # print("Button {} is {}".format(i + 1, button_state))

# Bucle principal
while True:
    print_button_state()
    time.sleep(1)
