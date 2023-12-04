# Sahas Munamala
# Created: Thu Nov 30 2023, 1:55PM PST
# Host made to represent nodes with asynchronous send
# and receive pipes
import asyncio

from packet import DDLPacket

class DDLHost():
    def __init__(self, hostname, num_ports):
        self.hostname = hostname
        self.num_ports = num_ports
        self.send_queues = [asyncio.Queue() for _ in range(num_ports)]
        self.recv_queues = [asyncio.Queue() for _ in range(num_ports)]
        self.data_sent_events = [asyncio.Event() for _ in range(num_ports)]
    
    async def send_frame(self, port, data):
        if port < 0 or port >= self.num_ports:
            raise ValueError("Invalid port number")
        self.data_sent_events[port].set()
        await self.send_queues[port].put(data)
        print(f"{self.hostname} -- sent: {data} to port {port}")

    async def recv_frame(self, port):
        if port < 0 or port >= self.num_ports:
            raise ValueError("Invalid port number")
        data = await self.recv_queues[port].get()
        print(f"{self.hostname} -- received: {data} from port {port}")
        return data
    
    async def loopback(self, port):
        while True:
            data = await self.recv_frame(port)
            await self.send_frame(port, data)
    
    async def initiator(self, port):
        init_frame = DDLPacket(16, 16, 16, 16)
        await self.send_frame(port, init_frame)
        await self.loopback(port)

