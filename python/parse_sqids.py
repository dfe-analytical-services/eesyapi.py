"""
parse_sqids.py
 
Parse API sqids (short unique IDs) into human-readable labels.
 
Sqids are auto-generated ID codes used by the EES API to identify
filter columns, filter items, indicators and locations. This module
converts those codes back into human-readable labels using metadata
returned by get_meta().
"""

import warnings
import re
import pandas as pd 
from typing import Dict, Any, Optional

# GEOG_LEVEL_LOOKUP
#
# Maps API geographic level short codes to human-friendly names.
# Used by parse_geographic_level_codes() to convert API responses.
# See also: geog_level_lookup.py for the full DataFrame version.

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

def parse_time_codes(time_periods: pd.DataFrame, verbose: bool = False) -> pd.DataFrame:   # DataFrame with "code" and "period" columns  # Print debug info if True
"""
    Parse API time period codes into human-readable labels.
 
    Renames columns from API format (code/period) to display format
    (time_identifier/time_period) and converts short codes to full names:
    - "AY" → "Academic year"
    - "FY" → "Financial year"
    - "CY" → "Calendar year"
    - "W1" → "Week 1", "W12" → "Week 12"
 
    Parameters
    ----------
    time_periods : pd.DataFrame
        DataFrame with "code" and "period" columns from API metadata.
    verbose : bool
        Print debug info. Default False.
 
    Returns
    -------
    pd.DataFrame
        DataFrame with "time_identifier" and "time_period" columns.
 
    Raises
    ------
    ValueError
        If time_periods is not a DataFrame.
    """
  # Validate input type — must be a DataFrame not a list or dict
    if not isinstance(time_periods, pd.DataFrame):
        raise ValueError(
            "time_periods should be a DataFrame, but has been provided as a "
            + str(type(time_periods))
        )
    # Rename API column names to display-friendly names
    # "period" → "time_period", "code" → "time_identifier"
    out = time_periods.rename(columns={"period": "time_period", "code": "time_identifier"}).copy()

    # Convert week codes: "W1" → "Week 1", "W12" → "Week 12"
    # Uses regex to extract the number after "W"
    out["time_identifier"] = out["time_identifier"].apply(
        lambda x: re.sub(r"W([0-9]+)", r"Week\1", x) if isinstance(x, str) else x
    )

    # Convert year type codes to full names using lookup dict
    year_map = {"AY": "Academic year", "FY": "Financial year", "CY": "Calendar year"}
    out["time_identifier"] = out["time_identifier"].apply(
        lambda x: year_map.get(x, x) if isinstance(x, str) else x
    )
    # Shorten year range format: "2024/2025" → "202425"
    # This removes the "20" prefix from the second year
    out["time_period"] = out["time_period"].apply(
        lambda x: re.sub(r"([0-9]+)/20([0-9]+)", r"\1\2", x) if isinstance(x, str) else x
    )

    return out

def parse_geographic_level_codes(
        geographic_levels: pd.Series,   # Series of API geographic level codes e.g. "NAT"
        verbose: bool = False           # Print debug info if True
) -> pd.DataFrame:
    """
    Convert API geographic level codes into human-readable names.
 
    Maps short API codes (e.g. "NAT", "REG", "LA") to full names
    (e.g. "National", "Regional", "Local authority") using GEOG_LEVEL_LOOKUP.
 
    Parameters
    ----------
    geographic_levels : pd.Series
        Series of API geographic level codes from API results.
    verbose : bool
        Print debug info. Default False.
 
    Returns
    -------
    pd.DataFrame
        Single-column DataFrame with "geographic_level" column.
 
    Raises
    ------
    ValueError
        If geographic_levels is a list, dict or DataFrame instead of Series.
    """
     # Reject list, dict and DataFrame — must be a Series
    if isinstance(geographic_levels, (list, dict, pd.DataFrame)):
        raise ValueError(
            "geographic_levels should be a Series or list, but has been provided as a "
            + str(type(geographic_levels))
        )
    # Convert list to Series if needed
    if isinstance(geographic_levels, list):
        geographic_levels = pd.Series(geographic_levels)
        
    # Warn about any unknown level codes not in the lookup
    api_levels = set(GEOG_LEVEL_LOOKUP.keys())
    unknown = set(geographic_levels.unique()) - api_levels
    if unknown:
        warnings.warn(
            "The following geographic_levels were returned by your query, "
            "but are not a part of the standard data set: "
            + ", ".join(unknown)

        )
    # Map each code to its human-readable name
    # Unknown codes are kept as-is (pass-through behaviour)
    result = geographic_levels.map(
        lambda x: GEOG_LEVEL_LOOKUP.get(x,x)
    )
    # Return as single-column DataFrame
    return pd.DataFrame({"geographic_level": result})

