import re
from typing import Optional, Union, List

VALID_ENVIRONMENTS = ("dev","test","preprod","prod")

VALID_ENDPOINTS = (
    "get-publications",
    "get-data-catalogue",
    "get-dataset-versions",
    "get-summary",
    "get-meta",
    "get-csv",
    "get-data",
    "post-data"
)

VALID_FILTER_TYPES = (
    "time_periods",
    "geographic_levels",
    "locations",
    "filter_items",
)

VALID_ID_LEVELS = ("publication", "dataset", "location", "filter_item","indicator")

def validate_ees_environment(ees_environment: str)-> None:
    """
    Validate EES environment string.

    Parameters
    ees_environment : str
        one of: "dev", "test", "preprod","prod"
    
    Raises

    ValueError
        If the environment is not valid.
    """

    if ees_environment not in VALID_ENVIRONMENTS:
        raise ValueError(
            "You have entered invalid EES environment."
            "The environment should be one of:\n"
            "  -dev, test, preprod or prod"
        )
    

def validate_api_version(api_version: Union[str, int, float]) -> None:
    """
    Validate API Version - must be numeric only.

    Parameters

    api_version : str, int or float
        API version to validate.
    
    Raises
    ValueError
        If the api_version contains non-numeric characters.
    """
    if re.search(r"[a-z_%+\-]", str(api_version), re.IGNORECASE):
        raise ValueError(
            "You have entered an invalid API version in the api_version argument."
            "This should be numerical values only"
        )

def validate_endpoint(endpoint: Optional[str]) -> None:
    """
    Validate API endpoint.

    Parameters

    endpoint: str or None
        Endpoint name to validate.
    
    
    Raises 

    ValueError
        if endpoint is None or not a valid endpoint name.
    """
    if endpoint is None:
        raise ValueError("Endpoint must be set, can not be None")

    if endpoint not in VALID_ENDPOINTS:
       raise ValueError(
           "You have entered an invalid endpoint, this should be one of: "
           + ", ".join(VALID_ENDPOINTS)
       )

def validate_time_periods(time_periods: List[str]) -> None:
    """
    Validate time periods are in the format  {period}{code}

    Parameters

    time_periods: list of str
        Time periods to validate, e.g. ["2024|AY", "2023|W21"]
    
        
    
    Raises

    ValueError
        if any time period is not in the correct format.
    """

    invalid = []
    for tp in time_periods:
        pipes = re.sub(r"[a-zA-Z0-9]", "",tp)
        if len(pipes) != 1:
            invalid.append(tp)
    
    if invalid:
        raise ValueError(
            "Invalid time periods provided: " + ", ".join(invalid) + "\n"
            "These should be in the format {period}}|{code}, e.g. 2024|AY, 2023|W21"
        )
    

def validate_ees_id(
        element_id: Optional[Union[str, List[str]]],
        level: str = "publication",
        verbose: bool = False
) -> None:
    """
    validate element IDs for publications, datasets, locations, filters, indicators.

    Parameters

    element_id : str, list of str, or None
        The ID(s) to validate.
    level: str
        one of : "publication", "dataset", "location", "filter_item", "indicator")
    verbose : bool
        Run in verbose mode.

    Raises

    ValueError 
         If the level is invalid or element_id is None.
    """

    if level not in VALID_ID_LEVELS:
        raise ValueError(
            "Non-valid element level received by validate_id.\n"
            "Should be one of: " + ", ".join(VALID_ID_LEVELS) + "."
        )
    
    if element_id is None:
        raise ValueError(
            "The variable" + level + "_id is None, "
            "please provide a valid " + level + "_id."
        )
    
    if not isinstance(element_id, (str, list)) or element_id == "":
        raise ValueError(
            "Invalid " + level + "_id provided. Must be a non-empty string or list."
        )

    if level == "location":
        ids = [element_id] if isinstance(element_id, str) else element_id
        for loc in ids:
            parts = loc.split("|")
            if len(parts) != 3 or any(p == "" for p in parts):
                raise ValueError(
                    'Invalid locations found, these should be of the form "LEVEL|XXXX|1b3d5".'
                )
            
            location_id_type = parts[1]
            if location_id_type not in ("id", "code"):
                raise ValueError(
                    'The middle entry in "LEVEL|xxxx|1b3d5" should be one of "id" or "code"'
                )
    
    
            
def validate_ees_filter_type(filter_type: str) -> None:
    """
    Validate filter type.

    Parameters

    filter_type : str
        one of: "time_periods", "geographic_levels", "locations", "filter_items"
    
    Raises

    ValueError 
        if filter_type is not valid.
    """

    if filter_type not in VALID_FILTER_TYPES:
        raise ValueError(
            'filter_type keyword should be one of "time_periods", "geographic_levels",'
            '"locations" or "filter_items"'
        )

def validate_page_size(page_size: Optional[Union[int, float]], min_size: int = 1, max_size: int =40) -> None:
    """
    Validate page size is within allowed range.

    Parameters

    page_size : int, float or None
        Page size to validate.
    
    
    min : int
        Minimum valid page Size (default 1).
    
    max : int
        Maximum valid page size (default 40).
    
    
    Raises

    ValueError
        If page_size is not numeric or outside allowed range.
    """
    if page_size is not None:
        if isinstance(page_size, bool):
            valid = False
        elif isinstance(page_size, (int, float)):
            valid = min_size <= page_size <= max_size
        else:
            valid = False
        
        if not valid:
            raise ValueError(
                "The page size can only be a numeric value within the range " 
                + str(min_size) + " <= page_size <= " + str(max_size) + "."

            )

def validate_dataset_version(dataset_version: Optional[Union[str, int, float]]) -> None:
    """
    Validate dataset version format.


    Accepts:
    - "*" wildcard
    - "major.minor.patch" format with optional wildcards e.g. "2.0.0", "2.*", "*"
    - Numeric values for backwards compatibility


    Parameters

    dataset_version : str, int, float or None
        Dataset version to validate 

    Raises

    ValueError 
        If dataset_version is not in valid format.
    """
    if dataset_version is not None:
        if isinstance(dataset_version, bool):
            valid = False
        
        elif isinstance(dataset_version, str):
            pattern = r"^\*$|^(\d+)(\.(\d+|\*)){0, 2}$"
            valid = bool(re.match(pattern, dataset_version))
        elif isinstance(dataset_version, (int, float)):
            valid = True
        
        else:
            valid = False

    if not valid:
        raise ValueError(
            "The dataset version must be a character string in the format"
            "'major.minor.patch', optionally using '*' wildcards "
            "(e.g. '8.2.3','2.3.*', '*')."
        )

