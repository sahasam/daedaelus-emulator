import asyncio

import networkx as nx
import websockets
import json

from host import DDLHost
from link import DDLLink

class DDLEmulator:
    def __init__(self, G:nx.Graph):
        self.G     = G
        self.hosts = []
        self.links = []
        self.clients = set()

        for i in range(len(G.nodes)):
            self.hosts.append(DDLHost(G.nodes[i]['hname'], G.nodes[i]['num_ports']))

        for edge in G.edges:
            host_0 = self.hosts[edge[0]].reserve_port('a')
            host_1 = self.hosts[edge[1]].reserve_port('b')
            
            # SHOULD BE ERROR HANDLED
            self.links.append(DDLLink(self.hosts[edge[0]], host_0, self.hosts[edge[1]], host_1))
            self.links.append(DDLLink(self.hosts[edge[1]], host_1, self.hosts[edge[0]], host_0))
        
        self.tasks = []
        for host in self.hosts:
            self.tasks += host.get_asyncio_loops()

        for link in self.links:
            self.tasks.append(asyncio.create_task(link.run()))
        
        self.tasks.append(asyncio.create_task(self.webserver()))

    # add new connections to subscriber group
    async def connection_handler(self, websocket):
        self.clients.add(websocket)
        print(f"New connection: {websocket}")
        try:
            async for message in websocket:
                print(message)
        finally:
            self.clients.remove(websocket)
    
    # broadcast message to subscribers
    async def notify_clients(self, message):
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])
    
    async def poll_network_state(self):
        poll_period = 1/20 # seconds
        while True:
            payload = {
                "nodes": [{"id": self.hosts[i].hostname} for i in range(len(self.hosts))],
                "links": [],
                "host_data": []
            }
            for edge in self.links:
                payload['links'].append({"source": edge.host_a.hostname, "target": edge.host_b.hostname})
                payload['links'].append({"source": edge.host_b.hostname, "target": edge.host_a.hostname})
            for host in self.hosts:
                payload['host_data'].append(host.get_state())

            # serialized_payload = json.dumps(payload)
            await self.notify_clients(json.dumps(payload))
            await asyncio.sleep(poll_period) # poll period in seconds
        
    async def webserver(self):
        async with websockets.serve(self.connection_handler, "localhost", 8765):
            await asyncio.gather(asyncio.Future(), self.poll_network_state())

async def main_one_link():
    G = nx.Graph()
    G.add_nodes_from([
        (0, {"hname": "HOST_A", "num_ports": 1}),
        (1, {"hname": "HOST_B", "num_ports": 1}),
    ])
    G.add_edges_from([
        (0,1)
    ])

    emulator = DDLEmulator(G)
    await asyncio.gather(*emulator.tasks)


async def main_triangle():
    G = nx.Graph()
    G.add_nodes_from([
        (0, {"hname": "HOST_A", "num_ports": 3}),
        (1, {"hname": "HOST_B", "num_ports": 3}),
        (2, {"hname": "HOST_C", "num_ports": 3})
    ])
    G.add_edges_from([
        (0,1),
        (0,2),
        (1,2)
    ])

    emulator = DDLEmulator(G)
    await asyncio.gather(*emulator.tasks)


async def main_quad():
    G = nx.Graph()
    G.add_nodes_from([
        (0, {"hname": "HOST_A", "num_ports": 3}),
        (1, {"hname": "HOST_B", "num_ports": 3}),
        (2, {"hname": "HOST_C", "num_ports": 3}),
        (3, {"hname": "HOST_D", "num_ports": 3})
    ])
    G.add_edges_from([
        (0,1), (0,2), (0,3),
        (1,2), (1,3), (2,3)
    ])

    emulator = DDLEmulator(G)
    await asyncio.gather(*emulator.tasks)

async def main_tensor():
    G = nx.Graph()
    G.add_nodes_from([
        (0, {"hname": "HOST_A", "num_ports": 8}),
        (1, {"hname": "HOST_B", "num_ports": 8}),
        (2, {"hname": "HOST_C", "num_ports": 8}),
        (3, {"hname": "HOST_D", "num_ports": 8}),
        (4, {"hname": "HOST_D", "num_ports": 8}),
        (5, {"hname": "HOST_D", "num_ports": 8}),
        (6, {"hname": "HOST_D", "num_ports": 8}),
        (7, {"hname": "HOST_D", "num_ports": 8}),
        (8, {"hname": "HOST_D", "num_ports": 8}),
    ])
    G.add_edges_from([
        (0,1), (0,3), (0,4),
        (1,2), (1,5), (1,4), (1,3),
        (2,5), (2,4),
        (3,4), (3,7), (3,6),
        (4,6), (4,7), (4,8), (4,5),
        (5,7), (5,8),
        (6,7), (7,8)
    ])

    emulator = DDLEmulator(G)
    await asyncio.gather(*emulator.tasks)

#asyncio.run(main_triangle())
# asyncio.run(main_quad())
asyncio.run(main_tensor())
