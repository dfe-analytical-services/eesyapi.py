"""
api_url.py

Url builder for Explore Education Statistics (EES) API 

"""

from urllib.parse import urlencode
from typing import Optional, List, Dict, Any 

def api_url(
    endpoint: str = "get-publications",
    search: Optional[str] = None, 
    publication_id: Optional[str] = None, 
    dataset_id: Optional[str] = None, 
    indicators: Optional[list] = None, 
    time_periods: Optional[list] = None, 
    geographic_levels: Optional[list] = None,
    locations: Optional[list] = None, 
    filter_items: Optional[list] = None, 
    dataset_version: Optional[str] = None, 
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
          publication_id: Publication ID key 
          dataset_id: Data set ID key
          indicators: Indicators for data set query 
          time_periods: Time periods for data set query
          geographic_levels: Geographic levels for data set query
          locations: Locations for data set query
          filter_items: Filter items for data set query
          dataset_version: Dataset version
          ees_environment: API environment, such as dev, test, preprod or prod.
          api_version: API version to use.
          page_size: Number of records to return per page.
          page: Specific page number to fetch. If None, all pages are fetched.
          verbose: If True, prints the API URLs being requested.

    Returns:
        str: The API URL for the requested endpoint.

    Example:
        ```python
        api_url()
        ```

    """     
#Default Values

     if ees_environment is None:
        ees_environment = "prod"
    
     if api_version is None:
           api_version = "1"

#Base URL

     _base_urls = {
        "dev": "https://pp-api.education.gov.uk/statistics-dev/", 
        "test": "https://pp-api.education.gov.uk/statistics-test/", 
        "preprod": "https://pp-api.education.gov.uk/statistics-preprod/", 
        "prod": "https://api.education.gov.uk/statistics/"
     }

     base = _base_urls[ees_environment] + "v" + api_version + "/"

#Get Publications 

     if endpoint == "get-publications":
         
         params = {}

         if page_size:
              params["pageSize"] = page_size
        
         if page:
              params["page"] = page

         if search:
              params["search"] = search 

         url = base + "publications"

         if params:
              url += "?" + urlencode(params)


# Get Data Catalogue

     elif endpoint == "get-data-catalogue":

         if not publication_id:
              raise ValueError("publication_id is required")

         params = {}

         if page_size:
              params["pageSize"] = page_size

         if page:
              params["page"] = page

         url = base + f"publications/{publication_id}/data-sets"

         if params:
              url += "?" + urlencode(params) 


# Dataset Endpoints     

     else:
         
         if not dataset_id:
              raise ValueError("dataset_id is required")
         
         url = base + f"data-sets/{dataset_id}"

         if endpoint == "get-dataset-versions":
              url += "/versions"

         elif endpoint != "get-summary":
              
              if endpoint == "get-meta":
                   url += "/meta"

              elif endpoint == "get-csv":
                   url = base + f"data-sets/{dataset_id}/csv"

              else:
                   url += "/query"

              if dataset_version:
                   url += f"?dataSetVersion={dataset_version}"

# Get data(filters)

         if endpoint == "get-data":
              
              params ={}

              if indicators:
                   params["indicators"] = ",".join(indicators)
             
              if time_periods:
                   params["timeperiods"] = ",".join(time_periods)
              
              if geographic_levels:
                   params["geographicLevels"] = ",".join(geographic_levels)

              if locations:
                   params["locations"] = ",".join(locations)
            
              if filter_items:
                   params["filters"] = ",".join(filter_items)


# Pagination Logic

              if page and not page_size:
                   page_size = 1000

              if page_size and not page:
                   page = 1
              
              if page_size:
                   params["pageSize"] = page_size

              if page:
                   params["page"] = page
            
              if params:
                   url += "?" + urlencode(params)

# Verbose

     if verbose:
         print("Generated URL:")
         print(url)
     return url 
