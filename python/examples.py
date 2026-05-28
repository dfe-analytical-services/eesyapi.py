import requests
from typing import Any, Dict, List, Union 
from api_url import api_url
import pandas as pd 


# Example IDs used for testing different EES API environments.

# The dictionary is organised by:
#   1. Data group: attendance / absence
#   2. Environment: dev / test / prod
#   3. Example values: publication ID, dataset ID, filters, indicators, etc.
#
# These IDs are useful when writing tests or examples without manually
# searching for valid publication, dataset, location, filter, and indicator IDs.

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
            
             # Long filter example containing multiple values per category.
            "filter_items_long": {
                "attendance_status": ["pmRSo", "7SdXo"],
                "attendance_type": ["CvuId","6AXrf"],
                "education_phase":["ThDPJ","crH31"],
                "day_number": ["uLQo4"],
                "reason": ["bBrtT"]
            },
            
            # Short filter example used for simpler test queries.
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
      """
    Convert input parameters into the JSON structure required by the EES API.

    This function is useful when creating a request body for endpoints that
    expect indicators, time periods, geographies, and filters.

    Args:
        indicators: A single indicator ID or a list of indicator IDs.
        time_periods: A single time period or a list of time periods.
        geographies: Geography query data.
        filter_items: Filter items to apply in the API query.

    Returns:
        Dict: JSON-compatible dictionary for the API request body.
    """
    return {
        # If a single indicator is passed as a string, convert it to a list.
        "indicators":[indicators] if isinstance(indicators, str) else indicators,
        # If a single time period is passed as a string, convert it to a list.
        "timePeriods":[time_periods] if isinstance(time_periods, str) else time_periods,
        "geographies": geographies,
        "filters" : filter_items
    }

def todf_geographies(location_codes: List[str]):
    """
    Convert location code strings into geography dictionaries.

    Example:
        "NAT|code|E92000001"

    becomes:
        {
            "geographicLevel": "NAT",
            "locationId": "E92000001"
        }

    Args:
        location_codes: List of location code strings.

    Returns:
        list: List of geography dictionaries.
    """

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
    Return example IDs for a selected group and environment.

    Args:
        level: Single key, list of keys, or "all".
               Example: "dataset", "indicator", ["dataset", "indicator"], "all".
        ees_environment: EES API environment. Must be "dev", "test", or "prod".
        group: Data group. Must exist in EXAMPLE_ID_LIST.

    Returns:
        Any: Requested example value, list of values, or full example dictionary.

    Raises:
        ValueError: If group, environment, or level is invalid.
    """
    # Check if the requested group exists.
    if group not in EXAMPLE_ID_LIST:
        raise ValueError(f"chosen group '{group}' not found in example list.")
    # Validate the requested environment.
    if ees_environment not in ["dev","test","prod"]:
        raise ValueError(f"chosen ees_environmenr ({ees_environment}) should be one of: dev, test or prod.")
    # Get examples for the selected group and environment.
    group_examples = EXAMPLE_ID_LIST[group][ees_environment]

    # Return all values if "all" is requested.
    if isinstance(level, list):
        if "all" in level:
            return group_examples
    else:
        if level == "all":
            return group_examples
     # Convert level into a list so the logic below works for both string and list input.  
    levels = level if isinstance(level, list) else [level]
    
    # Validate each requested level.
    for l in level:
        if l not in group_examples:
            raise ValueError("Non-valid element level received.\n"
                             "should be one of:\n\"" + 
                             "\", \"".join(group_examples.keys()) + "\".")
        
    # If multiple levels are requested, return a combined list of values.
    if len(levels) > 1:
        result = []

        for l in levels:
            val = group_examples[l]
            # If the value is already a list, extend the result.
            if isinstance(val, list):
                result.extend(val)
            else:
                result.append(val)

        return result
    # If only one level is requested, return that value directly.
    return group_examples[levels[0]]       
        

def example_data_raw(group: str = "attendance", size: int = 32) :
  
   """
    Fetch raw example data from the EES API.

    This function builds a get-data API URL using a sample dataset and
    indicator, sends a GET request, and returns the results.

    Args:
        group: Data group to use. Default is "attendance".
        size: Number of records to request from the API.

    Returns:
        list: Raw result records from the API response.

    Raises:
        Exception: If the API response status code is not 200.
    """
   
    # Get sample dataset and indicator IDs for the selected group.
    dataset_id  = example_id("dataset", group=group)
    indicator = example_id("indicator", group=group)
    # Build the API URL for the get-data endpoint.
    url = api_url(
        endpoint = "get-data",
        dataset_id = dataset_id,
        indicators = indicator,
        page = 1,
        page_size = size
    )
    # Send request to the API.
    response = requests.get(url)
    # Raise an error if the API request fails.
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code}")
    # Convert response to JSON and return only the results list.
    data =  response.json()
    return data.get("results",[])


def example_json_query(ees_environment: str = "prod"):
   """
    Create an example JSON query body for the attendance dataset.

    This query can be used when testing API endpoints that require a JSON
    request body containing indicators, time periods, geographies, and filters.

    Args:
        ees_environment: EES API environment. Default is "prod".

    Returns:
        Dict: JSON-compatible query body.
    """

    return parse_tojson_params(
            indicators = example_id("indicator", group="attendance", ees_environment=ees_environment),
            time_periods = example_id("time_period", group="attendance", ees_environment=ees_environment),
            geographies=todf_geographies(example_id("location_codes",group="attendance",ees_environment=ees_environment)),
            filters = example_id("filter_items_short", group="attendance",ees_environment=ees_environment)
    )

def example_geography_query(level: str = "nat_yorks"):
   """
    Return an example geography query as a pandas DataFrame.

    Args:
        level: Name of the geography example to return.

    Returns:
        pd.DataFrame: Geography query data.

    Raises:
        ValueError: If the requested level is invalid.
    """
    # Dictionary of available geography query examples.
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
     # Validate requested geography query level.
    if level not in example_geography_query:
        raise ValueError("Invalid level")
    
    return example_geography_query[level]

