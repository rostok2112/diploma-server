import asyncio
import json
import websockets
from environment import settings, redis_conn

             
class WebSocketServer:
    def __init__(self, host="", port=settings.WS_SERVER_PORT):
        self.host = host
        self.port = port
        self.redis_conn = redis_conn
        self.websocket_connections = []

    async def handler(self, websocket, path):
        self.websocket_connections.append(websocket)   
        while True:
            try:
                message = await websocket.recv()
                await websocket.send("Message from server: " + message)
                await asyncio.sleep(0.0001)
            except Exception as e:
                self.websocket_connections.remove(websocket)
                break

    async def broadcast(self, message):
        await asyncio.gather(*[
            websocket.send(message) 
            for websocket in self.websocket_connections
        ])
    
    async def redis_listener(self):
        pubsub = self.redis_conn.pubsub()
        await pubsub.psubscribe("__keyspace@0__:euler_degs")
        while True:
            try:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message:
                    event = message['data'].decode('utf-8')
                    if event == 'set':
                        data = await self.redis_conn.get('euler_degs')
                        if data:
                            data = data.decode('utf-8')
                            await self.broadcast(data)
                await asyncio.sleep(0.0001)
            except Exception as e:
                pass
                   
    async def run(self):
        print("\n\nPress Ctrl-C to exit...\n\n")
        asyncio.create_task(self.redis_listener())
        async with websockets.serve(self.handler, self.host, self.port):
            await asyncio.Future()  # run forever