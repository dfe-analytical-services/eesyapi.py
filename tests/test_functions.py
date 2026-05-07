import eesyapi


from eesyapi.api_url_pages import api_url_pages
from eesyapi.api_url_query import build_query_body, query
from eesyapi.convert_api_filter_type import convert_api_filter_type
from eesyapi.get_dataset_versions import get_dataset_versions

print("basic function checks")
print("---------------------")

publication_id = "8b7474f9-5870-4ecc-7557-08da5f64dcf1"

dataset_id = None

def test_api_url():
    try:
        result = eesyapi.api_url()
        print("api_url: PASS")
        print(result)
    except Exception as e:
        print("api_url: FAIL")
        print(e)


# api_url_pages

def test_api_url_pages():
    try:
        result = api_url_pages(page_size=10, page=2)
        print("api_url_pages: PASS")
        print(result)
    except Exception as e:
        print("api_url_pages: FAIL")
        print(e)

