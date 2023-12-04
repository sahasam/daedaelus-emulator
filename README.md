# Daedaelus Simulator

Python proof of concept of a link simulator. Uses an event loop to simulate parallell handling of packets
on links and ports.

* link.py - simulates a link by piping packets from one host's queue to another
* host.py - simulates a fpga host by taking in and sending out packets as fast as possible
* packet.py - shallow wrapper of a byte-packed struct

## Running

    python3 main.py

Uncomment the routine you want to run. currently just loops packets endlessly until you hit ^C.
