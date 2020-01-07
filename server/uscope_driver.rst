.. _uscope_driver:

========================
µScope low level driver
========================

The first component in the µScope server stack is the low level driver, this
component is in charge of all the comunications between application server and
hardware. It's separation from the main server component is beneficial for
multiple reasons. First, it helps avoiding concurrency issues, in order to
improve responsiveness and page load times the main server uses multiple 
processes to serve multiple concurrent requests, the driver sitting between
them and the hardware provide a convenient centralised spot where to implement
all the required locking and serialization, avoiding the need to synch between 
multiple processes. A second advantage of this separation is the possibility
to use the most suitable programming language for each task.

----------------------
Simplebus access
----------------------

The main task the driver is designed to carry out is to allow the HMI to have
proxied access to the Simplebus bus that controls the custom logic portion of 
the stack. Two different type of access mode are allowed, the simple register 
read and write are used to read and write the values of a single 32 bit
memory mapped register through the bus. When two or more registers need to be
accessed the bulk read or write primitives are advised, as the communication
between driver and application server can introduce latency and concurrency issues
that can result unexpected behaviour in the custom logic.

-------------------------------------
On screen oscilloscope data handling
-------------------------------------

A second task the driver is designed to perform is the data handling for the
on screen oscilloscope. When in run mode, the driver simply collects the 
data from the in RAM DMA buffer and sends it over to the application server to be
transmitted to the client. When in single capture mode the data is instead
collected, ordered and stored in a buffer in the driver. Once the acquisition
is complete, The data is transmitted to the client in bulk. This intermediate
step, while adding complexity is necessary as the full stack is not fast enough
to handle capture at higher speeds.

-------------------------
Application server Interfaces
-------------------------

The driver communicates with the application server through two distinct interfaces.
Message passing through a couple of `Redis <https://redis.io/>`_ 
`PUB/SUB <https://redis.io/topics/pubsub>`_ mailbox pairs is used for both the
main control flow and when small ammount of data is needed, like in the case of
bulk register read and writes.

A shared memory interface is instead used instead when large ammount of data needs to be transfered
between processes, since for this use case redis is inefficient. In this case the application server writes
the data to a specific shared memory file, where they can be then read back from the other components,
as needed. this communication channel is unidirectional, since no large ammount of data need to be
sent from the client to the programmable logic. There are also no embedded flow control information
in the data itself, as the transfer is managed through messages passed through the above mentioned
interfaces.