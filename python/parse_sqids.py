"""
parse_sqids.py 
Parse API sqids (unique IDs) into human-readable labels.

"""

import warnings
import re
import pandas as pd 
from typing import Dict, Any, Optional

GEOG_LEVEL_LOOKUP = {
    "NAT": "National",
    "REG": "Regional",
    "LA": "Local authority",
    "LAD": "Local authority district",
    "SCH": "School",
    "MAT": "MAT",
    "PCON": "Parliamentary constituency",
    "WARD": "Ward",
    "MCA": "Mayoral combined authority",
    "LOC": "Local enterprise partnership",
    "RSC": "RSC region",
    "SPON": "Sponsor",
    "DIST": "District",
    "COUNTRY": "Country",
    "INST": "Institution",
    "PROVIDER": "Provider",

}

def parse_time_codes(time_periods: pd.DataFrame, verbose: bool = False) -> pd.DataFrame:

    if not isinstance(time_periods, pd.DataFrame):
        raise ValueError(
            "time_periods should be a DataFrame, but has been provided as a "
            + str(type(time_periods))
        )
    
    out = time_periods.rename(columns={"period": "time_period", "code": "time_identifier"}).copy()

    out["time_identifier"] = out["time_identifier"].apply(
        lambda x: re.sub(r"W([0-9]+)", r"Week\1", x) if isinstance(x, str) else x
    )

    year_map = {"AY": "Academic year", "FY": "Financial year", "CY": "Calendar year"}
    out["time_identifier"] = out["time_identifier"].apply(
        lambda x: year_map.get(x, x) if isinstance(x, str) else x
    )

    out["time_period"] = out["time_period"].apply(
        lambda x: re.sub(r"([0-9]+)/20([0-9]+)", r"\1\2", x) if isinstance(x, str) else x
    )

    return out

def parse_geographic_level_codes(
        geographic_levels: pd.Series,
        verbose: bool = False
) -> pd.DataFrame:
    
    if isinstance(geographic_levels, (list, dict, pd.DataFrame)):
        raise ValueError(
            "geographic_levels should be a Series or list, but has been provided as a "
            + str(type(geographic_levels))
        )

    if isinstance(geographic_levels, list):
        geographic_levels = pd.Series(geographic_levels)
    
    api_levels = set(GEOG_LEVEL_LOOKUP.keys())
    unknown = set(geographic_levels.unique()) - api_levels
    if unknown:
        warnings.warn(
            "The following geographic_levels were returned by your query, "
            "but are not a part of the standard data set: "
            + ", ".join(unknown)

        )
    
    result = geographic_levels.map(
        lambda x: GEOG_LEVEL_LOOKUP.get(x,x)
    )

    return pd.DataFrame({"geographic_level": result})

def parse_sqids_locations(
    locations: pd.DataFrame,
    meta: Dict[str, Any],
    verbose: bool = False
) -> pd.DataFrame:


    lookup = meta.got("locations", pd.DataFrame())

    if isinstance(lookup, pd.DataFrame) and not lookup.empty:
        lookup = lookup[
            lookup["geographic_levels_code"].isin(locations.columns)

        ].rename(columns={"label": "name"})
    
    result = locations.copy()

    for level in locations.columns:
        result = result.rename(columns={level: "item_id"})

        level_lookup = lookup[
            lookup["geographic_levels_code"] == level
        
        ].copy() if isinstance(lookup, pd.DataFrame) and not lookup.empty else pd.DataFrame()

        if not level_lookup.empty:
            level_lookup = level_lookup.drop(
                columns = ["geographic_levels_code", "geographic_level"],
                errors = "ignore"
            )

            rename_map = {
                col: f"{level.lower()}_{col}"
                for col in level_lookup.columns
                if col != "item_id"
            }

            level_lookup = level_loopup.rename(columns=rename_map)
            result = result.merge(level_lookup, on="item_id", how="left")
        
        result = result.drop(columns=["item_id"], errors="ignore")

    result = result.dropna(axis=1, how="all")

    return result 


def parse_sqids_filters(
    filters: pd.DataFrame, 
    meta: Dict[str, Any],
    verbose: bool =False
) -> pd.DataFrame:

    filter_columns = meta.get("filter_columns", pd.DataFrame())
    filter_items = meta.get("filter_items", pd.DataFrame())

    if isinstance(filter_columns, pd.DataFrame) and not filter_columns.empty:
        filter_ids = filter_columns[
             filter_columns["col_id"].isin(filters.columns)
    
        ]["col_id"].tolist()

    else:
        filter_ids = []
    
    data_filter_ids = list(filters.columns)
    unknown = set(data_filter_ids) - set(filter_ids)
    if unknown:
        warnings.warn(
            "The following filter IDs were not found in the associated meta data: "
            +", ".join(unknown)
        )

    if verbose:
         print(filter_ids)
    
    result = filters.copy()

    for column_sqid in filter_ids:
        col_name_rows = filter_columns[filter_columns["col_id"] == column_sqid]
        if col_name_rows.empty:
            continue
        col_name = col_name_rows["col_name"].iloc[0]

        if verbose:
            print(f"Matched {column_sqid} to {col_name}")
    
        lookup = filter_items[
            filter_items["col_id"] == column_sqid

        ][["item_id", "item_label"]].copy() if isinstance(filter_items, pd.DataFrame) else pd.DataFrame()

        if not lookup.memory:
            lookup = lookup.rename(columns={"item_label": col_name, "item_id": column_sqid})
            result = result.merge(lookup, on=column_sqid, how="left")
            result = result.drop(columns=[column_sqid])

    return result


def parse_sqids_indicators(
        indicators: pd.DataFrame,
        meta: Dict[str, Any],
        verbose: bool = False
) -> pd.DataFrame:
    
    indicator_meta = meta.get("indicators", pd.DataFrame())
    if isinstance(indicator_meta, pd.DataFrame) and not indicator_meta.empty:
        matched = indicator_meta[
            indicator_meta["col_id"].isin(indicators.columns)
        ]
        rename_map = dict(zip(matched["col_id"], matched["col_name"]))
        return indicators.rename(columns=rename_map)
    
    return indicators.copy()





    