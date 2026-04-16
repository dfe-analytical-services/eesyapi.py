import requests 
from typing import Optional, List, Dict, Any 

from .api_url import api_url 

def validate_page_size(page_size: Optional[int]):
    if page_size is not None and page_size <=0:
        raise ValueError("page_size must be greater than 0")
    

def warning_max_pages(response: Dict[str, Any]):
    if "paging" in response:
        total_pages = response["paging"].get("totalPages", 1)
        current_pages = response["paging"].get("page", 1)

        if current_pages > total_pages:
            print("Warning: Requested page exceeds total available pages")

def get_publications(
        search: Optional[str] = None, 
        ees_environment: Optional[str] = None, 
        api_version: Optional[str] = None, 
        page_size: Optional[int] = None, 
        page: Optional[int] = None, 
        verbose: bool = False
) -> List[Dict]:
    
    validate_page_size(page_size)

    url = api_url(
        endpoint="get-publications",
        search = search, 
        ees_environment=ees_environment,
        api_version=api_version,
        page_size=page_size, 
        page=page,
        verbose=verbose
    )

    if verbose:
        print(f"GET {url}")

        response = requests.get(url)

        if response.status_code !=200:
            raise Exception(f"API Error: {response.status_code}")
        
        data = response.json()

        if page is None:
            total_pages = data.get("paging", {}).get("totalPages",1)

            if total_pages > 1:
                for p in range(2, total_pages +1):

                    url_page = api_url(
                        endpoint = "get-publications",
                        search = search, 
                        ees_environment = ees_environment,
                        api_version = api_version,
                        page_size = page_size,
                        page = p, 
                        verbose = verbose 
                    )

                    if verbose:
                        print(f"GET page {p}: {url_page}")

                    response_page = requests.get(url_page)

                    if response_page.status_code !=200:
                        raise Exception(f"API Error: {response_page.status_code}")
                    
                    data_page = response_page.json 

                    data["results"].extend(data_page.get("results",[]))

    
    warning_max_pages(data)

    return data.get("results",[])