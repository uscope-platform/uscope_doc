
*********************************
General System level components
*********************************

.. _enable_gen:

======================
Enable Generator
======================

    .. image:: ../assets/Enable_gen.svg

    |

    This templated block implements an enable generator with and arbitrary number of output signals.
    It is implemented as a simple up counter that feeds a battery of compare registers.
    Each one of them has two modes of operation, clock and trigger mode, in the first one the comparator
    output will be high from the match to the end of the cycle, in trigger mode the output is only pulsed
    on and of for a single clock cycle.

    **PARAMETERS**

        - **BASE_ADDRESS**: Base address for the Sipmplebus interface. Default value 0x43C00000
        - **COUNTER_WIDTH**: Width of the enable generator counter. Default value 32

    **INPUTS**

        - **clock**: Main clock input
        - **reset**: Active low synchronous reset input
        - **sb_address**: Simplebus slave address signal
        - **sb_read_strobe**: Simplebus slave read_strobe signal
        - **sb_write_strobe**: Simplebus slave write strobe signal
        - **sb_write_data**: Simplebus slave write data signal
        - **gen_enable_in**: Enable input signal

    **OUTPUTS**

        - **sb_ready**: Simplebus slave ready signal
        - **sb_read_data**: Simplebus slave read data signal
        - **enable_out_1**: Generated Enable signal #1
        - **enable_out_n**: Generated Enable signal #n

    .. toctree::
        :maxdepth: 1

        register_maps/system/enable_generator_regmap


======================
fCore
======================

======================
dma_manager
======================
This module can be used to initialize and operate a Xilinx AXI DMA IP in order to allow completely autonomous data trasnfer from an AXI stream,
to the main external system memory (DDR3 DRAM) without any involvement by the processor cores, that are only notified of a completed transaction
through an interrupt.

======================
AXI terminator
======================

======================
uScope
======================