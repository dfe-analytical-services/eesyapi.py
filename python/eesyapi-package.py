"""
eesyapi Package
 
Python SDK for the Explore Education Statistics (EES) API.
 
This is the main package entry point. It exposes the most commonly
used functions at the top level so users can import them directly:
 
    from eesyapi import api_url
    from eesyapi import get_publications
    from eesyapi import query_dataset
 
instead of having to import from individual modules:
 
    from eesyapi.api_url import api_url
    from eesyapi.get_publications import get_publications
 
This file is the Python equivalent of the R package NAMESPACE file,
which controls what is exported and visible to end users.
"""

# Expose main function for easy access 

# URL builders

# Core URL builder — constructs EES API endpoint URLs
from .api_url import api_url

# POST query body builder — builds and executes paginated data queries
from .api_url_query import api_url_query

# Filter utilities
# Converts user-supplied filter dicts/lists into API-compatible format
from .convert_api_filter_type import convert_api_filter_type

# Publication and catalogue functions

# Returns list of all publications available via the EES API
from .get_publications import get_publications

# Returns list of all API datasets within a given publication
from .get_data_catalogue import get_data_catalogue

# Dataset functions

# Returns metadata for a dataset: filters, indicators, time periods, locations
from .get_meta import get_meta

# Returns dataset summary information
from .get_dataset import get_dataset
 
# Returns all available versions of a dataset
from .get_dataset_versions import get_dataset_versions
 
# Returns a preview of the raw CSV data for a dataset
from .preview_dataset import preview_dataset

# Query functions

# Main function for querying datasets — supports POST and GET methods
from .query_dataset import query_dataset
 
# POST-specific dataset query function
from .post_dataset import post_dataset

# Package metadata

__version__ = "0.1.0"           # Current package version
__author__  = "DfE Analytical Services"  # Package author

