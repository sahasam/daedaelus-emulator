import asyncio

from host import DDLHost
from link import DDLLink

async def main_one_link():
    host_a = DDLHost("Alice", num_ports=1)
    host_b = DDLHost("Bobby", num_ports=1)

    link = DDLLink('000', host_a, 0, host_b, 0)

    task1 = asyncio.create_task(host_a.loopback(0))
    task2 = asyncio.create_task(host_b.initiator(0))
    task3 = asyncio.create_task(link.run())

    await asyncio.gather(task1, task2, task3)
 


async def main_triangle():
    host_a = DDLHost("HOST_A", num_ports=2)
    host_b = DDLHost("HOST_B", num_ports=2)
    host_c = DDLHost("HOST C", num_ports=2)

    link_ab = DDLLink('0', host_a, 0, host_b, 0)
    link_ac = DDLLink('1', host_a, 1, host_c, 0)
    link_bc = DDLLink('2', host_b, 1, host_c, 1)

    tasks = [
        asyncio.create_task(host_a.initiator(0)),
        asyncio.create_task(host_a.initiator(1)),
        asyncio.create_task(host_b.loopback(0)),
        asyncio.create_task(host_b.loopback(1)),
        asyncio.create_task(host_c.loopback(0)),
        asyncio.create_task(host_c.initiator(1)),
        asyncio.create_task(link_ab.run()),
        asyncio.create_task(link_ac.run()),
        asyncio.create_task(link_bc.run())
    ]

    await asyncio.gather(*tasks)

#asyncio.run(main_one_link())
asyncio.run(main_triangle())
