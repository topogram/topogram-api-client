.. Topogram API Client documentation master file, created by
   sphinx-quickstart on Tue Jul 12 01:03:03 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Python API Client
===============================================

.. only:: html

    :Release: |version|
    :Date: |today|

**Topogram API Client** is a Python library that allow you to work with Topogram, a web-based network solution. Using the API client, you can create, edit, delete and modify networks and topograms in any running instance of the Topogram software.

::

    from topogram_client import TopogramAPIClient

    topogram = TopogramAPIClient("http://localhost:3000")

    # login as a user
    topogram.user_login("test@test.com", "password")

    # create a new network
    r = topogram.create_topogram("test")

    topogram_id = r["data"]["id"]
    topogram.create_node(topogram_id, id="my awesome node", x=103, y=502, data={"lat" : 3.12, "lng": 5.27})
    topogram.create_node(topogram_id, id="my other awesome node")
    topogram.create_edge(topogram_id, "my awesome node", "my other awesome node", name="my great edge")

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
