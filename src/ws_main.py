import asyncio
from ws_server import WebSocketServer


if __name__ == "__main__":
    server = WebSocketServer()
    asyncio.run(server.run())