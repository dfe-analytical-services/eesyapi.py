import pytest
from api_url_pages import api_url_pages

class TestApiUrlPages:
    def test_returns_string(self):
        assert isinstance(api_url_pages(), str)

    def test_default_page_size_40(self):
        result = api_url_pages()
        assert "pageSize=40" in result

    def test_custom_page_is_none(self):
        result = api_url_pages()
        assert "page=" not in result

    def test_custom_page_size(self):
        result = api_url_pages(page_size=100)
        assert "pageSize=100" in result

    def test_custom_page(self):
        result = api_url_pages(page_size=40, page=2)
        assert "page=2" in result

    def test_page_none_not_in_result(self):
        result = api_url_pages(page_size=40, page=None)
        assert "page=" not in result

    def test_both_params_joined_with_ampersand(self):
        result = api_url_pages(page_size=10, page=3)
        assert "&" in result
        assert "page=3" in result
        assert "pageSize=10" in result

    def test_page_1(self):
        result = api_url_pages(page_size=50, page=1)
        assert "page=1" in result
        assert "pageSize=50" in result

    def test_large_page_size(self):
        result = api_url_pages(page_size=1000)
        assert "pageSize=1000" in result

    def test_only_page_size_no_ampersand(self):
        result = api_url_pages(page_size=40)
        assert "&" not in result

    def test_page_comes_before_page_size(self):
        result = api_url_pages(page_size=40, page=2)
        assert result.index("page=") < result.index("pageSize=")

    def test_page_size_zero(self):
        result = api_url_pages(page_size=0)
        assert "pageSize=0" in result

    def test_page_size_none_not_in_result(self):
        result = api_url_pages(page_size=None, page=1)
        assert "pageSize=" not in result

    def test_both_none_returns_empty_string(self):
        result = api_url_pages(page_size=None, page=None)
        assert result == ""

    def test_page_10(self):
        result = api_url_pages(page_size=40, page=10)
        assert "page=10" in result