"""
http_request_error.py
 
Translates HTTP response status codes into contextual error messages
for the Explore Education Statistics (EES) API.
 
HTTP status codes are grouped by their first digit:
- 2xx: Success
- 4xx: Client error (bad request, invalid IDs, etc.)
- 5xx: Server error (internal EES API error)
"""

import json 
from typing import Any, Dict 


def http_request_error(response, verbose: bool = False) -> str:  # HTTP response object from requests library   # Print detailed error messages if True
    """
    Translate HTTP response into contextual error message

    Checks the HTTP status code and raises an exception for 4xx and 5xx
    responses, with additional detail extracted from the API error body.
    Returns a success message for 2xx responses.
 
    Parameters
    ----------
    response : requests.Response
        HTTP response object with status_code and json() method.
    verbose : bool
        Print API error messages to console. Default False.
 
    Returns
    -------
    str
        Success message for 2xx responses.
 
    Raises
    ------
    ValueError
        If response object has no status_code attribute.
    Exception
        For 4xx and 5xx responses, with full error detail from API.
    """
   # Status code group lookup
    # Maps first digit of HTTP status to a human-friendly message
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
    
    # Extract status code — raise if response has no status_code attribute
    status_code = getattr(response, "status_code", None)

    if status_code is None:
        raise ValueError("Response object does not contain status_code")
    # Get the status group — first digit of status code
    # e.g. 404 → 4, 200 → 2, 500 → 5
    status_group = status_code // 100
    # Look up the default message for this status group
    # Falls back to unrecognised message if group not in lookup
    status_response_text = status_lookup.get(
        status_group,
        "API http response code not recognised."
    )
    # For error responses (4xx, 5xx) — extract detailed error info from body
    if status_group in [4, 5]:
        
        try:
            data = response.json()
        except Exception:
            data = {}
            
        # Get the errors array from the response body
        # EES API returns errors in format: {"errors": [{"message": "...", "detail": {...}}]}
        api_errors = data.get("errors")

        if api_errors:
            # Extract unique error messages — use set to avoid duplicates
            messages = list({e.get("message", "") for e in api_errors})
            # Extract detail dicts which may contain items, values and allowed values
            details = [e.get("detail",{}) for e in api_errors]
            # Join all error messages into one string
            error_message = "\n".join(messages)
            # Build additional info string from error details
            extra_info = ""

            for d in details:
                # Items that caused the error e.g. invalid sqids
                if "items" in d:
                    extra_info += "\n   Error items: "+" ,".join(map(str, d["items"]))
                # The values that were provided in the request
                if "value" in d:
                    extra_info += "\n   Provided values: "+" ,".join(map(str, d["value"]))
                # The values that are actually allowed
                if "allowed" in d:
                    extra_info += "\n   Allowed values: "+" ,".join(map(str, d["allowed"]))
            # Combine error message with extra detail info
            status_response_text = error_message + extra_info

             # Print error messages to console if verbose mode is on
            if verbose:
                print("API Error Messages:", messages)

             # Raise exception for all non-2xx status codes
            # Include status code and full error message in exception
            if status_group !=2:
                raise Exception(
                    f"\nHTTP connection error: {status_code}\n{status_response_text}"
                )
            
            return status_response_text
