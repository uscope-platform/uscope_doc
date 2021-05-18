.. _platform-overview:

==========================
Plaform overview
==========================

For the server platform a Linux based operating system was chosen, this
solution while requiring more upfront work, with respect to a bare metal
full custom application, has several advantages.

- Availiability of a large ammount of high quality open source infrastructure,
  both in the form of production grade server applications, development and
  deployment tools.
- Better longevity and manteinability due to the large degree of decoupling 
  between the operating system and rest of the stack, with possiblility of
  independent updates
- Fully featured networking stack with out of the box support for a wide array
  of both consumer and enterprise grade protocols.
- Better safety with full support of strong encryption.

As standard  practice in the embedded development community a custom distribution has 
been produced, through the toolchains and systems developed by the `Yocto project <https://www.yoctoproject.org>`_
along with several Xilinx developed meta layers, adding supoort for various Zynq specific software compoents and a custom one containing all 
remaining configurations and components.

----------------------------------
Kernel and drivers
----------------------------------

When using a fully fledged operating system, the userspace applications do not have
direct access to the hardware, as this is a prerogative of the kernel, this is true
not only for the hardware peripherials of the SoC but also for the soft
ones, implemented in the FPGA fabric. It is the responsibility of kernel device
drivers to expose them to the userspace through well defined interfaces.

For this reason a kernel level device drives is used, compiled as a loadable kernel module, that
handles all aspects of software-hardware communication. Among its responsibilities are:

- Handles configuration of the FPGA clock PLLs, by relaying user space requests to the kernel common clocking framework
- Allocation of the DMA buffer in main memory, used for real time data display and acquisition.
- Exposes the PS-PL AXI busses to userspace, allowing remotion, from the production kernel of the devmem interface.

The first function is exposed to userspace as a set of attributes that can be configured through the sysfs interface, while the others 
use standard character devices (/dev/uscope_data, /dev/uscope_BUS_0 and /dev/uscope_BUS_1). To easily access the various registers and peripherals
on the two busses the relative files need to be memory mapped (through the mmap() syscal), while the live data can be accessed through a simple read operation.

----------------------------------
Docker
----------------------------------


To ease development, deployment and increase security, all components of the management layer are containerized as follows.

- Frontend: In this container an nginx instance server the static files for the HMI layer (HTML, JS bundle, images, etc.) and proxies the RESTFUL API requests from the client to the python backend server. This component also acts as The SSL termination, as all subsequent traffic is between services on the same host.
- API SERVER: This container runs the pyhton server that acts as the backend for the HMI layer, it allows persistance of user generated data, and marshals hardware access requests to the driver.
- Postgres Database: This container enables persistance of the user generated data by storing it on non-volatile memory. The relational model of the database is instrumental for the role based authorization feature.
- Redis Databased: This database is used to mantain a coherent shared state between all the API server threads serving user requests. A NoSQL key-value data store is necessary in this role, as the performance of the main database is not enough for the main hot code path (scope data refresh)
- driver: This component handles low level access to the FPGA resources, sorting the captured data, etc.
  

To enhance security all communications between containers happen through a virtual internal network, completely separated from the insecure external connection. The docker engine has been selected as the container creation and management environment.
  