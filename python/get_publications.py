import requests 
from typing import Optional, List, Dict, Any 

from api_url import api_url 

def validate_page_size(page_size: Optional[int]):
    """
    Validate the page size value before calling the API.

    Args:
        page_size: Number of records requested per page.

    Raises:
        ValueError: If page_size is less than or equal to 0.
    """
    # page_size is optional, so only validate it when a value is provided.
    if page_size is not None and page_size <=0:
        raise ValueError("page_size must be greater than 0")
    

def warning_max_pages(response: Dict[str, Any]):
    """
    Print a warning when the requested page number is greater than
    the total number of available pages.

    Args:
        response: JSON response from the API.
    """
     # Check whether the API response contains paging information.
    if "paging" in response:
        total_pages = response["paging"].get("totalPages", 1)
        current_pages = response["paging"].get("page", 1)
        
        # Warn the user if they requested a page that does not exist.
        if current_pages > total_pages:
            print("Warning: Requested page exceeds total available pages")

def get_publications(
        search: Optional[str] = None, 
        ees_environment: Optional[str] = None, 
        api_version: Optional[str] = None, 
        page_size: Optional[int] = None, 
        page: Optional[int] = None, 
        verbose: bool = False
) -> List[Dict]:
     """
    Fetch publication records from the Explore Education Statistics API.

    If a specific page is provided, only that page is returned.
    If page is None, the function fetches all available pages and combines
    the results into one list.

    Args:
        search: Optional search keyword for filtering publications.
        ees_environment: API environment, such as dev, test, or prod.
        api_version: API version to use.
        page_size: Number of records to return per page.
        page: Specific page number to fetch. If None, all pages are fetched.
        verbose: If True, prints the API URLs being requested.

    Returns:
        List[Dict]: A list of publication records.

    Raises:
        Exception: If the API request returns a non-200 status code.
    """
    # Validate page_size before creating the API request.
    validate_page_size(page_size)

   # Build the API URL for the first request.
    url = api_url(
        endpoint="get-publications",
        search = search, 
        ees_environment=ees_environment,
        api_version=api_version,
        page_size=page_size, 
        page=page,
        verbose=verbose
    )
    # Print the API URL when verbose mode is enabled.
    if verbose:
        print(f"GET {url}")
   # Send GET request to the API.
    response = requests.get(url)
  # Raise an error if the API response is not successful.
    if response.status_code !=200:
            raise Exception(f"API Error: {response.status_code}")
    # Convert API response to JSON.   
    data = response.json()
   # If page is not provided, fetch all pages automatically.
    if page is None:
        total_pages = data.get("paging", {}).get("totalPages",1)
       # If there is more than one page, fetch pages 2 to total_pages.
        if total_pages > 1:
            for p in range(2, total_pages +1):
                # Build URL for the next page.
                url_page = api_url(
                    endpoint = "get-publications",
                    search = search, 
                    ees_environment = ees_environment,
                    api_version = api_version,
                    page_size = page_size,
                    page = p, 
                    verbose = verbose 
                )
                 # Build URL for the next page.
                if verbose:
                    print(f"GET page {p}: {url_page}")
                    
                # Send request for the current page.
                response_page = requests.get(url_page)
                
                # Raise an error if the page request fails.
                if response_page.status_code !=200:
                    raise Exception(f"API Error: {response_page.status_code}")
                # Convert page response to JSON.  
                data_page = response_page.json()
                # Add results from this page to the main results list.
                data["results"].extend(data_page.get("results",[]))

    # Warn user if requested page is beyond available pages.
    warning_max_pages(data)
    # Return only the publication records.
    return data.get("results",[])

