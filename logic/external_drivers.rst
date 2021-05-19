====================
External Drivers
====================




--------------
AD2S1210
--------------

This modules acts as a "driver" handling the Analog Devices AD2S1210 (and similar) resolver to digital (RDC) converters, largely abstacing away their complexity.
A read of both speed and angle values can be simply triggered through a rising edge on the *read_speed* and *read_angle* input, with the result being presented on the
*data_out* axi stream. The Simplebus interface allows the configuration of the RDC internal registers and the clearing of eventual faults.


**PARAMETERS**

    - **BASE_ADDRESS**: Base address of the peripheral on the Simplebus. Default value 0x43c00000

**INPUTS**

    - **clock**: Main clock input
    - **reset**: Active low synchronous reset input
    - **read_angle**: Triggers the read of the angle measurement fron the RDC chip
    - **read_speed**: Triggers the read of the speed measurement fron the RDC chip
    - **MISO**: RDC SPI interface Master In Slave Out signal

**OUTPUTS**

    - **MOSI**: RDC SPI interface Master Out Slave In signal
    - **SS**: RDC SPI Slave Select signal
    - **SCLK**: RDC SLAVE SPI Clock signal
    - **R_RESET**: RDC RESET signal
    - **R_SAMPLE**: RDC Sample signal
    - **R_A**: RDC R_A signals
    - **R_RES**: RDC R_RES signals

**INTERFACES**

    - **data_out**: AXI stream master interface that carries the angles/speed values and eventual faults present on the RDC
    - **sb**: Simplebus slave interface for control and configuration
  
.. toctree::
    :maxdepth: 1

    register_maps/external_drivers/ad2s1210



--------------
SI5351
--------------

This module handles, in conjunction with an instance of the :ref:`I2C` module, the configuration of the Silicon Labs Si5351 clock generator IC.
The configuration to be written to the device is stored in a hardcoded map, requiring recompilation to vary the clock generator paraneters.


**PARAMETERS**

    - **BASE_ADDRESS**: Base address of the companion I2C module. Default value 0x43c00000
    - **WAIT_COUNT**: Number of clock cycles waited between subsequent writes
    - **AUTOMATED_WRITE_OFFSET**: offset of the I2C module automated write register

**INPUTS**

    - **clock**: Main clock input
    - **reset**: Active low synchronous reset input
    - **start**: Starts the configuration process
    - **slave_address**: Address of the Si5351 Clock generator

**OUTPUTS**

    - **done**: Flag that is raised once the configuration process has ended.
  
**INTERFACES**

    - **sb**: Simplebus master interface controlling the :ref:`I2C` module connected to the clock generator
  