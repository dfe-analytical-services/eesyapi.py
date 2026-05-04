import requests
from typing import Any, Dict, List, Union 
from api_url import api_url
import pandas as pd 

EXAMPLE_ID_LIST = {
    "attendance": {
        "dev": {
            "publication": "b6d9ed96-be68-4791-abc3-08dcaba68c04",
            "dataset": "7c0e9201-c7c0-ff73-bee4-304e731ec0e6",
            "time_period":"2024|W23",
            "time_periods":["2024|W21", "2024|W23"],
            "location_id": "NAT|id|dP0Zw",
            "location_ids":["NAT|id|dP0Zw", "REG|id|rg3Nj"],
            "location_code":"NAT|code|E92000001",
            "location_codes":["REG|code|E12000001", "REG|code|E12000002"],
            "filter":"4kdUZ",
            "filter_item":"5UNdi",
            "filter_items_long": {
                "attendance_status": ["pmRSo", "7SdXo"],
                "attendance_type": ["CvuId","6AXrf"],
                "education_phase":["ThDPJ","crH31"],
                "day_number": ["uLQo4"],
                "reason": ["bBrtT"]
            },

            "filter_items_short": {
                "attendance_status": ["pmRSo"],
                "attendance_type": ["CvuId", "6AXrf"],
                "education_phase": ["ThDPJ", "crH31"],
                "day_number": ["uLQo4"],
                "reason": ["bBrtT"]
            },

            "indicator": "bqZtT"
            
        },

        "test": {
            "publication" : "25d0e40b-643a-4f73-3ae5-08dcf1c4d57f",
            "dataset" : "57b69201-033a-2c77-a19f-abcce2b11341",
            "time_period" : "2024|W23",
            "time_periods" : ["2024|W24", "2024|W25"],
            "location_id" : "NAT|id|mRj9K",
            "location_ids" : ["LA|id|arLPb", "REG|id|zecFQ"],
            "location_code" : "NAT|code|E92000001",
            "location_codes" : ["REG|code|E12000001", "REG|code|E12000002"],
            "filter" : "5Zdi9",
            "filter_item" : "rQkNj",
            "filter_items_long" : {
                 "attendance_status" : ["BfP7J", "zvUFQ"],
                 "attendance_type" : ["TuxPJ", "tj0Em", "5Tsdi", "fzaYF"],
                 "education_phase" : ["Poqeb", "dPE0Z"],
                 "day_number" : ["AOhGK"],
                 "reason" : ["9Ru4v"]
            },
            "filter_items_short": {
                 "attendance_status": ["qGJjG"],
                 "attendance_type": ["cZO31", "jgoAM"],
                 "education_phase": ["Poqeb", "dPE0Z"],
                 "day_number": ["AOhGK"],
                 "reason": ["9Ru4v"]
            },
            "indicator" : "tj0Em",
            "indicators" : ["tj0Em", "fzaYF"]
       },
        "prod": {
        "publication" : "9676af6b-d563-41f4-d071-08da8f468680",
        "dataset" : "63629501-d3ca-c471-9780-ec4cb6fdf172",
        "time_period" : "2025|W3",
        "time_periods": ["2025|W3", "2025|W4"],
        "location_id" : "LA|id|it6Xr",
        "location_ids": ["LA|id|it6X", "REG|id|ACyGK"],
        "location_code" : "NAT|code|E92000001",
        "location_codes" : ["REG|code|E12000001","REG|code|E12000002"],
        "filter" : "z4FQE",
        "filter_item" : "y2daB",
        "filter_items_long": {
            "attendance_status": ["e4wuS","TmQP"],
            "attendance_type": ["P9Aeb","VPw5X","uUIo4","ls5cB"],
            "education_phase": ["rbyNj","GBMgr"],
            "time_frame":["RL5ka"],
            "reason": ["S0OVx"]
        },
        
        "filter_items_short" : {
            "attendance_type": ["P9Aeb","VPw5X"],
            "education_phase" : ["rbyNj","GBMgr"],
            "time_frame" : ["5ezdi"]
        

        },
        "indicator" : "X9fKb",
        "indicators" : ["X9fKb","cg31S"]
    }
},

"absence": {
    "dev": {
        "publication": "d823e4df-626f-4450-9b21-08dc8b95fc02",
        "dataset": "830f9201-9e11-ad75-8dcd-d2efe2834457",
        "location_id": "LA|id|ml79K",
        "location_code": "NAT|code|E92000001",
        "location_codes": ["REG|code|E12000001","REG|code|E12000002"],
        "filter": "01tT5",
        "filter_item": "wEZcb",
        "indicator": "PbNeb",
     },

     "test" : {
        "publication" : "25d0e40b-643a-4f73-3ae5-08dcf1c4d57f",
        "dataset" : "e1ae9201-2fff-d376-8fa3-bd3c3660d4c8",
        "location_id": "NAT|id|mRj9K",
        "location_code" : "NAT|code|E92000001",
        "filter" : "arLPb",
        "filter_item" : "VN5XE",
        "filter_items" : ["VN5XE","PEebW"],
        "indicator": "dPe0Z",
        "indicators" : ["OBXCL","7YFXo"]

    },

    "prod" : {
        "publication" : "9676af6b-d563-41f4-d071-08da8f468680",
        "dataset" : "55629501-e98b-0c75-adba-f95a0cfbb5e9",
        "location_id" : "LA|id|it6Xr",
        "location_code" : "NAT|code|E92000001",
        "filter": "BT7J3",
        "filter_item": "oUXmX",
        "indicator": "uxo41",
        "indicators": ["uxo4"]

    }
     
  }
}

