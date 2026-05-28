import requests
import pandas as pd 
from typing import Optional, Dict, Any, List

from api_url import api_url 

def get_meta_response(
        dataset_id: str,
        dataset_version: Optional[str] = None, 
        preview_token: Optional[str] = None, 
        ees_environment: Optional[str] = None, 
        api_version: Optional[str] = None, 
        parse: bool = True, 
        verbose: bool = False
) -> Any:
        """
    Send a request to the EES API get-meta endpoint.

    This function fetches metadata for a specific dataset. The metadata
    usually includes time periods, locations, filters, and indicators.

    Args:
        dataset_id: Unique dataset ID.
        dataset_version: Optional dataset version.
        preview_token: Optional preview token for unpublished/private datasets.
        ees_environment: API environment, such as dev, test, or prod.
        api_version: API version to use.
        parse: If True, return JSON. If False, return the raw response object.
        verbose: If True, print extra API URL information from api_url.

    Returns:
        Any: Parsed JSON response or raw response object.

    Raises:
        ValueError: If parse is not a boolean.
        Exception: If API request fails.
    """
    # Ensure parse is only True or False.
    if not isinstance(parse, bool):
        raise ValueError("parse must be True or False")
    # Build the get-meta API URL.
    url = api_url(
        endpoint="get-meta",
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        ees_environment=ees_environment,
        api_version=api_version,
        verbose=verbose
    )

    # Create request headers.
    # Preview token is only added when provided.
    headers = {}
    if preview_token:
        headers["Preview-Token"] = preview_token
    # Send GET request to the API.
    response = requests.get(url, headers=headers)

    # Raise an error if the API response is not successful.
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code}")
            
     # Return parsed JSON or raw response based on parse value.
    return response.json() if parse else response

def parse_meta_time_periods(api_meta_time_periods):
         """
    Parse time period metadata into a pandas DataFrame.

    The function also sorts time periods by numeric code value where possible.

    Args:
        api_meta_time_periods: Time period metadata from the API.

    Returns:
        pd.DataFrame: Parsed and sorted time period metadata.
    """

   # Return an empty DataFrame if no time periods are available.
    if not api_meta_time_periods:
        return pd.DataFrame()
            
    # Convert time period metadata to a DataFrame.
    df = pd.DataFrame(api_meta_time_periods)

# If the DataFrame is empty or does not contain code column, return as it is.
    if df.empty or "code" not in df.columns:
        return df
    # Extract numeric part from the code column for sorting.
    # Example: "W23" becomes 23.
    df["code_num"] = pd.to_numeric(
        df["code"].str.replace(r"[a-zA-Z]", "", regex=True),
        errors="coerce"
    ).fillna(0)

     # Sort by numeric code and remove helper column.
    df = df.sort_values("code_num").drop(columns=["code_num"])

    return df

def parse_meta_location_ids(api_meta_locations):
        """
    Parse location metadata into a pandas DataFrame.

    This function supports both list-based and dictionary-based location
    metadata structures returned by the API.

    Args:
        api_meta_locations: Location metadata from the API.

    Returns:
        pd.DataFrame: Parsed location metadata.
    """
    # Return empty DataFrame if no location metadata is available.
    if not api_meta_locations:
        return pd.DataFrame

    all_rows = []

   # Case 1: API returns locations as a list.
    if isinstance(api_meta_locations, list):
        for item in api_meta_locations:
           # Skip invalid location items.
            if not isinstance(item, dict):
                continue
            level = item.get("level", {})
            options = item.get("options", [])
           # Skip if there are no location options.
            if not options:
                continue
           # Convert options into DataFrame.
            df = pd.DataFrame(options)
            # Add geographic level information.
            df["geographic_levels_code"] = level.get("code", "")
            df["geographic_level"] = level.get("label", "")
            # Rename id column to item_id for consistency.
            df = df.rename(columns={"id": "item_id"})
            all_rows.append(df)

    # Case 2: API returns locations as a dictionary.
    elif isinstance(api_meta_locations, dict):
        levels = api_meta_locations.get("level", [])
        options = api_meta_locations.get("options", [])
        if levels and options:
            for i in range(len(levels)):
                # Stop if there are more levels than options.
                if i >= len(options):
                    break 
                # Convert each location option group into DataFrame.
                df = pd.DataFrame(options[i])
                # Add geographic level information.
                df["geographic_levels_code"] = levels[i].get("code", "")
                df["geographic_level"] = levels[i].get("label", "")
                # Rename id column to item_id.
                df = df.rename(columns={"id": "item_id"})
                all_rows.append(df)
                    
    # Return empty DataFrame if no valid rows were created.
    if not all_rows:
        return pd.DataFrame()
    # Combine all location rows into one DataFrame.
    return pd.concat(all_rows, ignore_index=True)

