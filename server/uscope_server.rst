.. _uscope-server:

==========================
µScope Application Server
==========================

The µScope Applicatio server is the main component of the whole server infrastructure, 
it is serves as the main REST gateway where a series of web API allow the client to directly
control the whole hardware platform.

---------------------------
web API backends
---------------------------

The server, written in python, uses the `Flask framework <https://www.palletsprojects.com/p/flask/>`_,
along with the `flask-restful <https://flask-restful.readthedocs.io/en/latest/>`_ extension,
to handle all the low level networking details, while various `blueprints <https://flask.palletsprojects.com/en/1.1.x/blueprints/>`_
implement all the required API

^^^^^^^^^^^^^^^^^^^^
Application API
^^^^^^^^^^^^^^^^^^^^
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


^^^^^^^^^^^^^^^^^^^^
Plot API
^^^^^^^^^^^^^^^^^^^^
This API implements the on screen oscilloscope feature, 

**ENDPOINTS:**

.. http:get:: /plot/capture

    Start a single capture run on the enabled channels

.. http:post:: /plot/capture

    return the previously captured data

.. http:get:: /plot/channels/specs

    returns the specs of the currently available channels

.. http:post:: /plot/channels/params

    Modify channel parameters

.. http:get:: /plot/channels/data

    returns the last set of acquired data

^^^^^^^^^^^^^^^^^^^^
Registers API
^^^^^^^^^^^^^^^^^^^^
This API is used to access the memory mapped registers on the programmable logic part of the SoC.

**ENDPOINTS:**

api.add_resource(RegisterValue, '') GP
api.add_resource(RegisterDescriptions, '') G


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

^^^^^^^^^^^^^^^^^^^^
Peripherals API
^^^^^^^^^^^^^^^^^^^^
This API manages the manages the peripherals definitions, allowing their creation update and removal.

**ENDPOINTS:**

.. http:post:: /tab_creator/diagram

    Upload the diagram for a peripheral

.. http:post:: /tab_creator/create_peripheral

    Add a peripheral, specified as a parameter, to the database

.. http:get:: /tab_creator/remove_peripheral/(string:peripheral)

    Removes the specified `peripheral` from the database

------------------------
Data store and Redis db
------------------------

-------------
Deployment
------------