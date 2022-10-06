import RPi.GPIO as GPIO
from time import sleep
from lib import RpiMotorLib

class Motor:

    # Driver values
    direction_pin = 24
    step_pin = 25
    no_microstep = (-1, -1, -1)
    board_type = "A4988"

    # Motor values
    motor_clockwise = False
    motor_step_type = "Full"
    motor_num_steps = 200
    motor_step_delay = 0.005
    motor_lib_verbose = False
    motor_init_delay = 0.05

    def __init__(self):
        self.driver = RpiMotorLib.A4988Nema(
                self.direction_pin, 
                self.step_pin, 
                self.no_microstep, 
                self.board_type
        )

    def dispenseFood(self, revolutions):
        total_steps = self.motor_num_steps * revolutions
        self.driver.motor_go(
                self.motor_clockwise, 
                self.motor_step_type, 
                total_steps, 
                self.motor_step_delay, 
                self.motor_lib_verbose, 
                self.motor_init_delay
        )
