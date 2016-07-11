import sys
import unittest
import json
from requests import ConnectionError

from topogram_client import TopogramAPIClient, set_debugging

# hack to support python 3
python2 = sys.version_info[0] == 2
if not python2:
    unicode = str

class TestTopogramAPIClient(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # init client
        self.client = TopogramAPIClient("http://localhost:3000", debug=True)

    def test_make_url(self):
        """URLs should be conformed, errors should be raised when passing wrong paths """

        self.assertRaises(ValueError, lambda : self.client.make_url("/start-with-slash") )
        self.assertRaises(ValueError, lambda : self.client.make_url("http://myapp.com/api") )
        self.assertEqual(self.client.make_url("lalalala"), "http://localhost:3000/api/lalalala")

    def test_has_active_connection(self):
        self.assertRaises(ConnectionError, lambda : TopogramAPIClient("http://localhost:5000", debug=True) )

    # def test_create_network(self):
    #     self.assertEqual(True, False)
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
