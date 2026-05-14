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
    

    if time_periods is None:
        return None
    
    validate_time_periods(time_periods)

    rows = []
    for tp in time_periods:
        parts = tp.split("|")
        rows.append({"period": parts[0], "code": parts[1]})
    
    items = ",\n".join(
        '           {\n                   "priod": "' + r["period"] +
        '",\n             "code": "' + r["code"] + '"\n                  }'
        for r in rows 
    )

    return(
        ' {\n         "timePeriods": {\n           "in": [\n'
        + items                                              
        +'\n           ]\n       }\n       ]'
    )

def parse_tojson_filter_in(
    items: Optional[Union[List[str], str]],
    filter_type: str = "filter_items"

) -> Optional[str]:
    

    validate_ees_filter_type(filter_type)

    if items is None:
        return None
    
    if isinstance(items, str):
        items = [items]

    

    api_filter_type = convert_api_filter_type(filter_type)
    items_str = '",\n           "'.join(items)

    return (
        '     {\n      "' + api_filter_type +
        '": {\n          "in": [\n          "' +
        items_str +
        '"\n         ]\n        }\n   }'

    )

def parse_tojson_filter_eq(
        items: Optional[Union[List[str], str]],
        filter_type: str = "filter_items"
) -> Optional[str]:
    

    validate_ees_filter_type(filter_type)

    if items is None:
        return None
    
    if isinstance(items, str):
        items = [items]
    

    api_filter_type = convert_api_filter_type(filter_type)


    return "\n".join(
        '        {\n             "' + api_filter_type +
        '": {\n                 "eq": "' + item +
        '"\n         }\n              }'

        for item in items

    )

def parse_tojson_filter(
        items: Optional[Union[List[str], Dict[str, List]]],
        filter_type: str = "filter_items"

) -> Optional[str]:
    


    validate_ees_filter_type(filter_type)

    if items is None:
        return None
    
    if isinstance(items, dict):

        parts = [parse_tojson_filter_in(v, filter_type) for v in items.values()]
        parts = [p for p in parts if p is not None]
        return '{\n"and": [\n' + ",\n".join(parts) + "\n]\n}"
    
    elif isinstance(items, list):
        return parse_tojson_filter_in(items, filter_type)

    return None

def parse_tojson_location(
        geographies: pd.DataFrame, 
        include_comma: bool = False
) -> List[str]:
    


    comma_str = " , " if include_comma else ""
    results = []


    for _, row in geographies.iterrows():
        if row.get("location_id_type", "") != "":
            loc_json = (
                comma_str +
                '\n     {\n       "locations":  {\n      "in": [\n'
                '            {\n            "level": "' + str(row["location_level"]) +
                '",\n             "' + str(row["location_id_type"]) + 
                '":  "' + str(row["location_id"]) +
                '"\n           }\n         ]\n      }\n    }'
            )

        else:
            loc_json = ""
        
        results.append(loc_json)
    
    return results


def parse_tojson_geographies(
    geographies: Optional[Any]
)-> Optional[str]:
    


    if geographies is None:
        return None
    
    geo_df = todf_geographies(geographies)

    rows = []

    for _, row in geo_df.iterrows():
        eq_part = parse_tojson_filter_eq(
            [row["geographic_level"]],
            filter_type="geographic_levels"
        )

        loc_parts = "".join(loc_parts)
        rows.append(
            '         {\n          "and": [\n'
            +(eq_part or "")
            + loc_str
            + '\n ]\n }'
        )
    
    return (
        ' {\n     "or": [\n'
        + ",\n".join(rows)
        + '\n   ]\n    }'
    )

def parse_tojson_indicators(
        indicators: Union[str, List[str]]
) -> str:
    
    validate_ees_id(indicators, level="indicator")

    if isinstance(indicators, str):
        indicators = [indicators]
    

    items_str = '",\n  "'.join(indicators)
    return '\n"indicators": [\n  "' + items_str + '"\n]'


def parse_tojson_params(
    indicators: Union[str, List[str]], 
    time_periods: Optional[List[str]] = None, 
    geographies: Optional[Any] = None, 
    filter_items: Optional[Union[List[str], Dict[str, List[str]]]] = None,
    page: Optional[int] =1, 
    page_size: int = 1000, 
    debug: bool = False,
    verbose: bool = False
) -> str: 
    

    bridge = "\n  ]\n},"
    debug_str = f',\n"debug": {str(debug).lower()}'
    page_num = page if page is not None else 1
    pages_str = f',\n"page": {page_num}, \n"pageSize": {page_size}\n}}'

    has_criteria = any(X is not None for X in [time_periods, geographies, filter_items])

    if has_criteria:
        criteria_parts = [
            parse_tojson_time_periods(time_periods),
            parse_tojson_geographies(geographies),
            parse_tojson_filter(filter_items, filter_type="filter_items"),
        ]

        criteria_parts = [p for p in criteria_parts if p is not None]
        criteria_str = (
            '"criteria": {\n  "and": [\n'
            + ",\n".join(criteria_parts)
            + bridge
        )
    
    else:
        criteria_str = ""
    
    json_query = (
        "{\n"
        + criteria_str
        + parse_tojson_indicators(indicators)
        + debug_str
        + pages_str
    )


    if verbose:
        print(json_query)

    return json_query
        
