import json 
import warnings
from typing import Any, Dict, List, Optional, Union 

import pandas as pd 
import requests

from api_url import api_url
from post_dataset_utils import parse_tojson_params
from query_dataset_utils import todf_geographies
from warning_max_pages import warning_max_pages
from parse_api_dataset import parse_api_dataset


def post_dataset(
        dataset_id: str, 
        indicators: Optional[List[str]] = None, 
        time_periods: Optional[List[str]] = None, 
        geographies: Optional[Any] = None, 
        filter_items: Optional[Union[List[str], Dict[str, List[str]]]] = None, 
        json_query: Optional[Union[str, dict]] = None, 
        dataset_version: Optional[str] = None, 
        preview_token: Optional[str] = None, 
        ees_environment: Optional[str] = None, 
        api_version: Optional[str] = None, 
        page_size: int = 10000, 
        parse: bool =True, 
        page: Optional[int] = None, 
        debug: bool = False, 
        verbose: bool = False
        
)-> Optional[pd.DataFrame]:
    

    if indicators is None and json_query is None:
        raise ValueError("At least one of either inidcators or json_query must not be None.")
    
    geographies = todf_geographies(geographies)
    
    if json_query is not None:

        if any(x is not None for x in [indicators, time_periods, geographies, filter_items]):
            warnings.warn(
                "json_query is set - ignoring indicators, time_periods, geographies "
                "and filter_items_params."
            )
        
        if isinstance(json_query, str) and json_query.endswith(".json"):
            with open(json_query, "r") as f:
                json_body = f.read()
        
        elif isinstance(json_query, dict):
            json_body = json.dumps(json_query)
        
        else:
            if verbose:
                print("Parsing query options")
            
            json_body = json_query
    
    else:
        json_body = parse_tojson_params(
            indicators=indicators, 
            time_periods=time_periods, 
            geographies=geographies,
            filter_items=filter_items,
            page=page, 
            page_size=page_size,
            debug=debug,
            verbose=verbose

        )
    
    if verbose:
        print(json_body)
    

    url = api_url(
        "get-data", 
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        ees_environment=ees_environment,
        api_version=api_version,
        verbose=verbose

    )

    headers = {"Content-Type": "application/json"}
    if preview_token:
        headers["Preview-Token"] = preview_token

    
    if isinstance(json_body, str):
        try:
            body_dict = json.loads(json_body)
        except json.JSONDecodeError:
            body_dict = {}
        
    else:
        body_dict = json_body
    
    response = requests.post(url, json=body_dict, headers=headers)

    if verbose:
        print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        raise Exception(
            f"\nHTTP connection error: {response.status_code}\n{response.text}"
        )
    
    response_json = response.json()

    if verbose:
        total_pages = response_json("paging", {}).get("totalPages", 1)
        print(f"Total number of pages: {total_pages}")
    
    warning_max_pages(response_json)


    df_results = response_json.get("results", [])

    if page is None and json_query is None:
        paging = response_json.get("paging", {})
        total_pages = paging.get("totalPages", 1)

        if total_pages > 1:
            total_rows = total_pages * page_size
            if total_pages > 1:
                total_rows = total_pages * page_size
                if total_rows > 100000:
                    print(
                        f"Downloading up to {total_rows} rows. This may take a while."
                        "We recommend downloading the full data set using preview_dataset() "
                        "for large volume of data."
                    )

                for p in range(2, total_pages +1):
                    page_body = parse_tojson_params(
                        indicators=indicators, 
                        time_periods=time_periods, 
                        geographies=geographies, 
                        filter_items=filter_items,
                        page=p,
                        page_size=page_size,
                        verbose=verbose
                    )

                    try:
                        page_body_dict = json.loads(page_body)
                    except json.JSONDecodeError:
                        page_body_dict = {}
                    

                    page_response = requests.post(url, json=page_body_dict, headers=headers)

                    if page_response.status_code != 200:
                        raise Exception(
                            f"\nHTTP connection error on page {p}: {page_response.status_code}"

                        )
                    
                    page_json = page_response.json()
                    warning_max_pages(page_json)
                    df_results.extend(page_json.get("result", []))
    
    if parse and df_results:
        return parse_api_dataset(
            df_results, 
            dataset_id=dataset_id,
            dataset_version=dataset_version,
            preview_token=preview_token,
            ees_environment=ees_environment,
            verbose=verbose
        )
    
    return pd.DataFrame(df_results) if df_results else None
