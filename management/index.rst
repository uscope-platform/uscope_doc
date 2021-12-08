=======================
Management Layer
=======================

The uPlatform platform server, referred as server from now on, is the component
of the stack that is responsible for all the high level interactions between
the control platform hardware and the outside world, and in particular it is the
component in charge of the human machine interface (HMI). For easier 
deployment the whole server infrastructure is implemented in the processor
system of the Zynq SoC and it interfaces the outside world through standard 
Ethernet connectivity.

.. image:: ../assets/server_structure.svg

.. _management_layer:

.. toctree::
    :maxdepth: 2
    :caption: Management layer

    platform_overview
    layer_components
    API_reference
