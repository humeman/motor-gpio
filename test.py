from utils import gpio
import time

# Basic test
gpio.standby(True)

gpio.set_motor(1, "forward") # Set motor 1 to forward
gpio.set_motor(2, "forward")

gpio.standby(False)

time.sleep(1)

gpio.standby(True)

gpio.set_motor(1, "backward")
gpio.set_motor(2, "backward")

gpio.standby(False)

time.sleep(1)

gpio.stop()