"""
post_dataset_utils.py
 
Utility functions for building JSON query bodies for POST requests
to the Explore Education Statistics (EES) API.
 
These functions convert Python parameters (time periods, geographies,
filters, indicators) into JSON string fragments that are combined into
a complete POST request body by parse_tojson_params().
"""
import json 
import re 
from typing import Any, Dict, List, Optional, Union 

import pandas as pd

from validation_rules import validate_ees_id, validate_ees_filter_type, validate_time_periods
from utils import convert_api_filter_type
from query_dataset_utils import todf_geographies


def parse_tojson_time_periods(
        time_periods: Optional[List[str]]
)-> Optional[str]:
        """
    Convert time periods list into a JSON criteria fragment.
 
    Splits "period|code" strings into separate period and code fields
    as required by the EES API JSON query format.
 
    Parameters
    ----------
    time_periods : list of str or None
        Time periods in "period|code" format. Returns None if None.
 
    Returns
    -------
    str or None
        JSON fragment for time periods criteria, or None if not provided.
 
    Examples
    --------
    >>> parse_tojson_time_periods(["2024|AY"])
    '{ "timePeriods": { "in": [{"period": "2024", "code": "AY"}] } }'
    """
    
    
    # Return None if no time periods — caller skips this criteria block
    if time_periods is None:
        return None
    # Validate format — raises ValueError if any period is not "period|code"
    validate_time_periods(time_periods)

   # Convert each "period|code" string into {"period": ..., "code": ...} dict
    rows = []
    for tp in time_periods:
        parts = tp.split("|")   # Split on pipe e.g. "2024|AY" → ["2024", "AY"]
        rows.append({"period": parts[0], "code": parts[1]})
            
    # Build JSON string for each time period dict
    items = ",\n".join(
        '           {\n                   "priod": "' + r["period"] +
        '",\n             "code": "' + r["code"] + '"\n                  }'
        for r in rows 
    )
# Wrap items in the timePeriods.in criteria structure
    return(
        ' {\n         "timePeriods": {\n           "in": [\n'
        + items                                              
        +'\n           ]\n       }\n       ]'
    )

def parse_tojson_filter_in(
    items: Optional[Union[List[str], str]],  # Filter sqids to match
    filter_type: str = "filter_items"        # One of the valid filter types

) -> Optional[str]:
        """
    Build a JSON "in" filter fragment for a list of filter values.
 
    Creates an "in" criteria that matches rows where the filter value
    is any of the provided sqids.
 
    Parameters
    ----------
    items : list of str, str or None
        Filter sqids to match. Returns None if None.
    filter_type : str
        Filter type. One of: "time_periods", "geographic_levels",
        "locations", "filter_items". Default "filter_items".
 
    Returns
    -------
    str or None
        JSON fragment for an "in" filter, or None if items is None.
    """
    
   # Validate filter type — raises ValueError if invalid
    validate_ees_filter_type(filter_type)

   # Return None if no items — caller skips this criteria block
    if items is None:
        return None
            
    # Wrap single string in list for consistent processing
    if isinstance(items, str):
        items = [items]

    
   # Convert Python filter type to API field name e.g. "filter_items" → "filters"
    api_filter_type = convert_api_filter_type(filter_type)
   # Join multiple sqids with comma separator in JSON format
    items_str = '",\n           "'.join(items)
   # Build and return the "in" filter JSON fragment
    return (
        '     {\n      "' + api_filter_type +
        '": {\n          "in": [\n          "' +
        items_str +
        '"\n         ]\n        }\n   }'

    )

def parse_tojson_filter_eq(
        items: Optional[Union[List[str], str]],   # Filter sqids for exact match
        filter_type: str = "filter_items"         # One of the valid filter types
) -> Optional[str]:

        """
    Build a JSON "eq" (equals) filter fragment for exact matching.
 
    Creates one "eq" criteria per item — used for exact value matching
    rather than "in" list matching.
 
    Parameters
    ----------
    items : list of str, str or None
        Filter sqids for exact matching. Returns None if None.
    filter_type : str
        Filter type. Default "filter_items".
 
    Returns
    -------
    str or None
        JSON fragment with one "eq" filter per item, or None if items is None.
    """
    
  # Validate filter type — raises ValueError if invalid
    validate_ees_filter_type(filter_type)

    # Return None if no items
    if items is None:
        return None
    # Wrap single string in list for consistent processing
    if isinstance(items, str):
        items = [items]
    
   # Convert Python filter type to API field name
    api_filter_type = convert_api_filter_type(filter_type)

   # Build one "eq" filter JSON block per item and join with newlines
    return "\n".join(
        '        {\n             "' + api_filter_type +
        '": {\n                 "eq": "' + item +
        '"\n         }\n              }'

        for item in items

    )

