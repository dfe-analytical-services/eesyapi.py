"""
eesyapi Package 

Python SDK for the Explore Education Statistics (EES) API

"""

# Expose main function for easy access 
from .api_url import api_url
from .api_url_pages import api_url_pages
from .api_url_query import api_url_query
from .convert_api_filter_type import convert_api_filter_type
from .datasets_documentation import datasets_documentation
from .generate_ees_meta import generate_ees_meta
from .get_data_catalogue import get_data_catalogue
from .get_dataset_versions import get_dataset_versions
from .get_dataset import get_dataset
from .get_meta import get_meta
from .get_publications import get_publications

__all__ = [
    "api_url",
    "api_url_pages",
    "api_url_query",
    "convert_api_filter_type",
    "datasets_documentation",
    "generate_ees_meta",
    "get_data_catalogue",
    "get_dataset_versions",
    "get_dataset",
    "get_meta",
    "get_publications",
]