import socket
import threading
import json

_DEFAULT_PORT = 1883
_DEFAULT_BUFFER_SIZE = 1024

class Client:
    client_id = 0

    def __init__(self, ip_address, buffer_size = None, port = None):
        self.port = port or _DEFAULT_PORT
        self.buffer_size = buffer_size or _DEFAULT_BUFFER_SIZE
        self.ip_address = ip_address
        self.upd_client_socket = socket.socket(
            family = socket.AF_INET, type = socket.SOCK_DGRAM)
        self.client_id = Client.client_id
        Client.client_id = Client.client_id + 1

        def publish(self, message: str, topic: str):
            """no failures"""
            payload= {
                "topic": topic,
                "type": "publish",
                "message": message,
                "client_id":self.client_id,
                "port": self.port,
                "ip": self.ip_address
            }
            data_bytes = str.encode(f"topic:{topic},type: publish, message:" 
                                    f"{message}, client_id{self.client_id}")
            self.upd_client_socket.send(data_bytes,(self.ip_address, self.port))
            broker_response = self.upd_client_socket.recvfrom(self.buffer_size)
            print((f"Response received {broker_response[0]} from {broker_response[1]}"))

        def subscribe(self, topic: str):
            """no failures"""
            payload= {
                "topic": topic,
                "type": "subscribe",
                "message": "placeholder",
                "client_id":self.client_id,
                "port": self.port,
                "ip": self.ip_address
            }
            data_bytes = str.encode(f"topic:{topic}, type: subscribe")
            self.upd_client_socket.send(data_bytes,(self.ip_address, self.port))
            brocker_response = self.upd_client_socket.recvfrom(self.buffer_size)
            print((f"Most recent response received {brocker_response[0]}" 
            f"from{brocker_response[1]}"))

        def listen(self,ip: str, port: int):
            thread = threading.Thread(target = Client.listen_function, args = (self, ))
            thread.start()

        @staticmethod
        def listen_function(client):
            while True:
                response = client.upd_listen_socket.recvfrom(client.bufferSize)
                message = response[0]
                address = response[1]
                print(f"Message: {message}")
                print(f"Address: {address}")