"""
generate_ees_meta.py
 
Generates a standardised EES metadata DataFrame from API metadata.
 
This module converts the raw metadata returned by get_meta() into
a single flat DataFrame that maps column names to their types, labels,
units and formatting — compatible with the EES data upload template.
"""
import pandas as pd 

def generate_ees_meta(api_meta: dict) -> pd.DataFrame:
   """
    Generate a standardised EES metadata DataFrame from API metadata.
 
    Combines filter columns and indicator columns from get_meta() output
    into a single DataFrame with columns matching the EES upload template.
 
    Parameters
    ----------
    api_meta : dict
        Metadata dict as returned by get_meta(). Must contain keys:
        - "filter_columns": DataFrame with "col_name" and "label" columns
        - "indicators":     DataFrame with "col_name" and "label" columns
 
    Returns
    -------
    pd.DataFrame
        DataFrame with one row per column containing:
        - col_name:              column name (sqid-based)
        - col_type:              "Filter" or "Indicator"
        - label:                 human-readable column label
        - indicator_grouping:    grouping for indicators (empty by default)
        - indicator_unit:        "%" for percent columns, "" otherwise
        - indicator_dp:          decimal places — "0" for counts, "1" for percents
        - filter_hint:           hint text for filters (empty by default)
        - filter_grouping_column: grouping column for filters (empty by default)
        - filter_default:        default filter value (space " " for filters)
 
    Examples
    --------
    >>> meta = get_meta(dataset_id="...", ees_environment="prod")
    >>> generate_ees_meta(meta)
    """
   # Build filters DataFrame
   # Extract col_name and label from filter_columns metadata
    filters_df = pd.DataFrame({
        "col_name": api_meta["filter_columns"]["col_name"],
        "label": api_meta["filter_columns"]["label"]
    })

    # Mark all rows in this DataFrame as Filter type
    filters_df["col_type"] = "Filter"
    # Set default filter value to a space (EES template requirement)
    filters_df["filter_default"] = " "

   # Build indicators DataFrame
   # Extract col_name and label from indicators metadata
    indicators_df = pd.DataFrame({
        "col_name": api_meta["indicators"]["col_name"],
        "label": api_meta["indicators"]["label"]
    })

    # Mark all rows in this DataFrame as Indicator type
    indicators_df["col_type"] = "Indicator"

    # Derive indicator unit from column name
    # Columns containing "percent" get "%" unit, all others get empty string
    indicators_df["indicator_unit"] = indicators_df["col_name"].apply(
        lambda x: "%" if "percent" in x else ""
    )
   # Derive decimal places (dp) from column name
    # count columns → "0" dp (whole numbers)
    # percent columns → "1" dp (one decimal place)
    # all others → "" (no dp specified)

    def get_dp(col):
        if "count" in col:
            return "0"
        elif "percent" in col:
            return "1"
        return ""
    

    indicators_df["indicator_dp"] = indicators_df["col_name"].apply(get_dp)

    # Combine filters and indicators into a single DataFrame
    # ignore_index=True resets row numbers after concatenation
    df = pd.concat([filters_df, indicators_df], ignore_index=True) 

    # Add empty columns required by the EES metadata template
    df["filter_hint"] = ""              # Optional hint text shown in EES UI
    df["indicator_grouping"] = ""       # Optional grouping for indicators
    df["filter_grouping_column"] = ""   # Optional grouping for filters

    # Ensure all expected columns exist — add empty string if missing
    # This handles cases where filters or indicators section was empty
    for col in ["indicator_unit", "indicator_dp", "filter_default"]:
        if col not in df.columns:
            df[col] = ""

    # Replace any remaining NaN values with empty strings
    df = df.fillna("")

    # Reorder columns to match the EES metadata template column order
    df = df[
        [
            "col_name",              # Column name used in the dataset
            "col_type",              # "Filter" or "Indicator"
            "label",                 # Human-readable label
            "indicator_grouping",    # Optional indicator group
            "indicator_unit",        # Unit e.g. "%" or ""
            "indicator_dp",          # Decimal places e.g. "0", "1" or ""
            "filter_hint",           # Optional hint text
            "filter_grouping_column", # Optional filter group
            "filter_default"          # Default filter value
        ]
    ]

    return df
