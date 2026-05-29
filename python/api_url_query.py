"""
api_url_query.py

Builds POST request bodies and excutes paginated queries against
the Explore Education Statistics (EES) API query endpoint.

Per EES API docs, the POST /query endpoint expects:
-URL: /data-sets/{dataSetId}/query (no page/pageSize in URL)
-Body: {"criteria": {}, "indicators": [], "page": 1, "pageSize": 100}
"""


from api_url import api_url
import requests
from typing import Dict, Any, List, Optional 
from utils import check_response, extract_results
from convert_api_filter_type import convert_api_filter_type

def build_query_body(
        indicators: Optional[List[str]] = None,             # Indicator sqids to return e.g.. ["X9fKb]
        time_periods: Optional[List[str]] = None,           # Time periods e.g. ["2024|AY", "2023|W12"]
        geographic_levels: Optional[List[str]] = None,      # Level codes e.g. ["NAT", "REG"]
        locations: Optional[List[str]] = None,              # Location sqids e.g. ["dPOZw"]
        filters: Optional[List[Dict[str, Any]]] = None,     # Filter dicts with "field" and "values"
        page: int= 1,                                       # Page number - goes in body not URL 
        page_size: int = 100                                # Results per page - goes in body not URL 
) -> Dict[str, Any]:
    
 """
 Build POST request body for EES API query endpoint.

 Constructs a JSON-serialisable dict containing criteria filters, 
 indicators and pagination. Per API spec, page and pageSize belong 
 in the body - Not in the URL query string.
 """

#Start with empty criteria - only populated if filters are provided
 criteria = {}

# filter items - extract sqid values from filter dicts or strings
 if filters:
   filter_ids = [] 
   for f in filters:
     if isinstance(f, dict) and "values" in f:
         # Dict format: {"field": "absence_type", "Values": ["abc123"]}
         filter_ids.extend(f["values"])
     elif isinstance(f, str):
       # string format: just the sqid directly
       filter_ids.append(f)
   if filter_ids:
     # Add as "in" filter - matches any of the provided sqids
     criteria["filters"] = {"in": filter_ids}

#Add geographic level filters if provided e.g. {"in":  ["NAT", "REG"]}
 if geographic_levels:
    criteria["geographicLevels"] = {"in": geographic_levels}

#Add location filter if provided
 if locations:
   criteria["locations"] = {"in": locations}


#Time periods - convert "period|code" strings to API dict format

 if time_periods:
     parsed =[]
     for tp in time_periods:
       if "|" in tp:
         # Split on first pipe only to handle edge cases
         period, code = tp.split("|", 1)
         parsed.append({"period": period, "code": code})
       else:
            # Pass through as-is if no pipe separator found
            parsed.append(tp)
     criteria["timePeriods"] = {"in": parsed}
  
#Build final body dict
#page and pageSize must be in the body - Not the URL

 body = {"criteria": criteria,
         "indicators": indicators if indicators else [], #Default to empty list if None
         "page": page,    #Page number for pagination
         "pageSize": page_size   #Results per page
         }

 return body


def query(
    dataset_id: str,                                      #Dataset ID to query (required)
    indicators: Optional[List[str]] = None,               # Indicator sqids to return
    time_periods: Optional[List[str]] = None,             # Time period filters
    geographic_levels: Optional[List[str]] = None,        # Geographic level filters
    locations: Optional[List[str]] = None,                # Location sqids filters
    filters: Optional[List[Dict[str, Any]]] = None,       # Filter item sqids
    dataset_version: Optional[str] = None,                # Optional dataset version
    ees_environment: str ='prod',                         # Target environment
    api_version: str = "1",                               # API version
    page_size: int = 100,                                 # Results per page
    paginate: bool = True,                                # If True fetch all pages
    max_pages: int = 10,                                  # safetly limit on total pages 
    verbose: bool = False                                 #Print debug info if True
) -> List[Dict[str, Any]]:
  
  """
  Query a dataset from the EES API using POST requests.

  Sends a POST request to the /query endpoint with a JSON body 
  containing criteria filters, indicators and pagination.
  Optionally paginates through all result pages up to max_pages.


  Returns:
      List of results (optionally paginated)
  """

  # Validate required inputs before making any API calls

  if not dataset_id:
    raise ValueError("dataset_id must be provided")
  
  if page_size <= 0:
    raise ValueError("page_size must be greater than 0")
  
   # Normalise filter format - converts dicts/None to list of filter dicts
  filters = convert_api_filter_type(filters)

 
  # Build the URL once- page/pageSize go in body so URL stays constant
  url = api_url(
      endpoint = "get-data",
      dataset_id = dataset_id,
      dataset_version=dataset_version,
      ees_environment=ees_environment,
      api_version=api_version,
    )

# Accumulate all results across pages here
  all_results =[]
  page = 1   # Start at page 1 


  # Pagination loop - continues until one of the break condition is met 
  while True:

    # Build fresh body for each page with updated page number
    body = build_query_body(
    indicators=indicators,
    time_periods=time_periods,
    geographic_levels=geographic_levels,
    locations=locations,
    filters=filters,
    page=page,
    page_size=page_size
  )
    

    # Print debug info if verbose mode is on 

    if verbose:
      print(f"[QUERY] Page {page}")
      print(f'Post{url}')
      print(f"Body: {body}")

    # Send POST request with JSON body
    response = requests.post(url, json=body)

    # Raise exception if response status is not 200

    check_response(response)

    # Parse JSON response
    data = response.json()


    # Extract the results returned on this page
    results = extract_results(data)

    # stop if no results returned on this page
    if not results:
      if verbose:
        print("[QUERY] No more results - stopping")
      break 
    
    # Add this page's results to the accumulated list
    all_results.extend(results)

    # Stop after first page if pagination is disabled
    if not paginate:
      break

    # Stop if we've reached the max pages safetly limit 
    if page >= max_pages:
      if verbose:
        print(f"[QUERY] max_pages {max_pages} reached - stopping")
      break
    
    # stop if we've collected all available results
    total_results  = data.get("paging", {}).get("totalResults")
    if total_results is not None and len(all_results) >= total_results:
        if verbose:
          print("[Query] all results fetched")
        break
        
    # Move to next pages
    page += 1

  return all_results
    
  
  
  
