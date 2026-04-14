import pandas as pd 

def generate_ees_meta(api_meta: dict) -> pd.DataFrame:
    """
    Generate EES metadata dataframe
    """

    filters_df = pd.DataFrame({
        "col_name": api_meta["filter_columns"]["col_name"],
        "label": api_meta["filter_columns"]["label"]
    })


    filters_df["col_type"] = "Filter"
    filters_df["filter_default"] = " "

    indicators_df = pd.DataFrame({
        "col_name": api_meta["indicators"]["col_name"],
        "label": api_meta["indicators"]["label"]
    })

    indicators_df["col_type"] = "Indicator"


    indicators_df["indicator_unit"] = indicators_df["col_name"].apply(
        lambda x: "%" if "percent" in x else ""
    )

    def get_dp(col):
        if "count" in col:
            return "0"
        elif "percent" in col:
            return "1"
        return ""
    

    indicators_df["indicator_dp"] = indicators_df["col_name"].apply(get_dp)

    df = pd.concat([filters_df, indicators_df], ignore_index=True)

    df["filter_hint"] = ""
    df["indicator_grouping"] = ""
    df["filter_grouping_column"] = ""


    for col in ["indicator_unit", "indicator_dp", "filter_default"]:
        if col not in df.columns:
            df[col] = ""


    df = df.fillna("")


    df = df[
        [
            "col_name",
            "col_type",
            "label",
            "indicator_grouping",
            "indicator_unit",
            "indicator_dp",
            "filter_hint",
            "filter_grouping_column",
            "filter_default"
        ]
    ]

    return df