#!/usr/bin/env python
# -*- coding: utf-8 -*-

from topogram_client import TopogramAPIClient
from random import randint

# credentials
TOPOGRAM_URL = "http://localhost:3000" # "https://app.topogram.io"
USER = "myself@email.com"
PASSWORD = "password"


# data
NODES_COUNT = 5
EDGES_COUNT = 8
my_edges = []

my_nodes = [{
    "data" : {
        "id": str(i),
        "name" : "Node %s"%i
    }
}for i in range(0,NODES_COUNT)]

for n in range(0,EDGES_COUNT):
    src = str(randint(0,NODES_COUNT))
    tgt = str(randint(0,NODES_COUNT))
    edge = {
        "data" : {
            "source" : src,
            "target" : tgt,
            "weight" : 5,
            "name" : "Edge from %s to %s"%(src, tgt)
        }
    }
    my_edges.append(edge)

print my_edges
print my_nodes

# connect to the topogram instance
topogram = TopogramAPIClient(TOPOGRAM_URL)

# create a new user
# topogram.create_user(USER, PASSWORD)

# login a new user if needed
# topogram.user_login(USER, PASSWORD)

def create_topogram(title, nodes, edges):

    print "Creating topogram '%s'"%title

    r = topogram.create_topogram(title)
    print r
    print r["message"]
    topogram_ID = r["data"]["_id"]

    # get and backup existing nodes and edges
    existing_nodes = topogram.get_nodes(topogram_ID)["data"]
    existing_edges = topogram.get_edges(topogram_ID)["data"]


    # clear existing graph
    if len(existing_nodes):
        topogram.delete_nodes([n["_id"] for n in existing_nodes])
        print "%s nodes deleted"%len(existing_nodes)
    if len(existing_edges):
        topogram.delete_edges([n["_id"] for n in existing_edges])
        print "%s edges deleted"%len(existing_edges)

    r = topogram.create_nodes(topogram_ID, nodes)
    print "%s nodes created."%len(r["data"])
    r = topogram.create_edges(topogram_ID, edges)
    print "%s edges created."%len(r["data"])

    print "done. Topogram has been updated. Check it at %s/topograms/%s/view"%(TOPOGRAM_URL, topogram_ID)


create_topogram("Test", my_nodes, my_edges)
