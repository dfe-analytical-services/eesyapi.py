"""
parse_api_dataset.py
 
Parse raw API dataset results into a human-readable pandas DataFrame.
 
Takes the raw JSON results from the EES API and converts all sqid codes
(filters, indicators, locations) into human-readable labels using metadata
from get_meta(). This is the main parsing function called after a query.
"""
import warnings
import pandas as pd 
from typing import Any, Dict, List, Optional


from validation_rules import validate_ees_id
from get_meta import get_meta
from parse_sqids import (
    parse_time_codes,                  # Converts time period codes to readable labels
    parse_geographic_level_codes,      # Converts "NAT" → "National" etc
    parse_sqids_locations,              # Converts location sqids to names/codes
    parse_sqids_filters,                # Converts filter sqids to item labels
    parse_sqids_indicators,             # Renames indicator sqid columns to col_names
)


def parse_api_dataset(
    api_data_result: Any,                             # Raw API response — dict or list of result rows
    dataset_id: Optional[str] = None,                  # Dataset ID — used to fetch metadata
    dataset_version: Optional[str] = None,            # Optional dataset version
    preview_token: Optional[str] = None,              # Optional token for unpublished datasets
    ees_environment: Optional[str] = None,             # One of: "dev", "test", "preprod", "prod"
    api_version: Optional[str] = None,                # API version — defaults to "1"
    verbose: bool = False                             # Print debug info if True
)-> Optional[pd.DataFrame]:

     """
    Parse raw EES API dataset results into a human-readable DataFrame.
 
    Converts a raw API response containing sqid codes into a DataFrame
    where all codes have been replaced with human-readable labels using
    the dataset's metadata. Handles five data sections per row:
    - timePeriod:       → time_period and time_identifier columns
    - geographicLevel:  → geographic_level column
    - locations:        → location name and code columns
    - filters:          → filter item label columns
    - values:           → indicator value columns
 
    Parameters
    ----------
    api_data_result : dict or list
        Raw JSON from the EES API. Can be:
        - A dict with a "results" key (full API response)
        - A list of result row dicts
    dataset_id : str, optional
        Dataset ID for fetching metadata to decode sqids.
    dataset_version : str, optional
        Dataset version e.g. "2.1.0".
    preview_token : str, optional
        Preview token for unpublished datasets.
    ees_environment : str, optional
        One of "dev", "test", "preprod", "prod".
    api_version : str, optional
        EES API version. Default "1".
    verbose : bool
        Print debug info including response keys. Default False.
 
    Returns
    -------
    pd.DataFrame or None
        Parsed DataFrame with human-readable columns and values,
        or None if no rows were returned by the query.
    """
    
    # Validate dataset_id format if provided
    if dataset_id is not None:
        validate_ees_id(dataset_id, level="dataset")
    # Unwrap results from full API response dict if needed
    # Full response has structure: {"results": [...], "paging": {...}}
    if isinstance(api_data_result, dict) and "results" in api_data_result:
        api_data_result = api_data_result["results"]
        
    # Handle empty results — warn user and return None
    if api_data_result is None or len(api_data_result) == 0:
        if not verbose:
            warnings.warn(
                "No rows were returned for your query."
                "Set verbose=True to see detailed API response."
            )
        else:
            warnings.warn("No rows were returned for your query.")
        
        return None
    # Print structure of first result row to help with debugging
    if verbose:
        if isinstance(api_data_result, list) and len(api_data_result) > 0:
            print("Keys in result:", list(api_data_result[0].keys()))
            if "locations" in api_data_result[0]:
                print("Location keys:", list(api_data_result[0]["locations"].keys()))
            if "filters" in api_data_result[0]:
                print("Filter keys:", list(api_data_result[0]["filters"].keys()))
                
     # Fetch metadata for this dataset — needed to decode all sqid codes
    # This makes one API call to /meta before parsing begins
    meta = get_meta(
        dataset_id, 
        dataset_version=dataset_version, 
        preview_token=preview_token, 
        ees_environment = ees_environment, 
        api_version=api_version, 
        verbose=verbose
    )
    # Ensure results is a list — wrap single dict in list if needed
    results = api_data_result if isinstance(api_data_result, list) else [api_data_result]

    # Extract each section from result rows into separate DataFrames
    # Each row has: timePeriod, geographicLevel, locations, filters, values

    # Extract time period dicts e.g. {"period": "2024", "code": "AY"}
    time_periods_df = pd.DataFrame([r.get("timePeriod", {}) for r in results])
   # Extract geographic level codes e.g. "NAT", "REG"
    geo_levels = pd.Series([r.get("geographicLevel", None) for r in results])

    # Extract location sqid dicts e.g. {"NAT": "dP0Zw", "LA": "BT7J3"}
    locations_list = [r.get("locations", {}) for r in results]
    locations_df = pd.DataFrame(locations_list)

    # Extract filter sqid dicts e.g. {"f1sqid": "item_sqid"}
    filters_list = [r.get("filters", {}) for r in results]
    filters_df = pd.DataFrame(filters_list)

    # Extract indicator value dicts e.g. {"X9fKb": "42.5"}
    values_list = [r.get("values", {}) for r in results]
    values_df = pd.DataFrame(values_list)

     # Parse each section — replace sqids with human-readable labels

   # Convert time period codes to readable labels e.g. "AY" → "Academic year"
    parsed_time = parse_time_codes(time_periods_df, verbose=verbose)
    # Convert geographic level codes e.g. "NAT" → "National"
    parsed_geo = parse_geographic_level_codes(geo_levels, verbose=verbose)
   # Convert location sqids to names and codes using metadata
    parsed_locations = parse_sqids_locations(locations_df, meta, verbose=verbose)
   # Convert filter sqids to human-readable item labels using metadata
    parsed_filters = parse_sqids_filters(filters_df, meta, verbose=verbose)
     # Rename indicator sqid columns to human-readable col_names using metadata
    parsed_indicators = parse_sqids_indicators(values_df, meta, verbose=verbose)

    # Combine all parsed sections into a single DataFrame
    # axis=1 joins columns side by side (not stacking rows)
    result_df = pd.concat(
        [parsed_time, parsed_geo, parsed_locations, parsed_filters, parsed_indicators],
        axis=1
    )

    return result_df
                                               
