from components.sensor import Sensor
import machine
import time

class FlowMeterSensor(Sensor):
    def __init__(self, pin):
        self.pin = machine.Pin(pin, machine.Pin.IN)
        self.pulses = 0
        self.last_time = time.ticks_ms()
        
        # Configura la interrupción en el pin del caudalímetro
        self.pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=self._count_pulse)
    
    def _count_pulse(self, pin):
        self.pulses += 1

    def read(self, duration=1):
        self.pulses = 0  # Reinicia el contador de pulsos
        self.last_time = time.ticks_ms()
        
        time.sleep(duration)
        
        # Detiene la interrupción
        self.pin.irq(handler=None)
        
        current_time = time.ticks_ms()
        time_elapsed = current_time - self.last_time
        pulsos_por_segundo = (self.pulses / time_elapsed) * 1000  # Caudal en pulsos por segundo
        caudal = pulsos_por_segundo / (7.5 * 60)  # Caudal en litros por segundo
        return caudal
    
    def start_measuring(self):
        self.pulses = 0  # Reinicia el contador de pulsos
        self.last_time = time.ticks_ms()

        # Configura la interrupción en el pin del caudalímetro
        self.pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=self._count_pulse)

    def get_measurment_in_litters(self):
        current_time = time.ticks_ms()
        time_elapsed = current_time - self.last_time
        pulsos_por_segundo = (self.pulses / time_elapsed) * 1000
        caudal = pulsos_por_segundo / (7.5 * 60) # Caudal en litros por segundo
        return caudal * time_elapsed / 1000


    
    


