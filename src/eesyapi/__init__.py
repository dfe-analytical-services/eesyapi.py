"""
eesyapi Package 

Python SDK for the Explore Education Statistics (EES) API

"""

# Expose main function for easy access 


from eesyapi.api_url import (
    api_url
)


from eesyapi.get_publications import (
    get_publications,
    validate_page_size,
    validate_environment,
    warning_max_pages
)
