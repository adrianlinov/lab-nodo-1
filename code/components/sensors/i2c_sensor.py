from components.sensor import Sensor
import machine
import time

class I2CSensor(Sensor):
    
    def __init__(self, id, pool, i2c, hidden=True, address=None):
        super().__init__(id, pool, hidden=hidden)
        # USAR UART2
        self.i2c = i2c
        self.device_address = address
        self.last_value = None

    def get_new_temperature_compensation(self, temperatureCompensation):
        return (0.008136597*(temperatureCompensation**5))-(1.1190774448*(temperatureCompensation**4))+(61.0359530777*(temperatureCompensation**3))-(1649.2663660844*(temperatureCompensation**2))+(22068.5792281778*temperatureCompensation)-116923.597038709
            
    def read(self, temperatureCompensation=None):
        '''Lee el valor del sensor'''
        try:
            results = []
            for c in range(0, 10):
                if temperatureCompensation != None:
                    if temperatureCompensation > 0:
                        self.i2c.writeto(self.device_address, b"T,"+str(round(temperatureCompensation,2)))
                        time.sleep(1)
                        response = self.i2c.readfrom(self.device_address, 7)
                    else:
                        self.i2c.writeto(self.device_address, b"T,25")
                        time.sleep(1)
                        response = self.i2c.readfrom(self.device_address, 7)
                self.i2c.writeto(self.device_address, b"R")
                time.sleep(1)
                response = self.i2c.readfrom(self.device_address, 7)
                response = float(response.decode("utf-8")[1:5])
                if self.id == "SC1":
                    response = int(response - self.get_new_temperature_compensation(temperatureCompensation))
                results.append(float(response))
                time.sleep(1)
            final_response = sum(results) / len(results)
            if self.id == "SC1":
                final_response = int(final_response)
            else:
                final_response = round(final_response, 2)
            self.last_value = final_response
            return final_response
        
        except:
            return 0.0
