import warnings
from typing import Dict, Any

def warning_max_pages(api_result: Dict[str, Any]) -> Dict[str, Any]:
    paging = api_result.get("paging", {})
    page = paging.get("page")
    total_pages = paging.get("totalPages")

    if page is not None and total_pages is not None and page > total_pages:
        warnings.warn(
            f"The query has requested a page number ({page}) greater than the "
            f"available number of result pages ({total_pages})."
            f"The API will have returned an empty array to this query."
        )
    
    return api_result