import re
import json
import re
import signal
from datetime import datetime, timedelta
from io import BytesIO
from subprocess import PIPE, Popen
from time import sleep, strftime

import pytest
import requests

url = 'http://127.0.0.1:5000'

@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python", "server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

def test_Search(url):
    '''test output of search'''
    searchData = {
        'searchOption': 'Movie',
        'keyword': 'tiger',
        'sortOption': 'Name',
    }

    response = requests.get(f'{url}', params=searchData).json()
    assert response[0][1] == "A Night for Dying Tigers"
    
def test_longKeyword(url):
    '''test long keyword > 40 - 400 error'''
    searchData = {
        'keyword': 'a'*41,
    }
    response = requests.get(f'{url}', params=searchData)
    assert response.status_code == 400

def test_emptyKeyword(url):
    '''test empty keyword - 400 error'''
    searchData = {
        'keyword':""
    }
    response = requests.get(f'{url}', params=searchData)
    assert response.status_code == 400
    response = requests.get(f'{url}', params={})
    assert response.status_code == 400
    