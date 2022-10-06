# Automatic Pet Food Bowl

> **Note**: This project is a work in progress, it will change!

## Overview
This repository contains the firmware for a Raspberry-Pi-powered automatic pet food bowl written entirely in python. As of now, the food bowl is equipped with two OLED displays, a status LED, a 5kg load cell, and a Nema 17 stepper motor; the device's firmware contains drivers for each of these components. The goal is to have two processes running simultaneously: one to automatically dispense a specified amount of food at specified intervals, update displays, etc. Another running a web server listening for commands (dispense food, chaneg preferences, etc).

## Modules
Below is a detailed description of each module in the firmware.

### Server (server/server.py)
A BARE-bones (seriously, just the bare minimum functionality) web server that listens for a GET request at the endpoint `/dispense`. Hitting the endpoint activates the stepper motor to dispense food on demand.

#### Next Steps
- Add ability to adjust dispense time using query parameters.
- Add ability to change preferences using query parameters.
- Implement an endpoint that returns satus info, including food level.

### Displays (displays/oled.py)

### Status LED (statusLight/led.py)

### Load Cell (loadCell/hx711.py)

### Motor (motor/motor.py)
