"""
eesyapi Package 

Python SDK for the Explore Education Statistics (EES) API

"""

# Expose main function for easy access 

from .api_url import api_url
from .api_url_pages import api_url_pages
from .api_url_query import api_url_query
from .convert_api_filter_type import convert_api_filter_type
from .get_publications import get_publications
from .get_meta import get_meta
from .get_dataset import get_dataset
from .get_data_catalogue import get_data_catalogue