**************************
Interconnect components
**************************

======================
Simplebus
======================

^^^^^^^^^^^^^^^^^^^^^^^
Interconnect
^^^^^^^^^^^^^^^^^^^^^^^

    The simplebus interconnect module is the centerpiece of the whole simplebus interface, it is a crosspoint that allows multiple masters and slaves
    to communicate seamlessy, the block is fully templated through a custom `python/jinja2` script that allows the generation of specific modules
    with any number of master and slaves for security and power consumption reasons this block acts as a router, blocking the propagation
    of all the simplebus signals to all but the targeted nodes.
    
    .. warning:: The following connections are an example for a 2 master 2 slave module.

    **PARAMETERS**

        - **SLAVE_1_LOW**: Slave interface 1 address space low bound. Default value 0x00000000
        - **SLAVE_1_HIGH**: Slave interface 1 address space high bound. Default value 0xffffffff
        - **SLAVE_2_LOW**: Slave interface 2 address space low bound. Default value 0x00000000
        - **SLAVE_2_HIGH**: Slave interface 2 address space high bound. Default value 0xffffffff
        
    **INPUTS**

        - **clock**: Main clock input

    **INTERFACES**
        - **master_1** Simplebus interface to the first master
        - **master_2** Simplebus interface to the second master
        - **slave_1** Simplebus interface to the first slave
        - **slave_2** Simplebus interface to the second slave
      
^^^^^^^^^^^^^^^^^
APB to Simplebus
^^^^^^^^^^^^^^^^^

    This module provides a simple combinatorial, bidirectional bridge between an APB master and a Simplebus slave interface.


    **PARAMETERS**

    - **READ_LATENCY**: Number of cycles between read transaction start and response arrival. Default value 2

    **INPUTS**

    - **PCLK**: Main clock input
    - **PRESETn**: Active low synchronous reset input

    **INTERFACES**

    - **apb** AMBA APB interface towards the master
    - **spb** Simplebus interface to the downstream modules

    
^^^^^^^^^^^^^^^^^^^^^^^^
Configurator
^^^^^^^^^^^^^^^^^^^^^^^^
    
    This module provides a simple combinatorial, bidirectional bridge between an APB master and a Simplebus slave interface.

    **PARAMETERS**

    - **N_CONFIG**: Number of configuration values to write. Default value 2

    **INPUTS**

    - **clock**: Main clock input
    - **start**: A high level pulse on this input triggers the configuration process
    - **config_address**: Array of the addresses to write the configurations to
    - **config_data**: Array of configuration data to write

    **OUTPUTS**

    - **done**: Flag raised upon completion of the configuration process.
    
    **INTERFACES**

    - **sb** Simplebus interface the configuration is written to.

        
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Simplebus Clock Domain Crossing (CDC)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    This module implemnts a handshaken clock domain crossing for a Simplebus interface.

    .. warning:: Only write transactions are supported.
    .. warning:: This module is Xilinx Specific.

    **INPUTS**

    - **in_clock**: Clock for the input domain
    - **out_clock**: Clock for the output domain
    - **reset**: Active low synchronous reset input
    
    **INTERFACES**

    - **in_sb** Simplebus interface input.
    - **out_sb** Simplebus interface output.
           

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ROM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    This utility module implements a Simplebus connecter read only memory area.
    
    **PARAMETERS**
    - **BASE_ADDRESS**: Base address for the Simplebus interface. Default value 0x43c00000

    **INPUTS**

    - **clock**: Main clock input
    - **reset**: Active low synchronous reset input

    **INTERFACES**

    - **sb** Simplebus interface.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
