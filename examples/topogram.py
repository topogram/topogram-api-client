#!/usr/bin/env python
# -*- coding: utf-8 -*-

from topogram_client import TopogramAPIClient
from random import randint
from csv import DictReader
from datetime import datetime

# credentials
TOPOGRAM_URL = "http://localhost:3000" # "https://app.topogram.io"
USER = "myself@email.com"
PASSWORD = "password"

# data
my_nodes = []
my_edges = []

with open('data/test_data_nodes.csv') as f :
    reader = DictReader(f)
    for n in reader :
        node = {
            "id" : n["id"],
            "name" : n["name"],
            "lat" : float(n["lat"]),
            "lng" : float(n["lng"]),
            "weight" : float(n["weight"]),
            "start" : datetime(n["year_start"],1,1,0,0,1).isoformat(),
            "end" : datetime(n["year_stop"],1,1,0,0,1).isoformat()
            }
        my_nodes.append({ "data" : node })

print my_nodes

with open('data/test_data_edges.csv') as f :
    reader = DictReader(f)
    for e in reader :
        edge = {
            "source" : e["source"],
            "target" : e["target"],
            "weight" : float(e["weight"])
        }
        my_edges.append({ "data" : edge })

# print my_edges

def create_topogram(title, nodes, edges):

    print "Creating topogram '%s'"%title

    try :
        r = topogram.create_topogram(title)
    except ValueError:
        print '> Topogram already exists'
        r = topogram.get_topogram_by_name(title)

    topogram_ID = r["data"]["_id"]
    print "topogram ID : %s"%topogram_ID

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
    print r
    print "%s nodes created."%len(r["data"])
    r = topogram.create_edges(topogram_ID, edges)
    print "%s edges created."%len(r["data"])

    print "done. Topogram has been updated. Check it at %s/topograms/%s"%(TOPOGRAM_URL, topogram_ID)

# connect to the topogram instance (pass debug=True params for more info )
topogram = TopogramAPIClient(TOPOGRAM_URL) #, debug=True)

# create a new user
try :
    topogram.create_user(USER, PASSWORD)
except ValueError:
    print "> User has already been created."

# login a new user if needed
resp_user_login = topogram.user_login(USER, PASSWORD)
print resp_user_login

assert(resp_user_login["status"] == "success")
assert(resp_user_login["status_code"] == 200)

create_topogram("Geo-time network", my_nodes, my_edges)
