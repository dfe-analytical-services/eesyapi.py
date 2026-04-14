from typing import Dict, List, Any, Union 

def convert_single_filter(field: str, value: Union[str, List[str]]) -> Dict[str, Any]:

    """
    Convert a single filter into API-compatible format 

    """
    if isinstance(value, str):
        values = [value]
    
    elif isinstance(value, list):
        values = value

    else:
        raise ValueError(f"Invalid filter value type for {field}")
    
    return{
        "field" : field,
        "values": values
         
     }


def convert_api_filter_type(
        filters: Union[
            Dict[str, Union[str, List[str]]],
            List[Dict[str, Any]],
            None
        ]
) -> List[Dict[str, Any]]:
    
    """
    Convert user input filters into API-compatible format 

    """

    if filters is None:
        return []
    
    if isinstance(filters, list):
        for f in filters:
            if "field" not in f or "values" not in f:
                raise ValueError("Invalid filter format in list input")
         
        return filters
    
    if isinstance(filters, dict):
        converted = []


        for field, value in filters.items():
            converted.append(convert_single_filter(field, value))

        return converted 
    
    raise ValueError("Filters must be dict,list or None")