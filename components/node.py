class _Node():
    def __init__(self):
        self.sensors = []
        # self.sensors.append(Sensor(data))
        self.actuators = []
        # self.actuators.append(Actuator(data))
        self.next = None

    def get_sensor(self, sensor_id):
        for sensor in self.sensors:
            if sensor.get_id() == sensor_id:
                return sensor
        return None

    def get_actuator(self, actuator_id):
        for actuator in self.actuators:
            if actuator.get_id() == actuator_id:
                return actuator
        return None

    def get_sensor_list(self):
        return self.sensors

    def get_actuator_list(self):
        return self.actuators

node = _Node()