DMA master with an AXI stream output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    This module can be used to read values from a simplebus accessible memory location and transmit them on an axi stream interface. Performing
    what ammounts to a two dimensional dma trasfer. The source address is consequently composed by two parts, a channel related one, corresponding to
    the row index in a table view, and a destination offset, that corresponds to the column index. The module is designed to pull data from a femtocore processor
    and push it to an RTCU communication interface.
    
    **PARAMETERS**

    - **BASE_ADDRESS**: Base address of the simplebus accessible target memoty area. Default value 0x43c00000
    - **CHANNEL_OFFSET**: Offset between  the addresses of two contiguous memory cells in a column. Default value 0x0
    - **DESTINATION_OFFSET**: Offset of the target cell memory cell in its row. Default value 0x0
    - **CHANNEL_NUMBER**: Number of transfers in each DMA transactions. Default value 3
    - **SB_DELAY**: Delay between simplebus read transaction start and read data availability. Default value 5
    - **TARGET_ADDRESS**: Address for the message on the other end of the RTCU link. Default value 0x18
    - **SOURCE_CHANNEL_SEQUENCE**: Array of row indexes to read from, usefull to reorder data. Default value {3,2,1}
    - **TARGET_CHANNEL_SEQUENCE**: Array of values for the AXI stream destination field. Default value {3,2,1}

    **INPUTS**

    - **clock**: Main clock input.
    - **reset**: Active low synchronous reset input.
    - **enable**: A high value on this input triggers a dma transaction sequence.
    
    **INTERFACES**

    - **source** Simplebus interface to the DMA endpoint.
    - **target** AXI stream output interface


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
DMA master with an AXI stream input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    This module can be used to axi stream received values to a Simplebus accessible memory location. It can perform two dimentional dma transfers
    with the simplebus target address being composed of two parts, a channel related one, corresponding to
    the row index in a table view, and a destination offset, that corresponds to the column index. The module is designed to push data from an axi stream
    to a femtocore processor.
    
    **PARAMETERS**

    - **BASE_ADDRESS**: Base address of the simplebus accessible target memoty area. Default value 0x43c00000
    - **CHANNEL_OFFSET**: Offset between  the addresses of two contiguous memory cells in a column. Default value 0x0
    - **DESTINATION_OFFSET**: Offset of the target cell memory cell in its row. Default value 0x0
    - **CHANNEL_NUMBER**: Number of transfers in each DMA transactions. Default value 3
    - **SB_DELAY**: Delay between adjacent simplebus write transactions. Default value 3
    - **LAST_DESTINATION**:  Index of the last destination value in an axi stream group of data defining a transaction. Default value 
    - **FIFO_DEPTH**: Depth of the FIFO used to temporarily hold the AXI stream received data while it is bein transmitted on the Simplebus. Default value {3,2,1}
    - **CHANNEL_SEQUENCE**: Array of values defining the row of the data table to write to. Default value {3,2,1}

    **INPUTS**

    - **clock**: Main clock input.
    - **reset**: Active low synchronous reset input.
    - **enable**: A high value on this input triggers a dma transaction sequence.
    
    **OUTPUT**
    - **done**: Flag raised when a full transaction has been compleated
    
    **INTERFACES**

    - **source** Simplebus interface to the DMA endpoint.
    - **target** AXI stream output interface

    
======================
AXI stream
======================

        
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 AXI stream Clock Domain Crossing (CDC)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    This module provvides clock domain crossing for an axi stream interface. two implementations are provvided, a simpler flip-flop based one
    which is lower latency and consumes less area, but is more fragile and a more robust handshaken one that takes more time and area.

    .. warning:: Some features of this module are Xilinx Specific.

    **PARAMETERS**

    - **CDC_STYLE**: Type of Clock domain crossing implementation ( FF for flip-flop based, HANDSHAKE for handshaken) Default Value FF
    - **N_STAGES**: Number of flip-flop stages used for the FF implementation. Default value 3
    - **DATA_WIDTH**: Width of the axi stream data signal. Default value 32
    - **USER_WIDTH**: Width of the axi stream user signal. Default value 32
    - **DEST_WIDTH**: Width of the axi stream destination signal. Default value 32

    **INPUTS**

    - **in_clock**: Clock for the input domain
    - **out_clock**: Clock for the output domain
    - **reset**: Active low synchronous reset input
    
    **INTERFACES**

    - **in** AXI stream input interface.
    - **out** AXI stream  output interface.

^^^^^^^^^^^^^^^^^
Combiner
^^^^^^^^^^^^^^^^^

    This module is used to combine combine AXI streams into a single one, the input ports have fixed priorities, thus in case of a collision
    the one with the lowest index will prevail, **all others else will be ignored**. The block is fully templated through a custom `python/jinja2`
    script allowing a combiner with an arbitrary number of ports to be generated as needed. The input and output axi streams interface are also
    customizable thanks to the parametrised width

    **PARAMETERS**

    - **INPUT_DATA_WIDTH**: Width of the input axi stream data signal. Default value 16
    - **OUTPUT_DATA_WIDTH**: Width of the output axi stream data signal. Default value 32
    - **MSB_DEST_SUPPORT**: Put the Lowest significant byte of the axi stream destination signal in the most significant byte of the output stream. Default value TRUE
    - **N_CHANNELS**: Number of combined AXI streams. Default value 6

    **INPUTS**

    - **clock**: Main clock input.
    - **reset**: Active low synchronous reset input.
  
    **INTERFACES**

    - **stream_in_1** AXI stream input to combine number 1.
    - **stream_in_2** AXI stream input to combine number 2.
    - **stream_out** Combined axi stream output interface.

