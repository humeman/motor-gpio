# motor-gpio
Simple motor controller script for sending commands to a TB6612 motor controller on a Raspberry Pi. Nothing fancy, just needed a basic script to handle motor output.

Pinouts can be changed in `utils/gpio.py`. Default is:
* Motor 1
    * PWMA: 7
    * AIN2: 11
    * AIN1: 12
* Motor 2
    * PWMB: 18
    * BIN1: 15
    * BIN2: 16
* Other
    * STBY: 13

## Usage
```py
from utils import gpio

gpio.setup() # Defines pinouts

# Set motor states
# States can be: forward, backward, stop
gpio.set_motor(1, "forward")
gpio.set_motor(2, "forward")

# Take it off of standby to start motors
gpio.standby(False)

# Wait a little
time.sleep(1)

# Pause
gpio.standby(True)

# Go backwards
gpio.set_motor(1, "backward")
gpio.set_motor(2, "backward")

# Unpause
gpio.standby(False)

# Wait
time.sleep(1)

# Shut it down
gpio.stop()
```