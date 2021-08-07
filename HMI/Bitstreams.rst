
.. _bitstreams:

================
Bitstreams
================

Bitstream files are fundamental for the whole system operation, as they are used to configure the programmable logic implemented on the FPGA portion of the System on chip.
For these reasons the uScope system integrate some basic bitstream handling capabilities. Through the associated manager the user can upload, rename and dump bitstream files.


------------------
 Bitstream fields
------------------
Each bitstream file is assiciated with the following metadata:

- **ID**: Integer used to identify the register in scripts
- **name**: User defined string defining the bitstream name on the target filesystem (it can be different form the name of the bitstream file on the host computer. 