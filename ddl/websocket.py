# Sahas Munamala
# Created: Sat Dec 16 2023, 9:36PM PST

import asyncio
import json
import logging
import websockets

class DDLWebsocket:
    """Maintain connections, provide updates to user, """
    def __init__(self, interface, port, parent_emulator):
        self.interface = interface
        self.port = port
        self.parent_emulator = parent_emulator

        self.clients = set()

    async def connection_handler(self, websocket):
        """Setup new connections, add them to clients set, send them most up to date
        information"""
        self.clients.add(websocket)
        print(f"New connection: {websocket}") # TODO: change to logging

        try:
            async for message in websocket:
                print(message)
        finally:
            self.clients.remove(websocket)
    

    # broadcast message to subscribers
    async def notify_clients(self, message):
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])
    

    # TODO: change to event based notifications
    # instead of polling, only on an event being raised
    # by the emulator, should an update packet be sent.
    async def poll_network_state(self):
        poll_period = 1/2 # seconds
        while True:
            # serialized_payload = json.dumps(payload)
            await self.notify_clients('hello world')
            await asyncio.sleep(poll_period) # poll period in seconds


    async def run(self):
        async with websockets.serve(self.connection_handler, self.interface, self.port):
            await asyncio.gather(asyncio.Future(), self.poll_network_state())
