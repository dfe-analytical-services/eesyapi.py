"""
utils.py 

Helper functions for EES API 

"""

#Valid Filter Types 

VALID_FILTER_TYPES = [
    "time_periods",
    "geographic_levels", 
    "locations",
    "filter_items"
]

# Validate Filter Type 

def validate_ees_filter_type(filter_type):
    if filter_type not in VALID_FILTER_TYPES:
        raise ValueError(
            f"Invalid filter_type: {filter_type}. Must be one of {VALID_FILTER_TYPES}"
        )
    

# Convert filter Type

def convert_api_filter_type(filter_type):
    mapping ={
        "time_periods": "timePeriods",
        "geographics_levels": "geographicLevels", 
        "locations": "locations", 
        "filter_items": "filters"
    }

    return mapping.get(filter_type)

#Main Function 

def parse_tourl_filter_in(items, filter_type):
    """
    Create <filter>.in query string for URL queries 
    """
    
    validate_ees_filter_type(filter_type)

    type_string = convert_api_filter_type(filter_type)

    if items is None:
        return ""
    
    if filter_type in ["time_periods", "locations"]:
        items = [item.replace("|", "%7C") for item in items]

    joined_tems = "%2C".join(items)

    return f"{type_string}.in={joined_tems}&"