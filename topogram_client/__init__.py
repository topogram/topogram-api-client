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
