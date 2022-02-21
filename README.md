# Budenkiln

Web-enabled hardening and tempering kiln for the forge.

## Requirements
See requirements.txt, or:  
`pip install -r requirements.txt`

### Using python venv
Create the virtual environment:  
`python3 -m venv .pyvenv`  
Environment names other than `.pyvenv` are possible, are not yet covered by `.gitignore` though.     
Activate the venv (linux - command will vary based on OS):  
`source .pyvenv/bin/activate`  
Then work like normal (i.e. pip install)  
Deactivate the venv:  
`deactivate`

## Django
Start server:  
`python3 manage.py runserver`

Setup Database:  
`python3 .\manage.py makemigrations budenkiln` (if required)  
`python3 .\manage.py migrate`

## Remote RasPi Development (VS Code)
1. Install `Remote - SSH` extension
2. Install `Python/Pylance` extension on remote host  
(open extension explorer, should show "Install in SSH: \<Host IP>")  

## TODO
- follow curve in `hardware_controller.py`
- handle curve submit with existing name
- watchdog ?
- switch relay based on actual temp vs target temp