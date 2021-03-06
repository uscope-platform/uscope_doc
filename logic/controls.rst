**************************
Control peripherals
**************************


================
PWM Generator
================

    .. image:: ../assets/PwmGenerator.svg

    |

    This module implements an advanced and highly customizable PWM generator. Its operations are governed through a
    Simplebus slave interface offered by the Control unit. This block contains a parametrized number of a PWM chained
    submodule. Each one of them contains a single independent counter feeding a bank of comparators. Allowing to easily
    generate both traditional and multi-carrier set of PWM signals. The first component of this block is a prescaler that enables
    the generation of a timebase signal with close to an arbitrary frequency. This signal is then fed to the counters; they generate
    the carrier signal used in the modulation (both triangular and sawtooth waveforms can be configured) of the desired amplitude.
    A phase shift between carriers can also be introduced by staggering the enable signals. The output of the counters is
    then fed to a bank of comparator pairs (window comparators), each one is responsible for the production of a single PWM
    signal, the complementary signal generation with automatic dead-time insertion is available.

    For more advanced modulation techniques such as variable frequency carriers, for spread spectrum operation or pulse frequency modulation.


    **PARAMETERS**

        - **BASE_ADDRESS**: Base address for the Simplebus interface. Default value 0x43C00000
        - **COUNTER_WIDTH**: Width of the pwm generator counter. Default value 16
        - **INITIAL_STOPPED_STATE**: State of the PWM output when the generator is not configured and/or stopped

    **INPUTS**

        - **clock**: Main clock input
        - **reset**: Active low synchronous reset input
        - **ext_timebase**: External timebase input
        - **fault**: Fault input, when set to high the PWM generator is stopped and the output status set to the default value
  
    **OUTPUTS**

        - **timebase**: Timebase output
        - **pwm_out**: PWM signals output

    **INTERFACES**

        - **sb**: Simplebus slave interface for control and configuration

    .. toctree::
        :maxdepth: 1

        register_maps/controls/pwm_gen_regmap



================================
Transform Acceleration Unit
================================

    .. image:: ../assets/TAU.svg

    |

    This module Implements the standard abc to dq transforms used in field oriented control. A look-up table in Block RAM
    contains the first quadrant (0 to ??/2 radians) of the sine function, all the other values are derived from it thanks
    to periodicity and other trigonometric identities. The transforms can be chained together in the standard fashion or
    used independently, this behavior is selectable through the Simplebus interface of the Control unit.

    **PARAMETERS**

        - **BASE_ADDRESS**: Base address for the Simplebus interface. Default value 0x43C00000

    **INPUTS**

        - **clock**: Main clock input
        - **reset**: Active low synchronous reset input
        - **theta**: Angle input
        - **clarke_in**: abc -> ???? input
        - **park_in**: ???? -> dq input
        - **inverse_clarke_in**: ???? -> abc input
        - **inverse_park_in**: dq -> ???? input

    **OUTPUTS**

        - **clarke_out**: abc -> ???? output
        - **park_out**: ???? -> dq output
        - **inverse_clarke_out**: ???? -> abc output
        - **inverse_park_out**: dq -> ???? output

    **INTERFACES**

        - **spb**: Simplebus slave Interface

    .. toctree::
        :maxdepth: 1

        register_maps/controls/tau_regmap


====
PID
====

    .. warning:: The derivative action in this controller has not yet been implemented

    .. image:: ../assets/PID.svg

    |

    This block implements a Simplebus controlled PID controller. AXI stream interfaces are used for all
    the data inputs and outputs. All configurations can be performed through the Simplebus Interface.
    The proportional, integral and derivative gains are implemented as fractional fixed integer numbers.
    To reduce area consumption the denominator is implemented as left shift, rather than division or multiplication 
    by the reciprocal, restricting the choice of values to only integer powers of two.
    Due to the limited range of 16 bit fixed integer values the integrator is substituted with a simple accumulator consequently,
    to achieve the correct system response, all gains need to be scaled by the sampling period.
    Configurable saturators are available on both the output and integrator internal state, to avoid the wind-up phenomenon.

    **PARAMETERS**

        - **BASE_ADDRESS**: Base address for the Simplebus interface. Default value 0x43C00000
        - **INPUT_DATA_WIDTH**: Width of the input data bus. Default value 12
        - **OUTPUT_DATA_WIDTH**: Width of the output data bus. Default value 16

    **INPUTS**

        - **clock**: Main clock input
        - **reset**: Active low synchronous reset input
    
    **INTERFACES**
        - **reference**: AXI stream slave reference signal
        - **feedback**: AXI stream slave feedback signal
        - **out**: AXI stram master output signal
        - **error_mon** AXI stream master Error output (useful for monitoring Controller tuning
        - **sb** Simplebus slave interface for configuration and control
        
    .. toctree::
        :maxdepth: 1

        register_maps/controls/pid_regmap




========
GPIO
========

    .. ima==ge:: ../assets/GPIO.svg

    |

    This block implements a Simplebus controlled GPIO peripheral, allowing a parametrized number of input and outputs to be controlled
    through Simplebus reads and writes.

    **PARAMETERS**

        - **BASE_ADDRESS**: Base address for the Simplebus interface. Default value 0x43C00000
        - **INPUT_WIDTH**: Width of the input port. Default value 8
        - **OUTPUT_WIDTH**: Width of the output port. Default value 8

    **INPUTS**

        - **clock**: Main clock input
        - **reset**: Active low synchronous reset input
        - **gpio_i**: GPIO input port

    **OUTPUTS**

        - **gpio_o**: GPIO output port

    **INTERFACES**
        - **sb** Simplebus slave interface for configuration and control

    .. toctree::
        :maxdepth: 1

        register_maps/controls/gpio_regmap


======================
Phase Reconstructor
======================

    This module reconstructs the n-th phase waveform from a set of n-1 samples for a symmetric set of waveforms by enforcing the algebraic
    sum of the set to be zero. The output of this module is an AXI stream where the missing quantity is transmitted following the other (n-1).

    **PARAMETERS**
    
    - **N_PHASES**: Number of phases in the overall set (including the missing one)
    - **MISSING_PHASE**: Index of the missing phase 
    - **DATA_PATH_WIDTH**: Width of the data path in bits
    - **TARGET_ADDRESS**: Address of the generated RTCU transaction

    **INPUTS**

    - **clock**: Main clock input
    - **reset**: Active low synchronous reset input
    - **enable**: Module enable

    **INTERFACES**
    - **phases_in** AXI stream input to the module
    - **phases_out**: AXI stream output of the module




======================
Edge Aligner
======================

    .. warning:: This block is specific to a set of hardware, consequently only minimal documentation is provvided

    This module performs all the calculations necessary to configure the pwm generator to produce a set of signals with 
    an asymmetric deadtime to compensate for specific gate driver problems.

    **PARAMETERS**

        - **BASE_ADDRESS**: Base address for the Simplebus interface. Default value 0x0
        - **PWM_GENERATOR_ADDRESS**: Address of the target pwn generator on the Simplebus output. Default value 0

    **INPUTS**

        - **clock**: Main clock input
        - **reset**: Active low synchronous reset input

    **OUTPUTS**

        - **disconnect_output**: Signal used for Fault emulation

    **INTERFACES**
        - **sb_in** Slave simplebus used for both configuration, control and runtime data
        - **sb_out** Master simplebus interface to the target PWM generator

    .. toctree::
        :maxdepth: 1

        register_maps/controls/edge_aligner_regmap