#!/bin/bash
source .pyvenv/bin/activate
(python3 hardware_controller.py) & (python3 manage.py runserver 0.0.0.0:8000)