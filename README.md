# Topogram Python API Client

A python lib to communicate with Topogram

## How it works

    from topogram-python-client import RhiziAPIClient

    topogram = TopogramAPIClient("http://localhost:3000")

    # create a new network
    topogram.create_topogram("test")

## command-line

    topogram-client

## tests

You will need to run a test instance of [Topogram](http://github.com/topogram/topogram) with a different DB on the 3030 port.

    export MONGO_URL=mongodb://localhost:27017/test_topogram; meteor --port 3030

Install the dev dependencies

    pip install -r dev_requirements.txt

Then you can run the tests

    nosetests --rednose tests
