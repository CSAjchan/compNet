import socket
import threading
import json

_DEFAULT_BUFFER_SIZE = 1024

class Subscriber:

    def __init__(self, sub_ip: str, sub_port: int, broker_ip: str, broker_port: int):
        self.buffer_size = _DEFAULT_BUFFER_SIZE
        self.sub_port = sub_port
        self.sub_ip = sub_ip
        self.broker_ip = broker_ip
        self.broker_port = broker_port

        self.udp_send_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_listen_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_listen_socket.bind((self.sub_ip, self.sub_port))

    def unsubscribe(self, topic: str):
        payload= {
            "topic": topic,
            "type": "unsubscribe",
            "sub_ip":self.sub_ip,
            "sub_port": self.sub_port,
        }
        
        data = json.dumps(payload)

        self.udp_send_socket.connect((self.broker_ip, self.broker_port))
        self.udp_send_socket.sendall((data.encode()))


    def subscribe(self, topic: str):
        payload= {
            "topic": topic,
            "type": "subscribe",
            "sub_ip":self.sub_ip,
            "sub_port": self.sub_port,
        }

        data = json.dumps(payload)

        self.udp_send_socket.connect((self.broker_ip, self.broker_port))
        self.udp_send_socket.sendall((data.encode()))
        #brocker_response = brocker_response.decode("utf-8")
        #print((f"Most recent response received {brocker_response[0]}" 
        #    f"from{brocker_response[1]}"))

    def listen(self, ):
        thread = threading.Thread(target = Subscriber.listen_function, args = (self, ))
        thread.start()

    @staticmethod
    def listen_function(subscriber):
        while True:
            response = subscriber.udp_listen_socket.recvfrom(subscriber.buffer_size)

            message = response[0].decode()
            address = response[1]
            
            print(f"Message: {message} Sub_port: {subscriber.sub_port}")
            #print(f"Sub_port: {subscriber.sub_port}")