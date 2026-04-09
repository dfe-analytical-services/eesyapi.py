import json 
from typing import Any, Dict 


def http_request_error(response, verbose: bool = False) -> str:
    """
    Translate HTTP response into contextual error message
    """

    status_loop = {
        2: "Successful API request.",
        4: (
            "Invalid quey, data set ID, data set version or API version submitted to API."
        ),
        5:(
            "Internal server error encountered - please contact the EES API team at "
            "explore.statistics@education.gov.uk providing the query you were attempting to submit."
        )
    }

    status_loop = get