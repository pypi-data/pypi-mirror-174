import pytest
from bs4 import BeautifulSoup

def test_soup_factory(Parser):
    assert type(Parser._soup_factory('')) is BeautifulSoup
