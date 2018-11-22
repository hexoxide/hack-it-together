from multiprocessing import Process
import argparse
import zmq

parser = argparse.ArgumentParser()
parser.add_argument("port")
args = parser.parse_args()

context = zmq.Context()


def flp():
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:%s" % args.port)

    while True:
        data = socket.recv()
        print("Received: {}".format(data))


def icn():
    socket_beat = context.socket(zmq.SUB)
    socket_beat.connect("tcp://localhost:%s" % "5556")
    socket_beat.setsockopt_string(zmq.SUBSCRIBE, "")

    socket_beat_send = context.socket(zmq.PUSH)
    socket_beat_send.connect("tcp://localhost:%s" % "5555")

    while True:
        target = int(socket_beat.recv())
        print("Received Heartbeat")
        socket_beat_send.send(str.encode("EPN {} is alive".format(args.port)))


if __name__ == "__main__":
    Process(target=flp).start()
    Process(target=icn).start()
