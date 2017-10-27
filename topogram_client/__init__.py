#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random
import logging

logging.basicConfig()
log = logging.getLogger('topogram-client')

def set_debugging():
    log.setLevel(logging.DEBUG)

class TopogramAPIClient(object):
    """
    TopogramAPIClient is the main class to communicate with Topogram software

    """

    def __init__(self, base_url, debug=False):
        """Returns the instance."""
        self.base_url = base_url
        self.session = requests.session()
        if debug: set_debugging()

        log.debug("Init Topogram API at %s", base_url)
        self.check_active_connection() # check if the connection is ready

    def make_url(self, path):
        if path[0] == "/" : raise ValueError("URL path should not start with /")
        if path[0:4] == "http" : raise ValueError("URL path should contains only path no http://'). Already : %s"%self.base_url)

        return self.base_url+"/api/"+path

    def make_request(self, method, path, data):
        assert method in ["POST", "GET", "PUT", "DELETE"]
        assert type(data) is dict

        # make API url
        req_url = self.make_url(path)
        log.debug( "%s API call : %s %s", method, req_url, str(data))

        if method == "POST":
            r = self.session.post(req_url, json=data)
        elif method == "DELETE":
            r = self.session.delete(req_url, json=data)
        elif method == "GET":
            r = self.session.get(req_url, json=data)
        elif method == "PUT":
            r = self.session.put(req_url, json=data)
        else :
            raise ValueError("Unknown method : %s"%method)

        log.debug( "%s : %s", r.status_code, r.text)

        if r.status_code >= 500 : # handle 403 error
            err = "%s - Error : %s"%(r.status_code, r.json()["message"])
            log.error(err)
            raise ValueError(err)

        if r.status_code == 403 : # handle 403 error
            log.error("403 Unauthorized request")
            raise ValueError("403 Unauthorized request")

        return self.parse_res(r)

    def parse_res(self, r):
        data = r.json()
        if type(data) is not list : data["status_code"] = r.status_code
        return data

    def check_active_connection(self):
        r = self.make_request("GET", " ", {})
        assert r["status_code"] == 200

    ## Users
    def create_user(self, email, password):
        return self.make_request("POST", "users", { "email" : email, "password" : password })

    def user_login(self, email, password):
        r = self.make_request("POST", "login", { "email" : email, "password" : password })
        self.session.headers.update({ "X-Auth-Token": r["data"]["authToken"],  "X-User-Id": r["data"]["userId"]})
        return r

    def delete_user(self, _id):
        """DELETE - Delete a user"""
        return self.make_request("DELETE", "users/"+_id, {})

    def create_topogram(self, title):
        """Create a topogram based on a title"""
        assert type(title) == str
        return self.make_request("POST", "topograms", { "title" : title })

    def makePublic(self, _id):
        """Make a topogram public based on its id"""
        return self.make_request("POST", "topograms/" + _id + "/public", {})

    def makePublic(self, _id):
        """Make a topogram public based on its id"""
        return self.make_request("POST", "topograms/" + _id + "/public", {})

    def makePrivate(self, _id):
        """Make a topogram public based on its id"""
        return self.make_request("POST", "topograms/" + _id + "/private", {})

    def get_public_topograms(self):
        """GET all public topograms. Returns a list of topograms"""
        return self.make_request("GET", "publicTopograms", {})

    def get_topograms(self):
        """GET private topograms from the logged-in user. Returns a list of topograms"""
        return self.make_request("GET", "topograms", {})

    def get_topogram(self, _id):
        """GET a single topogram with its _id. Returns a topogram"""
        return self.make_request("GET", "topograms/"+_id, {})

    def get_topogram_by_name(self, name):
        """GET a single topogram with its name. Returns a topogram"""
        assert type(name) == str
        return self.make_request("POST", "topograms/getByName", { "name" : name })

    def delete_topogram(self, _id):
        """DELETE a topogram from its _id. Returns an empty topograms"""
        return self.make_request("DELETE", "topograms/"+_id, {})

    def create_node(self, topogramId, id=None, x=None, y=None, data={}):
        """POST Create a single node. Returns the created node."""
        assert type(data) is dict
        if id : assert type(id) is str
        if x : assert type(x) is float or type(x) is int
        if y : assert type(y) is float or type(y) is int

        el = {
            "id" : id,
            "x" : x,
            "y" : y
        }
        for k in data :
            el[k] = data[k]

        node = { "element" : el, "data" : data }
        return self.make_request("POST", "nodes", { "topogramId" : topogramId, "nodes" : [ node ]})

    def create_nodes(self, topogramId, nodes):
        """POST Create a bunch of nodes. Returns the created nodes"""
        assert type(nodes) is list
        return self.make_request("POST", "nodes", { "topogramId" : topogramId, "nodes" : nodes})

    def get_node(self, _id):
        """GET a single node. Returns a node"""
        return self.make_request("GET", "nodes/"+_id, {})

    def update_node(self, _id, id=None, x=None, y=None, data={}):
        """PUT update a single node. Returns the updated node"""
        return self.make_request("PUT", "nodes/"+_id, { "id" : id, "x" : x, "y" : y, "data" : data })

    def delete_node(self, _id):
        """DELETE a node. Returns an empty node"""
        return self.make_request("DELETE", "nodes/"+_id, {})

    def delete_nodes(self, _ids):
        """POST a bunch of edges. Returns empty nodes"""
        return self.make_request("POST", "nodes/delete", { "nodes" : _ids })

    def create_edge(self, topogramId, source, target, name=None, data={}):
        """POST Create a single edge. Returns the created edge."""
        assert type(data) is dict
        assert type(source) is str
        assert type(target) is str
        if name : assert type(name) is str
        print name
        el = {
            "id" : name,
            "source" : source,
            "target" : target
        }
        for k in data :
            el[k] = data[k]
        edge = { "element" : el, "data" : data }
        return self.make_request("POST", "edges", { "topogramId" : topogramId, "edges" : [ edge ] })

    def create_edges(self, topogramId, edges):
        """POST Create a bunch of edges. Returns the created edges"""
        assert type(edges) is list
        return self.make_request("POST", "edges", { "topogramId" : topogramId, "edges" : edges})


    def update_edge(self, _id, source=None, target=None, name=None, data={}):
        """PUT update a single edge. Returns the updated edge"""
        return self.make_request("PUT", "nodes/"+_id, { "id" : name, "source" : source, "target" : target, "data" : data })

    def update_edge_by_source_target(self, _source, _target, source=None, target=None, name=None, data={}):
        """PUT update a single edge. Returns the updated edge"""
        return self.make_request("PUT", "edges?source=%s&target=%s"%(_source,_target), { "id" : name, "source" : source, "target" : target, "data" : data })


    def delete_edges(self, _ids):
        """DELETE a bunch of edges. Returns empty edges"""
        return self.make_request("POST", "edges/delete", { "edges" : _ids })

    def get_edges(self, topogramId):
        """GET all edges from a topogram. Returns a list of edges"""
        return self.make_request("GET", "topograms/"+topogramId+"/edges", {})

    def get_nodes(self, topogramId):
        """GET all nodes from a topogram. Returns a list of node"""
        return self.make_request("GET", "topograms/"+topogramId+"/nodes", {})
