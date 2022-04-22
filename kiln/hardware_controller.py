from threading import Thread
from queue import Empty, Queue
from time import sleep
from time import time

import board
from digitalio import DigitalInOut, Direction
import adafruit_max31855

from gi.repository import GLib

import dbus
import dbus.service
import dbus.mainloop.glib

_controller = None

class Controller(Thread):
    def __init__(self):
        self._queue = Queue()
        self._temperature_history = dict()
        super(Controller, self).__init__()

    def set_temp_curve(self, curve):
        print("Set Curve: ", curve)
        self._queue.put_nowait(dict(curve))

    def get_temp_history(self):
        return self._temperature_history

    def run(self):
        spi = board.SPI()
        cs = DigitalInOut(board.CE0)
        max31855 = adafruit_max31855.MAX31855(spi, cs)
        relais = DigitalInOut(board.D15)
        relais.direction = Direction.OUTPUT

        relais.value = False

        curve = {}
        start_time = time()

        thermocouple_error_count=0
        while True:
            try:
                new_curve = self._queue.get_nowait()
                print("GOT", new_curve)
                curve = new_curve
                start_time = time()
                self._temperature_history = dict()
            except Empty:
                pass

            if len(curve) < 2:
                print("No curve set!")
                sleep(1)
                continue

            try:
                measured_temperature = max31855.temperature
                print("Measured Temperature = {}".format(measured_temperature))
                thermocouple_error_count=0
            except RuntimeError:
                # For some reason casing of thermocouple is connected to one terminal so sometimes when it first touches
                # the kiln metal casing it gets confused - error in case there is an actual connection to ground or smth
                print("Thermocouple error")
                thermocouple_error_count+=1
                if (thermocouple_error_count > 15):
                    relais.value = False
                    raise RuntimeError("Thermocouple short to ground!")
                sleep(0.1)
                continue

            current_second = time() - start_time
            # Log temperature
            self._temperature_history[current_second] = measured_temperature

            timestamps = sorted(curve.keys())

            for timestamp in timestamps:
                if current_second >= timestamp:
                    first_point = timestamp
                    # ensures second_point is never undefined in case last point in list is first_point
                    second_point = timestamp
                else:
                    second_point = timestamp
                    break

            first_temp = curve[first_point]
            second_temp = curve[second_point]

            points_temp_difference = second_temp - first_temp
            points_time_difference = second_point - first_point
            time_since_first_point = current_second - first_point
            if (points_time_difference > 0):
                target_temp = first_temp + (points_temp_difference * (time_since_first_point / points_time_difference) )
            else:
                # Curve is finished. Maintain last temperature setting
                target_temp = second_temp

            #print(f"First Temp at Time {first_point} = {first_temp}")
            #print(f"Second Temp at Time {second_point} = {second_temp}")
            print(f"Target Temp at Time {current_second} = {target_temp}")
            absolute_accepted_error = target_temp * 0.01

            if measured_temperature < (target_temp - absolute_accepted_error):
                relais.value = True
            elif measured_temperature > (target_temp + absolute_accepted_error):
                relais.value = False
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

    @dbus.service.method("de.budenkiln.ControllerInterface",
                         in_signature='', out_signature='a{ii}')
    def GetTempHistory(self):
        return _controller.get_temp_history()

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
