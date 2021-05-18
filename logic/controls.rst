====================
Control peripherals
====================

.. _pwm_gen:

--------------
PWM Generator
--------------

    .. image:: ../assets/PwmGenerator.svg

    |

    This module implements an advanced and higly customizable pwm generator. Its operations are governed through a
    Simplebus slave interface offered by the Control unit. This block contains a parametrized number of a PWM chained
    sub-module. each one of them contains a single independent counter feeding a bank of comparators. Allowing to easily
    generate both thraditional and multi-carrier set of pwm signals. The first component of this block is a prescaler that enables
    the generation of a timebase signal with close to an arbitrary frequency. This signal is then fed to the counters; they generate
    the carrier signal used in the modulation (both trianular and sawtooth waveforms can be configured) of the desired amplitude.
    A phase shift between carriers can also be introduced by staggering the enable singals. The output of the counters is
    then fed to a bank of comparator pairs  (window comparators), each one is responsible for the production of a single PWM
    signal, the complementary signal generation with automatic dead-time insertion is available.

    For more advanced modulation techniques such as variable frequency carriers, for spread spectrum operation or pulse frequency modulation.


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

    .. toctree::
        :maxdepth: 1

        register_maps/controls/pwm_gen_regmap


.. _tau:

----------------------------
Transform Acceleration Unit
----------------------------

    .. image:: ../assets/TAU.svg

    |

    This module Implements the standard abc to dq transforms used in field oriented control. A look up table in Block RAM
    contains the first quardrant (0 to π/2 radians) of the sine function, all the other values are derived from it thanks
    to periodicity and other trigonometric identities. The transforms can be chained together in the standard fashion or
    used independently, this behaviour is selectable through the Simplebus interface of the Control unit.

    **PARAMETERS**

        - **BASE_ADDRESS**:Base address for the Sipmplebus interface. Default value 0x43C00000

    **INPUTS**

        - **clock**: Main clock input
        - **reset**: Active low synchronous reset input
        - **theta**: Angle input
        - **clarke_in**: abc -> αβ input
        - **park_in**: αβ -> dq input
        - **inverse_clarke_in**: αβ -> abc input
        - **inverse_park_in**: dq -> αβ input

    **OUTPUTS**

        - **clarke_out**: abc -> αβ output
        - **park_out**: αβ -> dq output
        - **inverse_clarke_out**: αβ -> abc output
        - **inverse_park_out**: dq -> αβ output

    **INTERFACES**

        - **spb**: Simplebus slave Interface

    .. toctree::
        :maxdepth: 1

        register_maps/controls/tau_regmap


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

    .. toctree::
        :maxdepth: 1

        register_maps/controls/pid_regmap


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


    .. toctree::
        :maxdepth: 1

        register_maps/controls/gpio_regmap


.. _phase_reconstructor:

--------------------
Phase Reconstructor
--------------------

    Lorem Ipsum

.. _edge_aligner:

--------------------
Edge Aligner
--------------------

    Lorem Ipsum