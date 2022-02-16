from asyncio.subprocess import PIPE
from socket import timeout
from django.apps import AppConfig
import subprocess
import sys


class BudenkilnConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'budenkiln'

    def ready(self):
        p = subprocess.Popen([sys.executable, 'hardware_controller.py'], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
        # TODO communication
        #p.stdin.write('Test')
        print(p.wait())