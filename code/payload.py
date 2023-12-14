import json
import uuid
import constants
import machine
from logger import logger

class Payload:
    # JSON as string to be parsed
    def __init__(self, payload=None):
        if payload != None:
            self.str_payload_with_checksum = bytes(payload, 'utf-8').decode("utf-8").replace("'", '"')
            self.str_payload_without_checksum = self.str_payload_with_checksum.split("}-")[0] + "}"
            self.str_payload_checksum = self.str_payload_with_checksum.split("}-")[1]
            payload_as_json = json.loads(self.str_payload_without_checksum)
            # Payload content deserialized
            self.p_id = payload_as_json["p_id"]
            self.sender = payload_as_json["s"]
            self.receiver = payload_as_json["r"]
            self.action = payload_as_json["a"]
            self.data = payload_as_json["d"]
            self.tx_ack1_count = 0
            self.tx_last_ack1_time = None
            self.rx_ack1_count = 0
            self.priority = payload_as_json["p"]
            self.tx_payload_send_count = 0
        else:
            self.tx_payload_send_count = 0
            self.tx_ack1_count = 0
            self.rx_ack1_count = 0
            self.tx_last_ack1_time = None
            self.priority = 2
            self.sender = constants.node_id
            self.p_id = str(uuid.uuid4())[:8]
            self.data = {}

    def to_dic(self):
        return {
            "s": self.sender,
            "r": self.receiver,
            "a": self.action,
            "p": self.priority,
            "d": self.data,
            "p_id": self.p_id
        }

    def generate_ack1(self):
        self.rx_ack1_count = self.rx_ack1_count + 1
        response_payload = Payload()
        if self.rx_ack1_count > 3:
            response_payload.priority = 1
        if self.rx_ack1_count > 30:
            response_payload.priority = 0
        if self.rx_ack1_count > 150:
            machine.reset()
            # utils.remove_prev_name
        response_payload.receiver = self.sender
        response_payload.action = "ack_1"
        response_payload.data["ack_1"] = self.p_id
        return response_payload

    def generate_ack2(self):
        response_payload = Payload()
        self.tx_ack1_count += 1
        if self.tx_ack1_count > 3:
            response_payload.priority = 1            
        if self.tx_ack1_count > 30:
            response_payload.priority = 0            
        if self.tx_ack1_count > 150:
            machine.reset()

        response_payload = Payload()
        response_payload.sender = self.sender
        response_payload.receiver = self.receiver
        response_payload.action = "ack_2"
        response_payload.data["ack_2"] = self.p_id
        return response_payload

    def to_json(self):
        return json.dumps(self.to_dic()).replace(" ", '').replace("null", "0")
        
    def to_json_with_checksum(self):
        return self.to_json().replace(" ", '').replace("null", "0") + "-" + str(sum(bytearray(self.to_json(),'utf8'))).replace("null", "0")

    def print(self):
        if self.action == "ack_1":
            logger.log(f"{self.sender} -> {self.receiver}: ID: {self.p_id} ACTION: {self.action} OF: {self.data['ack_1']} LEN:{len(self.to_json_with_checksum())} RTY:{self.rx_ack1_count}")
            # print(f"{self.sender} -> {self.receiver}: ID: {self.p_id} ACTION: {self.action} OF: {self.data['ack_1']} LEN:{len(self.to_json_with_checksum())} RTY:{self.rx_ack1_count}")

        if self.action == "ack_2":
            logger.log(f"{self.sender} -> {self.receiver}: ID: {self.p_id} ACTION: {self.action} OF: {self.data['ack_2']} LEN:{len(self.to_json_with_checksum())} RTY:{self.tx_ack1_count}")
            # print(f"{self.sender} -> {self.receiver}: ID: {self.p_id} ACTION: {self.action} OF: {self.data['ack_2']} LEN:{len(self.to_json_with_checksum())} RTY:{self.tx_ack1_count}")
        else:
            logger.log(f"{self.sender} -> {self.receiver}: ID: {self.p_id} ACTION: {self.action} LEN:{len(self.to_json_with_checksum())} RTY:{self.rx_ack1_count}")
            # print(f"{self.sender} -> {self.receiver}: ID: {self.p_id} ACTION: {self.action} LEN:{len(self.to_json_with_checksum())} RTY:{self.rx_ack1_count}")
