"""
test_api_url.py

Url builder for Explore     Education Statistics (EES) API 

"""

from urllib.parse import urlparse, parse_qs
from eesyapi import api_url
import pytest


def parse_url(url: str):
    "return (base_without_query, query_dict) for easy assertions."
    parsed = urlparse(url)
    base = parsed.scheme + "://" + parsed.netloc + parsed.path
    params = parse_qs(parsed.query)
    return base, params

class Testapiurl:
#testing api_url returns expected base output
    def test_api_url_noparams(self):
        url = api_url()
        assert url == "https://api.education.gov.uk/statistics/v1/publications"

    def test_with_search(self):
        url = api_url(search="absence")
        base, params = parse_url(url)
        assert base.endswith("/publications")
        assert params["search"] == ["absence"]
