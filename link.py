# Sahas Munamala
# Created: Thu Nov 30 2023, 2:13PM PST
# class that encapsulates a link by connecting send/receive
# pipes from two hosts
import asyncio

class DDLLink:
    def __init__(self, link_name, host_a, port_a, host_b, port_b):
        self.link_name = link_name
        self.host_a = host_a
        self.port_a = port_a
        self.host_b = host_b
        self.port_b = port_b
        self.link_state = 1
    
    async def run(self):
        while True:
            # Transfer data from host A's port to host B's port
            if not self.host_a.send_queues[self.port_a].empty():
                data = await self.host_a.send_queues[self.port_a].get()
                await self.host_b.recv_queues[self.port_b].put(data)
                self.host_a.data_sent_events[self.port_a].clear()

            # Transfer data from host B's port to host A's port
            if not self.host_b.send_queues[self.port_b].empty():
                data = await self.host_b.send_queues[self.port_b].get()
                await self.host_a.recv_queues[self.port_a].put(data)
                self.host_b.data_sent_events[self.port_b].clear()

            # Transfer control back to event loop while waiting for new packets to move
            await asyncio.wait(
                [self.host_a.data_sent_events[self.port_a].wait(), self.host_b.data_sent_events[self.port_b].wait()],
                return_when=asyncio.FIRST_COMPLETED
            )
              
