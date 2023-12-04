# Sahas Munamala
# Created: Thu Nov 30 2023, 7:51pm PST
import struct

class DDLPacket:
    def __init__(self, aProto=0, aLive=0, aState=0, aTrans=0):
        self.aProto = aProto
        self.aLive  = aLive
        self.aState = aState
        self.aTrans = aTrans

    def pack(self):
        return struct.pack('8B56x', self.aProto, self.aLive, self.aState, self.aTrans)