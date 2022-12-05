import os
from threading import Thread
from queue import Empty, Queue
from time import sleep
from time import time

import zmq
import pickle
import signal

import board
from digitalio import DigitalInOut, Direction
import adafruit_max31855

_kiln_service = None

class Controller(Thread):
    def __init__(self):
        self._input_queue = Queue()
        self._temperature_history = dict()
        self._shutdown = False
        self._loop_duration_s = 1
        self._max_error_duration_s = 60
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
        return True

    def get_temp_history(self):
        return self._temperature_history

    """ TODO Change temp_hist to list of touples instead of dict
    def get_temp_recent_change(self):
        averaging_range = 5
        hist_count = len(self._temperature_history)
        if hist_count == 0:
            return 0
        else:
            limit = max(hist_count, averaging_range)
            for n in range(0, limit-1):
    """

    def relais_off(self):
        self.relais.value = False

    def shutdown(self):
        self._shutdown = True

    def run(self):
        # Start with relais off
        self.relais.value = False

        curve = {}
        start_time = time()

        # required for EMI resistance
        thermocouple_error_count=0

        try:
            while True:
                if self._shutdown:
                    self.relais_off()
                    break

                sleep(self._loop_duration_s)

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
                    if (thermocouple_error_count > (self._max_error_duration_s / self._loop_duration_s)):
                        self.relais.value = False
                        raise RuntimeError("Thermocouple short to ground!")
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

        except:
            # Ensure deactivation of relais on error
            print("control loop terminating - shutting down heater power!")
            self.relais_off()
            raise

class KilnService():
    def __init__(self):
        self._controller = Controller()
        self._controller.daemon = True

        self._shutdown = False

    def start(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        print("Start Controller Thread")
        self._controller.start()

        print("Start Controller Server")
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        try:
            # setup server
            # replace IP with ipc://<path> on linux
            socket.bind("tcp://*:5555")
            while True:
                message = socket.recv()
                request, content = self.parse_request(message)
                reply = self.instantiate_rpc(request, content)

                serialized_reply = pickle.dumps(reply)
                socket.send(serialized_reply)
        except:
            print("Controller terminating - shutting down heater power!")
            self._controller.relais_off()

        self._controller.join()
        if self._shutdown:
            print("Shutting down!")
            # TODO does not work without sudo while in user session, should work once in autostart
            os.system("systemctl poweroff")

    def parse_request(self, message):
        return pickle.loads(message)

    def instantiate_rpc(self, request, content):
        # technically allows (limited) remote code execution, maybe seal behind interface ?
        methodCall = getattr(self, request, self.unknown_member)
        return methodCall(content)
    
    def set_curve(self, curve):
        self._controller.set_temp_curve(curve=curve)

    def get_temp_history(self, content):
        return self._controller.get_temp_history()

    def unknown_member(self, content):
        return False

    def shutdown_kiln(self):
        self._shutdown = True
        self._controller.shutdown()
        
def start():
    global _kiln_service

    print("HARDWARE CONTROLLER")

    if _kiln_service is None:
        _kiln_service = KilnService()
        _kiln_service.start()

start()
