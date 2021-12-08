
*********************************
General System level components
*********************************

======================
AXI terminator
======================

This utility module is used to terminate a processor AXI interface correctly responding to transactions to avoid hanging the bus.

**INPUTS**

- **clock**: Main clock input.
- **reset**: Active low synchronous reset input.

**INTERFACES**

- **axi**: AXI interface to terminate

======================
dma_manager
======================

This module can be used to initialize and operate a Xilinx AXI DMA IP in order to allow completely autonomous data transfer from an AXI stream,
to the main external system memory (DDR3 DRAM) without any involvement by the processor cores, that are only notified of a completed transaction
through an interrupt.

**PARAMETERS**

- **DMA_BASE_ADDRESS**: Base address of the target DMA manager. Default value 0x40400000
- **C_M00_AXI_ADDR_WIDTH**: Width of the AXI address signals. Default value 32
- **C_M00_AXI_DATA_WIDTH**: Width of the AXI data signals. Default value 32

**INPUTS**

- **clock**: Main clock input
- **reset**: Active low synchronous reset input
- **enable**: Enable signal for the DMA manager
- **start_dma**: This signal triggers the start of the DMA process.
- **dma_done**: Signal indicating the completion of a DMA transfer.
- **transfer_size**: Size of the DMA transfer to perform
- **buffer_base_address**: Base address of the buffer to transfer the data to

**OUTPUTS**

- **m00_axi_error**: flag indicating an AXI interface error
- **m00_axi_txn_done**: flag indicating the completion of an AXI transaction

**INTERFACES**

- **simple_bus**: Simplebus slave Interface for configuration and control
- **data_in**: AXI stream slave interface for input data
- **data_out**: AXI stream master interface for output data


.. _enable_gen:

======================
Enable Generator
======================

    .. image:: ../assets/Enable_gen.svg

    |

    This templated block implements an enable signals generator with and arbitrary number of output signals.
    It is implemented as a simple up counter that feeds a battery of compare registers.
    Each one of them has two modes of operation, clock and trigger mode, in the first one the comparator
    output will be high from the match to the end of the cycle, in trigger mode the output is only pulsed
    on and off for a single clock cycle.

    **PARAMETERS**

        - **BASE_ADDRESS**: Base address for the Simplebus interface. Default value 0x43C00000
        - **COUNTER_WIDTH**: Width of the enable signals generator counter. Default value 32

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
femtoCore (fCore)
======================

    femtoCore embedded DSP, see dedicated documentation for more info.

**PARAMETERS**

- **FAST_DEBUG**: When set to TRUE the instruction store content is initialized by reading INIT_FILE instead of through the AXI interface. Default value TRUE
- **INIT_FILE**: Path of the fast debug instruction store initialization file. Default value init.mem
- **DMA_BASE_ADDRESS**: Base address of the dma enpoint Simplebus interface. Default value 0x43c00000
- **INSTRUCTION_STORE_SIZE**: Maximum number of words that can be held in the instruction store. Default value 4096
- **INSTRUCTION_WIDTH**: Width of a single instruction Default value 32
- **DATAPATH_WIDTH**: Width of the main data path.  Default value 32
- **ALU_OPCODE_WIDTH**: Size of the ALU opcode.  Default value 5
- **OPCODE_WIDTH**: Size of the opcode.  Default value 5
- **REGISTER_FILE_DEPTH**: Number of registers for each channel in the register file. Default value 32
- **MAX_CHANNELS**: Maximum number of channels supported by the core. Default value 4 

**INPUTS**

- **clock**: Main clock input
- **reset**: Active low synchronous reset input
- **run**: Trigger to start the execution of the core

**OUTPUTS**

- **done**: Flag indicating the completion of the execution of the program

**INTERFACES**

- **sb**: Simplebus slave Interface for configuration and control of the uScope control unit
- **axi**: AXI interface to the instruction store for femtoCore programming
- **axis_dma**: AXI stream interface granting direct write address to the core registers

======================
uScope
======================

This module implements the uScope real time capture features.

**PARAMETERS**

- **BASE_ADDRESS**: Base address of the uScope Simplebus. Default value 0x40400000
- **TH_BASE_ADDRESS**: Width of the AXI address signals. Default value 32
- **N_TRIGGERS**: Width of the AXI data signals. Default value 32

**INPUTS**

- **clock**: Main clock input
- **reset**: Active low synchronous reset input
- **dma_done**: Signal indicating the completion of a DMA transfer.

**OUTPUTS**

- **trigger_out**: output trigger signals

**INTERFACES**

- **sb**: Simplebus slave Interface for configuration and control of the uScope control unit
- **th_sb**: Simplebus slave Interface for configuration and control of the trigger hub
- **in_1**: AXI stream slave input channel 1
- **in_2**: AXI stream slave input channel 2
- **in_3**: AXI stream slave input channel 3
- **in_4**: AXI stream slave input channel 4
- **in_5**: AXI stream slave input channel 5
- **in_6**: AXI stream slave input channel 6
- **in_7**: AXI stream slave input channel 7
- **in_8**: AXI stream slave input channel 8
- **out**: AXI stream interface to the DMA IP
- **dma_axi**: AXI lite interface to control the DMA IP