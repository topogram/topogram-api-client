**********
Installing
**********

Before installing Topogram, you need to have
`setuptools <https://pypi.python.org/pypi/setuptools>`_ installed.

Quick install
=============

Get Topogram from the Python Package Index at
http://pypi.python.org/pypi/networkx

or install it with

::

   pip install topogram_client

and an attempt will be made to find and install an appropriate version
that matches your operating system and Python version.

You can install the development version (at github.com) with

::

  pip install git://github.com/topogram/topogram-api-client.git#egg=topogram

Or using `setuptools`

::
  git clone git://github.com/topogram/topogram-api-client
  python setup.py install

Requirements
============

Python
------

To use Topogram you need Python 2.7, 3.2 or later.

Requests
------

All communication with the Topogram server instance is made via HTTP requests that consumes the REST API.
