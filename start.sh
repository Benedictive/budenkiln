#!/bin/bash
# Assumes an existing virtual environment in .pyvenv and that the necessary packages are installed.
(.pyvenv/bin/python3 -u hardware_controller.py) & (.pyvenv/bin/python3 kiln/manage.py runserver 0.0.0.0:8000)