def parse_tojson_params(
        indicators=None,
        time_periods=None,
        geographies=None,
        filter_items=None
) -> Dict:
    
    return {
        "indicators":[indicators] if isinstance(indicators, str) else indicators,
        "timePeriods":[time_periods] if isinstance(time_periods, str) else time_periods,
        "geographies": geographies,
        "filters" : filter_items
    }

def todf_geographies(location_codes: List[str]):

    result = []

    for code in location_codes:
        parts = code.split("|")
        result.append({"geographicLevel": parts[0], "locationId": parts[-1]})

    return result



def example_id(
        level: Union[str, List[str]] = "dataset",
        ees_environment: str = "prod",
        group: str = "absence"
) -> Any:
    
    """
    Return example IDs for testing 
    """

    if group not in EXAMPLE_ID_LIST:
        raise ValueError(f"chosen group '{group}' not found in example list.")
    
    if ees_environment not in ["dev","test","prod"]:
        raise ValueError(f"chosen ees_environmenr ({ees_environment}) should be one of: dev, test or prod.")
    
    group_examples = EXAMPLE_ID_LIST[group][ees_environment]

    
    if isinstance(level, list):
        if "all" in level:
            return group_examples
    else:
        if level == "all":
            return group_examples
        
    levels = level if isinstance(level, list) else [level]
    
    
    for l in level:
        if l not in group_examples:
            raise ValueError("Non-valid element level received.\n"
                             "should be one of:\n\"" + 
                             "\", \"".join(group_examples.keys()) + "\".")
        

    if len(levels) > 1:
        result = []

        for l in levels:
            val = group_examples[l]
            if isinstance(val, list):
                result.extend(val)
            else:
                result.append(val)

        return result

    return group_examples[levels[0]]       
        

def example_data_raw(group: str = "attendance", size: int = 32) :
    """
    Fetch raw example data from API 
    """

    dataset_id  = example_id("dataset", group=group)
    indicator = example_id("indicator", group=group)

    url = api_url(
        endpoint = "get-data",
        dataset_id = dataset_id,
        indicators = indicator,
        page = 1,
        page_size = size
    )

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code}")
    
    data =  response.json()
    return data.get("results",[])


def example_json_query(ees_environment: str = "prod"):
    """
    Create example JSON query body 
    """

    return parse_tojson_params(
            indicators = example_id("indicator", group="attendance", ees_environment=ees_environment),
            time_periods = example_id("time_period", group="attendance", ees_environment=ees_environment),
            geographies=todf_geographies(example_id("location_codes",group="attendance",ees_environment=ees_environment)),
            filters = example_id("filter_items_short", group="attendance",ees_environment=ees_environment)
    )

def example_geography_query(level: str = "nat_yorks"):
    """
    Return example geography query
    """

    example_geography_query = {
        "nat_yorks": pd.DataFrame
            ({
                "geographic_level": "NAT",
                "location_level": "NAT",
                "location_id_type": "code",
                "location_id": "E92000001"

            }),
           
        
        "nat_yorks_yorkslas": pd.DataFrame
            ({
                "geographic_level": "NAT",
                "location_level":"NAT",
                "location_id_type": "code",
                "location_id": "E92000001"
            })
            
        
    }

    if level not in example_geography_query:
        raise ValueError("Invalid level")
    
    return example_geography_query[level]

