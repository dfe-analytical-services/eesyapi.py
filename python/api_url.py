"""
api_url.py

Url builder for Explore Education Statistics (EES) API 

"""

from urllib.parse import urlencode

def api_url(
    endpoint: str = "get-publications",
    search = None, 
    publication_id = None, 
    dataset_id = None, 
    indicators = None, 
    time_periods = None, 
    geographic_levels = None,
    locations = None, 
    filter_items = None, 
    dataset_version = None, 
    ees_environment = None, 
    api_version = None, 
    page_size = None, 
    page = None, 
    verbose = False ):
        
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


# print(api_url())
print(api_url(
    endpoint="get-data-catalogue", 
    publication_id="8b7474f9-5870-4ecc-7557-08da5f64dcf1",
    filter_items="Absence reason"
))