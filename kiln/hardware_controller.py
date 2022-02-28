from threading import Thread
from queue import Empty, Queue
from time import sleep
from time import time

from gi.repository import GLib

import dbus
import dbus.service
import dbus.mainloop.glib

_controller = None

class Controller(Thread):
    def __init__(self):
        self._queue = Queue()
        super(Controller, self).__init__()

    def set_temp_curve(self, curve):
        print("Set Curve: ", curve)
        self._queue.put_nowait(dict(curve))

    def run(self):
        curve = {}
        start_time = time()
        while True:
            # TODO implement 
            try:
                new_curve = self._queue.get_nowait()
                print("GOT", new_curve)
                curve = new_curve
            except Empty:
                pass

            if len(curve) < 2:
                sleep(1)
                continue

            current_second = time() - start_time
            timestamps = sorted(curve.keys())

            for timestamp in timestamps:
                print(f"Enumerating {current_second}")
                if current_second >= timestamp:
                    first_point = timestamp
                else:
                    second_point = timestamp
                    break

            first_temp = curve[first_point]
            second_temp = curve[second_point]

            print(f"First Temp at Time {first_point} = {first_temp}")
            print(f"Second Temp at Time {second_point} = {second_temp}")

            sleep(1)

def set_temp_curve(curve):
    _controller.set_temp_curve(curve)

def start():
    global _controller

    print("HARDWARE CONTROLLER")

    if _controller is None:
        _controller = Controller()
        _controller.daemon = True
        _controller.start()

class KilnService(dbus.service.Object):
    
    @dbus.service.method("de.budenkiln.ControllerInterface",
                         in_signature='a{ii}', out_signature='')
    def SetCurve(self, curve):
        _controller.set_temp_curve(curve=curve)

    def start(self):
        dbus_loop = GLib.MainLoop()
        dbus_loop.run()
        

start()

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
session_bus = dbus.SessionBus()
name = dbus.service.BusName("de.budenkiln.ControllerService", session_bus)
service_object = KilnService(session_bus, '/KilnService')

dbus_loop = GLib.MainLoop()
print("Start Controller Thread")
dbus_thread = Thread(target=dbus_loop.run())
dbus_thread.daemon = True
dbus_thread.start()

while (True):
    sleep(0.1)