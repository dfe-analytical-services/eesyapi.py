from api_url import api_url
import requests
from typing import Dict, Any, List, Optional 

from api_url import api_url 
from utils import check_response, extract_results
from convert_api_filter_type import convert_api_filter_type

def build_query_body(
        indicators: Optional[List[str]] = None, 
        time_periods: Optional[List[str]] = None, 
        geographic_levels: Optional[List[str]] = None, 
        locations: Optional[List[str]] = None, 
        filters: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    
 """
 Build request body for EES API query endpoint 
 """

 body = {}

 if indicators:
    body["indicators"] = indicators

 if time_periods:
   body["timePeriods"] = time_periods

 if geographic_levels:
   body["geographicLevels"] = geographic_levels

 if locations:
   body["locations"] = locations 

 if filters:
   body["filters"] = filters 

 return body


def query(
    dataset_id: str, 
    indicators: Optional[List[str]] = None, 
    time_periods: Optional[List[str]] = None, 
    geographic_levels: Optional[List[str]] = None, 
    locations: Optional[List[str]] = None, 
    filters: Optional[List[Dict[str, Any]]] = None, 
    dataset_version: Optional[str] = None, 
    ees_enivronment: str ='prod',
    api_version: str = "1", 
    page_size: int = 100, 
    paginate: bool = True, 
    verbose: bool = False
) -> List[Dict[str, Any]]:
  
  """
  Query dataset from EES API 

  Returns:
      List of results (optionally paginated)
  """

  if not dataset_id:
    raise ValueError("dataset_id must be provided")
  
  if page_size <= 0:
    raise ValueError("page_size must be greater than 0")
  
  filters = convert_api_filter_type(filters)

  body = build_query_body(
    indicators=indicators,
    time_periods=time_periods,
    geographic_levels=geographic_levels,
    locations=locations,
    filters=filters
  )

  all_results =[]
  page = 1

  while True:
    url = api_url(
      endpoint = "data",
      dataset_id = dataset_id,
      dataset_version=dataset_version,
      ees_environment=ees_enivronment,
      api_version=api_version,
      page=page,
      page_size=page_size
    )


    if verbose:
      print(f"[QUERY] Page {page}")
      print(f'Post{url}')
      print(f"Body: {body}")


    response = requests.post(url, json=body)

    check_response(response)

    data = response.json()

    results = extract_results(data)

    if not results:
      if verbose:
        print("[QUERY] No more results - stopping")
      break 

    all_results.extend(results)

    if not paginate:
      break 

    total_results  = data.get("totalResults")
    if total_results is not None and len(all_results) >= total_results:
        if verbose:
          print("[Query] all results fetched")
        break
        
      
    page += 1

  return all_results
    
  
  
  