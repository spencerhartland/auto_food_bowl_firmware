import RPi.GPIO as GPIO
from time import sleep

# Pins
red = 17
green = 27
blue = 22
pins = (17, 27, 22)

class LED:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        for pin in pins: 
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
        self.pwmR = GPIO.PWM(red, 2000)
        self.pwmG = GPIO.PWM(green, 2000)
        self.pwmB = GPIO.PWM(blue, 2000)
        self.pwmR.start(0)
        self.pwmG.start(0)
        self.pwmB.start(0)

    def setValue(self, r, g, b): # 0-100
        self.pwmR.ChangeDutyCycle(r)
        self.pwmG.ChangeDutyCycle(g)
        self.pwmB.ChangeDutyCycle(b)

    def cleanup(self):
        self.pwmR.stop()
        self.pwmG.stop()
        self.pwmB.stop()
        GPIO.cleanup()

    def blink(self, repeat, r, g, b):
        for i in range(repeat):
            self.setValue(r, g, b)
            sleep(1.25)
            self.setValue(0, 0, 0)
            sleep(0.5)

    def redGlow(self):
        for repeat in range(3):
            for value in range(100):
                self.setValue(value, 0, 0)
                sleep(0.015)

            sleep(0.15)
        
            for value in range(99, 0, -1):
                self.setValue(value, 0, 0)
                sleep(0.02)

