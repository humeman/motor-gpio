from utils import ws, gpio

gpio.setup()

websocket = ws.WebsocketServer(
    require_auth = True,
    auth_keys = ["test"],
    port = 5000
)

websocket.start()