"""
api_url_pages.py

Builds parameters (page and pageSize) are appended to API URL requests.

Pagination parameters (page and pageSize) are appended to API URLs
to control how many results are returned and which page to retrieve.
"""




def api_url_pages(page_size: int = 40, page: int = None) -> str:

    """
    Build pagination query string for use in EES API URLs.

    Constructs the page and pageSize portion of a URL query string.
    for example: "page=2&pageSize=40"

    Parameters

    page_size : int 
        Number of results to return per page. Default is 40 
        Pass None to omit pageSize from the query string.
    
    page : int or None

        page number to retrieve. Default is None (omitted from query string).
        pass an integer to request a specific page.
    
    Returns

    str

        A query string containing page and/or pageSize parameters,
        joined by "&". Returns empty string if both are None.
    
    Examples

    >>> api_url_pages()
    'pageSize=40'

    >>> api_url_pages(page_size=100, page=2)
    'page=2&pageSize=100'

    >>> api_url_pages(page_size=None, page=None)

    """

    #Collect query string parts in order: page first, then pageSize
    parts = []

    #Only include page if explicity provided - None means omit from URL 

    if page is not None:
        parts.append(f"page={page}")
    
    #Only include pageSize if nor None- allows caller to omit it entirely

    if page_size is not None:
        parts.append(f"pageSize={page_size}")
    
    # Join parts with "&" - returns empty string if no params were 

    return "&".join(parts)