^^^^^^^^^^^^^^^^^
Constant
^^^^^^^^^^^^^^^^^

    This module is meant to push a constant value to others through an AXI stream interface. A dedicated input can be used to 
    can be used to ensure Synchronization of the axi stream transaction with an external timebase signal. 

    **PARAMETERS**

    - **BASE_ADDRESS**: Base address for the Simplebus interface. Default value 0x43C00000
    - **CONSTANT_WIDTH**: Width of the output axi stream data signal. Default value 32

    **INPUTS**

    - **clock**: Main clock input.
    - **reset**: Active low synchronous reset input.
    - **sync**: Synchronization input, AXI stream write transactions will be delayed until a high signal is present on this line.

    **INTERFACES**

    - **sb** Simplebus slave interface for configuration and control
    - **const_out** AXI stream output interface


    .. toctree::
        :maxdepth: 1

        register_maps/interconnects/axis_constant



^^^^^^^^^^^^^^^^^
prioritised FIFO
^^^^^^^^^^^^^^^^^

    This module allows to merge two different AXI streams of different priorities, while also completely mitigating the risk of transaction drops
    due to conflicts between transactions, thanks to internal FIFOs on both inputs. The depth of whom is parametrised to allow the trade off between
    area and flexibility.
    The module will always privilege high priority transactions in spite anything else, it will thus empty the HP fifo before starting on the LP one.
    no amount of round robin arbitration between inputs is performed, thus enough downstream bandwidth should be available if starvation of the LP
    input is to be avoided.

    **PARAMETERS**

    - **FIFO_DEPTH**: Depth of the FIFO. Default value 16
    - **INPUT_DATA_WIDTH**: Width of the axi stream data signal. Default value 32

    **INPUTS**

    - **clock**: Main clock input.
    - **reset**: Active low synchronous reset input.
    - **data_in_lp**: Low priority AXI stream input data signal.
    - **data_in_lp_valid**: Low priority AXI stream input valid signal.
    - **data_in_lp_tlast**: Low priority AXI stream input tlast signal.
    - **data_in_hp**: High priority AXI stream input data signal.
    - **data_in_hp_valid**: High priority AXI stream input valid signal.
    - **data_in_hp_tlast**: High priority AXI stream input tlast signal.
    - **data_out_ready**: AXI stream output ready signal.


    **OUTPUT**

    - **data_in_lp_ready**: Low priority AXI stream input ready signal.
    - **data_in_hp_ready**: High priority AXI stream input ready signal.
    - **data_out**: AXI stream output data signal.
    - **data_out_valid**: AXI stream output valid signal.
    - **data_out_tlast**: AXI stream output tlast signal.

^^^^^^^^^^^^^^^^^
XPM FIFO
^^^^^^^^^^^^^^^^^

    This module provvides a simple AXI stream FIFO, implemented through Xilinx parametrised Macros.
    
    .. warning:: This module is Xilinx Specific.

    **PARAMETERS**

    - **FIFO_DEPTH**: Depth of the FIFO. Default value 16
    - **INPUT_DATA_WIDTH**: Width of the axi stream data signal. Default value 32
    - **INPUT_DEST_WIDTH**: Width of the axi stream destination signal Default value 16

    **INPUTS**

    - **clock**: Main clock input.
    - **reset**: Active low synchronous reset input.

    **INTERFACES**

    - **in** AXI stream input interface
    - **out** AXI stream output interface


^^^^^^^^^^^^^^^^^
FIFO
^^^^^^^^^^^^^^^^^

    This module provvides a simple AXI stream FIFO, implemented as simple behavioural system verilog code.

    **PARAMETERS**

    - **FIFO_DEPTH**: Depth of the FIFO. Default value 16
    - **DATA_WIDTH**: Width of the axi stream data signal. Default value 32
    - **DEST_WIDTH**: Width of the axi stream destination signal Default value 16
    - **USE_WIDTH**: Width of the axi stream user signal Default value 16

    **INPUTS**

    - **clock**: Main clock input.
    - **reset**: Active low synchronous reset input.

    **INTERFACES**

    - **in** AXI stream input interface
    - **out** AXI stream output interface



^^^^^^^^^^^^^^^^^
Limiter
^^^^^^^^^^^^^^^^^

    This module saturates the value of the axi stream data passing through it.


    **PARAMETERS**

    - **BASE_ADDRESS**: Base address for the Simplebus interface. Default value 0x43C00000

    **INPUTS**

    - **clock**: Main clock input.
    - **reset**: Active low synchronous reset input.

    **INTERFACES**

    - **in** AXI stream input interface
    - **out** AXI stream output interface
    - **sb**: Simplebus slave interface for control and configuration
  
    .. toctree::
        :maxdepth: 1

        register_maps/interconnects/axis_limiter


