import argparse
import zmq

parser = argparse.ArgumentParser()
parser.add_argument("ports", type=int, nargs="+")
args = parser.parse_args()

context = zmq.Context()
data = b"aaaaaaaa"


def epn():
    socket_beat = context.socket(zmq.SUB)
    socket_beat.connect("tcp://localhost:%s" % "5556")
    socket_beat.setsockopt_string(zmq.SUBSCRIBE, "")

    socket_beat_send = context.socket(zmq.PUSH)
    socket_beat_send.connect("tcp://localhost:%s" % "5555")

    sockets = []

    for port in args.ports:
        print(port)
        socket = context.socket(zmq.PUSH)
        socket.connect("tcp://localhost:%s" % port)
        sockets.append(socket)

    while True:
        target = int(socket_beat.recv())
        print("Received Heartbeat")

        print("Sending data to {}".format(sockets[target]))
        sockets[target].send(data)

        socket_beat_send.send(str.encode("FLP {} is alive".format(-1)))


if __name__ == "__main__":
    epn()
