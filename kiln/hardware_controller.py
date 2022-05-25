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
from dbus.mainloop.glib import DBusGMainLoop

_kiln_service = None

class Controller(Thread):
    def __init__(self):
        self._input_queue = Queue()
        self._temperature_history = dict()
        super(Controller, self).__init__()
        # Setup Hardware IO
        spi = board.SPI()
        cs = DigitalInOut(board.CE0)
        self.max31855 = adafruit_max31855.MAX31855(spi, cs)
        self.relais = DigitalInOut(board.D15)
        self.relais.direction = Direction.OUTPUT

        self.relais.value = False

    def set_temp_curve(self, curve):
        print("Set Curve: ", curve)
        self._input_queue.put_nowait(dict(curve))

    def get_temp_history(self):
        return self._temperature_history

    def relais_off(self):
        self.relais.value = False

    def run(self):
        # Start with relais off
        self.relais.value = False

        curve = {}
        start_time = time()

        # required for EMI resistance
        thermocouple_error_count=0

        try:
            while True:
                # Check for new input curve
                try:
                    new_curve = self._input_queue.get_nowait()
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

                # Fetch temperature from probe
                try:
                    measured_temperature = self.max31855.temperature
                    print("Measured Temperature = {}".format(measured_temperature))
                    thermocouple_error_count=0
                except RuntimeError:
                    # Signal Noise due to EMI will occasionally confuse the MAX31855
                    # Assume actual error if error persists for long duration
                    print("Thermocouple error")
                    thermocouple_error_count+=1
                    if (thermocouple_error_count > 5):
                        self.relais.value = False
                        raise RuntimeError("Thermocouple short to ground!")
                    sleep(1)
                    continue

                current_second = time() - start_time
                # Log temperature
                self._temperature_history[current_second] = measured_temperature

                # Find start and end of current interval
                timestamps = sorted(curve.keys())
                first_point = second_point = list(timestamps)[0]
                for timestamp in timestamps:
                    if current_second >= timestamp:
                        first_point = timestamp
                        # ensures second_point is never before first in case last point in list is reached
                        second_point = timestamp
                    else:
                        second_point = timestamp
                        break

                # Find previous and next target temperature
                first_temp = curve[first_point]
                second_temp = curve[second_point]

                # Interpolate target temperature based on start and end temperature with current time
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
                #print(f"Target Temp at Time {current_second} = {target_temp}")
                absolute_accepted_error = target_temp * 0.01

                if measured_temperature < (target_temp - absolute_accepted_error):
                    self.relais.value = True
                elif measured_temperature > (target_temp + absolute_accepted_error):
                    self.relais.value = False

                sleep(1)
        except:
            # Ensure deactivation of relais on error
            print("control loop terminating - shutting down heater power!")
            self.relais_off()
            raise

class KilnService(dbus.service.Object):
    def __init__(self, conn, object_path):
        self._controller = Controller()
        self._controller.daemon = True

        dbus.service.Object.__init__(self, conn, object_path)

    
    @dbus.service.method("de.budenkiln.ControllerInterface",
                         in_signature='a{ii}', out_signature='')
    def SetCurve(self, curve):
        self._controller.set_temp_curve(curve=curve)

    @dbus.service.method("de.budenkiln.ControllerInterface",
                         in_signature='', out_signature='a{ii}')
    def GetTempHistory(self):
        return self._controller.get_temp_history()

    def start(self):
        print("Start Controller Thread")
        self._controller.start()

        print("Start DBus Interface")
        dbus_loop = GLib.MainLoop()
        try:
            dbus_loop.run()
        except:
            print("Controller terminating - shutting down heater power!")
            self._controller.relais_off()
            raise
        
def start():
    global _kiln_service

    print("HARDWARE CONTROLLER")

    if _kiln_service is None:
        DBusGMainLoop(set_as_default=True)
        session_bus = dbus.SessionBus()
        name = dbus.service.BusName("de.budenkiln.ControllerService", session_bus)

        _kiln_service = KilnService(session_bus , '/KilnService')
        _kiln_service.start()

start()
