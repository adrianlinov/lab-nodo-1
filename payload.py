import json
import uuid
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
            self.sender = payload_as_json["sender"]
            self.receiver = payload_as_json["receiver"]
            self.action = payload_as_json["action"]
            self.data = payload_as_json["data"]
            self.number_of_ack1_send = 0
        else:
            self.sender = "nodo_a"
            self.p_id = str(uuid.uuid4())[:8]
            self.data = {}
        print("init finished")
    def run(self):
        # do stuff
        return "success"
    def to_dic(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "action": self.action,
            "timestamp": "timestamp",
            "data": self.data,
            "p_id": self.p_id
        }

    def generate_ack1(self):
        self.number_of_ack1_send = self.number_of_ack1_send + 1
        response_payload = Payload()
        response_payload.receiver = self.sender
        response_payload.action = "ack_1"
        response_payload.data["ack_1"] = self.p_id
        return response_payload

    def response(self):
        response_payload = Payload()
        response_payload.receiver = self.sender
        response_payload.action = "ack_1"
        response_payload.data["ack_1"] = self.p_id
        return response_payload

    def to_json(self):
        return json.dumps(self.to_dic())
    def to_json_with_checksum(self):
        return self.to_json() + "-" + str(sum(bytearray(self.to_json(),'utf8')))
