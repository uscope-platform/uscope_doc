====================
Control peripherals
====================

.. _pwm_gen:

--------------
PWM Generator
--------------

lorem ipsum


    .. image:: ../assets/PwmGenerator.svg

    |

    **PARAMETERS**

        - **BASE_ADDRESS**:Base address for the Sipmplebus interface. Default value 0x43C00000
        - **COUNTER_WIDTH**: Width of the pwm generator counter. Default value 16

    **INPUTS**

        - **clock**: Main clock input
        - **reset**: Active low synchronous reset input
        - **sb_address**: Simplebus slave address signal
        - **sb_read_strobe**: Simplebus slave read_strobe signal
        - **sb_write_strobe**: Simplebus slave write strobe signal
        - **sb_write_data**: Simplebus slave write data signal
        - **ext_timebase**: External timebase input

    **OUTPUTS**

        - **sb_ready**: Simplebus slave ready signal
        - **sb_read_data**: Simplebus slave read data signal
        - **timebase**: Timebase output
        - **pwm_out**: PWM signals output


.. _enable_gen:

-----------------
Enable Generator
-----------------

    .. image:: ../assets/Enable_gen.svg

    |

    This templated block implements an enable generator with and arbitrary number of output signals.
    It is implemented as a simple up counter that feeds a battery of compare registers.
    Each one of them has two modes of operation, clock and trigger mode, in the first one the comparator
    output will be high from the match to the end of the cycle, in trigger mode the output is only pulsed
    on and of for a single clock cycle.

    **PARAMETERS**

        - **BASE_ADDRESS**:Base address for the Sipmplebus interface. Default value 0x43C00000
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

.. _tau:

----------------------------
Transform Acceleration Unit
----------------------------

lorem ipsum

.. _pid:

----
PID
----

    .. warning:: The derivative action in this controller has not yet been implemented

    .. image:: ../assets/PID.svg

    |

    This block implemnets a Simplebus conrolled PID controller. AXI stream interfaces are used for all
    the data inputs and outputs. The integrator implements a clamping anti-windup mechanism.

    **PARAMETERS**

        - **BASE_ADDRESS**:Base address for the Sipmplebus interface. Default value 0x43C00000
        - **INPUT_DATA_WIDTH**: Width of the input data bus. Default value 12
        - **OUTPUT_DATA_WIDTH**: Width of the output data bus. Default value 16

    **INPUTS**

        - **clock**: Main clock input
        - **reset**: Active low synchronous reset input
        - **sb_address**: Simplebus slave address signal
        - **sb_read_strobe**: Simplebus slave read_strobe signal
        - **sb_write_strobe**: Simplebus slave write strobe signal
        - **sb_write_data**: Simplebus slave write data signal
        - **reference**: Reference AXI Stream slave data signal
        - **reference_valid**: Reference AXI Stream slave valid signal
        - **feedback**: Feedback AXI Stream slave data signal
        - **feedback_valid**: Feedback AXI Stream slave valid signal
        - **out_ready**: output AXI Stream master ready signal

    **OUTPUTS**

        - **sb_ready**: Simplebus slave ready signal
        - **sb_read_data**: Simplebus slave read data signal
        - **reference_ready**: Reference AXI Stream slave ready signal
        - **feedback_ready**: Feedback AXI Stream slave ready signal
        - **out_valid**: output AXI Stream master valid signal
        - **PID_out**: output AXI Stream master data signal


.. _gpio:

-----
GPIO
-----

    .. image:: ../assets/GPIO.svg

    |

    This block implements a Simplebus controlled GPIO peripheral, allowing a parametrized number of input and outputs to be controlled
    through Simplebus reads and writes.

    **PARAMETERS**

        - **BASE_ADDRESS**:Base address for the Sipmplebus interface. Default value 0x43C00000
        - **INPUT_WIDTH**: Width of the input port. Default value 8
        - **OUTPUT_WIDTH**: Width of the output port. Default value 8

    **INPUTS**

        - **clock**: Main clock input
        - **reset**: Active low synchronous reset input
        - **sb_address**: Simplebus slave address signal
        - **sb_read_strobe**: Simplebus slave read_strobe signal
        - **sb_write_strobe**: Simplebus slave write strobe signal
        - **sb_write_data**: Simplebus slave write data signal
        - **gpio_i**: GPIO input port

    **OUTPUTS**

        - **sb_ready**: Simplebus slave ready signal
        - **sb_read_data**: Simplebus slave read data signal
        - **gpio_o**: GPIO output port


