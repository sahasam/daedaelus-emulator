# Sahas Munamala
# Created: Thu Nov 30 2023, 2:13PM PST
# class that encapsulates a link by connecting send/receive
# pipes from two hosts
import asyncio
import numpy as np
from PIL import Image

class DDLLink:
    def __init__(self, host_a, port_a, host_b, port_b):
        self.host_a = host_a
        self.port_a = port_a
        self.host_b = host_b
        self.port_b = port_b
        self.link_state = 1

        self.record_link_history = False
        self.link_history = []
    
    def convert_to_binary_array(self, byte_array):
        # Convert each byte to its binary representation and flatten the array
        bit_array = np.array([int(bit) for byte in byte_array for bit in bin(byte)[2:].zfill(8)])
        return bit_array

    def generate_img(self, filename):
        print(self.link_history)

        # Define colors for alternating rows
        blue = (0, 255, 0)
        orange = (255, 0, 255)

        image_data = np.zeros((1920, 64, 3), dtype=np.uint8)

        # Fill the image data array
        for row_index, bits in enumerate(self.link_history):
            color = blue if row_index % 2 == 0 else orange
            for col_index, bit in enumerate(bits):
                if bit == 1:
                    image_data[row_index, col_index] = color
        
        image = Image.fromarray(image_data, 'RGB')
        image.save(filename)

    async def run(self):
        while True:
            # Transfer data from host A's port to host B's port
            if not self.host_a.send_queues[self.port_a].empty():
                data = await self.host_a.send_queues[self.port_a].get()
                if self.record_link_history:
                    self.link_history.append(self.convert_to_binary_array(data.slice0))
                    if len(self.link_history) > 1920:
                        self.generate_img('./host_0_link_0_trace.png')
                        self.record_link_history = False
                await self.host_b.recv_queues[self.port_b].put(data)
                self.host_a.data_sent_events[self.port_a].clear()

            # Transfer data from host B's port to host A's port
            if not self.host_b.send_queues[self.port_b].empty():
                data = await self.host_b.send_queues[self.port_b].get()
                if self.record_link_history:
                    self.link_history.append(self.convert_to_binary_array(data.slice0))
                    if len(self.link_history) > 1920:
                        self.generate_img(f'./{self.host_a.hostname}_{self.host_b.hostname}_trace.png')
                        self.record_link_history = False
                await self.host_a.recv_queues[self.port_a].put(data)
                self.host_b.data_sent_events[self.port_b].clear()

            # Transfer control back to event loop while waiting for new packets to move
            await asyncio.wait(
                [self.host_a.data_sent_events[self.port_a].wait(), self.host_b.data_sent_events[self.port_b].wait()],
                return_when=asyncio.FIRST_COMPLETED
            )
