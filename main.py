# This is the program running 24/7 that controls all foodbowl logic.

import RPi.GPIO as GPIO
from motor import motor
from displays import oled
from statusLight import led
from time import sleep
import asyncio
import sys
import os

# Constants
foodLevel = 0.6
initialWakeDelay = 3 # Should be 30
dispenseTime = 2
cycleDelay = 10 # should be 21600

# Set up display
display = oled.OLED()

# Boot image
display.displayBootImage()

# Set up status light
statusLight  = led.LED()
statusLight.blink(5, 100, 2, 0)

# Food level display startup sequence
display.animateFoodLevel(foodLevel)

# Status display startup sequence
# ...

# Set up motor
motor = motor.Motor()

# Main loop
while True:
    try:
        # Check food weight
        # ...
        # Decided if food needs to be dispensed
        # ...
        # Dispense food
        motor.dispenseFood(1)
        print("Food dispensed")
        # Food dispensed notification
        statusLight.setValue(100, 8, 3)
        display.alertGlow()
        statusLight.setValue(0, 0, 0) # off
        # Update food level and display
        foodLevel = foodLevel - 0.1
        display.animateFoodLevel(foodLevel)
        # Dim the display after a little while
        sleep(2.0)
        display.dim(0)
        # Update status display
        # ...
        # Sleep for user's desired time
        sleep(cycleDelay)

    except KeyboardInterrupt:
        statusLight.cleanup()
        GPIO.cleanup()
        try:
            sys.exit(0)
        except:
            os._exit(0)
