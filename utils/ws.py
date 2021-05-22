"""
utils/ws.py

Websocket that allows for remote control of the motors.
For more information, see docs/Socket.md
"""

import websockets
import json
import asyncio

from utils import gpio

class WebsocketServer:
    def __init__(
            self,
            require_auth: bool = True,
            auth_keys: list = [],
            port: int = 5000
        ):

        self.auth = require_auth

        self.keys = auth_keys

        self.state = {
            "standby": True,
            "motor1": "stop",
            "motor2": "stop"
        }

        self.port = port

        self.registers = {
            "set": WebsocketRegisters.set,
            "standby": WebsocketRegisters.standby,
            "stop": WebsocketRegisters.stop
        }

    def start( 
            self
        ):

        asyncio.get_event_loop().run_until_complete(websockets.serve(self.recv, "0.0.0.0", self.port))
        asyncio.get_event_loop().run_forever()

    async def send(
            self,
            websocket,
            message
        ):

        await websocket.send(
            json.dumps(
                {
                    "success": True,
                    "message": message
                }
            )
        )

    async def error(
            self,
            websocket,
            message
        ):

        await websocket.send(
            json.dumps(
                {
                    "success": False,
                    "reason": message
                }
            )
        )

    async def recv(
            self,
            websocket,
            path
        ):

        async for message in websocket:
            try:
                data = json.loads(message)

            except:
                await self.error(websocket, "Invalid JSON data")
                continue

            # Check auth
            if self.auth:
                if "key" not in data:
                    await self.error(websocket, "Missing key")
                    continue

                if data["key"] not in self.keys:
                    await self.error(websocket, "Invalid key")
                    continue

            # Find command
            if "command" not in data:
                await self.error(websocket, "No command")
                continue

            command = data["command"]

            if command not in self.registers:
                await self.error(websocket, "Invalid command")
                continue

            try:
                await self.registers[command](websocket, data)

            except:
                await self.error(websocket, "An unexpected error occurred")

class WebsocketParsers:
    def verify(
            data,
            key,
            key_type
        ):

        return type(data.get(key)) == key_type

    def bulk_verify(
            data,
            keys
        ):

        for key, key_type in keys.items():
            if type(data.get(key)) != key_type:
                return False

        return True

class WebsocketRegisters:
    async def set(
            wsserver,
            websocket, 
            data
        ):

        if not WebsocketParsers.verify(data, "motors", list):
            await wsserver.error(websocket, "Missing key motors")
            return

        for motor in data["motors"]:
            if type(motor) != dict:
                await wsserver.error(websocket, "Motor must be a dict containing: id, state")
                return

            if not WebsocketParsers.bulk_verify(data, {"id": int, "state": str}):
                await wsserver.error(websocket, "Missing keys: id, state")
                return

            if data["id"] not in gpio.motors:
                await wsserver.error(websocket, f"Motor {data['id']} does not exist")
                return

            if data["state"] not in ["forward", "backward", "stop"]:
                await wsserver.error(websocket, f"Invalid sate {data['state']}")
                return

            gpio.set_motor(data["id"], data["state"])

            if data.get("autostart"):
                gpio.standby(False)

            await wsserver.send(websocket, f"Set motor states")

    async def standby(
            wsserver,
            websocket,
            data
        ):

        if not WebsocketParsers.verify(data, "standby", bool):
            await wsserver.error(websocket, "Missing key standby")
            return

        gpio.standby(data["standby"])

        await wsserver.send(websocket, f"Set standby to {data['standby']}")

    async def stop(
            wsserver,
            websocket,
            data
        ):

        gpio.stop()

        await wsserver.send(websocket, "Stopped controller")