^^^^^^^^^^^^^^^^^
MUX
^^^^^^^^^^^^^^^^^

    This module selects one of many input axi streams

    **PARAMETERS**

    - **DATA_WIDTH**: Width of the axi stream data signal. Default value 32

    **INPUTS**

    - **clock**: Main clock input.
    - **reset**: Active low synchronous reset input.
    - **address**: Index of the selected axi stream.
  
    **INTERFACES**

    - **stream_in_1**: AXI stream input number 1
    - **stream_in_2**: AXI stream input number 2
    - **stream_out**: AXI stream output


^^^^^^^^^^^^^^^^^
Register slice
^^^^^^^^^^^^^^^^^

    This module adds a configurable ammount of delay stages to an axi stream. When N_STAGES is set to 1 this module can be also used 
    as a register to break up a combinatorial path during timing closure.

    **PARAMETERS**

    - **DATA_WIDTH**: Width of the axi stream data signal. Default value 32
    - **DEST_WIDTH**: Width of the axi stream destination signal. Default value 32
    - **USER_WIDTH**: Width of the axi stream user signal. Default value 32
    - **N_STAGES**: Number of delay stages. Default value 1
    - **READY_REG**: When set to 1 the ready signal is delayed as wello. Default value 0

    **INPUTS**

    - **clock**: Main clock input.
    - **reset**: Active low synchronous reset input.

    **INTERFACES**

    - **in**: AXI stream input
    - **out**: AXI stream output


^^^^^^^^^^^^^^^^^^^^^^
Synchronized repeater
^^^^^^^^^^^^^^^^^^^^^^

    This module is used to synchronize an axi stream to an external timebase. Since no buffering is present, the Synchronization
    signal frequency must be the same or higher than the axi stream data transmission rate, otherwise transactions will be dropped.

    **PARAMETERS**

    - **DATA_WIDTH**: Width of the axi stream data signal. Default value 32
    - **DEST_WIDTH**: Width of the axi stream destination signal. Default value 32
    - **USER_WIDTH**: Width of the axi stream user signal. Default value 32

    **INPUTS**

    - **clock**: Main clock input.
    - **reset**: Active low synchronous reset input.
    - **sync**: Synchronization signal input

    **INTERFACES**

    - **in**: AXI stream input
    - **out**: AXI stream output


^^^^^^^^^^^^^^^^^
Tlast Generator
^^^^^^^^^^^^^^^^^

    This modules monitors the axi stream connected to it's input, and repets it to the output with the addition of a tlast signal, that is
    asserted periodically after a parametrised number of transactions. It uses an internal 16 bit counter, allowing a maximum period between
    assertions of 65535 transactions.
    The block only supports the mandatory subset AXI stream signals (TDATA, TVALID, TREADY) at the input and (TDATA, TVALID, TREADY, TLAST) at
    the output

    **PARAMETERS**

    - **DATA_WIDTH**: Width of the axi stream data signal. Default value 32
    - **DEST_WIDTH**: Width of the axi stream destination signal. Default value 32
    - **USER_WIDTH**: Width of the axi stream user signal. Default value 32

    **INPUTS**

    - **clock**: Main clock input.
    - **reset**: Active low synchronous reset input.
    - **period**: period of the tlast signal
    - **in_data**: AXI stream input data signal.
    - **in_valid**: AXI stream input valid signal.
    - **out_ready**: AXI stream output ready signal.
    
    **OUTPUT**
    - **in_ready**: AXI stream input ready signal.
    - **out_data**: AXI stream output data signal.
    - **out_valid**: AXI stream output valid signal.
    - **out_tlast**: AXI stream output tlast signal.


^^^^^^^^^^^^^^^^^
traffic generator
^^^^^^^^^^^^^^^^^

    This module, part of the testing and validation infrastructure, is used as an axi stream data generator, the data are stored in an internal
    pre-initialized RAM block. While the enable signal is asserterf each clock cycle a new sample is sent to the output axi stream interface.
    If the data is needed at a lower rate, a periodically strobed enable signal can be used.


    **PARAMETERS**

    - **DATA_WIDTH**: Width of the axi stream data signal. Default value 32
    - **DEST_WIDTH**: Width of the axi stream destination signal. Default value 32
    - **USER_WIDTH**: Width of the axi stream user signal. Default value 32

    **INPUTS**

    - **clock**: Main clock input.
    - **reset**: Active low synchronous reset input.
    - **enable**: period of the tlast signal
    - **traffic_ready**: AXI stream output ready signal.

    **OUTPUT**

    - **traffic_data**: AXI stream output data signal.
    - **traffic_valid**: AXI stream output valid signal.
