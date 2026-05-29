"""
api_url_query_utils.py

Utility functions for building URL query string fragments for 
GET requests to the Explore Education Statistics (EES) API.

These helpers convert Python filter parameters into URL- encoded
query string segments like "timePeriods.in=2024%7CAY%2C2023%7CAY&"
"""


from typing import Optional, List
from validation_rules import validate_ees_filter_type
from utils import convert_api_filter_type


def parse_tourl_filter_in(
        items: Optional[List[str]],   # Filters values  e.g. ["2024|AY", "NAT"]
        filter_type:str               # One of: "time_periods", "geographic_levels",
)-> Optional[str]:                    #    "locations", "filter_items"
    
    """
    Create a URL query string fragment for a filter "in" clause.

    Convert a list of filter values into a URL-encoded query string 
    segment for use in EES API GET requests.

    for example:
    -time_periods ["2024|AY"]  -> "timePeriods.in=2024%7CAY&"
    -geographic_levels ["NAT"]  -> "geographicLevels.in=NAT&"
    -filter_items ["abc", "def"]  -> "filters.in=abc%2Cdef&"

    URL encoding:
    - "|" -> "%7C" (pipe in time periods and locations)
    - "," ->  "%2C" (comma separator between values)

    Parameters

    items: list of str or None
        Filter values to include. Returns None if items is None.
    filter_type: str
        Type of filter, one of:
        "time_periods",  "geographic_levels", "locations", "filter_items"
    
    Returns

    str or None 
        URL query string fragement ending with "&", or None if items is None.

    Examples

    >>> parse_tour1_filter_in(["2024|W11", "2024|W12"], "time_periods")
    'timePeriods.in=2024%7CW11%2C2024%7CW12&'

    >>> parse_tourl_filter_in(["NAT", "REG"], "geographic_levels")
    'geograpgicLevels.in=NAT%2CREG&'

    >>> parse_tour1_filters_in(None, "time_periods")
    None
    """

    #Validate that filter_type is one of the accepted values
    # Raises ValueError if an invalid filter type is passed 
    validate_ees_filter_type(filter_type)

    # Convert Python filter type name to the API field name 
    # e.g.., "time_periods" -> "timePeriods", "filter_items" -> "filters"
    type_string = convert_api_filter_type(filter_type)

    # Return None if no items provided - caller skips adding this param to URL 
    if items is None:
        return None

    # Wrap single string in a list for consistent processing below
    if isinstance(items, str):
        items = [items]
    

    #URL- encoded pipe characters for time_periods and locations only
    # e.g.. "2024|AY" -> "2024%7CAY"
    # Pipe is a special character in URLs so must be encoded 
    # Geographic levels and filoter items don't use pipes so skip this step

    if filter_type in ("time_periods", "locations"):
        items = [item.replace("|","%7C") for item in items]
    
    # Build and return the complete query string fragment:
    # type_string = API field name e.g. "timePeriods"
    # ".in="   = filter operator
    #"%2C".join() = URL-encoded comma between values
    # "&"   = trailing separator ready to append more params
    
    return type_string + ".in=" + "%2C".join(items) + "&"
