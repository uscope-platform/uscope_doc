.. _API_reference:

==========================
HMI REST API Reference
==========================
-----------------------
Application API
-----------------------
This API manages the whole application lifecycle, from creation, through edit and use up to its removal from the server.

**ENDPOINTS:**

.. http:get:: /application/remove/(string:application_name)

    Remove the application named `application_name` from the database.

.. http:get:: /application/all/specs

    returns all the applications present in the database

.. http:get:: /application/set/(string:application_name)

    set the application named `application_name` as the current one.

.. http:get:: /application/digest

    Return a digest that specifies the version of the application database

.. http:post:: /application/add

    Add the application passed as a parameter to the database

.. http:post:: /application/add

    Edit a field of an application in the database

.. http:get:: /application/get/(string:application_name)

    Retrn a specific application specification

-----------------------
Plot API
-----------------------
This API implements the on screen oscilloscope feature, 

**ENDPOINTS:**


/channels/ POST
/channels/widths POST


.. http:get:: /plot/capture

    return the previously captured data    

.. http:post:: /plot/capture

    Start a single capture run on the enabled channels

.. http:get:: /plot/channels/specs

    returns the specs of the currently available channels

.. http:post:: /plot/channels/params

    Modify channel parameters

.. http:get:: /plot/channels/data

    returns the last set of acquired data

.. http:post:: /plot/channels/status

    Modify the status of one or more channels

.. http:post:: /plot/channels/widths

    Moidfy the widths of one or more channel, this is used for sign extension.
    The values of 1 to 100 represent the width of a signed integer while 100 to 200 represent unsigned integers (subtract 100 to get the width in bits)

-----------------------
Registers API
-----------------------
This API is used to access the memory mapped registers on the programmable logic part of the SoC.

**ENDPOINTS:**

.. http:get:: /registers/(string:peripheral)/value

    Reads the value of a register, specified in the parameters from the supplied `peripheral`

.. http:post:: /registers/(string:peripheral)/value

    Writes the value of a register, specified in the parameters from the supplied `peripheral`

.. http:get:: /registers/(string:peripheral)/descriptions

    Returns the info of the registers of the specified `peripheral`

.. http:get:: /registers/all_peripheral/descriptions

    Returns the info of all the registers in all the peripherals

.. http:post:: /registers/bulk_write

    Writes specified values to multiple registers in multiple peripherals

.. http:get:: /registers/digest

    Returns an Hash of all the current peripheral specifications

-----------------------
Peripherals API
-----------------------
This API manages the manages the peripherals definitions, allowing their creation update and removal.

**ENDPOINTS:**

.. http:post:: /tab_creator/diagram

    Upload the diagram for a peripheral

.. http:post:: /tab_creator/create_peripheral

    Add a peripheral, specified as a parameter, to the database

.. http:post:: /tab_creator/edit_peripheral

    Modify a specific field in the specified peripheral

.. http:get:: /tab_creator/remove_peripheral/(string:peripheral)

    Removes the specified `peripheral` from the database


-----------------------
Authentication API
-----------------------

This API manages users and their authentication

**ENDPOINTS:**

.. http:post:: /auth/login

    Log in a user, either due to user action or automatically with remember me function

.. http:get:: /auth/logout

    Logs out a user

.. http:get:: /auth/user

    Get users list

.. http:post:: /auth/user

   Create a new user

.. http:delete:: /auth/user

    Remove a user

.. http:get:: /auth/onboarding

    Returns whether the onboarding flow needs to be run or not, allowing the creation of a single user without being logged in
    since no users are present in the database

.. http:post:: /auth/onboarding

    Creates a user account during the onboarding flow


-----------------------
Database API
-----------------------

This API allows import and export of the database

**ENDPOINTS:**

.. http:get:: /database/export

    Dumps the database to a Json object

.. http:post:: /database/import

    Loads the database from a Json object


-----------------------
Programs API
-----------------------

This API allows the management, compilation and loading of femtoCore programs

**ENDPOINTS:**

.. http:get:: /program/hash

    Returns a digest indicating the programs store version

.. http:post:: /program/Apply/(string:program_id)

    Loads loads a specified program to a femtoCore

.. http:get:: /program/compile/(string:program_id)

    Compiles the specified program and returns either success or a compilation error

.. http:get:: /program/(string:program_id)

    Returns the specified program

.. http:post:: /program/(string:program_id)

    Create a new program with the specified id

.. http:patch:: /program/(string:program_id)

    Edit the program with the specified id

.. http:delete:: /program/(string:program_id)

    Delete the program with the specified id


-----------------------
Scripts API
-----------------------

This API allows the management, of user scripts

**ENDPOINTS:**

.. http:get:: /script/hash

    Returns a digest indicating the scripts store version

.. http:get:: /script/(string:script_id)

    Returns the specified script

.. http:post:: /script/(string:script_id)

    Create a new script with the specified id

.. http:patch:: /script/(string:script_id)

    Edit the script with the specified id

.. http:delete:: /script/(string:script_id)

    Delete the script with the specified id
