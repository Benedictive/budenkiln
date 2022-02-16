from asyncio.subprocess import PIPE
from asyncio.windows_events import NULL
from socket import timeout
from django.apps import AppConfig
import subprocess
import sys


class BudenkilnConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'budenkiln'
    # TODO how to access in view
    hardware_controller = NULL

    def ready(self):
        if (self.hardware_controller is NULL):
            self.hardware_controller = subprocess.Popen([sys.executable, 'hardware_controller.py'], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
            # TODO communication
            self.hardware_controller.stdin.write('Test\n')
            self.hardware_controller.stdin.flush()
            result = self.hardware_controller.stdout.readline()
            print(result)
            #print(p.wait())