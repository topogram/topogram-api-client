import sys
import unittest
import json
from requests import ConnectionError, session

from topogram_client import TopogramAPIClient, set_debugging

# clear DB on start
from pymongo import MongoClient
c = MongoClient('localhost', 27017) #Connect to mongodb
c.drop_database('test_topogram')

#
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
        r = self.client.create_topogram("test topogram")
        self.assertEqual(r["status"], "success")
        self.assertEqual(r["status_code"], 201)
        self.assertEqual(r["data"]["name"], "haha")

    def test_get_public_topograms_list(self):
        self.client.get_public_topograms_list()
        self.assertEqual(True, False)

    #
    # def test_delete_network(self):
    #     self.assertEqual(True, False)
    #
    # def test_create_single_node(self):
    #     self.assertEqual(True, False)
    #
    # def test_update_node(self):
    #     self.assertEqual(True, False)
    #
    # def test_create_a_bunch_of_nodes(self):
    #     self.assertEqual(True, False)
    #
    # def test_update_a_bunch_of_nodes(self):
    #     self.assertEqual(True, False)
    #
    # def test_create_a_single_edge(self):
    #     self.assertEqual(True, False)
    #
    # def test_update_a_single_edge(self):
    #     self.assertEqual(True, False)
    #
    # def test_create_a_bunch_of_edges(self):
    #     self.assertEqual(True, False)
    #
    # def test_update_a_bunch_of_edges(self):
    #     self.assertEqual(True, False)
