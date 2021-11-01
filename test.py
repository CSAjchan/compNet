from broker import Broker
from publisher import Publisher
from subscriber import Subscriber
import time 


def main():
    broker = Broker("127.0.0.1", 49000)
    publisher_1 = Publisher("127.0.0.1", 49000, "127.0.0.1", 49001)
    publisher_2 = Publisher("127.0.0.1", 49000, "127.0.0.1", 49004)
    subscriber_1 = Subscriber("127.0.0.1", 49002, "127.0.0.1", 49000)
    subscriber_2 = Subscriber("127.0.0.1", 49003, "127.0.0.1", 49000)

    broker.listen()
    print("MAIN: Broker listening")
    subscriber_1.listen()
    subscriber_2.listen()
    print("MAIN: Both subscribers listening")

    subscriber_1.subscribe("IQ")
    subscriber_1.subscribe("5EX")
    subscriber_2.subscribe("IQ")

    print("MAIN: All subscribers subscribed to the relevant topics")

    publisher_1.publish("IQ", "friends","This guy has 0 iq(Vitali).")
    publisher_1.publish("5EX", "friends", "I am not dumb.")
    publisher_2.publish("IQ", "friends", "This guy has 400 iq(Pasha while pivo = true).")

    print("MAIN: Publisher sent all messages to broker")

    broker.sendMessage()

    subscriber_2.unsubscribe("IQ")
    publisher_2.publish("IQ", "friends", "No clue how much IQ this guy has(Anton).")

    print("End of main THREAD")

if __name__ == "__main__":
    main()