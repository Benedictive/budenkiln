import os, sys
from time import sleep

fifofile = "/tmp/testFifo"
if not os.path.exists(fifofile):
    os.mkfifo(fifofile)

fifo = open(fifofile, 'r')

test = fifo.readline()

while (True):
    text = fifo.readline()
    print(repr(text))
    print(text, end="")