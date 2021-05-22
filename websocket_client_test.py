import websockets
import asyncio
import json

class WebsocketClient:
    def __init__(
            self,
            ip,
            key: str = None
        ):

        self.socket = None

        self.ip = ip

        if key:
            self.auth = {"key": key}

        else:
            self.auth = {}

    async def start(
            self
        ):

        self.socket = await websockets.connect(
            self.ip
        )

        recv_task = asyncio.get_event_loop().create_task(self.recv())
        send_task = asyncio.get_event_loop().create_task(self.send_loop())

        done, pending = await asyncio.wait(
            [recv_task, send_task],
            return_when = asyncio.FIRST_COMPLETED
        )

        for task in pending:
            task.cancel()

        print("Done")

    async def recv(
            self
        ):

        async for message in self.socket:
            print(message)

    async def send_loop(
            self
        ):

        await self.set(
            {1: "forward", 2: "forward"},
            True
        )

        await asyncio.sleep(1)

        await self.set(
            {1: "backward", 2: "backward"},
            True
        )

        await asyncio.sleep(1)

        await self.standby(True)
        await self.stop()

    async def set(
            self,
            motors: dict,
            autostart: bool = False
        ):

        comp = [
            {"id": motor_id, "state": state} for motor_id, state in motors.items()
        ]

        await self.socket.send(
            json.dumps(
                {
                    "command": "set",
                    "motors": comp,
                    "autostart": autostart,
                    **self.auth
                }
            )
        )

    async def standby(
            self,
            standby: bool
        ):

        await self.socket.send(
            json.dumps(
                {
                    "command": "standby",
                    "standby": standby,
                    **self.auth
                }
            )
        )

    async def stop(
            self
        ):

        await self.socket.send(
            json.dumps(
                {
                    "command": "stop",
                    **self.auth
                }
            )
        )

websocket = WebsocketClient(
    "ws://localhost:5000",
    key = "test"
)

asyncio.get_event_loop().run_until_complete(websocket.start())
asyncio.get_event_loop().run_forever()