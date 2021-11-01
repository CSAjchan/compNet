import socket
import json

_DEFAULT_BUFFER_SIZE = 1024

class Publisher:

    def __init__(self, broker_ip: str, broker_port: int, pub_ip: str, pub_port: int):
        self.buffer_size = _DEFAULT_BUFFER_SIZE
        self.broker_ip = broker_ip
        self.broker_port = broker_port
        self.pub_ip = pub_ip
        self.pub_port = pub_port

        self.udp_send_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)


    def publish(self, topic: str, sub_topic: str, message: str):
        payload= {
            "topic": topic,
            "sub_topic":sub_topic,
            "type": "publish",
            "message": message,
            "pub_ip":self.pub_ip,
            "pub_port": self.pub_port,
        }

        data = json.dumps(payload)
        
        self.udp_send_socket.connect((self.broker_ip, self.broker_port))
        #self.udp_send_socket.sendto(data.encode(),(self.broker_ip, self.broker_port))
        self.udp_send_socket.sendall((data.encode()))
        #brocker_response = brocker_response.decode("utf-8")
        #print((f"Most recent response received {brocker_response[0]}:" 
        #    f"from{brocker_response[1]}"))