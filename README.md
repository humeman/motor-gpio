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
### Direct GPIO example
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

### Websocket example
__**Server creation**__
```py
from utils import ws, gpio

gpio.start()

websocket = ws.WebsocketServer(
    requre_auth = True, # Enable/disable key authentication
    auth_keys = ["test"], # If auth is enabled, valid keys
    port = 5000 # Port to run on
)
websocket.start()
```

__**Sending messages**__

Messages should all be sent in JSON format.
To tell the socket what to do, specify the 'command' key.

#### Valid messages
__Turn on both motors__
```js
{
    "command": "set",
    "motors": [ // Don't have to specify both if you're not updating the state of the other.
        {
            "id": 1,
            "state": "forward" // Can be 'forward', 'backward', or 'stop'
        },
        {
            "id": 2,
            "state": "backward"
        }
    ],
    "autostart": true // Optional. If true, will automatically exit standby state.
}
```

__Change standby state__
```js
{
    "command": "standby",
    "standby": true // Or false, of course. True = stop running, False = begin running
}
```

__Stop everything__
```js
{
    "command": "stop"
}
```
