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

    def create_topogram(self, name):
        """Create a topogram based on a name or a dict"""
        assert type(name) == str
        return self.make_request("POST", "topograms", { "name" : name })

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

    def delete_topogram(self, _id):
        """DELETE a topogram from its _id. Returns an empty topograms"""
        return self.make_request("DELETE", "topograms/"+_id, {})

    def create_node(self, topogramId, id=None, x=None, y=None, data={}):
        """POST Create a single node. Returns the created node."""
        assert type(data) is dict
        if id : assert type(id) is str
        if x : assert type(x) is float or type(x) is int
        if y : assert type(y) is float or type(x) is int

        el = {
            "id" : id,
            "x" : x,
            "y" : y
        }
        return self.make_request("POST", "nodes", { "element" : el, "data" : data })

    def get_node(self, _id):
        """GET a single node. Returns a node"""
        return self.make_request("GET", "nodes/"+_id, {})

    def update_node(self, _id, id=None, x=None, y=None, data={}):
        """PUT update a single node. Returns the updated node"""
        return self.make_request("PUT", "nodes/"+_id, { "id" : id, "x" : x, "y" : y, "data" : data })

    def delete_node(self, _id):
        """DELETE a node. Returns an empty node"""
        return self.make_request("DELETE", "nodes/"+_id, {})
