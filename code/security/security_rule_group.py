
import components.node as Node
import sys
from logger import logger

class SecurityRuleGroup:
    def __init__(self, id, id_output_actuator, if_violated_value=None, if_not_violated_value=None, method="all", take_action=True):
        self.id = id
        self.security_rules = []
        self.id_output_actuator = id_output_actuator
        self.if_violated_value = if_violated_value
        self.if_not_violated_value = if_not_violated_value
        self.method = method
        self.violated = False
        self.take_action = take_action
 
    def is_violated(self):
        try:
            violations = []
            for rule in self.security_rules:
                violations.append(rule.is_violated())
            if self.method == "all":
                if False not in violations:
                    if self.take_action:
                        Node.set_actuator_state(self.id_output_actuator,self.if_violated_value, validate_rule=False)
                        self.violated = True
                    return True
                else:
                    if self.take_action:
                        if self.if_not_violated_value is not None:
                            Node.set_actuator_state(self.id_output_actuator,self.if_not_violated_value, validate_rule=False)
                        self.violated = False
                    return False
            
            if self.method == "one":
                if True in violations:
                    if self.take_action:
                        Node.set_actuator_state(self.id_output_actuator,self.if_violated_value, validate_rule=False)
                        self.violated = True
                    return True
                else:
                    if self.take_action:
                        if self.if_not_violated_value is not None:
                            Node.set_actuator_state(self.id_output_actuator,self.if_not_violated_value, validate_rule=False)
                        self.violated = False
                    return False
        except Exception as e:
            logger.logException(e)





