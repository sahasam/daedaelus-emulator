# Sahas Munamala
# Created: Thu Nov 30 2023, 7:51pm PST
import struct
import asyncio

class DDLPacket:
    def __init__(self, type):
        self.slice0 = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.data   = bytearray(b'\x00'*56)
        self.rt_count = 0
        self.last_rt = 0
        self.lock   = asyncio.Lock()