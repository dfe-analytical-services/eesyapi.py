"""
api_url.py

Url builder for Explore Education Statistics (EES) API.

This module constructs the correct API URL for each endpoint type.
handling environment selection, versioning and query parameter encoding.

"""

from urllib.parse import urlencode

def api_url(
    endpoint: str = "get-publications",  #API endpoint name - default is publications list
    search=None,                         #Optional search string for filtering publications
    publication_id=None,                 #Required for "get-data-catalogue" endpoint
    dataset_id=None,                     #Required for all dataset-level endpoints
    indicators=None,                     #List of indicator sqids for GET data queries
    time_periods=None,                   #List of time period strings e.g.., ["2024|AY"]
    geographic_levels=None,              #List of geographic level codes e.g.., ["NAT", "REG"]
    locations=None,                      #List of location codes e.g.., ["NAT|code|E92000001"]
    filter_items=None,                   #List of filter item sqids
    dataset_version=None,                #Optional dataset version e.g.., "2.1.0" or "2.*"
    ees_environment=None,                #Target environment: "dev", "test", "preprod", "prod"
    api_version=None,                    #API version number - default to "1"
    page_size=None,                      #Number of results per page
    page=None,                           #Page number to retrieve
    verbose=False,                       #If True, prints the constructed URL
):
    
    """
    Build and return a URL for connecting to the EES API.

    The URL structure depends on the endpoint chosen:
    -get-publications  -> /publications
    -get-data-catalogue -> /publications/{id}/data-sets
    -get-dataset-versions -> /data-sets/{id}/versions
    -get-summary          ->/data-sets/{id}
    -get-meta             ->/data-sets/{id}/meta
    -get-csv              ->/data-sets/{id}/csv
    -get-data / post-data ->/data-sets/{id}/query
    """
    
    #Environment validation 
    #Default to "prod" if environment  is not one of the valid options

    if ees_environment not in ("dev","test","preprod","prod"):
        ees_environment = "prod"
    else:
        ees_environment = ees_environment
    
    #Default API version to "1" if not provided

    if api_version is None:
        api_version = "1"

    # Base URLs for each environment
    # dev/test/preprod require DFE VPN access

    base_urls = {
        "dev": "https://pp-api.education.gov.uk/statistics-dev/",
        "test": "https://pp-api.education.gov.uk/statistics-test/",
        "preprod": "https://pp-api.education.gov.uk/statistics-preprod/",
        "prod": "https://api.education.gov.uk/statistics/",
    }

    # Combine base URL with API version e.g.., "https://api.education.gov.uk/statistics/v1/"

    endpoint_base_version  = base_urls[ees_environment] + "v" + api_version + "/"

    # Keep base URL reference (unused but kept for potential future use)

    base = base_urls[ees_environment]

    #Build URL based on endpoint type

    if endpoint == "get-publications":
        #Publications list endpoint - supports pagination and search filtering 

        params = {}

        if page_size:
            params["pageSize"] = page_size  # Number of results per page

        if page:
            params["page"] = page  # Page number to retrieve

        if search:
            params["search"] = search   # Filter publications by title/summary
        
        # Base publications URL 

        url = endpoint_base_version + "publications"

        # Append query params if any were provided

        if params:
            url += "?" + urlencode(params)

    # Get Data Catalogue

    # Returns all API datasets within a given publication

    elif endpoint == "get-data-catalogue":

        # publication_id is mandatory for this endpoint

        if not publication_id:
            raise ValueError("publication_id is required")

        params = {}

        if page_size:
            params["pageSize"] = page_size

        if page:
            params["page"] = page
        
        #URL pattern: /publications/{publication_id}/data-sets

        url = endpoint_base_version + f"publications/{publication_id}/data-sets"

        if params:
            url += "?" + urlencode(params)

    # Dataset Endpoints
    # All remaining endpoints require a dataset_id

    else:

        # dataset_id is mandatory for all dataset-level endpoints
        if not dataset_id:
            raise ValueError("dataset_id is required")
        
        # Start with the base dataset URL

        url = endpoint_base_version + f"data-sets/{dataset_id}"

        if endpoint == "get-dataset-versions":
            # Returns all available versions of a dataset
            url += "/versions"

        elif endpoint != "get-summary":
            # get-summary uses the base dataset URL with no suffix

            if endpoint == "get-meta":
                # Returns metadata: filters, indicators, time periods, locations
                url += "/meta"

            elif endpoint == "get-csv":
                # Returns the full dataset as a downloadable CSV file
                url = endpoint_base_version + f"data-sets/{dataset_id}/csv"

            else:
                # get-data and post-data both use the /query suffix
                url += "/query"

            # Append dataset versions as query param if provided
            if dataset_version:
                url += f"?dataSetVersion={dataset_version}"

        # Get data endpoint - append filter params to URL query string 
        # Note: POST data endpoint uses a JSON body instead (not build here)

        if endpoint == "get-data":

            params = {}

            # Add indicator sqids as comma-separated list

            if indicators:
                params["indicators"] = ",".join(indicators)
            
            # Add time period filters e.g.., "2024|AY, 2023|AY"

            if time_periods:
                params["timeperiods"] = ",".join(time_periods)

            # Add geographic level filters e.g.., "NAT, REG"

            if geographic_levels:
                params["geographicLevels"] = ",".join(geographic_levels)
            
            # Add locations filters e.g.., "NAT|code|E92000001"

            if locations:
                params["locations"] = ",".join(locations)
            
            # Add filter item sqids

            if filter_items:
                params["filters"] = ",".join(filter_items)

            # Pagination Logic
            #If only one of page/page_size is provided, default the other

            if page and not page_size:
                page_size = 1000   #Default page size if page given but no size

            if page_size and not page:
                page = 1           # Default to page 1 if size given but no page

            if page_size:
                params["pageSize"] = page_size

            if page:
                params["page"] = page
            
            # Append all GET params to the URL

            if params:
                url += "?" + urlencode(params)
                
    # Return the fully constructed URL 
    return url
