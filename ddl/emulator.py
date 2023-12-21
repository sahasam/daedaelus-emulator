# Sahas Munamala
# Created: Sat Dec 16 2023, 9:16PM PST

import asyncio
import networkx as nx

from .host import DDLHost
from .link import DDLLink
from .websocket import DDLWebsocket

class DDLEmulator:
    def __init__(self, G:nx.Graph):
        self.G     = G
        self.hosts = []
        self.links = []
        self.probes = []

        for i in range(len(G.nodes)):
            self.hosts.append(DDLHost(G.nodes[i]['hname'], G.nodes[i]['num_ports']))

        for edge in G.edges:
            host_0 = self.hosts[edge[0]].reserve_port('a')
            host_1 = self.hosts[edge[1]].reserve_port('b')
            
            self.links.append(DDLLink(self.hosts[edge[0]], host_0, self.hosts[edge[1]], host_1))
        
        self.tasks = []
        for host in self.hosts:
            self.tasks += host.get_asyncio_loops()

        for link in self.links:
            self.tasks.append(asyncio.create_task(link.run()))


    def add_link_probe (self, edgeIndex):
        self.links[edgeIndex].record_link_history = True
        self.probes.append(edgeIndex)
    
    def dump_probes_data(self):
        for probeLinkIdx in self.probes:
            self.links[probeLinkIdx].generate_img(f'./probe_data_link_{probeLinkIdx}.png')

    
    def add_host(self, hostname, connections):
        pass

    def remove_host(self, hostname):
        pass

    def block_link(self, link, link_state):
        pass

    def clear_link(self, link):
        pass

    def get_instant_network_state(self):
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

        return payload
        
        
 
