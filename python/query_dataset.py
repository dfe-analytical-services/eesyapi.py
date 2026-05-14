import warnings
from typing import Any, Dict, List, Optional, Union

import pandas as pd 

from get_meta import get_meta
from query_dataset_utils import todf_geographies


def query_dataset(
        dataset_id: str, 
        indicators: Optional[List[str]] = None, 
        time_periods: Optional[List[str]] = None, 
        geographies: Optional[Any] = None, 
        filter_items: Optional[Union[List[str], Dict[str, List[str]]]] = None, 
        json_query: Optional[Union[str, dict]] = None, 
        method: str = "POST", 
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
    
    if method not in ("POST", "GET"):
        raise ValueError(
            "Invalid method selected. The keyword method should be set to GET or POST."
        )
    
    if indicators is None and json_query is None and parse:
        warnings.warn("No indicators provided, defaulted to using all indicators from meta data")
        try:
            from get_meta import get_meta
            meta = get_meta(
                dataset_id,
                dataset_version=dataset_version,
                preview_token=preview_token,
                ees_environment=ees_environment,
                api_version=api_version,
                verbose=verbose
            )
            indicator_meta = meta.get("indicators", pd.DataFrame())
            if isinstance(indicator_meta, pd.DataFrame) and not indicator_meta.empty:
                indicators = list(indicator_meta["col_id"].values)
            else:
                indicators = None
        
        except Exception as e:
            if verbose:
                print(f"Could not fetch indicators from meta: {e}")
            
            indicators = None


    if method == "POST":
        from post_dataset import post_dataset
        return post_dataset(
            dataset_id=dataset_id, 
            indicators=indicators, 
            time_periods=time_periods, 
            geographies=geographies, 
            filter_items=filter_items, 
            json_query=json_query, 
            dataset_version = dataset_version, 
            preview_token=preview_token, 
            ees_environment=ees_environment, 
            api_version=api_version, 
            page_size=page_size,
            page=page, 
            parse=parse, 
            debug=debug, 
            verbose=verbose
        )
    
    else:

        warnings.warn(
            "Using GET to query a data set offers limited functionality, we recommed "
            "using POST alongside a JSON structured query instead:\n"
            "  -query_dataset(...., method='POST')"
        )

        geo_df = todf_geographies(geographies)

        geographic_levels=None
        locations = None


        if geo_df is not None:
            non_empty_levels = geo_df[geo_df["geographic_level"] != ""]["geographic_level"]
            if not non_empty_levels.empty:
                geographic_levels = list(non_empty_levels.unique())
            

            geo_df = geo_df.copy()
            geo_df["locations"] = (
                geo_df["location_level"] + "|" +
                geo_df["location_id_type"] + "|" +
                geo_df["location_id"]
            )

            geo_df["locations"] = geo_df["locations"].str.replace(r"\|{2,}", "", regex=True)

            non_empty_locs = geo_df[geo_df["locations"] != ""]["locations"]
            if not non_empty_locs.empty:
                locations = non_empty_locs.unique().tolist()

        
        if verbose:
            print(f"geographic_levels: {', '.join(geographic_levels or [])}")
            print(f"locations: {', '.join(locations or [])}")
        


        from get_dataset import get_dataset
        return get_dataset(
            dataset_id=dataset_id, 
            indicators=indicators, 
            time_periods=time_periods, 
            geographic_levels=geographic_levels, 
            locations=locations,
            filter_items=filter_items, 
            dataset_version = dataset_version, 
            preview_token=preview_token, 
            ees_environment=ees_environment, 
            api_version=api_version, 
            page_size=page_size,
            page=page, 
            parse=parse,  
            verbose=verbose
        )