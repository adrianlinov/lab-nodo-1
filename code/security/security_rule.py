
class SecurityRule:
    def __init__(self, id, actuator, sensor, conditional, conditional_value, if_valid_value, if_not_valid_value):
        self.id = id
        self.actuator = actuator
        self.sensor = sensor
        self.conditional = conditional
        self.conditional_value = conditional_value
        self.if_valid_value = if_valid_value
        self.if_not_valid_value = if_not_valid_value

    def is_violated(self, take_action = False):
        if self.conditional == ">":
            if self.actuator.get_state() > self.conditional_value:
                if take_action:
                    self.actuator.set_state(self.if_valid_value)
                return True
            else:
                if take_action:
                    self.actuator.set_state(self.if_not_valid_value)
                return False
        elif self.conditional == "<":
            if self.actuator.get_state() < self.conditional_value:
                if take_action:
                    self.actuator.set_state(self.if_valid_value)
                return True
            else:
                if take_action:
                    self.actuator.set_state(self.if_not_valid_value)
                return False
        elif self.conditional == "==":
            if self.actuator.get_state() == self.conditional_value:
                if take_action:
                    self.actuator.set_state(self.if_valid_value)
                return True
            else:
                if take_action:
                    self.actuator.set_state(self.if_not_valid_value)
                return False

        elif self.conditional == "!=":
            if self.actuator.get_state() != self.conditional_value:
                if take_action:
                    self.actuator.set_state(self.if_valid_value)
                return True
            else:
                if take_action:
                    self.actuator.set_state(self.if_not_valid_value)
                return False

        elif self.conditional == ">=":
            if self.actuator.get_state() >= self.conditional_value:
                if take_action:
                    self.actuator.set_state(self.if_valid_value)
                return True
            else:
                if take_action:
                    self.actuator.set_state(self.if_not_valid_value)
                return False

        elif self.conditional == "<=":
            if self.actuator.get_state() <= self.conditional_value:
                if take_action:
                    self.actuator.set_state(self.if_valid_value)
                return True
            else:
                if take_action:
                    self.actuator.set_state(self.if_not_valid_value)
                return False

        else:
            print("Invalid conditional")
            return None
