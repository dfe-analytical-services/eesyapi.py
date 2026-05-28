"""
get_dataset.py
 
Retrieve summary information for a specific EES API dataset.
 
Returns metadata about a dataset such as its title, summary, status
and latest version. This is different from get_meta() which returns
the statistical metadata (filters, indicators, time periods).
"""
import requests 
from typing import Optional, List, Dict, Any 

from api_url import api_url

def validate_ees_id(ees_id: str):
    """
    Validate that a dataset ID is a non-empty string.
 
    Parameters
    ----------
    ees_id : str
        Dataset ID to validate.
 
    Raises
    ------
    ValueError
        If ees_id is empty, None or not a string.
    """
    # Reject empty strings, None and non-string types
    if not ees_id or not isinstance(ees_id, str):
        raise ValueError("Invalid dataset_id")

def validate_page_size(page_size: Optional[int]):
    """
    Validate that page_size is a positive integer.
 
    Parameters
    ----------
    page_size : int or None
        Page size to validate. None is allowed.
 
    Raises
    ------
    ValueError
        If page_size is provided and not greater than 0.
    """
    # Only validate if a value was provided — None means use API default
    if page_size is not None and page_size <=0:
        raise ValueError("page_size must be greater than 0")
    

def warning_max_pages(response: Dict[str, Any]):
    """
    Warn if the requested page exceeds total available pages.
 
    Parameters
    ----------
    response : dict
        API response dict containing "paging" key with page info.
    """
    # Only check if paging info is present in the response
    if "paging" in response:
        total_pages = response["paging"].get("totalPages", 1)
        current_page = response["paging"].get("page", 1)
        # Warn if requested page number is beyond what is available
        if current_page > total_pages:
            print("Warning: Requested page exceeds total available pages")

def get_dataset(
        dataset_id: str,                              # Unique ID of the dataset (required)
        dataset_version: Optional[str] = None,        # Optional version e.g. "2.1.0" or "2.*"
        ees_environment: Optional[str] = None,        # One of: "dev", "test", "preprod", "prod"
        api_version: Optional[str] =None,             # EES API version — defaults to "1"
        page_size: Optional[int] = None,              # Results per page — None uses API default
        page: Optional[int] = None,                   # Specific page to fetch — None fetches all
        verbose: bool = False                         # Print URLs and debug info if True
) -> List[Dict]:

    """
    Retrieve summary information for a specific EES API dataset.
 
    Returns dataset summary including title, summary, status and
    latest version info. For statistical metadata (filters, indicators,
    time periods), use get_meta() instead.
 
    If page is None, automatically paginates through all pages and
    returns all results combined.
 
    Parameters
    ----------
    dataset_id : str
        Unique ID of the dataset. Required.
    dataset_version : str, optional
        Version in "major.minor.patch" format with optional wildcards
        e.g. "2.1.0", "2.*", "*". Defaults to latest version.
    ees_environment : str, optional
        One of "dev", "test", "preprod", "prod". Default "prod".
    api_version : str, optional
        EES API version. Default "1".
    page_size : int, optional
        Number of results per page. None uses the API default.
    page : int, optional
        Specific page to retrieve. If None, all pages are fetched.
    verbose : bool
        Print request URLs and debug info. Default False.
 
    Returns
    -------
    list of dict
        List of dataset summary dicts containing id, title, summary,
        status and latestVersion fields.
 
    Raises
    ------
    ValueError
        If dataset_id is invalid or page_size is not positive.
    Exception
        If the API returns a non-200 status code.
 
    Examples
    --------
    >>> get_dataset(
    ...     dataset_id="1d419801-a90e-f970-9335-a13623faccbe",
    ...     ees_environment="prod"
    ... )
    """
    
   # Validate inputs before making any API calls
    validate_ees_id(dataset_id)
    validate_page_size(page_size)

   # Build URL for the first (or only) page request
    # Uses "get-summary" endpoint which returns dataset summary info
    url = api_url(
        endpoint="get-dataset",                 # get-dataset maps to get-summary endpoint
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        ees_environment=ees_environment,
        api_version=api_version,
        page_size=page_size,
        page=page,
        verbose=verbose
    )
    # Print the request URL in verbose mode
    if verbose:
        print(f"GET {url}")
    # Send GET request to the dataset summary endpoint
    response = requests.get(url)
    # Raise exception if request failed
    if response.status_code !=200:
        raise Exception(f"API Error: {response.status_code}")
    # Parse JSON response
    data = response.json()

   # Auto-pagination — fetch all pages if no specific page was requested
    if page is None:
        # Check total number of pages available
        total_pages = data.get("paging", {}).get("totalPages", 1)

        if total_pages > 1:
            # Fetch pages 2 through total_pages and append results
            for p in range(2, total_pages + 1):
                # Build URL for this specific page
                url_page = api_url(
                    endpoint = "get-dataset",
                    dataset_id=dataset_id,
                    dataset_version=dataset_version,
                    ees_environment=ees_environment,
                    api_version=api_version,
                    page_size=page_size,
                    page=p,
                    verbose=verbose
                )

                if verbose:
                    print(f"GET page {p}: {url_page}")
                 # Fetch this page
                response_page = requests.get(url_page)
                # Raise exception if any page request fails
                if response_page.status_code !=200:
                    raise Exception(f"API Error: {response_page.status_code}")
                
                data_page = response_page.json()
                # Append this page's results to the first page's results
                data["results"].extend(data_page.get("results", []))
    # Warn if requested page exceeded available pages
    warning_max_pages(data)
    # Return the combined results list
    return data.get("results", [])
