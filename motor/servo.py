import RPi.GPIO as GPIO
from time import sleep

# Constants
motorPin = 23 # BCM
dutyCycleValue = 15

class Servo:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(motorPin, GPIO.OUT)
        self.pwm = GPIO.PWM(motorPin, 50)

    def spinFor(self, seconds):
        self.pwm.start(0)
        self.pwm.ChangeDutyCycle(dutyCycleValue)
        sleep(seconds)
        self.pwm.stop()
        GPIO.cleanup()

def dispense(seconds):
    servo = Servo()
    servo.spinFor(seconds)
