.. Topogram API Client documentation master file, created by
   sphinx-quickstart on Tue Jul 12 01:03:03 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Topogram API Client's documentation!
===============================================

.. only:: html

    :Release: |version|
    :Date: |today|

**Topogram API Client** is a Python library that allow you to work with Topogram, a web-based network solution. Using the API client, you can create, edit, delete and modify networks and topograms in any running instance of the Topogram software.

::

    from topogram-python-client import RhiziAPIClient

    topogram = TopogramAPIClient("http://localhost:3000")

    # login as a user
    topogram.login("test@test.com", "password")

    # create a new network
    topogram.create_topogram("test")


Contents:

.. toctree::
   :maxdepth: 2
   
   install
   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
