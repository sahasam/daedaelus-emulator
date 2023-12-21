import asyncio

import networkx as nx

from ddl.emulator import DDLEmulator

emulator = None

async def main_plane(rows, cols):
    global emulator
    # rows x cols fully connected mesh graph
    G = nx.Graph()
    G.add_nodes_from([
        (i, {"hname":f'HOST_{i}', "num_ports":8}) for i in range(rows*cols)
    ])
    edges = []
    for i in range(rows*cols):
        if (i%cols==0 and (i/cols)<rows-1):
            edges += [(i, i+1), (i,i+cols), (i, i+cols+1)]
        elif (i%cols==0):
            edges += [(i, i+1)]
        elif (i%cols < cols-1) and (i/cols) < rows-1:
            edges += [(i, i+cols-1), (i, i+cols), (i, i+cols+1), (i, i+1)]
        elif (i%cols == cols-1) and (i/cols) < rows-1:
            edges += [(i, i+cols-1), (i, i+cols)] 
        elif (i/cols) == rows-1 and i%cols < cols-1:
            edges += [(i, i+1)]
    G.add_edges_from(edges)

    emulator = DDLEmulator(G)
    emulator.add_link_probe(0)
    emulator.add_link_probe(4)
    # emulator.add_link_probes(edges[0]) # generate log in form of image, of all packets on given link
    await asyncio.gather(*emulator.tasks)

asyncio.run(main_plane(15,15))