def parse_meta_filter_columns(api_meta_filters):
         """
    Parse filter column metadata into a pandas DataFrame.

    Args:
        api_meta_filters: Filter metadata from the API.

    Returns:
        pd.DataFrame: DataFrame containing filter column IDs, names, and labels.
    """
   # Return an empty DataFrame with expected columns if no filters exist.
    if not api_meta_filters:
        return pd.DataFrame(columns=["col_id", "col_name", "label"])
   # Extract filter-level information.
    return pd.DataFrame({
        "col_id": [f["id"] for f in api_meta_filters], 
        "col_name": [f["column"] for f in api_meta_filters],
        "label": [f["label"] for f in api_meta_filters]
    })


def parse_meta_filter_item_ids(api_meta_filters):
        """
    Parse filter item metadata into a pandas DataFrame.

    This function extracts individual filter option IDs and labels for
    every filter column.

    Args:
        api_meta_filters: Filter metadata from the API.

    Returns:
        pd.DataFrame: DataFrame containing filter item IDs and labels.
    """
   # Return empty DataFrame if no filters are available.
    if not api_meta_filters:
        return pd.DataFrame()

    rows = []
    # Loop through each filter column.
    for f in api_meta_filters:
        col_id = f["id"]
        col_name = f["column"]
        label = f["label"]
            
       # Loop through each option under the filter column.
        for opt in f.get("options", []):
            rows.append({
                "col_id": col_id,
                "col_name": col_name,
                "label": label, 
                "item_id": opt.get("id"),
                "item_label": opt.get("label"), 
                "isAggregate": opt.get("isAggregate")

            })
    
    # Return empty DataFrame if no filter options are found.
    if not rows:
        return pd.DataFrame()
    # Convert filter item rows into DataFrame.
    df = pd.DataFrame(rows)
   # Ensure isAggregate column exists.
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
        """
    Fetch and parse metadata for a dataset.

    This is the main helper function. It calls get_meta_response() to fetch
    metadata from the API, then parses important sections into pandas
    DataFrames.

    Args:
        dataset_id: Unique dataset ID.
        dataset_version: Optional dataset version.
        preview_token: Optional preview token for unpublished/private datasets.
        ees_environment: API environment, such as dev, test, or prod.
        api_version: API version to use.
        verbose: If True, prints extra API request information.

    Returns:
        Dict[str, Any]: Dictionary containing parsed metadata:
            - time_periods
            - locations
            - filter_columns
            - filter_items
            - indicators
    """
    # Fetch metadata response from the API.  
     response = get_meta_response(
          dataset_id,
          dataset_version=dataset_version, 
          preview_token=preview_token, 
          ees_environment=ees_environment, 
          api_version=api_version,
          parse = True, 
          verbose = verbose

     )
    # Parse different metadata sections into structured DataFrames.
     meta_data = {
         "time_periods":    parse_meta_time_periods(response.get("timePeriods", [])),
         "locations":       parse_meta_location_ids(response.get("locations", [])),
         "filter_columns":  parse_meta_filter_columns(response.get("filters", [])), 
         "filter_items":    parse_meta_filter_item_ids(response.get("filters", [])),
        # Indicators follow a similar structure to filters,
        # so the same parser can be reused here.
         "indicators":      parse_meta_filter_columns(response.get("indicators",[]))
     }

     return meta_data




         
     
