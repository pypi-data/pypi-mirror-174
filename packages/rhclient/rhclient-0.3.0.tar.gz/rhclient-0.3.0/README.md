#### <strong>This software is the sole property of Prime Solutions Group, Inc.</strong>

# <strong>REST Harness - Python Client</strong>

REST Harness is a robust tool that acts to stand in place of another RESTful service. This can be used to mock out a service that doesn't exist yet or where there is a need to reproduce a particular set of inputs from an opaque service. It can also serve as a simple shared cache. This software runs as a daemon service by default. This library contains a client developed in Java that can be used to interact with the REST Harness web server.

### Requirements
Python3, boto3 and requests.

### Building the client
To build:
1. pull the source into any folder.
2. Open a terminal and CD to the source folder.
3. Use any of the python lifecycle phase flags with the prefix -m (so it is ran as a script), such as `build`.

### Importing the client and using it in an application
Importing the client is like installing and importing any other python dependency. 
To import:
1. In your project environment, type `pip install rhclient`
2. To use it in your scripts, type `from rhclient import client` where you'd normally import dependencies



