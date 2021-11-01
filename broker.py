import socket
import json
import threading
import dataclasses
import typing
import time

_DEFAULT_BUFFER_SIZE = 1024

#@dataclasses.dataclass
#class topics:
    #topic: str
    #sub_topics: typing.List[str]

@dataclasses.dataclass
class SubscriberData:
    sub_ip: int
    sub_port: int
    #topics: typing.List[topics]
    topics: typing.List[str]

class Broker:

    def __init__(self, broker_ip, broker_port):
        self.buffer_size = _DEFAULT_BUFFER_SIZE
        self.broker_ip = broker_ip
        self.broker_port = broker_port

        self.udp_send_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_listen_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_listen_socket.bind((self.broker_ip, self.broker_port))

        self.lock = threading.Lock()

        self.subscribers = {}
        self.messages = {}
        
    def sendMessage(self, ):
        thread = threading.Thread(target = Broker.sendMessage_Function, args = (self, ))
        thread.start()

    @staticmethod
    def sendMessage_Function(broker):
        while True:

            broker.lock.acquire()

            for topic, messages in broker.messages.items():

                if messages:
                    message = messages[0]

                    for subscriber, subscriberdata in broker.subscribers.items():
                        topics = subscriberdata.topics

                        if topic in topics:
                            sub_ip = subscriberdata.sub_ip
                            sub_port = subscriberdata.sub_port

                            broker.udp_send_socket.sendto(str.encode(message), (sub_ip, sub_port))               
                    
                    broker.messages[topic].pop(0)

            broker.lock.release()
                    
    def listen(self, ):
        thread = threading.Thread(target = Broker.listen_function, args = (self, ))
        thread.start()

    @staticmethod
    def listen_function(broker):
        while True:
            response = broker.udp_listen_socket.recvfrom(broker.buffer_size)[0]
            response = json.loads(response.decode())

            broker.lock.acquire()
            
            topic = response["topic"]
            type = response["type"]

            if type == "subscribe":
                sub_ip = response["sub_ip"]
                sub_port = response["sub_port"]

                if f"{sub_ip}:{sub_port}" in broker.subscribers:
                    if topic not in broker.subscribers[f"{sub_ip}:{sub_port}"].topics:
                        broker.subscribers[f"{sub_ip}:{sub_port}"].topics.append(topic)              
                else:
                    broker.subscribers[f"{sub_ip}:{sub_port}"] = SubscriberData(sub_ip, sub_port, [topic])

                print(f"Subscribed from: {sub_ip}:{sub_port} to topic: {topic}")

            elif type == "publish":
                pub_ip = response["pub_ip"]
                pub_port = response["pub_port"]
                sub_topic = response["sub_topic"] 
                message = response["message"]

                if topic in broker.messages:
                    broker.messages[topic].append(message)
                else:
                    broker.messages[topic] = [message]

                print(f"Published from: {pub_ip}:{pub_port} the message:{message}")

            elif type == "unsubscribe":
                sub_ip = response["sub_ip"]
                sub_port = response["sub_port"]

                if f"{sub_ip}:{sub_port}" in broker.subscribers:
                    if topic in broker.subscribers[f"{sub_ip}:{sub_port}"].topics:
                        broker.subscribers[f"{sub_ip}:{sub_port}"].topics.remove(topic)   

                print(f"Unsubscribed from: {sub_ip}:{sub_port} from topic: {topic}")  

            broker.lock.release()

