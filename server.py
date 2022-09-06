import asyncio
import websockets
from websockets import WebSocketServerProtocol

class Server:
    clients = set()
    
    async def register(self, ws: WebSocketServerProtocol):
        self.clients.add(ws)
        print(ws, 'connected')
    
    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        print(ws, 'disconnected')
    
    async def send_to_clients(self, message: str):
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])
            print('sent "', message, '" to ', len(self.clients), ' clients')
    
    async def ws_handler(self, ws: WebSocketServerProtocol, url: str):
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            print('received "', message, '" from', ws)
            await self.send_to_clients(message)

server = Server()
start_server = websockets.serve(server.ws_handler, '10.1.40.52', 3000)
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()