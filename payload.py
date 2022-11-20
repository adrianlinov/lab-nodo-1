import json
import uuid
import constants

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
            self.number_of_ack1_send = 0
        else:
            self.sender = constants.NODE_ID
            self.p_id = str(uuid.uuid4())[:8]
            self.data = {}

    def to_dic(self):
        return {
            "s": self.sender,
            "r": self.receiver,
            "a": self.action,
            "ts": "ts",
            "d": self.data,
            "p_id": self.p_id
        }

    def generate_ack1(self):
        self.number_of_ack1_send = self.number_of_ack1_send + 1
        response_payload = Payload()
        response_payload.receiver = self.sender
        response_payload.action = "ack_1"
        response_payload.data["ack_1"] = self.p_id
        return response_payload

    def generate_ack2(self):
        response_payload = Payload()
        response_payload.receiver = self.receiver
        response_payload.action = "ack_2"
        response_payload.data["ack_2"] = self.p_id
        return response_payload

    def to_json(self):
        return json.dumps(self.to_dic())
        
    def to_json_with_checksum(self):
        return self.to_json() + "-" + str(sum(bytearray(self.to_json(),'utf8')))

    def print(self):
        if self.action == "ack_1":
            print(f"{self.sender} -> {self.receiver}: ID: {self.p_id} ACTION: {self.action} OF: {self.data['ack_1']}")

        if self.action == "ack_2":
            print(f"{self.sender} -> {self.receiver}: ID: {self.p_id} ACTION: {self.action} OF: {self.data['ack_2']}")
        
        else:
            print(f"{self.sender} -> {self.receiver}: ID: {self.p_id} ACTION: {self.action}")