def parse_tojson_filter(
        items: Optional[Union[List[str], Dict[str, List]]],  # Filter sqids or dict
        filter_type: str = "filter_items"                     # One of the valid filter types

) -> Optional[str]:
    """
    Build a JSON filter fragment handling both list and dict formats.
 
    - List input: creates a single "in" filter matching any sqid
    - Dict input: creates an "and" combination of "in" filters,
      one per dict key (column), for cross-column filtering
 
    Parameters
    ----------
    items : list, dict or None
        Filter sqids as list (OR query) or dict (AND combination).
    filter_type : str
        Filter type. Default "filter_items".
 
    Returns
    -------
    str or None
        JSON filter fragment, or None if items is None.
 
    Examples
    --------
    >>> # List — rows matching any of these sqids
    >>> parse_tojson_filter(["abc", "def"], "filter_items")
 
    >>> # Dict — rows matching BOTH filters (AND combination)
    >>> parse_tojson_filter({"col1": ["abc"], "col2": ["def"]}, "filter_items")
    """

   # Validate filter type — raises ValueError if invalid
    validate_ees_filter_type(filter_type)
   # Return None if no filters provided
    if items is None:
        return None
    
    if isinstance(items, dict):
        
        # Dict format — build separate "in" filter for each column
        # then combine with "and" so all conditions must be met
        parts = [parse_tojson_filter_in(v, filter_type) for v in items.values()]
        parts = [p for p in parts if p is not None]
        return '{\n"and": [\n' + ",\n".join(parts) + "\n]\n}"
    
    elif isinstance(items, list):
        # List format — single "in" filter matching any sqid
        return parse_tojson_filter_in(items, filter_type)

    return None

def parse_tojson_location(
        geographies: pd.DataFrame, 
        include_comma: bool = False
) -> List[str]:
        """
    Build JSON location filter fragments from a geographies DataFrame.
 
    Converts each row of a geographies DataFrame into a JSON location
    criteria fragment for use in POST query bodies.
 
    Parameters
    ----------
    geographies : pd.DataFrame
        DataFrame with columns: location_level, location_id_type, location_id.
    include_comma : bool
        If True, prepends " , " to each fragment. Default False.
 
    Returns
    -------
    list of str
        JSON location fragments, one per row. Empty string if no location_id_type.
    """
    

    # Add comma prefix if this is not the first criteria in an "and" block
    comma_str = " , " if include_comma else ""
    results = []

   # Build a JSON location fragment for each row in the DataFrame
    for _, row in geographies.iterrows():
        if row.get("location_id_type", "") != "":
            # Row has a specific location — build location "in" filter
            loc_json = (
                comma_str +
                '\n     {\n       "locations":  {\n      "in": [\n'
                '            {\n            "level": "' + str(row["location_level"]) +
                '",\n             "' + str(row["location_id_type"]) + 
                '":  "' + str(row["location_id"]) +
                '"\n           }\n         ]\n      }\n    }'
            )

        else:
            # No location_id_type — skip location filter for this row
            loc_json = ""
        
        results.append(loc_json)
    
    return results


def parse_tojson_geographies(
    geographies: Optional[Any]   # Geographies in any accepted format
)-> Optional[str]:
     """
    Build a JSON geography criteria fragment from geography input.
 
    Converts geography input (str, list, dict or DataFrame) into an
    "or" combination of geographic level + location filters.
 
    Parameters
    ----------
    geographies : str, list, dict, pd.DataFrame or None
        Geographic levels and/or locations to filter by.
        Returns None if None.
 
    Returns
    -------
    str or None
        JSON fragment for geography criteria, or None if not provided.
    """

   # Return None if no geographies provided
    if geographies is None:
        return None
    # Standardise input to a DataFrame using todf_geographies()
    geo_df = todf_geographies(geographies)

    rows = [] 

    # Build one "and" block per geography row combining level + location
    for _, row in geo_df.iterrows():
        # Build "eq" filter for the geographic level e.g. {"geographicLevels": {"eq": "NAT"}}
        eq_part = parse_tojson_filter_eq(
            [row["geographic_level"]],
            filter_type="geographic_levels"
        )

        # Build location filter for this row
        loc_parts = "".join(loc_parts)
        # Combine level and location with "and" so both must match
        rows.append(
            '         {\n          "and": [\n'
            +(eq_part or "")
            + loc_str
            + '\n ]\n }'
        )
    # Wrap all geography rows in an "or" block — any geography can match
    return (
        ' {\n     "or": [\n'
        + ",\n".join(rows)
        + '\n   ]\n    }'
    )

