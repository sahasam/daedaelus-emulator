import asyncio

import networkx as nx

from ddl.emulator import DDLEmulator
from ddl.websocket import DDLWebsocket

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
        (4, {"hname": "HOST_E", "num_ports": 8}),
        (5, {"hname": "HOST_F", "num_ports": 8}),
        (6, {"hname": "HOST_G", "num_ports": 8}),
        (7, {"hname": "HOST_H", "num_ports": 8}),
        (8, {"hname": "HOST_I", "num_ports": 8}),
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
    # websocket = DDLWebsocket('', 8765, emulator)
    async def snapshot():
        await asyncio.sleep(1)
        payload = emulator.get_instant_network_state()
        print(payload)
    await asyncio.gather(asyncio.create_task(snapshot()), *emulator.tasks)

# asyncio.run(main_triangle())
# asyncio.run(main_quad())
asyncio.run(main_tensor())
