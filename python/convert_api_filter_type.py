"""
convert_api_filter_type.py

Converts user -supplied filter inputs into the standardised format 
excepted by the EES API query endpoint.

The API expects filters as a list of dicts:
[{"field": "absence_type", "values": ["abc123", "def456"]}]

This module handles conversion from the various formats a user might 
supply (dict, list, string values) into that standard format.

"""



from typing import Dict, List, Any, Union 

def convert_single_filter(field: str, value: Union[str, List[str]]) -> Dict[str, Any]:

    """
    Convert a single filter field and value into API-compatible format.

    Wraps a single string value in a list so all filters consistenly 
    use list format in the output.

    Parameters

    field : str
        The filter column name e.g.., "absence_type", "school_type"
    value : str or list of str
        The filter value(s). A single string is wrapped in a list.
    
    
    Returns

    dict 
        A dict with "filed" and "values" keys e.g.
        {"filed": "absence_type", "values": ["Authorised"]}
    
    Raises

    ValueError 
        If value is not a string or list.
    
    Examples

    >>> convert_single_filter("absence_type", "Authorised")
    {"field": "absence_type", "values":["Authorised"]}

    >>> convert_single_filter("school_type", ["Primary", "Secondary"])
    {"filed": "school_type", "values": ["Primary", "Secondary"]}

    """
    if isinstance(value, str):
        # Wrap single string in a list for consistent output format
        values = [value]
    
    elif isinstance(value, list):
        # List is already in the correct format - use as-is
        values = value

    else:
        # Reject any other types e.g., int, dict, None
        raise ValueError(f"Invalid filter value type for {field}")

    # Return in the standard API filter format 
    return{
        "field" : field,
        "values": values
         
     }


def convert_api_filter_type(
        filters: Union[
            Dict[str, Union[str, List[str]]],  # Dict format: {"filed": "value"}
            List[Dict[str, Any]],              # List format: [{"filed": ....., "values": [....]}]
            None                               # None means no filters - returns empty list 
        ]
) -> List[Dict[str, Any]]:
    
    """
    Convert user input filters into API-compatible format.

    Accepts filters in mutliple formats and normalises them to a 
    list of dicts with "filed" and "values" keys, as required by 
    the EES API POST query endpoint.

    Parameters

    filters : dict, list or None
     - None: no filters - returns empty list 
     -dict: {"absence_type": "Authorised", "school_type": ["Primary"]}
     -list: [{"filed": "absence_type", "values": ["Authorised"]}]
    
    Returns 

    list of dict 
        Filters in API format: [{"filed": "....", "values": [.....]}]
    
    Raises 

    ValueError
        If list items are missing "filed" or "values" keys.
        or if filters is not a dict, list or None

    Examples 
    >>> convert_api_filters_type(None)
    []

    >>> convert_api_filter_type({"absence_type": "Authorised"})
    [{"field": "absence_type", "values": ["Authorised"]}]

    >>> convert_api_filter_type([{"filed":"absence_type", "values": ["Authorised"]}])
    [{"filed":  "absence_type", "values": ["Authorised"]}]

    """


    # No filters provided - return empty list (no filtering period)
    if filters is None:
        return []
    
    if isinstance(filters, list):
        # Validate each item in the list has the required keys
        for f in filters:
            if "field" not in f or "values" not in f:
                raise ValueError("Invalid filter format in list input")
        # List is already in the correct format - return as-is
        return filters
    
    if isinstance(filters, dict):
        # Convert dict format to list format 
        # e.g. {"absence_type": "Authorised"} ->
        #      [{"filed": "absence_type", "values": ["Authorised"]}]
        converted = []


        for field, value in filters.items():
            # Use convert_single_filter to handle str/list values consistently
            converted.append(convert_single_filter(field, value))

        return converted 
    # Reject any other input types e.g. string, int, tuple
    raise ValueError("Filters must be dict,list or None")
