import board
from displays import ada_cp_ssd1306
from displays import adafruit_tca9548a
from PIL import Image
from time import sleep

class OLED:
    def __init__(self):
        # Create the I2C interface
        i2c = board.I2C()

        # Create teh TCA9548A object and give it the i2c bus
        self.tca = adafruit_tca9548a.TCA9548A(i2c)

        # Create the SSD1306 objects
        self.oled1 = ada_cp_ssd1306.SSD1306_I2C(128, 32, self.tca[0])
        self.oled2 = ada_cp_ssd1306.SSD1306_I2C(128, 32, self.tca[1])

    def clearDisplay(self, display):
        if display == 0:
                self.oled1.fill(0)
                self.oled1.show()
        elif display == 1:
                self.oled2.fill(0)
                self.oled2.show()

    def displayFoodLevel(self, level):
        # Calculate lines on display
        lines = int(128 * level)

        # Set the brightness
        self.oled1.contrast(100)
    
        for line in range(lines):
            # Create the line
            self.oled1.line(line, 0, line, 32, 1)
            
        # Show drawn lines
        self.oled1.show()
        # Wait a little
        sleep(0.045)
    
    def animateFoodLevel(self, level):
        # Calculate lines on display
        lines = int(128 * level)

        # Clear the display
        self.clearDisplay(0)

        # Set the brightness
        self.oled1.contrast(100)
    
        for line in range(lines):
            # Create the line
            self.oled1.line(line, 0, line, 32, 1)
            # Show line
            self.oled1.show()
            # Wait a little
            sleep(0.01)

    def alertGlow(self):
        # Clear the display
        self.clearDisplay(0)

        # Set brightness to 0
        self.oled1.contrast(0)

        # Turn all pixels on (still 0 brightness)
        self.oled1.fill(1)
        self.oled1.show()

        for repeat in range(5):
            # Slowly turn up brightness
            for percent in range(100):
                self.oled1.contrast(percent)
                sleep(0.015)

            sleep(0.15)

            # Slowly turn down brightness
            for percent in range(99, 0, -1):
                self.oled1.contrast(percent)
                sleep(0.02)
    
    def dim(self, display):
        for percent in range(99, 0, -1):
            if display == 0:
                self.oled1.contrast(percent)
            elif display == 1:
                self.oled2.contrast(percent)
            
            sleep(0.005)

    def displayBootImage(self):
        image = Image.open("/home/pi/developer/src/displays/boot.bmp")
        image = image.convert("1")
        self.oled1.image(image)
        self.oled1.show()
