import json 
from typing import Any, Dict 


def http_request_error(response, verbose: bool = False) -> str:
    """
    Translate HTTP response into contextual error message
    """

    status_lookup = {
        2: "Successful API request.",
        4: (
            "Invalid quey, data set ID, data set version or API version submitted to API."
        ),
        5:(
            "Internal server error encountered - please contact the EES API team at "
            "explore.statistics@education.gov.uk providing the query you were attempting to submit."
        )
    }

    status_code = getattr(response, "status_code", None)

    if status_code is None:
        raise ValueError("Response object does not contain status_code")
    
    status_group = status_code // 100

    status_response_text = status_lookup.get(
        status_group,
        "API http response code not recognised."
    )

    if status_group in [4, 5]:
        try:
            data = response.json()
        except Exception:
            data = {}
        
        api_errors = data.get("errors")

        if api_errors:
            messages = list({e.get("message", "") for e in api_errors})
            details = [e.get("detail",{}) for e in api_errors]

            error_message = "\n".join(messages)

            extra_info = ""

            for d in details:
                if "items" in d:
                    extra_info += "\n   Error items: "+" ,".join(map(str, d["items"]))
                if "value" in d:
                    extra_info += "\n   Provided values: "+" ,".join(map(str, d["value"]))
                if "allowed" in d:
                    extra_info += "\n   Allowed values: "+" ,".join(map(str, d["allowed"]))

            status_response_text = error_message + extra_info

            if verbose:
                print("API Error Messages:", messages)

            
            if status_group !=2:
                raise Exception(
                    f"\nHTTP connection error: {status_code}\n{status_response_text}"
                )
            
            return status_response_text