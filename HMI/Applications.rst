
.. _applications:

================
Applications
================

.. figure:: ../assets/app_manager.png
    :scale: 30%
    :align: right

    Applications Manager

Given the extreme flexibility of the underlying platform, as peripherals and IP cores can be easily added and removed from the FPGA fabric dynamically a fixed function user 
interface is undesirable, as it would prove either too general, exposing too many low level details, or excessively specific with respect to the current system, and consequently incapable
of adapting to different requirements.

To solve this issue the concept of user defined applications is introduced. The system designer, along with the HDL designers can specify a set of peripherals, register, data channels, events and parameters
that make sense for the specific use case and associated FPGA bitstream, along with the scripts needed to translate them in a form that the lower layers can understand.

- **Peripherals**: Peripheral definitions stand at the heart of the HMI, they match the IP block present in the FPGA fabric and translate the list of registers they expose to more meaningful and user-friendly names that  simplify script writing.
- **Registers**: These values represent static, application specific, register configurations needed for correct functionality. They are configured only once at startup thus are not directly user accessible.
- **Data channels**: These define which the data streams that are collected inside the FPGA fabric and can be exported through the integrated scope.
- **Channel groups**: These select which of the available data channel are combined to be visualized or captured
- **Parameters**: Parameters are user defined floating point values that can be modified while the system is running to affect its behaviour, they are translated to machine understandable values through scripts
- **Events**:  The Events (old name macros) are user activated triggers to scripts. They can be used in conjunction with parameters when several of them must be modified in an atomic manner
- **Scripts**: Scripts are a powerful tool that allows the user to translate meaningful and user-friendly parameters to machine understandable register values. They must contain a single JavaScript function.

This information is compiled in a self-contained dictionary that is managed by the lower layers. Upon startup, the user will choose the desired application, allowing the UI to be configured to show the correct information.
To Allow the creation and management of user applications, along with all their components, several management pages are also provided that enable quick and easy creation, update and removal of all the aforementioned components.
Extensive importing and exporting options are also available for easy migration of all data between platforms.
