=======================
Interconnect components
=======================

-----------------------
Simplebus Interconnect
-----------------------

The simplebus interconnect module is the centerpiece of the whole simplebus interface, it is a crosspoint that allows multiple masters and slaves
to communicate seamlessy, the block is fully templated through a custom `python/jinja2` script that allows the generation of specific modules
with any number of master and slaves for security and power consumption reasons this block acts as a router, blocking the propagation
of all the simplebus signals to all but the targeted nodes.

---------------------------
AXI stream tlast generator
---------------------------

This modules monitors the axi stream connected to it's input, and repets it to the output with the addition of a tlast signal, that is
asserted periodically after a parametrised number of transactions. It uses an internal 16 bit counter, allowing a maximum period between
assertions of 65535 transactions.
The block only supports the mandatory subset AXI stream signals (TDATA, TVALID, TREADY) at the input and (TDATA, TVALID, TREADY, TLAST) at
the output

-----------------------------
AXI stream traffic generator
-----------------------------

This module, part of the testing and validation infrastructure, is used as an axi stream data generator, the data are stored in an internal
pre-initialized RAM block. While the enable signal is asserterf each clock cycle a new sample is sent to the output axi stream interface.
If the data is needed at a lower rate, a periodically strobed enable signal can be used.

--------------------
AXI stream combiner
--------------------

This module is used to multiplex multiple AXI streams into a single one, the input ports have fixed priorities, thus in case of a collision
the one with the lowest index will prevail, **all others else will be ignored**. The block is fully templated through a custom `python/jinja2`
script allowing a combiner with an arbitrary number of ports to be generated as needed. The input and output axi streams interface are also
customizable thanks to the parametrised width

----------------------------
AXI stream prioritised FIFO
----------------------------

This module allows to merge two different AXI streams of different priorities, while also completely mitigating the risk of transaction drops
due to conflicts between transactions, thanks to internal FIFOs on both inputs. The depth of whom is parametrised to allow the trade off between
area and flexibility.
The module will always privilege high priority transactions in spite anything else, it will thus empty the HP fifo before starting on the LP one.
no amount of round robin arbitration between inputs is performed, thus enough downstream bandwidth should be available if starvation of the LP
input is to be avoided.

-----------------
APB to Simplebus
-----------------

This module provides a simple combinatorial, bidirectional bridge between an APB master and a Simplebus slave interface.

------------
DMA manager
------------

This module can be used to initialize and operate a Xilinx AXI DMA IP in order to allow completely autonomous data trasnfer from an AXI stream,
to the main external system memory (DDR3 DRAM) without any involvement by the processor cores, that are only notified of a completed transaction
through an interrupt.