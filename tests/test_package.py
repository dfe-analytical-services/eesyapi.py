"""Check package imports and the existing publication API after integration."""

import subprocess
import sys
from urllib.parse import parse_qs, urlparse


def test_package_modules_import_without_network():
    script = """
import importlib
import pkgutil
import requests

def unexpected_request(*args, **kwargs):
    raise AssertionError('Importing the package must not make network requests')

requests.sessions.Session.request = unexpected_request
import eesyapi

for module in pkgutil.walk_packages(eesyapi.__path__, eesyapi.__name__ + '.'):
    importlib.import_module(module.name)
"""
    result = subprocess.run(
        [sys.executable, "-I", "-c", script],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_public_entrypoints_are_callable():
    import eesyapi

    expected = {
        "api_url", "get_publications", "get_data_catalogue", "get_dataset",
        "get_dataset_versions", "get_meta", "query_dataset", "post_dataset",
        "preview_dataset", "generate_ees_meta",
    }
    assert set(eesyapi.__all__) == expected
    assert all(callable(getattr(eesyapi, name)) for name in expected)


def test_existing_publication_pagination(monkeypatch):
    import eesyapi
    from eesyapi.get_publications import get_publications
    import requests

    calls = []
    records = [{"id": "first", "title": "First"}, {"id": "second", "title": "Second"}]

    class Response:
        status_code = 200

        def __init__(self, page):
            self.page = page

        def json(self):
            return {
                "paging": {"page": self.page, "totalPages": 2},
                "results": [records[self.page - 1]],
            }

    def get(url):
        params = parse_qs(urlparse(url).query)
        calls.append(params)
        assert len(calls) <= 2, "Publication pagination did not stop"
        return Response(int(params.get("page", ["1"])[0]))

    monkeypatch.setattr(requests, "get", get)
    assert eesyapi.get_publications is get_publications
    assert get_publications("attendance", "prod", "1", 1) == records
    assert [call.get("page", ["1"]) for call in calls] == [["1"], ["2"]]
    assert all(call["search"] == ["attendance"] for call in calls)
    assert all(call["pageSize"] == ["1"] for call in calls)

    calls.clear()
    assert get_publications("attendance", "prod", "1", 1, 2) == [records[1]]
    assert len(calls) == 1
