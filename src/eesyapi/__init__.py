"""
eesyapi Package 

Python SDK for the Explore Education Statistics (EES) API

"""

# Expose main function for easy access 


from eesyapi.get_publications import (
    get_publications,
    validate_page_size,
    warning_max_pages,
)