# Topogram Python API Client

![Read The Docs Build](https://readthedocs.org/projects/topogram/badge/?version=latest)

A python lib to communicate with Topogram

## How it works


```python 
from topogram-python-client import TopogramAPIClient

topogram = TopogramAPIClient("http://localhost:3000")

# create a new network
topogram.create_topogram("test")
```

See a complete example in [examples](./examples) folder

## Documentation

Read the docs at [http://topogram.readthedocs.io/](http://topogram.readthedocs.io/)


## Install
    
    pip install topogram-api-client
    
or using github

    git clone https://github.com/topogram/topogram-api-client
    cd topogram-api-client
    python setup.py install


## command-line

    topogram-client

## tests

You will need to run a test instance of [Topogram](http://github.com/topogram/topogram) with a different DB on the 3030 port.

    export MONGO_URL=mongodb://localhost:27017/test_topogram; meteor --port 3030

Install the dev dependencies

    pip install -r dev_requirements.txt

Then you can run the tests

    nosetests --rednose tests
