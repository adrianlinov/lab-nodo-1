
import components.node as Node


class SecurityRule:
    def __init__(self, id, input_actuator_id=None, input_sensor_id=None, conditional=None, conditional_value=None):
        self.id = id
        self.input_actuator_id = input_actuator_id
        self.input_sensor_id = input_sensor_id
        self.conditional = conditional
        self.conditional_value = conditional_value

    def is_violated(self):

        if self.input_actuator_id is not None:
            if self.conditional == ">":
                if Node.get_actuator(self.input_actuator_id).get_state() > self.conditional_value:
                    return True
                else:
                    return False
            elif self.conditional == "<":
                if Node.get_actuator(self.input_actuator_id).get_state() < self.conditional_value:
                    return True
                else:
                    return False
            elif self.conditional == "==":
                if Node.get_actuator(self.input_actuator_id).get_state() == self.conditional_value:
                    return True
                else:
                    return False

            elif self.conditional == "!=":
                if Node.get_actuator(self.input_actuator_id).get_state() != self.conditional_value:
                    return True
                else:
                    return False

            elif self.conditional == ">=":
                if Node.get_actuator(self.input_actuator_id).get_state() >= self.conditional_value:
                    return True
                else:
                    return False

            elif self.conditional == "<=":
                if Node.get_actuator(self.input_actuator_id).get_state() <= self.conditional_value:
                    return True
                else:
                    return False

            else:
                print("Invalid conditional")
                return None


        elif self.input_sensor_id is not None:
            if self.conditional == ">":
                if Node.get_sensor(self.input_sensor_id).get_state() > self.conditional_value:
                    return True
                else:
                    return False
            elif self.conditional == "<":
                if Node.get_sensor(self.input_sensor_id).get_state() < self.conditional_value:
                    return True
                else:
                    return False
            elif self.conditional == "==":
                if Node.get_sensor(self.input_sensor_id).get_state() == self.conditional_value:
                    return True
                else:
                    return False

            elif self.conditional == "!=":
                if Node.get_sensor(self.input_sensor_id).get_state() != self.conditional_value:
                    return True
                else:
                    return False

            elif self.conditional == ">=":
                if Node.get_sensor(self.input_sensor_id).get_state() >= self.conditional_value:
                    return True
                else:
                    return False

            elif self.conditional == "<=":
                if Node.get_sensor(self.input_sensor_id).get_state() <= self.conditional_value:
                    return True
                else:
                    return False

            else:
                print("Invalid conditional")
                return None
