import pytest
import pandas as pd 
from generate_ees_meta import generate_ees_meta

def make_api_meta(filter_cols=None, indicators=None):
    return {
        "filter_columns": filter_cols or {
            "col_name": ["absence_type", "school_type"],
            "label": ["Absence type", "School type"]
        },
        "indicators": indicators or {
            "col_name": ["sess_possible", "sess_authorised_percent"],
            "label": ["Session possible", "Authorised absence percent"]
        }
    }

class TestGenerateEesMeta:

    def test_returns_dataframe(self):
        result = generate_ees_meta(make_api_meta())
        assert isinstance(result, pd.DataFrame)

    def test_has_col_name_column(self):
        result = generate_ees_meta(make_api_meta())
        assert "col_name" in result.columns

    def test_has_col_type_column(self):
        result = generate_ees_meta(make_api_meta())
        assert "col_type" in result.columns

    def test_has_label_column(self):
        result = generate_ees_meta(make_api_meta())
        assert "label" in result.columns

    def test_has_indicator_unit_column(self):
        result = generate_ees_meta(make_api_meta())
        assert "indicator_unit" in result.columns
    
    def test_has_indicator_dp_column(self):
        result = generate_ees_meta(make_api_meta())
        assert "indicator_dp" in result.columns

    def test_has_filter_hint_column(self):
        result = generate_ees_meta(make_api_meta())
        assert "filter_hint" in result.columns
    
    def test_has_filter_grouping_column(self):
        result = generate_ees_meta(make_api_meta())
        assert "filter_grouping_column" in result.columns

    def test_has_filter_default_column(self):
        result = generate_ees_meta(make_api_meta())
        assert "filter_default" in result.columns
    
    def test_filter_col_type_is_filter(self):
        result = generate_ees_meta(make_api_meta())
        filters = result[result["col_type"] == "Filter"]
        assert len(filters) == 2

    def test_indicators_col_type_is_indicator(self):
        result = generate_ees_meta(make_api_meta())
        indicators = result[result["col_type"] == "Indicator"]
        assert len(indicators) == 2

    def test_total_rows_correct(self):
        result = generate_ees_meta(make_api_meta())
        assert len(result) == 4
    
    def test_percent_indicator_unit(self):
        result = generate_ees_meta(make_api_meta())
        percent_rows = result[result["col_name"].str.contains("percent")]
        assert all(percent_rows["indicator_unit"] == "%")
    
    def test_non_percent_indicator_unit_empty(self):
        result = generate_ees_meta(make_api_meta())
        non_percent = result[
            (result["col_type"] == "Indicator") &
            (~result["col_name"].str.contains("percent"))
        ]
        assert all(non_percent["indicator_unit"] == "")

    def test_count_indicator_dp_is_0(self):
        meta = make_api_meta(indicators={
            "col_name": ["sess_count"],
            "label": ["Session count"]
        })
        result = generate_ees_meta(meta)
        count_rows = result[result["col_name"].str.contains("count")]
        assert all(count_rows["indicator_dp"] == "0")


    def test_percent_indicator_dp_is_1(self):
        result = generate_ees_meta(make_api_meta())
        percent_rows = result[result["col_name"].str.contains("percent")]
        assert all(percent_rows["indicator_dp"] == "1")

    def test_no_nulls_in_result(self):
        result = generate_ees_meta(make_api_meta())
        assert not result.isnull().values.any()

    def test_single_filter_single_indicators(self):
        meta = make_api_meta(
            filter_cols={"col_name": ["type"], "label":["Type"]},
            indicators={"col_name": ["count"], "label":["Count"]}

        )
        result = generate_ees_meta(meta)
        assert len(result) == 2

    def test_multiple_filters_multiple_indicators(self):
        meta = make_api_meta(
            filter_cols={
                "col_name": ["f1", "f2", "f3"],
                "label": ["Filter 1", "Filter 2", "Filter 3"]
            },
            indicators={
                "col_name": ["ind1","ind2"],
                "label": ["Indicator 1", "Indicator 2"]
            }
        )
        result = generate_ees_meta(meta)
        assert len(result) == 5
    
    def test_column_order(self):
        result = generate_ees_meta(make_api_meta())
        expected_cols = [
            "col_name", "col_type", "label", "indicator_grouping",
            "indicator_unit", "indicator_dp", "filter_hint", 
            "filter_grouping_column", "filter_default"
        ]
        assert list(result.columns) == expected_cols

    def test_filter_default_is_space(self):
        result = generate_ees_meta(make_api_meta())
        filters = result[result["col_type"] == "Filter"]
        assert all(filters["filter_default"] == " ")
    
    def test_indicator_grouping_empty(self):
        result = generate_ees_meta(make_api_meta())
        assert all (result["indicator_grouping"] == "")

    def test_filter_hint_empty(self):
        result = generate_ees_meta(make_api_meta())
        assert all(result["filter_hint"] == "")