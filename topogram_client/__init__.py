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

        if path == "login" :
            return self.base_url + "/login"
        elif path == "signup":
            return self.base_url + "/signup"
        else :
            return self.base_url+"/api/"+path

    def make_request(self, method, path, data):
        assert method in ["POST", "GET", "DELETE"]
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
        else :
            raise ValueError("Unknown method : %s"%method)


        log.debug( "%s : %s", r.status_code, r.text)

        if r.status_code == 403 : # handle 403 error
            log.error("403 Unauthorized request")
            raise ValueError("403 Unauthorized request")
        return r

    def check_active_connection(self):
        r = self.make_request("GET", " ", {})
        print r
        assert r.status_code == 200
