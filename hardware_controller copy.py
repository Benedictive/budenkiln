from threading import Thread
from queue import Empty, Queue
from time import sleep
from time import time
import zmq
import signal

_kiln_service = None

class Controller(Thread):
    def __init__(self):
        self._input_queue = Queue()
        self._temperature_history = dict()
        self._shutdown = False
        self._loop_duration_s = 1
        self._max_error_duration_s = 15
        super(Controller, self).__init__()

    def set_temp_curve(self, curve):
        print("Set Curve: ", curve)
        self._input_queue.put_nowait(dict(curve))

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

    def shutdown(self):
        self._shutdown = True

    def run(self):
        # Start with relais off

        curve = {}
        start_time = time()

        # required for EMI resistance
        thermocouple_error_count=0

        try:
            while True:
                if self._shutdown:
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

        except:
            # Ensure deactivation of relais on error
            print("control loop terminating - shutting down heater power!")
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
                print("Huh")
                message = socket.recv()
                print("Rec req: {}".format(message))

                socket.send(b"World")
        except:
            print("Controller terminating - shutting down heater power!")
            raise

        self._controller.join()

        
def start():
    global _kiln_service

    print("HARDWARE CONTROLLER")

    if _kiln_service is None:
        _kiln_service = KilnService()
        _kiln_service.start()

start()
