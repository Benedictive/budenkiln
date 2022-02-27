from threading import Thread
from queue import Queue
from time import sleep

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
        self._queue.put_nowait({"curve": curve})

    def run(self):
        curve = {}
        while True:
            # TODO implement 
            item = self._queue.get()
            print("GOT", item)

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