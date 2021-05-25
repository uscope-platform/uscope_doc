****************************************************
Data acquisition and signal processing peripherals
****************************************************


======================
ADC post-processing
======================

    .. image:: ../assets/ADCprocessing.svg
    
    This module implements several common post-processing steps that can be enabled on an ADC channel. A decimation circuit sits at the heart of it,
    decoupling the ADC sample rate (that should be as high as possible to achieve better scope bandwidth) from the downstream data consumers. Two programmable window comparators
    denominated fast and slow monitor respectively the raw and filtered data stream and can trigger fault events. Both can be toggle between latching and hysteresis mode depending 
    on the application requirements. an output calibration block can be used to add a linearization constant, calibrating out any offsets from the analog domain
    
    
    |

    **PARAMETERS**

        - **BASE_ADDRESS**: Base address for the Sipmplebus interface. Default value 0x43C00000
        - **DATA_PATH_WIDTH**: Width of the data path. Default value 16
        - **DECIMATED**: Set to 0 for no decimation, set to 1 for standatd decimation, set to 2 for CIC/FIR decimation
        - **ENABLE_AVERAGE**: enable standard decimator averaging mode
      
    **INPUTS**

        - **clock**: Main clock input
        - **reset**: Active low synchronous reset input

    **OUTPUTS**

        - **fault**: Fault output for the associated ADC channel
        
    **INTERFACES**

        - **simple_bus**: Simplebus slave Interface for configuration and control
        - **data_in**: AXI stream slave interface for input data
        - **data_out**: AXI stream master interface for output data
      
    .. toctree::
        :maxdepth: 1

        register_maps/acquisition_signal_processing/adc_processing_regmap

======================
Standard decimator
======================

    This module is used to downsample an incoming input stream, by means of simple decimation. Since no image rejection filtering is
    performed, this approach can only be applied on properly band-limited signals to avoid the aliasign phenomenon. In addition to 
    straight 1 in n samples decimation averaging can also be used to enhance the output stream resolution.

    **PARAMETERS**

        - **MAX_DECIMATION_RATIO**: Maximum supported decimation ratio. Default value 
        - **DATA_WIDTH**: Width of the data path. Default value 16
        - **AVERAGING**: Set to 1 to enable averaging mode

    **INPUTS**

        - **clock**: Main clock input
        - **reset**: Active low synchronous reset input
        - **decimation_ratio**: Dynamic decimation ratio input

    **INTERFACES**

        - **data_in**: AXI stream slave interface for raw input data
        - **data_out**: AXI stream master interface for decimated output data


======================
Filtering Decimator
======================

    .. warning:: The tuning of the CIC and FIR filters is complex and highly application specific, the use of this module is only advised when strictly necessary to deal with aliasing problems.

    This module contains a filtering decimator, due to it's frequency characteristic it can be used on any input signal without aliasing.
    It is implemented as a CIC and FIR filter series, where the first provvides the bulk of attenuation while the second compensates
    its non-ideal frequenct characteristic.

    .. image:: ../assets/Decimator.svg

    |

    **INPUTS**

        - **clock**: Main clock input
        - **data_in_tdata**: input AXI stream slave data signal
        - **data_in_tvalid**: input AXI stream slave valid signal
        
    **OUTPUTS**

        - **data_in_tready**: input AXI stream slave ready signal
        - **data_out_tdata**: output AXI stream master data signal
        - **data_out_tvalid**: output AXI stream master valid signal


============================================
Multiphase Reference Generator
============================================


    This block implements a Direct Digital Synthesis (DDS) circuit that can be used to generate a set of sinusoids with arbitrary phase relationships
    and quadrature amplitudes. An internal angle generator can be used when an input angle signal is not present, whose frequency can be controlled through
    the Simplebus interface following the classic textbox relationships used for DDS synthesisers. A  monitoring angle output is provided 
    that always reports the currently in use angle (either taken from the input or self generated) for simplicity.

    **PARAMETERS**

        - **BASE_ADDRESS**: Base address for the Sipmplebus interface. Default value 0x43C00000
        - **DATA_PATH_WIDTH**: Width of the data path. Default value 16
        - **N_PHASES**: Number of output phases
      
    **INPUTS**

        - **clock**: Main clock input
        - **reset**: Active low synchronous reset input
        - **sync**: Synchronization input for the internal angle emulator
        - **Id**: Amplitude of the output direct axis component
        - **Iq**: Amplitude of the output quadrature axis component
        - **phase_shifts**: phase offsets of the output sinusoids from the reference angle

    **OUTPUTS**

        - **angle_emulation**: Flag raised when the ouput sinusoids are produced with a self generated angle
        
    **INTERFACES**

        - **simple_bus**: Simplebus slave Interface for configuration and control
        - **phase**: AXI stream slave interface for the input angle
        - **angle_out**: AXI stream master interface outputting the angle being used for the sinusoids generation
        - **reference_out** AXI stream master interface for the generated sinusoids
      
        .. toctree::
            :maxdepth: 1

            register_maps/acquisition_signal_processing/multiphase_ref_gen_regmap
