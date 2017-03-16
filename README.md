# Topogram Python API Client

![Read The Docs Build](https://readthedocs.org/projects/topogram/badge/?version=latest)

A python lib to communicate with Topogram

## How it works


```python 
from topogram-python-client import TopogramAPIClient

topogram = TopogramAPIClient("http://localhost:3000")

# create a new network
topogram.create_topogram("test")
```

## Documentation

Read the docs at [http://topogram.readthedocs.io/](http://topogram.readthedocs.io/)

## Install

    git clone https://github.com/topogram/topogram-api-client
    cd topogram-api-client
    python setup.py install

## Example

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from topogram_client import TopogramAPIClient
from random import randint

# credentials
TOPOGRAM_URL = "https://app.topogram.io" # http://localhost:3000
USER = "myself@email.com"
PASSWORD = "password"


# data
NODES_COUNT = 5
EDGES_COUNT = 8
my_edges = []

my_nodes = [{
    "id": i,
    "name" : "Node %s"%i
} for i in range(0,NODES_COUNT)]

for n in range(0,EDGES_COUNT):
    src = randint(0,NODES_COUNT)
    tgt = randint(0,NODES_COUNT)
    edge = {
        "source" : src,
        "target" : tgt,
        "weight" : 5,
        "name" : "Edge from %s to %s"%(src, tgt)
    }
    my_edges.append(edge)

# connect to the topogram instance
topogram = TopogramAPIClient(TOPOGRAM_URL)

# create a new user
topogram.create_user(USER, PASSWORD)

# login a new user if needed
topogram.user_login(USER, PASSWORD)

def create_topogram(title, nodes, edges):

    print "Creating topogram '%s'"%title

    r = topogram.create_topogram(title)
    print r["message"]
    topogram_ID = r["data"][0]["_id"]

    # get and backup existing nodes and edges
    existing_nodes = topogram.get_nodes(topogram_ID)["data"]
    existing_edges = topogram.get_edges(topogram_ID)["data"]

    # clear existing graph
    topogram.delete_nodes([n["_id"] for n in existing_nodes])
    print "nodes deleted"
    topogram.delete_edges([n["_id"] for n in existing_edges])
    print "edges deleted"

    r = topogram.create_nodes(topogram_ID, nodes)
    print "%s nodes created."%len(r["data"])
    r = topogram.create_edges(topogram_ID, edges)
    print "%s edges created."%len(r["data"])

    print "done. Topogram has been updated. Check it at %s/topograms/%s/view"%(TOPOGRAM_URL, topogram_ID)


create_topogram("Test", my_nodes, my_edges)
```

## command-line

    topogram-client

## tests

You will need to run a test instance of [Topogram](http://github.com/topogram/topogram) with a different DB on the 3030 port.

    export MONGO_URL=mongodb://localhost:27017/test_topogram; meteor --port 3030

Install the dev dependencies

    pip install -r dev_requirements.txt

Then you can run the tests

    nosetests --rednose tests