def parse_tojson_indicators(
        indicators: Union[str, List[str]]   # Indicator sqids to return
) -> str:
         """
    Build a JSON indicators fragment from indicator sqids.
 
    Parameters
    ----------
    indicators : str or list of str
        Indicator sqids to include in the query results.
 
    Returns
    -------
    str
        JSON fragment for the indicators section of a query body.
 
    Raises
    ------
    ValueError
        If indicators is None or invalid.
    """
    # Validate that indicators are provided and valid
    validate_ees_id(indicators, level="indicator")
    # Wrap single string in list for consistent processing
    if isinstance(indicators, str):
        indicators = [indicators]
    
    # Join multiple sqids with comma separator in JSON format
    items_str = '",\n  "'.join(indicators)
     # Return the indicators JSON fragment
    return '\n"indicators": [\n  "' + items_str + '"\n]'


def parse_tojson_params(
    indicators: Union[str, List[str]],                                          # Required — indicator sqids
    time_periods: Optional[List[str]] = None,                                   # Optional time period filters
    geographies: Optional[Any] = None,                                          # Optional geography filters
    filter_items: Optional[Union[List[str], Dict[str, List[str]]]] = None,      # Optional filter items
    page: Optional[int] =1,                                                     # Page number default 1
    page_size: int = 1000,                                                      # Results per page default 1000
    debug: bool = False,                                                        # Enable API debug mode                                                      
    verbose: bool = False                                                        # Print query if True
) -> str: 
    """
    Build a complete JSON query body string for POST requests to the EES API.
 
    Combines all criteria (time periods, geographies, filters) and indicators
    into a single JSON string ready to POST to the /query endpoint.
 
    Parameters
    ----------
    indicators : str or list of str
        Indicator sqids to return. Required.
    time_periods : list of str, optional
        Time periods in "period|code" format.
    geographies : str, list, dict or pd.DataFrame, optional
        Geographic levels and/or locations.
    filter_items : list or dict, optional
        Filter item sqids.
    page : int
        Page number. Default 1.
    page_size : int
        Results per page. Default 1000.
    debug : bool
        Enable API debug mode. Default False.
    verbose : bool
        Print the JSON query body to console. Default False.
 
    Returns
    -------
    str
        Complete JSON query body string for POST request.
    """
        
   # JSON bridge that closes criteria array and object
    bridge = "\n  ]\n},"
    # Debug flag as JSON boolean string
    debug_str = f',\n"debug": {str(debug).lower()}'
   # Page number defaults to 1 if None provided
    page_num = page if page is not None else 1
    # Pagination JSON closing fragment
    pages_str = f',\n"page": {page_num}, \n"pageSize": {page_size}\n}}'
        
    # Check if any criteria filters were provided
    has_criteria = any(X is not None for X in [time_periods, geographies, filter_items])

    if has_criteria:
        # Build each criteria fragment — None values are filtered out
        criteria_parts = [
            parse_tojson_time_periods(time_periods),                             # Time period filter
            parse_tojson_geographies(geographies),                                # Geography filter                       
            parse_tojson_filter(filter_items, filter_type="filter_items"),        # Filter items
        ]
            
        # Remove any None entries from criteria parts
        criteria_parts = [p for p in criteria_parts if p is not None]
        # Wrap all criteria in an "and" block — all conditions must be met
        criteria_str = (
            '"criteria": {\n  "and": [\n'
            + ",\n".join(criteria_parts)
            + bridge
        )
    
    else:
         # No criteria provided — omit criteria section entirely
        criteria_str = ""
    # Assemble complete JSON query body
    json_query = (
        "{\n"
        + criteria_str                             # Criteria block (if any)
        + parse_tojson_indicators(indicators)      # Indicators section (required)
        + debug_str                                # Debug flag
        + pages_str                                # Pagination
    )

    # Print query to console if verbose mode is on
    if verbose:
        print(json_query)

    return json_query
        
