from multiprocessing import Process
import argparse
import time
import zmq

parser = argparse.ArgumentParser()
parser.add_argument("epns", type=int)
args = parser.parse_args()

context = zmq.Context()
port = "5556"


def beat():
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)

    count = 0

    target = 0
    target_max = args.epns

    while True:
        count += 1
        data = "Ack - Heartbeat: {}".format(count)
        print(data)

        socket.send_string(str(target))

        target += 1
        if target == target_max:
            target = 0

        time.sleep(1)


def ack():
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:%s" % "5555")

    while True:
        data = socket.recv()
        print("Received: {}".format(data))


if __name__ == "__main__":
    Process(target=beat).start()
    Process(target=ack).start()
