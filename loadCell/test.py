#!/usr/bin/env python3
import RPi.GPIO as GPIO
from hx711 import HX711
import sys
import time

try:
    GPIO.setmode(GPIO.BCM)

    hx = HX711 = HX711(dout_pin=26, pd_sck_pin=19)

    err = hx.zero()

    if err:
        raise ValueError("Tare unsuccessful.")

    reading = hx.get_data_mean(readings=30)
    if reading:
        print('Data subtracted by offset but still not converted to units:',
              reading)
    else:
        print('invalid data', reading)

    input('Put known weight on the scale and then press Enter')
    reading = hx.get_data_mean(readings=30)
    if reading:
        print('Mean value from HX711 subtracted by offset:', reading)
        known_weight_grams = input(
            'Write how many grams it was and press Enter: ')
        try:
            value = float(known_weight_grams)
            print(value, 'grams')
        except ValueError:
            print('Expected integer or float and I have got:',
                  known_weight_grams)

        ratio = reading / value  # calculate the ratio for channel A and gain 128
        hx.set_scale_ratio(ratio)  # set ratio for current channel
        print('Ratio is set.')
    else:
        raise ValueError('Cannot calculate mean value. Try debug mode. Variable reading:', reading)

    print("Now, I will read data in infinite loop. To exit press 'CTRL + C'")
    input('Press Enter to begin reading')
    print('Current weight on the scale in grams is: ')
    while True:
        print(hx.get_weight_mean(30), 'g')

except (KeyboardInterrupt, SystemExit):
    print('Bye :)')

finally:
    GPIO.cleanup()
