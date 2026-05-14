from typing import Optional, List
from validation_rules import validate_ees_filter_type
from utils import convert_api_filter_type


def parse_tourl_filter_in(
        items: Optional[List[str]],
        filter_type:str
)-> Optional[str]:
    


    validate_ees_filter_type(filter_type)

    type_string = convert_api_filter_type(filter_type)

    if items is None:
        return None
    
    if isinstance(items, str):
        items = [items]
    
    if filter_type in ("time_periods", "locations"):
        items = [item.replace("|","%7C") for item in items]
    
    return type_string + ".in=" + "%2C".join(items) + "&"