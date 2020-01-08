.. _uscope-server:

==========================
µScope Application Server
==========================

The µScope Applicatio server is the main component of the whole server infrastructure, 
it is serves as the main REST gateway where a series of web API allow the client to directly
control the whole hardware platform.

------------------------
Data store and Redis db
------------------------

The Application server legerages a Redis database instance. All necessary data, including custom peripheral and application definitions are
stored in the logical database #2 as hashes, and persisted to non volatile memory. All the other logical databases, are treated as simple key
value stores and used to synchronize informations between various server threads/processes.
To decouple the server businnes logic from the details of the database implementation, all the accesses to it are done through the DataStore
module, to minimize the impact of a future database change on the rest of the server code.


---------------
Nginx frontend
---------------

The topmost component of the server software stack is an instance of the `Nginx <https://www.nginx.com/>`_ server.
On one hand, if necessary, it can serve all the necessary static files, in order to achieve fully self contained 
operation without the need for any installation procedure on the client side. On the other, it acts as a reverse 
proxy that allows the use of a separate API server while still complying with the same origin policy, removing
the need for cross origin resource sharing (CORS).


---------------------------
web API backends
---------------------------

The server, written in python, uses the `Flask framework <https://www.palletsprojects.com/p/flask/>`_,
along with the `flask-restful <https://flask-restful.readthedocs.io/en/latest/>`_ extension,
to handle all the low level networking details, while various `blueprints <https://flask.palletsprojects.com/en/1.1.x/blueprints/>`_
implement all the required API. As `advised <https://flask.palletsprojects.com/en/1.1.x/deploying/>`_ from the flask team, the server
has been deployed on top of an instance of the gunicorn WSGI HTTP server to allow multiple concurrent requests.

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