from multiprocessing import Process
import argparse
import zmq

parser = argparse.ArgumentParser()
parser.add_argument("code")
parser.add_argument("port")
parser.add_argument("beat")
args = parser.parse_args()

context = zmq.Context()
port_beat = "5556"
ack_beat = "ack"


def flp():
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:%s" % args.port)

    while True:
        print("Received: {}".format(socket.recv().decode()))


def icn():
    socket_beat = context.socket(zmq.SUB)
    socket_beat.connect("tcp://localhost:%s" % port_beat)
    socket_beat.setsockopt_string(zmq.SUBSCRIBE, ack_beat)

    socket_ack = context.socket(zmq.PAIR)
    socket_ack.connect("tcp://localhost:%s" % args.beat)

    while True:
        ack = socket_beat.recv()
        print("Received Heartbeat")
        socket_ack.send(str.encode("EPN {} is alive".format(args.code)))



if __name__ == "__main__":
    Process(target=flp).start()
    Process(target=icn).start()
