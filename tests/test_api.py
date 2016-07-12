#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest
import json
from requests import ConnectionError, session

from topogram_client import TopogramAPIClient, set_debugging

# clear DB on start
from pymongo import MongoClient

def drop_database():
    c = MongoClient('localhost', 27017) #Connect to mongodb
    c.drop_database('test_topogram')

test_server_url = "http://localhost:3030"

# hack to support python 3
python2 = sys.version_info[0] == 2
if not python2:
    unicode = str

class TestTopogramAPIClient(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # init client
        self.client = TopogramAPIClient(test_server_url, debug=True)
        self.session = session()

    def setUp(self):

        # clean the database
        drop_database()

        # create a new user
        self.client.create_user("tester@tester.com", "password")

        # log in
        r = self.client.user_login("tester@tester.com", "password")
        print r["data"]["authToken"], r["data"]["userId"]

    def test_make_url(self):
        """URLs should be conformed, errors should be raised when passing wrong paths """

        self.assertRaises(ValueError, lambda : self.client.make_url("/start-with-slash") )
        self.assertRaises(ValueError, lambda : self.client.make_url("http://myapp.com/api") )
        self.assertEqual(self.client.make_url("lalalala"), test_server_url+"/api/lalalala")

    def test_has_active_connection(self):
        self.assertRaises(ConnectionError, lambda : TopogramAPIClient("http://localhost:5000", debug=True) )

    # def test_create_user(self):
    #     self.client.create_user("tester@tester.com", "password")
    #     self.assertEqual(True, False)

    def test_user_login(self):
        r = self.client.create_user("haha@tester.com", "password")
        _id = r["data"]["_id"]
        self.assertEqual(type(_id), unicode)

        # need to be logged in to delete a user
        self.assertRaises(ValueError, lambda : self.client.delete_user(_id) )

    def test_create_topogram(self):
        # create with only a name
        r = self.client.create_topogram("test topogram")
        self.assertEqual(r["status"], "success")
        self.assertTrue( r["status_code"] == 200 )
        self.assertEqual(r["data"]["name"], "test topogram")

    def test_make_public(self):
        r = self.client.create_topogram("test topogram")
        _id = r["data"]["_id"]
        r = self.client.makePublic(_id)
        self.assertEqual(r["data"]["sharedPublic"], 1)
        r = self.client.makePrivate(_id)
        self.assertEqual(r["data"]["sharedPublic"], 0)

    def test_get_public_topograms_list(self):
        r = self.client.create_topogram("test topogram")
        _id = r["data"]["_id"]
        r = self.client.makePublic(_id)
        r = self.client.get_public_topograms()
        self.assertEqual(len(r), 1)

    def test_get_private_topograms_list(self):
        self.client.create_topogram("wonderful isn't it?")
        self.client.create_topogram("yes, absolutely stunning")
        self.client.create_topogram("well, not so bad")
        r = self.client.get_topograms()
        self.assertEqual(len(r["data"]), 3)

    def test_get_topogram(self):
        r = self.client.create_topogram("哈哈哈")
        _id = r["data"]["_id"]
        r = self.client.get_topogram(_id)
        self.assertEqual(r["data"]["name"].encode('utf-8'), "哈哈哈")

    def test_delete_topogram(self):
        r = self.client.create_topogram("to be deleted")
        _id = r["data"]["_id"]
        r = self.client.delete_topogram(_id)
        # TODO : assert that nodes and edges have correctly disappear
        r = self.client.get_topograms()
        self.assertEqual(len(r["data"]), 0)

    def test_create_node(self):
        r = self.client.create_topogram("ok")
        topogramId = r["data"]["_id"]
        r = self.client.create_node(topogramId, id="jojo", x=1, y=2, data={"lat" : 3})
        self.assertEqual(r["data"]["data"]["id"], "jojo")
        self.assertEqual(r["data"]["position"]["x"], 1)
        self.assertEqual(r["data"]["position"]["y"], 2)
        self.assertEqual(r["data"]["data"]["lat"], 3)

    def test_get_node(self):
        topogramId = "sth"
        r = self.client.create_node(topogramId, id="jojo", x=1, y=2)
        _id = r["data"]["_id"]
        r = self.client.get_node(_id)
        self.assertEqual(r["data"]["data"]["id"], "jojo")
        self.assertEqual(r["data"]["position"]["x"], 1)
        self.assertEqual(r["data"]["position"]["y"], 2)

    def test_update_node(self):
        topogramId = "sth"
        r = self.client.create_node(topogramId, id="jojo", x=1, y=2)
        _id = r["data"]["_id"]
        self.assertEqual(r["data"]["position"]["x"], 1)
        self.assertEqual(r["data"]["position"]["y"], 2)
        r = self.client.update_node(_id, x=3, y=4, data={"starred" : True})
        self.assertEqual(r["data"]["position"]["x"], 3)
        self.assertEqual(r["data"]["position"]["y"], 4)
        self.assertEqual(r["data"]["data"]["starred"], True)

    def test_delete_node(self):
        topogramId = "sth"
        r = self.client.create_node(topogramId, id="jojo", x=1, y=2)
        _id = r["data"]["_id"]
        r = self.client.delete_node(_id)
        r = self.client.get_node(_id)
        self.assertEqual(r["status"], "fail")
        self.assertIn("not found", r["message"])

    def test_create_edge(self):
        topogramId = "sth"
        r = self.client.create_edge(topogramId, "bla", "bli", data={"lat" : 2}, name = "kokoko")
        # _id = r["data"]["_id"]
        self.assertEqual(r["data"]["data"]["source"], "bla")
        self.assertEqual(r["data"]["data"]["target"], "bli")
        self.assertEqual(r["data"]["data"]["lat"], 2)
        self.assertEqual(r["data"]["id"], "kokoko")

    def test_update_edge(self):
        topogramId = "sth"
        r = self.client.create_edge(topogramId, "bla", "bli", data={"lat" : 2}, name = "kokoko")
        _id = r["data"]["_id"]
        self.assertEqual(r["data"]["data"]["source"], "bla")
        self.assertEqual(r["data"]["data"]["target"], "bli")
        self.assertEqual(r["data"]["data"]["lat"], 2)
        self.assertEqual(r["data"]["id"], "kokoko")

        r = self.client.create_edge(_id, source="blu", target="blo", data={"lat" : 3}, name = "kikiki")
        self.assertEqual(r["data"]["data"]["source"], "blu")
        self.assertEqual(r["data"]["data"]["target"], "blo")
        self.assertEqual(r["data"]["data"]["lat"], 3)
        self.assertEqual(r["data"]["id"], "kikiki")

    def test_create_nodes(self):
        topogramId = "sth"
        nodes = [
            { "x" : 1, "y" : 2, "id" : "love" },
            { "x" : 3, "y" : 4, "id" : "hate" },
            { "x" : 5, "y" : 6, "id" : "indifference" }
            ]

        r = self.client.create_nodes(topogramId, nodes)
        self.assertEqual(len(r["data"]), 3)
        self.assertEqual(set([ d["data"]["id"] for d in r["data"] ]), set(["love", "hate", "indifference"]))
        self.assertEqual(set([ d["position"]["x"] for d in r["data"] ]), set([1, 3, 5]))
        self.assertEqual(set([ d["position"]["y"] for d in r["data"] ]), set([2, 4, 6]))

    def test_create_edges(self):
        topogramId = "sth"
        edges = [
            { "source" : 1, "target" : 2, "id" : "love" },
            { "source" : 3, "target" : 4, "id" : "hate" },
            { "source" : 5, "target" : 6, "id" : "indifference" }
            ]

        r = self.client.create_edges(topogramId, edges)
        self.assertEqual(len(r["data"]), 3)
        self.assertEqual(set([ d["id"] for d in r["data"] ]), set(["love", "hate", "indifference"]))
        self.assertEqual(set([ d["data"]["source"] for d in r["data"] ]), set([1, 3, 5]))
        self.assertEqual(set([ d["data"]["target"] for d in r["data"] ]), set([2, 4, 6]))

    def test_get_edges(self):
        topogramId = "sth"
        edges = [
            { "source" : 1, "target" : 2, "id" : "love" },
            { "source" : 3, "target" : 4, "id" : "hate" },
            { "source" : 5, "target" : 6, "id" : "indifference" }
            ]
        self.client.create_edges(topogramId, edges)

        r = self.client.get_edges(topogramId)
        self.assertEqual(len(r["data"]), 3)
        self.assertEqual(set([ d["id"] for d in r["data"] ]), set(["love", "hate", "indifference"]))
        self.assertEqual(set([ d["data"]["source"] for d in r["data"] ]), set([1, 3, 5]))
        self.assertEqual(set([ d["data"]["target"] for d in r["data"] ]), set([2, 4, 6]))


    def test_get_nodes(self):
        topogramId = "sth"
        nodes = [
            { "x" : 1, "y" : 2, "id" : "love" },
            { "x" : 3, "y" : 4, "id" : "hate" },
            { "x" : 5, "y" : 6, "id" : "indifference" }
            ]
        self.client.create_nodes(topogramId, nodes)

        r = self.client.get_nodes(topogramId)
        self.assertEqual(len(r["data"]), 3 )
        self.assertEqual(set([ d["data"]["id"] for d in r["data"] ]), set(["love", "hate", "indifference"]))
        self.assertEqual(set([ d["position"]["x"] for d in r["data"] ]), set([1, 3, 5]))
        self.assertEqual(set([ d["position"]["y"] for d in r["data"] ]), set([2, 4, 6]))

    def test_delete_nodes(self):
        topogramId = "sth"
        nodes = [
            { "x" : 1, "y" : 2, "id" : "love" },
            { "x" : 3, "y" : 4, "id" : "hate" },
            { "x" : 5, "y" : 6, "id" : "indifference" }
            ]
        r = self.client.create_nodes(topogramId, nodes)
        ids = [ d["_id"] for d in r["data"]]

        r = self.client.get_nodes(topogramId)
        self.assertEqual(len(r["data"]), 3)

        self.client.delete_nodes(ids)

        r = self.client.get_nodes(topogramId)
        self.assertEqual(len(r["data"]), 0)

    def test_delete_edges(self):
        topogramId = "sth"
        edges = [
            { "source" : 1, "target" : 2, "id" : "love" },
            { "source" : 3, "target" : 4, "id" : "hate" },
            { "source" : 5, "target" : 6, "id" : "indifference" }
            ]

        r = self.client.create_edges(topogramId, edges)
        ids = [ d["_id"] for d in r["data"]]

        r = self.client.get_edges(topogramId)
        self.assertEqual(len(r["data"]), 3)

        self.client.delete_edges(ids)
        r = self.client.get_edges(topogramId)
        self.assertEqual(len(r["data"]), 0)


    # def test_update_a_bunch_of_nodes(self):
    #     self.assertEqual(True, False)
    #

    # def test_update_a_bunch_of_edges(self):
    #     self.assertEqual(True, False)
