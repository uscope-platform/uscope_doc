.. _os-overview:

==========================
Operating system overview
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


Due to the peculiarities of both the hardware platform and the intended
application, the use of a standard Linux distribution was not possible,
as support for the Zynq SoC and the uZed platform are spotty, of difficult
deployment ansd thus the resulting systems are frequently out of date and
often impossible to update. To solve this problem a custom system was produced
using the `Yocto project <https://www.yoctoproject.org>`_, along with the
`meta-xilinx <https://github.com/Xilinx/meta-xilinx>`_ and `meta-xilinx-tools <https://github.com/Xilinx/meta-xilinx-tools>`_
layers.


----------------------------------
Kernel drivers and device tree
----------------------------------

When using a fully fledged operating system, the userspace applications do not have
direct access to the hardware, as this is a prerogative of the kernel, this is true
not only for the hardware peripherials of the SoC but also for the soft
ones, implemented in the FPGA fabric. It is the responsibility of kernel device
drivers to expose them to the userspace through well defined interfaces.

Unfortunately the development of a kernel driver for the custom logic requires
a deep understanding of how the kernel works, and also poses a manteinance challenge,
as the kernel's internal API are in constant evolution, requiring ongoing development
in order to avoid obsolescence. Undertaking such an effort must be thus avoided if 
absolutely possible.

Due to the peculiarities of both the hardware platform and the intended
application, the use of a standard Linux distribution was not possible,
as support for the Zynq SoC and the uZed platform are spotty, of difficult
deployment ansd thus the resulting systems are frequently out of date and
often impossible to update. To solve this problem a custom system was produced
using the `Yocto project <https://www.yoctoproject.org>`_, along with the
`meta-xilinx <https://github.com/Xilinx/meta-xilinx>`_ and `meta-xilinx-tools <https://github.com/Xilinx/meta-xilinx-tools>`_
layers.


----------------------------------
Kernel drivers and device tree
----------------------------------

When using a fully fledged operating system, the userspace applications do not have
direct access to the hardware, as this is a prerogative of the kernel, this is true
not only for the hardware peripherials of the SoC but also for the soft
ones, implemented in the FPGA fabric. It is the responsibility of kernel device
drivers to expose them to the userspace through well defined interfaces.

Unfortunately the development of a kernel driver for the custom logic requires
a deep understanding of how the kernel works, and also poses a manteinance challenge,
as the kernel's internal API are in constant evolution, requiring ongoing development
in order to avoid obsolescence. Undertaking such an effort must be thus avoided if 
absolutely possible.

To adress this specific issue the `Userspace I/O <https://www.kernel.org/doc/html/latest/driver-api/uio-howto.html>`_
subsystem was created it is aimed specifically to give developers access to custom hardware
directly from userspace without the need of a full kernel driver, as long as no interactions with other
subsystems is necessary.

To simplify the things even further a set of generic modules are already present in 
the kernel, thus allowing the use of a fully stock kernel when only memory mapped IO
and interrupts are required. Of these the `uio_pdrv` is used.

The mechanism used by the arm kernel for configuration and hardware discovery is the
Device three, a text document that is used to specify among other things, which peripherials
are connecteced, where are they placed in the address space and what interrupts do they raise.

In order to add support
To adress this specific issue the `Userspace I/O <https://www.kernel.org/doc/html/latest/driver-api/uio-howto.html>`_
subsystem was created it is aimed specifically to give developers access to custom hardware
directly from userspace without the need of a full kernel driver, as long as no interactions with other
subsystems is necessary.

To simplify the things even further a set of generic modules are already present in 
the kernel, thus allowing the use of a fully stock kernel when only memory mapped IO
and interrupts are required. Of these the `uio_pdrv` is used.

The mechanism used by the arm kernel for configuration and hardware discovery is the
Device three, a text document that is used to specify among other things, which peripherials
are connecteced, where are they placed in the address space and what interrupts do they raise.

To add support for the custom logic the following code was added to the default uZed/zynq device tree::

    TODO: ADD DEVICE TREE snippet
    TODO: ADD DEVICE TREE snippet
    TODO: ADD DEVICE TREE snippet

