
import time
# import _thread
import machine


actuators = []
available_to_rx = False
pulses_actual = 0
flowing = False
reset = False



def test_i2c():
    while True:
        try:
            i2c = machine.SoftI2C(scl=machine.Pin(25), sda=machine.Pin(22), freq=100000)
            inpu = input("Ingrese comando: ")
            # inpu = "R"
            command = inpu.encode('utf-8')
            i2c.writeto(0x63, command)
            time.sleep(1)
            
            response = i2c.readfrom(0x63, 8)
            print(response.decode("utf-8"))
            time.sleep(1)
        except Exception as e:
            pass
            # logger.logException(e)




if __name__ == '__main__':
    try:
        # print("started")
        time.sleep(5)

        test_i2c()
        # try_ds18b20()
        # test_flowmeter()
        # main()
    except Exception as e:
        pass