def parse_sqids_locations(
    locations: pd.DataFrame,   # Location columns from API result
    meta: Dict[str, Any],      # Metadata dict from get_meta()
    verbose: bool = False      # Print debug info if True
) -> pd.DataFrame:
 """
    Replace location sqids with human-readable location names and codes.
 
    Looks up each location sqid in the metadata locations DataFrame
    and replaces it with the corresponding label, code and level info.
 
    Parameters
    ----------
    locations : pd.DataFrame
        DataFrame where columns are geographic level codes (e.g. "NAT")
        and values are location sqids.
    meta : dict
        Metadata dict from get_meta() containing "locations" DataFrame.
    verbose : bool
        Print debug info. Default False.
 
    Returns
    -------
    pd.DataFrame
        DataFrame with location sqids replaced by readable location info.
    """
    # Get the locations lookup DataFrame from metadata
    lookup = meta.get("locations", pd.DataFrame())
   # Filter lookup to only include levels present in the data
    if isinstance(lookup, pd.DataFrame) and not lookup.empty:
        lookup = lookup[
            lookup["geographic_levels_code"].isin(locations.columns)

        ].rename(columns={"label": "name"}) # Rename label to name for clarity
    
    result = locations.copy()

    # Process each geographic level column separately
    for level in locations.columns:
        # Temporarily rename the level column to "item_id" for merging
        result = result.rename(columns={level: "item_id"})
       # Get the lookup rows for this specific level
        level_lookup = lookup[
            lookup["geographic_levels_code"] == level
        
        ].copy() if isinstance(lookup, pd.DataFrame) and not lookup.empty else pd.DataFrame()

        if not level_lookup.empty:
            # Drop level columns already captured elsewhere to avoid duplicates
            level_lookup = level_lookup.drop(
                columns = ["geographic_levels_code", "geographic_level"],
                errors = "ignore"
            )
           # Prefix all columns with the level code e.g. "name" → "nat_name"
            rename_map = {
                col: f"{level.lower()}_{col}"
                for col in level_lookup.columns
                if col != "item_id"   # Keep item_id for merging
            }

            level_lookup = level_lookup.rename(columns=rename_map)
             # Merge location details into results on the sqid
            result = result.merge(level_lookup, on="item_id", how="left")
        # Remove the temporary item_id column after merging
        result = result.drop(columns=["item_id"], errors="ignore")
   # Remove any columns that are entirely NaN (no data for that level)
    result = result.dropna(axis=1, how="all")

    return result 


def parse_sqids_filters(
    filters: pd.DataFrame,    # Filter columns from API result
    meta: Dict[str, Any],     # Metadata dict from get_meta()
    verbose: bool =False      # Print debug info if True
) -> pd.DataFrame:
    """
    Replace filter sqids with human-readable filter item labels.
 
    Looks up each filter column sqid in metadata to get the column name,
    then replaces item sqids with their human-readable labels.
 
    Parameters
    ----------
    filters : pd.DataFrame
        DataFrame where columns are filter column sqids and values
        are filter item sqids from the API result.
    meta : dict
        Metadata dict from get_meta() containing "filter_columns"
        and "filter_items" DataFrames.
    verbose : bool
        Print debug info including matched column names. Default False.
 
    Returns
    -------
    pd.DataFrame
        DataFrame with sqid columns renamed and values replaced with labels.
    """
    
    # Get filter metadata from meta dict
    filter_columns = meta.get("filter_columns", pd.DataFrame())
    filter_items = meta.get("filter_items", pd.DataFrame())
    # Find which filter column sqids from metadata match the data columns
    if isinstance(filter_columns, pd.DataFrame) and not filter_columns.empty:
        filter_ids = filter_columns[
             filter_columns["col_id"].isin(filters.columns)
    
        ]["col_id"].tolist()

    else:
        filter_ids = []
    # Warn about any filter columns in data not found in metadata
    data_filter_ids = list(filters.columns)
    unknown = set(data_filter_ids) - set(filter_ids)
    if unknown:
        warnings.warn(
            "The following filter IDs were not found in the associated meta data: "
            +", ".join(unknown)
        )

    if verbose:
         print(filter_ids)   # Print matched filter IDs in verbose mode
    
    result = filters.copy()  
    
    #Process each matched filter column
    for column_sqid in filter_ids:
        # Look up the human-readable column name for this sqid
        col_name_rows = filter_columns[filter_columns["col_id"] == column_sqid]
        if col_name_rows.empty:
            continue   # Skip if sqid not found in metadata
        col_name = col_name_rows["col_name"].iloc[0]   # Get first match

        if verbose:
            print(f"Matched {column_sqid} to {col_name}")
            
       # Build lookup: item_id sqid → item label for this filter column
        lookup = filter_items[
            filter_items["col_id"] == column_sqid

        ][["item_id", "item_label"]].copy() if isinstance(filter_items, pd.DataFrame) else pd.DataFrame()

        if not lookup.empty:
            # Rename columns: item_label → col_name, item_id → column_sqid for merging
            lookup = lookup.rename(columns={"item_label": col_name, "item_id": column_sqid})
            # Merge labels into result on the sqid column
            result = result.merge(lookup, on=column_sqid, how="left")
             # Drop the original sqid column — now replaced by the label column
            result = result.drop(columns=[column_sqid])

    return result


def parse_sqids_indicators(
        indicators: pd.DataFrame,  # Indicator columns from API result
        meta: Dict[str, Any],      # Metadata dict from get_meta()
        verbose: bool = False      # Print debug info if True
) -> pd.DataFrame:
    """
    Rename indicator sqid columns to human-readable column names.
 
    Looks up each indicator column sqid in metadata and renames
    the column to its human-readable col_name.
 
    Parameters
    ----------
    indicators : pd.DataFrame
        DataFrame where columns are indicator sqids from API result.
    meta : dict
        Metadata dict from get_meta() containing "indicators" DataFrame.
    verbose : bool
        Print debug info. Default False.
 
    Returns
    -------
    pd.DataFrame
        DataFrame with indicator sqid columns renamed to col_names.
    """
    # Get indicators metadata from meta dict
    indicator_meta = meta.get("indicators", pd.DataFrame())
    if isinstance(indicator_meta, pd.DataFrame) and not indicator_meta.empty:
        # Find which indicator sqids from metadata match the data columns
        matched = indicator_meta[
            indicator_meta["col_id"].isin(indicators.columns)
        ]
         # Build rename map: sqid → col_name e.g. "X9fKb" → "sess_possible"
        rename_map = dict(zip(matched["col_id"], matched["col_name"]))
         # Rename columns using the map
        return indicators.rename(columns=rename_map)
    # If no metadata available, return a copy unchanged
    return indicators.copy()





    
