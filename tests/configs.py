import requests
import pytest
import configparser


def get_url():
    config = configparser.ConfigParser()
    config.read('tests/pytest.ini')
    baseurl = config.get('API', 'assets_endpoint')
    return baseurl





