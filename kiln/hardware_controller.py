from threading import Thread
from queue import Queue

_controller = None

class Controller(Thread):
    def __init__(self):
        self._queue = Queue()
        super(Controller, self).__init__()

    def set_temp_curve(self, curve):
        self._queue.put_nowait({"curve": curve})

    def run(self):
        while True:
            # TODO implement 
            item = self._queue.get()
            print("GOT", item)
            print(item["curve"].temperaturepoint_set.all())

def set_temp_curve(curve):
    _controller.set_temp_curve(curve)

def start():
    global _controller

    print("HARDWARE CONTROLLER")

    if _controller is None:
        _controller = Controller()
        _controller.daemon = True
        _controller.start()

# Test
# start()
# set_temp_curve([1, 2, 3])