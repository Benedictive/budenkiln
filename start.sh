#!/bin/bash
source .pyvenv/bin/activate
(python3 -u hardware_controller.py) & (python3 kiln/manage.py runserver 0.0.0.0:8000)