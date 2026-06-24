import requests
import pandas as pd 
from typing import Optional, Dict, Any, List

from .api_url import api_url 

def get_meta_response(
        dataset_id: str,
        dataset_version: Optional[str] = None, 
        preview_token: Optional[str] = None, 
        ees_environment: Optional[str] = None, 
        api_version: Optional[str] = None, 
        parse: bool = True, 
        verbose: bool = False
) -> Any:
    
    if not isinstance(parse, bool):
        raise ValueError("parse must be True or False")
    
    url = api_url(
        endpoint="get-meta",
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        preview_token=preview_token,
        ees_environment=ees_environment,
        api_version=api_version,
        parse= True,
        verbose=verbose
    )

    headers = {}
    if preview_token:
        headers["Preview-Token"] = preview_token
    
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code}")
    
    return response.json() if parse else response

def parse_meta_time_periods(api_meta_time_periods):

    df = pd.DataFrame(api_meta_time_periods)

    if "code" not in df.colums:
        raise ValueError("Code column not found in timePeriods data")
    
    df["code_num"] = df["code"].str.replace(r"[a-zA-Z]", "", regex=True).astype(float)
    df = df.sort_values("code_num").drop(columns=["code_num"])

    return df

def parse_meta_location_ids(api_meta_locations):

    levels = api_meta_locations["level"]
    options = api_meta_locations["options"]

    all_rows = []

    for i in range(len(levels)):
        df = pd.DataFrame(options[i])

        df["geographic_levels_code"] = levels[i]["code"]
        df["geographic_level"] = levels[i]["label"]

        df = df.rename(columns={"id": "item_id"})

        all_rows.append(df)

    return pd.concat(all_rows, ignore_index=True)

def parse_meta_filter_columns(api_meta_filters):

    return pd.DataFrame({
        "col_id": [f["id"] for f in api_meta_filters], 
        "col_name": [f["column"] for f in api_meta_filters],
        "label": [f["label"] for f in api_meta_filters]
    })


def parse_meta_filter_item_ids(api_meta_filters):

    rows = []

    for f in api_meta_filters:
        col_id = f["id"]
        col_name = f["column"]
        label = f["label"]

        for opt in f.get("options", []):
            rows.append({
                "col_id": col_id,
                "col_name": col_name,
                "label": label, 
                "item_id": opt.get("id"),
                "item_label": opt.get("label"), 
                "isAggregate": opt.get("isAggregate")

            })
    
    df = pd.DataFrame(rows)

    if "isAggregate" not in df.columns:
        df["isAggregate"] = None
    
    return df 

def get_meta(
     dataset_id: str,
     dataset_version: Optional[str] = None, 
     preview_token: Optional[str] = None, 
     ees_environment: Optional[str] = None, 
     api_version: Optional[str] = None, 
     verbose: bool = False
) -> Dict[str, Any]:

     response = get_meta_response(
          dataset_id,
          dataset_version=dataset_version, 
          preview_token=preview_token, 
          ees_environment=ees_environment, 
          api_version=api_version,
          parse = True, 
          verbose = verbose

     )

     meta_data = {
         "time_periods": parse_meta_time_periods(response.get("timePeriods", [])),
         "locations" : parse_meta_location_ids(response.get("locations", {})),
         "filter_columns" : parse_meta_filter_columns(response.get("filters", [])), 
         "filter_items" : parse_meta_filter_item_ids(response.get("filters", [])),
         "indicators" : parse_meta_filter_columns(response.get("indicators", ))
     }

     return meta_data




         
     