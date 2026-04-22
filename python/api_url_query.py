from api_url import api_url
import requests
from typing import Dict, Any, List, Optional 
from utils import check_response, extract_results
from convert_api_filter_type import convert_api_filter_type

def build_query_body(
        indicators: Optional[List[str]] = None, 
        time_periods: Optional[List[str]] = None, 
        geographic_levels: Optional[List[str]] = None, 
        locations: Optional[List[str]] = None, 
        filters: Optional[List[Dict[str, Any]]] = None,
        page: int = 1,
        page_size: int =100
) -> Dict[str, Any]:
    
 """
 Build POST request body for EES API query endpoint 
 """

 criteria = {}

 if filters:
   filter_ids = [] 
   for f in filters:
     if isinstance(f, dict) and "Values" in f:
         filter_ids.extend(f["values"])
     elif isinstance(f, str):
       filter_ids.append(f)
   if filter_ids:
     criteria["filters"] = {"in": filter_ids}

 if geographic_levels:
    criteria["geographicLevels"] = {"in": geographic_levels}
 if locations:
   criteria["locations"] = {"in": locations}
  
 if time_periods:
     parsed =[]
     for tp in time_periods:
       if "|" in tp:
         period, code = tp.split("|", 1)
         parsed.append({"period": period, "code": code})
       else:
            parsed.append(tp)
     criteria["timePeriods"] = {"in": parsed}
  

 body = {
   "criteria": criteria,
   "indicators": indicators if indicators else[],
   "page": page,
   "pageSize": page_size

  }

 return body


def query(
    dataset_id: str, 
    indicators: Optional[List[str]] = None, 
    time_periods: Optional[List[str]] = None, 
    geographic_levels: Optional[List[str]] = None, 
    locations: Optional[List[str]] = None, 
    filters: Optional[List[Dict[str, Any]]] = None, 
    dataset_version: Optional[str] = None, 
    ees_environment: str ='prod',
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
      endpoint = "get-data",
      dataset_id = dataset_id,
      dataset_version=dataset_version,
      ees_environment=ees_environment,
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
    
  
  
  