import warnings
import pandas as pd 
from typing import Any, Dict, List, Optional


from validation_rules import validate_ees_id
from get_meta import get_meta
from parse_sqids import (
    parse_time_codes, 
    parse_geographic_level_codes,
    parse_sqids_locations,
    parse_sqids_filters,
    parse_sqids_indicators,
)


def parse_api_dataset(
    api_data_result: Any, 
    dataset_id: Optional[str] = None,
    dataset_version: Optional[str] = None, 
    preview_token: Optional[str] = None, 
    ees_environment: Optional[str] = None, 
    api_version: Optional[str] = None, 
    verbose: bool = False
)-> Optional[pd.DataFrame]:
    

    if dataset_id is not None:
        validate_ees_id(dataset_id, level="dataset")
    
    if isinstance(api_data_result, dict) and "results" in api_data_result:
        api_data_result = api_data_result["results"]
    
    if api_data_result is None or len(api_data_result) == 0:
        if not verbose:
            warnings.warn(
                "No rows were returned for your query."
                "Set verbose=True to see detailed API response."
            )
        else:
            warnings.warn("No rows were returned for your query.")
        
        return None
    
    if verbose:
        if isinstance(api_data_result, list) and len(api_data_result) > 0:
            print("Keys in result:", list(api_data_result[0].keys()))
            if "locations" in api_data_result[0]:
                print("Location keys:", list(api_data_result[0]["locations"].keys()))
            if "filters" in api_data_result[0]:
                print("Filter keys:", list(api_data_result[0]["filters"].keys()))
    
    meta = get_meta(
        dataset_id, 
        dataset_version=dataset_version, 
        preview_token=preview_token, 
        ees_environment = ees_environment, 
        api_version=api_version, 
        verbose=verbose
    )

    results = api_data_result if isinstance(api_data_result, list) else [api_data_result]

    time_periods_df = pd.DataFrame([r.get("timePeriod", {}) for r in results])
    geo_levels = pd.Series([r.get("geographicLevel", None) for r in results])

    locations_list = [r.get("locations", {}) for r in results]
    locations_df = pd.DataFrame(locations_list)

    filters_list = [r.get("filters", {}) for r in results]
    filters_df = pd.DataFrame(filters_list)

    values_list = [r.get("values", {}) for r in results]
    values_df = pd.DataFrame(values_list)


    parsed_time = parse_time_codes(time_periods_df, verbose=verbose)
    parsed_geo = parse_geographic_level_codes(geo_levels, verbose=verbose)
    parsed_locations = parse_sqids_locations(locations_df, meta, verbose=verbose)
    parsed_filters = parse_sqids_filters(filters_df, meta, verbose=verbose)
    parsed_indicators = parse_sqids_indicators(values_df, meta, verbose=verbose)


    result_df = pd.concat(
        [parsed_time, parsed_geo, parsed_locations, parsed_filters, parsed_indicators],
        axis=1
    )

    return result_df
                                               