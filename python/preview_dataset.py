import warnings
import pandas as pd 
import requests
from io import StringIO
from typing import Optional, Union 

from api_url import api_url
from validation_rules import validate_ees_id


def preview_dataset(
        dataset_id: str, 
        dataset_version: Optional[str] = None, 
        api_version: Optional[str] = None, 
        ees_environment: Optional[str] = "prod",
        n_max: Optional[Union[int, float]] = 10,
        verbose: bool = False
) -> pd.DataFrame:
    
    if dataset_version is not None:
        warnings.warn(
            "Support for dataset_version is not yet available for downloading "
            "full data sets, Returning latest available version of data set."
        )
    
    if not isinstance(verbose, bool):
        raise ValueError("verbose must be a boolen value, either True or False")
    
    if n_max != float("inf"):
        if not isinstance(n_max, int) or n_max <= 0:
            raise ValueError("n_max must be positive integer value, e.g. 15, or float('inf')")
    
    validate_ees_id(dataset_id, level="dataset")


    query_url = api_url(
        endpoint="get-csv",
        ees_environment=ees_environment, 
        dataset_version=dataset_version,
        api_version=api_version,
        dataset_id=dataset_id,
        verbose=verbose
    )

    if verbose:
        print(f"Requesting data from: {query_url}")
    
    response = requests.get(query_url)

    if response.status_code != 200:
        raise Exception(
            f"HTTP connection error: {response.status_code}\n{response.text}"
        )
    
    if verbose:
        print("Reading response.....")

    
    content = response.text
    df = pd.read_csv(StringIO(content))

    if n_max != float("inf"):
        df = df.head(int(n_max))
    
    return df