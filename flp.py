import argparse
import time
import zmq

parser = argparse.ArgumentParser()
parser.add_argument("code")
parser.add_argument("ports", metavar="ports", type=int, nargs="+")
args = parser.parse_args()

context = zmq.Context()
sockets = []

for port in args.ports:
    socket = context.socket(zmq.PAIR)
    socket.connect("tcp://localhost:%s" % port)
    sockets.append(socket)

while True:
    print("Sent Data")

    for socket in sockets:
        socket.send(str.encode("Data from FLP {}".format(args.code)))

    time.sleep(1)
