from utils import ws

websocket = ws.WebsocketServer(
    requre_auth = True,
    auth_keys = ["test"],
    port = 5000
)

websocket.start()