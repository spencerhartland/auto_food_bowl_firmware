# Automatic Pet Food Bowl

**Note**: This project is a work in progress, it will change!

## Overview
This repository contains the firmware for a Raspberry-Pi-powered automatic pet food bowl written entirely in python. As of now, the food bowl is equipped with two OLED displays, a status LED, a 5kg load cell, and a Nema 17 stepper motor; the device's firmware contains drivers for each of these components. The goal is to have two processes running simultaneously: one to automatically dispense a specified amount of food at specified intervals, update displays, etc. Another running a web server listening for commands (dispense food, change preferences, etc).

## Modules
Below is a detailed discussion on each module in the firmware:

### Server (server/server.py)
Basic web server utilizing socket networking. Listens for requests on the local network that enable features like on-demand feeding and rich customization. This is the back bone of the iOS companion app. Code is a mess right now, I'm working on that!

#### Next Steps
- Add endpoints for adjusting feed schedule and getting food storage level.
- Clean up code and add documentation.

### Displays (displays/oled.py)
The two OLEDs are connected to the Pi via Adafruit's TCA9548A I^2^C Multiplexer.As such, the driver makes use of Adafruit's libraries for both the TCA9548A and the displays themselves (SSD1306). This driver provides functionality for both the food level and the status display.

#### Next Steps
- Implement status display functionality.

### Status LED (statusLight/led.py)
A simple LED driver that allows you to set any RGB value, blink an RGB value a specified number of times, or indicate an issue with a red glow.

### Load Cell (loadCell/)
Using a library I found on github (**will link later, gotta find it**). The intent is to weigh the container of food to determine the food level to display. As of now I need to work on calibration and getting a more stable value. Precision and accuracy aren't super important as I've abstracted the weight value into 4 levels, so it is not a huge task.

#### Next Steps
- Get calibration factor.
- Obtain stable values.
- Implement driver.

### Motor (motor/motor.py)
Uses RpiMotorLib to control the stepper connected via an A4988 driver. Current functionality allows food to be dispensed by specifying the number of full revolutions the motor will do.
