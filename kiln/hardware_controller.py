from threading import Thread
from threading import Semaphore
import sys

val = ""
sema = Semaphore(value=1)

def input_handler():
    global val
    while True:
        data = sys.stdin.readline()
        sys.stdout.write("Reply: " + str(data))
        sys.stdout.flush()
        sema.acquire()
        val = 10
        sema.release()

thread = Thread(target=input_handler)
thread.start()
thread.join()
exit(val)