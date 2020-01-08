=======================
Interconnection types
=======================

The backbone of any complex system on chip design is undoubtedly the interconnect system that stiches together
all the IP modules allowing various modules and subsystems to communicate together in a reliable and orederly
fashon. It is thus not surprising that several families of interconnection technologies have been introduced
over time by many vendors. As it is expected each solution is tailored to different kind of applications, depending
on each one's need.

---------
ARM AXI
---------

One of the industry wide standard interconnect families is ARM's AMBA, used in all designs including ARM processing
cores and IP blocks. The most popular specification from this family is the AXI (Advanced eXtensible Interface), which
is also used on the Zynq System on Chip as the only communication method betweeen programmable logic and processing system.
The main application this interconnect technology has been designed is, in multicore systems, the connection of several
processor cores among themselves and with other high bandwidth peripherals, like graphics processors and high speed communication
interfaces. It is apparent that several features of this interconnection system are specifically designed to allow
efficient and substained transfer of large blocks of data. This specific focus introduces a large ammount of complexity,
requiring separate adress, data and response channels, a large number of support signals. It is thus apparent that for the
applications that this system is designed to cater to, where data transfers are small and sporadic, all these features
add a large amount of unecessary complexity, and their use should be avoided whenever possible.

---------
ARM APB
---------

A second type of interconnect, from the same family, used to connect lower bandwidth peripherals is the
APB (Advanced Peripheral Bus). Its design is much simpler, with a bus topology, and a much smaller feature set with a much lower
complexity in the connected modules, and a smaller footprint overall. Another advantage of this bus is the availability
of conversion ip compatible with the previously mentioned AXI bus, avoiding the need to interface directly with it.

----------
Simplebus
----------

The large majority of the implemented components use this custom interconnect interface, It has an equivalent feature set with
respect to APB, and it is heavily influenced by the altera Avalon bus (of which is a loose subset), a bidirectional bridge towards
APB is available allowing it to be connected with the rest of the system. To complete a read or write transaction the master sets up
the required signals and then pulses the appropriate strobe signal high for a single clock cycle, if the slave is not ready
for another transaction it can pull the ready signal low and keep it so until it is.

**READ CYCLE**

.. figure:: ../assets/sb_read.svg
   :scale: 50 %

   Read cycle timing diagram

**WRITE CYCLE**

.. figure:: ../assets/sb_write.svg
   :scale: 50 %

   Write cycle timing diagram
