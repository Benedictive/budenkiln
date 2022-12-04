import zmq
import pickle
from time import sleep
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)
context = zmq.Context()

print("Conn")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

for req in range(10):
    print("Sending {}".format(req))
    data = {1:"text1", 2:"text2", req:"text{}".format(req)}
    message = ("setattr", data)
    serializedMessage = pickle.dumps(message)

    socket.send(serializedMessage)

    serializedReply = socket.recv()
    reply = pickle.loads(serializedReply)
    print("Rec {} : {}".format(req, reply))
    sleep(1)