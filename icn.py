from multiprocessing import Process
import time
import zmq

speed = 2

context = zmq.Context()


def ack():
    socket_ack = context.socket(zmq.PAIR)
    socket_ack.bind("tcp://*:%s" % "5554")

    while True:
        print(socket_ack.recv().decode())

def ack1():
    socket_ack = context.socket(zmq.PAIR)
    socket_ack.bind("tcp://*:%s" % "5555")

    while True:
        print(socket_ack.recv().decode())



def beat():
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % "5556")

    beat = 0

    log = []

    while True:
        beat += 1
        topic = "ack"
        messagedata = "Heartbeat: %d" % beat
        print("%s %s" % (topic, messagedata))
        socket.send_string("%s %s" % (topic, messagedata))
        time.sleep(speed)

if __name__ == "__main__":
    Process(target=beat).start()
    Process(target=ack).start()
    Process(target=ack1).start()
