
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


----------------------------
Channel Group Specification
----------------------------

- **name**: Name of the channel group (after creation it can be edited by double clicking the name in the creator)
- **ID**: String used internally to identify the channel group throughout the UI
- **Content**: list of channel IDs contained in this group. (A maximum of six channels can be added to each group)
- **Default group**: Set the current group as the default one selected when the application is launched. (only one group can be default at a time)

-----------------------
Channel specification
-----------------------


- **name**: Name of the channel (after creation it can be edited by double clicking the name in the creator)
- **ID**: String used internally to identify the channel throughout the UI
- **channel number**: Zero based integer indicating which hardware scope channel the data stream is connected To
- **mux setting**: Address setting of the mux that is needed to connect the data stream to the scope inputs
- **physical width**: Width in bits of the data stream coming from the hardware ( to indicate an unsigned data strean add 100 to the width, so a value of 16 would indicate a signed 16 bit integer while a value of 116 would indicate a 16 bit unsigned integer)
- **Max value**: This field is not used and will be removed in a future release
- **Min value**: This field is not used and will be removed in a future release
  

---------------------
Registers
---------------------

- **Address**: Address of the register to write to
- **value**: Value to write to the register

--------------------
Events
--------------------

- **Name**: Name of the event
- **Trigger**: String used to associate the event with the corresponding script

--------------------
Parameters
--------------------

- **name**: Name of the parameter (after creation it can be edited by double clicking the name in the creator)
- **ID**: String used internally to identify the parameter throughout the UI and in script
- **Trigger**: String used to associate the parameter with the corresponding script
- **value**: default value of the parameter
- **Visible**: Boolean option that controls whether the parameter is visible to the user or if it is only usefull in scrips

--------------------
Peripheral
--------------------

- **name**: Name of the peripheral (after creation it can be edited by double clicking the name in the creator)
- **ID**: String used internally to identify the peripheral throughout the UI and in script
- **Peripheral specification**: ID of the peripheral specification implemented by this peripheral 
- **Base Address**: Base address of this peripheral on the bus
- **Type**: Unused field, will be removed in a future release
- **Proxied peripheral**: Boolean option specifying whether the peripheral can be directly acessed or if a proxy needs to be used
- **Proxy address**: Address of the proxy used to access the preripheral
- **Proxy type**: Type of proxy used to acess the peripheral
- **user accessible**: Boolean option specifying whether a custom register view is accessible to the users

---------------------
Miscelaneous fields
---------------------

- **Application name**: Name of this application
- **Bitstream**: Name of the bitstream associated to this application
- **Clock frequency**: Frequency of the main FPGA clock
- **default core address**: Address of the femtocore processor
- **default core program**: ID of the program to load on the default femtocore at startup
- **n_enables**: Unused field, will be removed in a future release
- **scope_mux_address**: Base address of the uScope mux controller
- **timebase address**:Unused field, will be removed in a future release