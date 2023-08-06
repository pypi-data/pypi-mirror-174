import time
from BirdBrain import Hummingbird
#from pygame.locals import *

from HummingbirdDualMotorDriver import *
from HummingbirdJoystick import *
from HummingbirdJoystickCalculator import *
from HummingbirdLedButton import *

class HummingbirdRobot:
    def __init__(self, motor_device = 'A', joystick_device = None, button_device = None, minimum_motor_speed = None, joystick_calculator = None,
            joystick_rotation = None, button_brightness_up = None, button_brightness_down = None):
        self.motor_device = motor_device
        self.joystick_device = joystick_device
        self.button_device = button_device
        self.minimum_motor_speed = minimum_motor_speed
        self.joystick_calculator = joystick_calculator
        self.joystick_rotation = joystick_rotation

        self.motors = None
        self.joystick = None
        self.button = None

        self.init_motors(motor_device, minimum_motor_speed)
        self.init_joystick(joystick_device, joystick_calculator, joystick_rotation)
        self.init_button(button_device)

    def init_motors(self, motor_device = 'A', minimum_motor_speed = None):
        if motor_device is not None: self.motor_device = motor_device

        if self.motor_device is not None:
            if self.minimum_motor_speed is None: self.minimum_motor_speed = HummingbirdDualMotorDriver.MINIMUM_SPEED

            try:
                self.motors = HummingbirdDualMotorDriver(self.motor_device, self.minimum_motor_speed)
            except ConnectionRefusedError:
                print("Motor device not available")
                raise

    def init_joystick(self, joystick_device = None, joystick_calculator = None, joystick_rotation = None):
        if joystick_device is not None: self.joystick_device = joystick_device

        if self.joystick_device is not None:
            if self.joystick_rotation is None: self.joystick_rotation = HummingbirdJoystick.DEFAULT_ROTATION

            try:
                self.joystick = None if self.joystick_device is None else HummingbirdJoystick(self.joystick_device, self.joystick_rotation)

                if self.joystick_calculator is None: self.joystick_calculator = HummingbirdJoystickCalculator()
            except ConnectionRefusedError:
                print("Joystick device not available")
                raise

    def init_button(self, button_device = None):
        if button_device is not None: self.button_device = button_device

        if self.button_device is not None:
            try:
                self.button = HummingbirdLedButton(self.button_device)
            except ConnectionRefusedError:
                print("LED button device not available")
                raise

    def move(self):
        if self.motors is not None:
            x, y = self.joystick.values()

            self.motors.move(self.joystick_calculator.speeds(x, y))

    def button_down(self, port):
        if self.button_device is None:
            return False
        else:
            return self.button.down(port)

    def button_up(self, port):
        return not self.button.down(port)
