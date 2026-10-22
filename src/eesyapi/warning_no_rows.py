import warnings
from typing import Dict, Any


def warning_no_rows(api_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Warn if the API query returned zero rows.

    Parameters

    api_result : dict
        Output from an API get query containing paging info.
    
    Returns

    dict
        Original api_result unchanged

    Examples

    >>> result = {"paging": {"totalResults":0, "page":1, "totalPages":0}}
    >>> warning_no_rows(result)
    """
    paging = api_result.get("paging", {})
    if paging.get("totalResults", -1) == 0:
        warnings.warn("Your query returned zero rows.")
    return api_result