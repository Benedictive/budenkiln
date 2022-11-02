import os, sys
from time import sleep

fifofile = "/tmp/testFifo"
if not os.path.exists(fifofile):
    os.mkfifo(fifofile)

fifo = open(fifofile, 'w')

fifo.write("Test")
fifo.write(os.linesep)
fifo.flush()

while(True):
    text = input("Enter something:\n")
    print(repr(text))
    fifo.write(text)
    fifo.write(os.linesep)
    fifo.flush()