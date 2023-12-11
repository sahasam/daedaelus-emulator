# Sahas Munamala
# Created: Thu Nov 30 2023, 1:55PM PST
# Host made to represent nodes with asynchronous send
# and receive pipes
import asyncio
import time

from packet import DDLPacket

class DDLHost():
    def __init__(self, hostname, num_ports):
        self.hostname = hostname
        self.num_ports = num_ports
        self.send_queues = [asyncio.Queue() for _ in range(num_ports)]
        self.recv_queues = [asyncio.Queue() for _ in range(num_ports)]
        self.data_sent_events = [asyncio.Event() for _ in range(num_ports)]
        self.error = False
    
    async def send_pkt(self, port, data):
        if port < 0 or port >= self.num_ports:
            raise ValueError("Invalid port number")
        self.data_sent_events[port].set()
        await self.send_queues[port].put(data)
        # print(f"{self.hostname} -- sent: {data} to port {port}")

    async def recv_pkt(self, port):
        if port < 0 or port >= self.num_ports:
            raise ValueError("Invalid port number")
        data = await self.recv_queues[port].get()
        # print(f"{self.hostname} -- received: {data} from port {port}")
        return data
    
    async def host_loop(self, port):
        while True:
            pkt = await self.recv_pkt(port)

            # update slice0 in one step
            pkt = self.table_update(port, pkt, error=False)

            # return packet
            await self.send_pkt(port, pkt)
    
    async def initiator(self, port):
        init_frame = DDLPacket(type="init")
        await self.send_pkt(port, init_frame)
        await self.host_loop(port)
    
    def table_update(self, port, pkt, error=False):
        """slice0: [PB, LL, SM, ST,   PB, LL, SM, ST]"""

        slice0 = None
        match pkt.slice0:
            # INITIALIZE
            case       b'\x00\x00\x00\x00\x00\x00\x00\x00': # 0
                slice0 = bytearray([0x20, 0xC3, 0x01, 0x53,  0x20, 0x3C, 0x01, 0x93])
            

            # FORWARD (RT)
            case       b'\x20\xC3\x01\x53\x20\x3C\x01\x93': # 1
                if error: slice0 = bytearray([0x20, 0x3C, 0x01, 0x60,  0x20, 0xC3, 0x01, 0xA0])
                else:     slice0 = bytearray([0x20, 0x3C, 0x01, 0x5A,  0x20, 0xC3, 0x01, 0x9A])
            
            case       b'\x20\x3C\x01\x5A\x20\xC3\x01\x9A': # 2
                if error: slice0 = bytearray([0x20, 0xC3, 0x01, 0x63,  0x20, 0x3C, 0x01, 0xA3])
                else:     slice0 = bytearray([0x20, 0xA5, 0x01, 0x55,  0x20, 0x5A, 0x01, 0x95])
            
            case       b'\x20\xA5\x01\x55\x20\x5A\x01\x95': # 3
                if error: slice0 = bytearray([0x20, 0x5A, 0x01, 0x6C,  0x20, 0xA5, 0x01, 0xAC])
                else:     slice0 = bytearray([0x20, 0x5A, 0x01, 0x50,  0x20, 0xA5, 0x01, 0x90])
                
            case       b'\x20\x5A\x01\x50\x20\xA5\x01\x90': # 4
                pkt.rt_count += 1
                pkt.frequency = 1/(time.time() - pkt.last_rt)
                pkt.last_rt = time.time()
                print(f"{self.hostname}:{port} {round(pkt.frequency, 2)}Hz")

                if error: slice0 = bytearray([0x20, 0xA5, 0x01, 0x55,  0x20, 0x5A, 0x01, 0xA5])
                else:     slice0 = bytearray([0x00, 0x00, 0x00, 0x00,  0x00, 0x00, 0x00, 0x00])
                
    
            # REVERSE (RT)
            case       b'\x20\xA5\x01\x55\x20\x5A\x01\xA5': # 6
                slice0 = bytearray([0x20, 0x5A, 0x01, 0x6C,  0x20, 0xA5, 0x01, 0xAC])
            
            case       b'\x20\x5A\x01\x6C\x20\xA5\x01\xAC': # 7
                slice0 = bytearray([0x20, 0xC3, 0x01, 0x63,  0x20, 0x3C, 0x01, 0xA3])
            
            case       b'\x20\xC3\x01\x63\x20\x3C\x01\xA3': # 8
                slice0 = bytearray([0x20, 0x3C, 0x01, 0x60,  0x20, 0xC3, 0x01, 0xA0])
            
            case       b'\x20\x3C\x01\x60\x20\xC3\x01\xA0': # 9
                slice0 = bytearray([0x00, 0x00, 0x00, 0x00,  0x00, 0x00, 0x00, 0x00])
            

            # BREAK
            case _:
                slice0 = bytearray([0x0f, 0x0f, 0x0f, 0x0f,  0x0f, 0x0f, 0x0f, 0x0f])
    
        pkt.slice0 = slice0
        return pkt
    

    


    

