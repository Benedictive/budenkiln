from socket import timeout
from django.apps import AppConfig
import hardware_controller


class BudenkilnConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'budenkiln'

    def ready(self):
        hardware_controller.start()