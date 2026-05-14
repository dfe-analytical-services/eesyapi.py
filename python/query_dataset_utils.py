import pandas as pd 
from typing import Optional, Union, List, Dict, Any 

from parse_sqids import GEOG_LEVEL_LOOKUP


HUMAN_TO_API_LOOKUP = {v: k for k, v in GEOG_LEVEL_LOOKUP.items()}

def todf_geographies(
        geographies: Optional[Union[str, List[str], Dict, pd.DataFrame]]

)-> Optional[pd.DataFrame]:
    
    if geographies is None:
        return None
    
    if isinstance(geographies, pd.DataFrame):
        df = geographies.copy()

        if "locations" in df.columns:
            split = df["locations"].str.split("|", expand=True)
            if split.shape[1] == 3:
                df["location_level"] = split[0]
                df["location_id_type"] = split[1]
                df["location_id"] = split[2]
                df = df.drop(colums=["locations"])
            else:
                raise ValueError("Invalid locations format in DataFrame")
        
        required = {"location_level", "location_id_type", "location_id"}

        if required.issubset(set(df.columns)):
            if "geographic_level" not in df.columns:
                df["geographic_level"] = df["location_level"]
        
        elif list(df.columns) == ["geographic_level"]:
            df["location_level"] = ""
            df["location_id_type"] = ""
            df["location_id"] = ""
        
        else:
            raise ValueError(
                "Invalid geographies DataFrame provided - please check the geographies guide."

            )
        
    elif isinstance(geographies, dict):
        valid_keys = {"geographic_level", "locations"}
        invalid = set(geographies.keys()) - valid_keys
        if invalid:
            raise ValueError(
                'Input geographies dict should contain only "geographic_level" and/or "locations"'
            )
        
        if "locations" in geographies:
            locs = geographies["locations"]
            if isinstance(locs, str):
                locs = [locs]
            split_rows = [loc.split("|") for loc in locs]
            locations_df = pd.DataFrame(
                split_rows,
                columns=["location_level", "location_id_type", "location_id"]
            ).drop_duplicates()
        
        else:
            locations_df = pd.DataFrame(
                [{"location_level": "", "location_id_types": "", "location_id": ""}]
            )

        if "geographic_level" in geographies:
            geo_levels = geographies["geographic_level"]
            if isinstance(geo_levels, str):
                geo_levels = [geo_levels]
            geo_df = pd.DataFrame({"geographic_level": geo_levels})
        
        else:
            geo_df = pd.DataFrame({"geographic_level": locations_df["location_level"]})
        
        if len(geo_df)  != len(locations_df):
            geo_df["_key"] = 1
            locations_df["_key"] = 1
            df = geo_df.merge(locations_df, on="_key").drop(columns=["_key"])
        else:
            df = pd.concat([geo_df.reset_index(drop=True),
                            locations_df.reset_index(drop=True)], axis=1)
        
        df = df.fillna("")

    
    elif isinstance(geographies, (str, list)):
        if isinstance(geographies, str):
            geographies = [geographies]
        
        split_rows = [g.split("|") for g in geographies]
        n_cols = len(split_rows[0])

        if n_cols == 1:
            df = pd.DataFrame({
                "geographic_level": [r[0] for r in split_rows],
                "location_level": "",
                "location_id_type": "",
                "location_id": ""
            }).drop_duplicates()
        
        elif n_cols == 3:
            df = pd.DataFrame(
                split_rows,
                columns=["location_level", "location_id_type", "location_id"]

            )
            df["geographic_level"] = df["location_level"]
            df["location_level"] = df.apply(
                lambda row: "" if row["location_id_type"] == "" and row["location_id"] == ""
                else row["location_level"],
                axis = 1
            )
            df = df.drop_duplicates()
        
        else:
            raise ValueError(
                "Geographies should contain either geographic_levels in the format"
                '"NAT", "REG", etc or locations in the format'
                '"NAT|code|E92000001", "NAT|id|dP0Zw", etc'

            )
    
    else:
        raise ValueError(
            "The geographies parameter should be given as either a DataFrame, dict, list or string."
        )
    
    for col in ["geographical_level", "location_level"]:
        if col in df.columns:
            df[col] = df[col].map(
                lambda x: HUMAN_TO_API_LOOKUP.get(x, x) if isinstance(x, str) else x
            )
    
    df = df.drop_duplicates()
    return df