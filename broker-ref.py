import socket
import dataclasses
import typing
import threading
import json

_DEFAULT_PORT = 49000
_DEFAULT_BUFFER_SIZE = 1024

@dataclasses.dataclass
class SubscriberData:
    client_id: int
    ip: str
    port: int
    topics: typing.List[str]

@dataclasses.dataclass
class MessageData:
    topic: str
    type: str
    message: str
    client_id: int

class Broker:

    broker_id = 0

    def __init__(self, ip_address, buffer_size = None, port = None):
        self.port = port or _DEFAULT_PORT
        self.buffer_size = buffer_size or _DEFAULT_BUFFER_SIZE
        self.ip_address = ip_address
        self.upd
        



    def listen(self,ip: str, port: int):
        thread = threading.Thread(target = Client.listen_function, args = (self, ))
        thread.start()

    @staticmethod
    def listen_function(client):
        while True:
            response = client.upd_listen_socket.recvfrom(client.bufferSize)
            payload_json_string = str(response[0])
            json_payload = json.loads(payload_json_string)
            address = response[1]

            client_id = json_payload["client_id"]
            message = json_payload["message"]
            type = json_payload["type"]
            topic = json_payload["topic"]

            if type == "subscribe":
                if client_id in broker.subscribers:
                    if topic not in broker.subscribers[client_id].topics:
                        broker.subscribers[client_id].topics.append(topic)
                else:
                    broker.subscribers[client_id] = SubscriberData(client_id, ip, port, [topic])
            else type == "publish":
                if topic in broker.messages_by_topic:
                    broker.messages_by_topic[topic].append(message)
                else:
                    broker.message_by_topic[topic] = [message]

                

            print(f"Message: {json_payload}")
            print(f"Address: {address}")