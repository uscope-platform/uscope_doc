.. _layer_components:

============================
Management Layer components
============================

-------------------------
Nginx Frontend
-------------------------


The topmost component of the server software stack is an instance of the `Nginx <https://www.nginx.com/>`_ server.
On one hand, if necessary, it can serve all the necessary static files, in order to achieve fully self-contained 
operation without the need for any installation procedure on the client side. On the other, it acts as a reverse 
proxy transferring all REST API calls to the appropriate server. This component acts also as a TLS terminating proxy 
that encrypts and describes all data going to and coming from the client. 

It should be noted that the TLS certificate used in these operations can not be issued by a standard public Certificate Authority (CA),
as these require a static internet facing IP and a registered domain name for verification, while the uPlatform is intended 
to be deployed in mostly private and possibly air-gapped networks. A private CA, whose certificate needs to be installed by each user, is generated
during the commissioning process and then used to sign the server certificate. To minimize the risk of leaks the CA private key, this is deleted
after use, making it very difficult for an attacker to use it to spoof legitimate websites on client machines.

-------------------------
 REST API server
-------------------------


The server, written in python, uses the `Flask framework <https://www.palletsprojects.com/p/flask/>`_,
along with the `flask-restful <https://flask-restful.readthedocs.io/en/latest/>`_ extension,
to handle all the low level networking details, while various `blueprints <https://flask.palletsprojects.com/en/1.1.x/blueprints/>`_
implement all the required API. As `advised <https://flask.palletsprojects.com/en/1.1.x/deploying/>`_ from the flask team, the server
has been deployed on top of an instance of the gunicorn WSGI HTTP server to allow multiple concurrent requests.

--------------------------
Userspace Driver
--------------------------

This component is responsible for managing the low level hardware access. This allows the use of a programming language most suitable to this task,
like C++, that allow more direct access to system calls with respect to the higher level languages like Python used to implement REST servers.