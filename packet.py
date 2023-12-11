# Sahas Munamala
# Created: Thu Nov 30 2023, 7:51pm PST
import struct

class DDLPacket:
    def __init__(self, type):
        # INITIALIZATION PACKET
        #  PB   LL   SM   ST     PB   LL   SM   ST
        # 0x00 0x00 0x00 0x00   0x00 0x00 0x00 0x00
        self.slice0 = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.data   = bytearray(b'\x00'*56)
        self.rt_count = 0
        self.last_rt = 0

    def get_frame(self) -> bytes:
        return struct.pack('8B56x', *self.slice0)
    
    def swap(self) -> None:
        self.slice0[0:4], self.slice0[4:8] = self.slice0[4:8], self.slice0[0:4]