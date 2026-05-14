import pytest 
import pandas as pd 
from examples import (
    parse_tojson_params,
    todf_geographies,
    example_id,
    example_geography_query,
    EXAMPLE_ID_LIST
)

class TestParseToJsonParams:

    def test_returns_dict(self):
        result = parse_tojson_params()
        assert isinstance(result, dict)

    def test_has_indicators_key(self):
        result = parse_tojson_params()
        assert "indicators" in result

    def test_has_time_periods_key(self):
        result = parse_tojson_params()
        assert "timePeriods" in result

    def test_has_geographies_key(self):
        result = parse_tojson_params()
        assert "geographies" in result

    def test_has_filters_key(self):
        result = parse_tojson_params()
        assert "filters" in result

    def test_string_indicator_wrapped_in_list(self):
        result = parse_tojson_params(indicators="ind1")
        assert result["indicators"] == ["ind1"]

    def test_list_indicator_unchanged(self):
        result = parse_tojson_params(indicators=["ind1","ind2"])
        assert result["indicators"] == ["ind1", "ind2"]

    def test_string_time_period_wrapped_in_list(self):
        result = parse_tojson_params(time_periods="2024|AY")
        assert result["timePeriods"] == ["2024|AY"]

    def test_list_time_periods_unchanged(self):
        result = parse_tojson_params(time_periods=["2022|AY", "2023|AY"])
        assert result["timePeriods"] == ["2022|AY", "2023|AY"]

    def test_none_indicators_is_none(self):
        result = parse_tojson_params(indicators=None)
        assert result["indicators"] is None

    def test_geographies_passed_through(self):
        geo = [{"geographicLevel": "NAT", "locationId": "E92000001"}]
        result =parse_tojson_params(geographies=geo)
        assert result["geographies"] == geo

    def test_filters_passed_through(self):
        filters = {"attendance_status": ["abc"]}
        result = parse_tojson_params(filter_items=filters)
        assert result["filters"] == filters

class TestTodGeographies:
    def test_returns_list(self):
        result = todf_geographies(["NAT|code|E92000001"])
        assert isinstance(result, list)

    def test_single_code_parsed(self):
        result = todf_geographies(["NAT|code|E92000001"])
        assert len(result) == 1
        assert result[0]["geographicLevel"] == "NAT"
        assert result[0]["locationId"] == "E92000001"

    def test_mutliple_code_parsed(self):
        result = todf_geographies(["NAT|code|E92000001","REG|code|E12000001"])
        assert len(result) == 2

    def test_geographic_level_is_first_part(self):
        result = todf_geographies(["REG|id|abc123"])
        assert result[0]["geographicLevel"] == "REG"

    def test_location_id_is_last_part(self):
        result = todf_geographies(["LA|id|xyz789"])
        assert result[0]["locationId"] == "xyz789"

    def test_empty_list_returns_empty(self):
        result = todf_geographies([])
        assert result == []

    def test_result_dicts_have_correct_keys(self):
        result = todf_geographies(["NAT|code|E92000001"])
        assert "geographicLevel" in result[0]
        assert "locationId" in result[0]

class TestExampleId:

    def test_returns_dataset_id_prod(self):
        result = example_id(level="dataset", ees_environment="prod", group="attendance")
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_returns_dataset_id_dev(self):
        result = example_id(level="dataset", ees_environment="dev", group="attendance")
        assert isinstance(result, str)

    def test_returns_indicators_prod(self):
        result = example_id(level="indicator", ees_environment="prod", group="attendance")
        assert isinstance(result,dict)

    def test_returns_all_when_level_all(self):
        result = example_id(level="all", ees_environment="prod", group="attendance")
        assert isinstance(result,dict)

    def test_invalid_group_raises(self):
        with pytest.raises(ValueError, match="not found in example list"):
            example_id(level="dataset", ees_environment="prod", group="invalid_group")

    def test_invalid_environment_raises(self):
        with pytest.raises(ValueError):
            example_id(level="dataset", ees_environment="staging", group="attendance")

    def test_invalid_level_raises(self):
        with pytest.raises(ValueError):
            example_id(level="nonexistent_level",ees_environment="prod", group="attendance")

    def test_absence_group_prod(self):
        result = example_id(level="dataset", ees_environment="prod", group="absence")
        assert isinstance(result, str)

    def test_absence_group_dev(self):
        result = example_id(level="dataset", ees_environment="dev", group="absence")
        assert isinstance(result, str)
    
    def test_publication_level_prod(self):
        result = example_id(level="publications", ees_environment="prod", group="attendance")

    def test_list_of_levels_returns_list(self):
        result = example_id(level="filter", ees_environment="prod", group="attendance")
        assert isinstance(result,str)


class TestExampleGeographyQuery:

    def test_nat_yorks_returns_dataframe(self):
        result = example_geography_query("nat_yorks")
        assert isinstance(result, pd.DataFrame)
    
    def test_nat_yorks_yorkslas_returns_dataframe(self):
        result = example_geography_query("nat_yorks_yorkslas")
        assert isinstance(result, pd.DataFrame)
    
    def test_invalid_level_raises(self):
        with pytest.raises(ValueError, match="Invalid level"):
            example_geography_query("invalid_level")
    
    def test_default_level_works(self):
        result = example_geography_query()
        assert isinstance(result, pd.DataFrame)
    


class TestExampleIdList:

    def test_has_attendance_group(self):
        assert "attendance" in EXAMPLE_ID_LIST

    def test_has_absence_group(self):
        assert "absence" in EXAMPLE_ID_LIST

    def test_attendance_has_prod(self):
        assert "prod" in EXAMPLE_ID_LIST["attendance"]

    def test_attendance_has_dev(self):
        assert "dev" in EXAMPLE_ID_LIST["attendance"]

    def test_attendance_has_test(self):
        assert "test" in EXAMPLE_ID_LIST["attendance"]

    def test_attendance_prod_has_dataset(self):
        assert "dataset" in EXAMPLE_ID_LIST["attendance"]["prod"]

    def test_attendance_prod_has_indicator(self):
        assert "indicator" in EXAMPLE_ID_LIST["attendance"]["prod"]

    def test_adsence_prod_has_dataset(self):
        assert "dataset" in EXAMPLE_ID_LIST["absence"]["prod"]