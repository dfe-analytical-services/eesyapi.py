"""Retrieve education data from the Explore Education Statistics API."""

from .api_url import api_url
from .get_publications import get_publications
from .get_data_catalogue import get_data_catalogue
from .get_dataset import get_dataset
from .get_dataset_versions import get_dataset_versions
from .get_meta import get_meta
from .query_dataset import query_dataset
from .post_dataset import post_dataset
from .preview_dataset import preview_dataset
from .generate_ees_meta import generate_ees_meta

__all__ = [
    "api_url",
    "get_publications",
    "get_data_catalogue",
    "get_dataset",
    "get_dataset_versions",
    "get_meta",
    "query_dataset",
    "post_dataset",
    "preview_dataset",
    "generate_ees_meta",
]

__version__ = "0.1.0"
__author__ = "DfE Analytical Services"
