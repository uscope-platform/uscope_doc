====================================================
Data acquisition and signal processing peripherals
====================================================

--------------------
ADC post-processing
--------------------

    .. image:: ../assets/ADCprocessing.svg

    |

    **PARAMETERS**

        - **BASE_ADDRESS**:Base address for the Sipmplebus interface. Default value 0x43C00000
        - **DATA_PATH_WIDTH**: Width of the data path. Default value 16

    **INPUTS**

        - **clock**: Main clock input
        - **reset**: Active low synchronous reset input
        - **in_valid**: input AXI stream slave valid signal
        - **raw_data_in**: input AXI stream slave data signal
        - **out_ready**: output AXI stream master ready signal


    **OUTPUTS**

        - **data_out**: output AXI stream master data signal
        - **in_ready**: input AXI stream slave ready signal
        - **out_valid**: output AXI stream master valid signal
        - **out_tlast**: output AXI stream master tlast signal

    **INTERFACES**

        - **simple_bus**: Simplebus slave Interface

    .. toctree::
        :maxdepth: 1

        register_maps/acquisition_signal_processing/adc_processing_regmap



----------
Decimator
----------

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



