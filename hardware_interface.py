import board
from digitalio import DigitalInOut, Direction
import adafruit_max31855

class HardwareInterface():
    def __init__(self) -> None:
        self._spi = board.SPI()
        self._cs_pin = DigitalInOut(board.CE0)
        self._max31855 = adafruit_max31855.MAX31855(self._spi, self._cs_pin)
        self._relais = DigitalInOut(board.D15)
        self._relais.direction = Direction.OUTPUT

    def get_temperature(self) -> float:
        return self._max31855.temperature

    def set_relais(self, setting) -> None:
        self._relais.value = setting