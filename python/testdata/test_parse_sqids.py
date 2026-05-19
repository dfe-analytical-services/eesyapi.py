import pytest 
import warnings
import pandas as pd 
from parse_sqids import (
    parse_time_codes,
    parse_geographic_level_codes,
    parse_sqids_locations,
    parse_sqids_filters,
    parse_sqids_indicators,
    GEOG_LEVEL_LOOKUP,
)

class TestParseTimeCodes:

    def test_returns_dataframe(self):
        df = pd.DataFrame({"code": ["AY"], "period": ["2024"]})
        result = parse_time_codes(df)
        assert isinstance(result, pd.DataFrame)
    
    def test_has_time_period_column(self):
        df = pd.DataFrame({"code": ["AY"], "period": ["2024"]})
        result = parse_time_codes(df)
        assert "time_period" in result.columns
    
    def test_has_time_identifier_column(self):
        df = pd.DataFrame({"code": ["AY"], "period": ["2024"]})
        result = parse_time_codes(df)
        assert "time_identifier" in result.columns

    def test_academic_year_converted(self):
        df = pd.DataFrame({"code": ["AY"], "period": ["2024"]})
        result = parse_time_codes(df)
        assert result["time_identifier"].iloc[0] == "Academic year"
    
    def test_financial_year_converted(self):
        df = pd.DataFrame({"code": ["FY"], "period": ["2024"]})
        result = parse_time_codes(df)
        assert result["time_identifier"].iloc[0] == "Financial year"

    def test_calender_year_converted(self):
        df = pd.DataFrame({"code": ["CY"], "period": ["2024"]})
        result = parse_time_codes(df)
        assert result["time_identifier"].iloc[0] == "Calendar year"
    
    def test_week_code_converted(self):
        df = pd.DataFrame({"code": ["W1"], "period": ["2024"]})
        result = parse_time_codes(df)
        assert result["time_identifier"].iloc[0] == "Week1"

    def test_week_12_converted(self):
        df = pd.DataFrame({"code": ["W12"], "period": ["2024"]})
        result = parse_time_codes(df)
        assert result["time_identifier"].iloc[0] == "Week12"
    
    def test_non_dataframe_raises(self):
        with pytest.raises(ValueError):
            parse_time_codes([{"code": "AY", "period": "2024"}])

    def test_mutliple_rows(self):
        df = pd.DataFrame({
            "code": ["AY", "FY", "W1"],
            "period": ["2024", "2024", "2024"]
        })
        result = parse_time_codes(df)
        assert len(result) == 3

class TestParseGeographicLevelCodes:

    def test_returns_dataframe(self):
        result = parse_geographic_level_codes(pd.Series(["NAT"]))
        assert isinstance(result, pd.DataFrame)
    
    def test_has_geographic_level_column(self):
        result = parse_geographic_level_codes(pd.Series(["NAT"]))
        assert "geographic_level" in result.columns
    
    def test_nat_converted(self):
        result = parse_geographic_level_codes(pd.Series(["NAT"]))
        assert result["geographic_level"].iloc[0] == "National"
    
    def test_reg_converted(self):
        result = parse_geographic_level_codes(pd.Series(["REG"]))
        assert result["geographic_level"].iloc[0] == "Regional"
    
    def test_la_converted(self):
        result = parse_geographic_level_codes(pd.Series(["LA"]))
        assert result["geographic_level"].iloc[0] == "Local authority"
    
    def test_mutliple_levels(self):
        result = parse_geographic_level_codes(pd.Series(["NAT", "REG", "LA"]))
        assert len(result) == 3
    
    def test_unknown_level_warns(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            parse_geographic_level_codes(pd.Series(["UNKNOWN"]))
            assert len(w) == 1
    
    def test_dataframe_raises(self):
        with pytest.raises(ValueError):
            parse_geographic_level_codes(pd.DataFrame({"level": ["NAT"]}))

    def test_all_known_levels(self):
        levels = list(GEOG_LEVEL_LOOKUP.keys())
        result = parse_geographic_level_codes(pd.Series(levels))
        assert len(result) == len(levels)

class TestParseSqidaLocations:

    def make_meta(self):
        return {
            "locations": pd.DataFrame({
                "geographic_levels_code": ["NAT"],
                "geographic_level": ["National"],
                "item_id": ["abc123"],
                "label": ["England"]
            })
        }
    
    def test_returns_dataframe(self):
        locations = pd.DataFrame({"NAT": ["abc123"]})
        result = parse_sqids_locations(locations, self.make_meta())
        assert isinstance(result, pd.DataFrame)
    
    def test_empty_locations_returns_dataframe(self):
        locations = pd.DataFrame()
        result = parse_sqids_locations(locations, {})
        assert isinstance(result, pd.DataFrame)

class TestParseSqidsFilters:

    def make_meta(self):
        return {
            "filter_columns": pd.DataFrame({
                "col_id": ["f1"],
                "col_name": ["absence_type"],
                "label": ["Absence type"]
            }),
            "filter_items" : pd.DataFrame({
                "col_id" : ["f1"],
                "col_name": ["absence_type"],
                "label": ["Absence type"],
                "item_id": ["opt1"],
                "item_label": ["Authorised"]
            })
        }
    
    def test_returns_dataframe(self):
        filters = pd.DataFrame({"f1": ["opt1"]})
        result = parse_sqids_filters(filters, self.make_meta())
        assert isinstance(result, pd.DataFrame)
    
    def test_empty_filters_returns_dataframe(self):
        filters = pd.DataFrame()
        result = parse_sqids_filters(filters, {})
        assert isinstance(result, pd.DataFrame)

class TestParseSqidsIndicators:

    def make_meta(self):
        return {
            "indicators": pd.DataFrame({
                "col_id": ["ind1", "ind2"],
                "col_name": ["sess_possible", "sess_authorised"],
                "label" : ["Sessions possible", "Authorised sessions"]
            })
        }

    def test_return_dataframe(self):
        indicators = pd.DataFrame({"ind1": [100], "ind2": [50]})
        result = parse_sqids_indicators(indicators, self.make_meta())
        assert isinstance(result, pd.DataFrame)
    
    def test_columns_renamed(self):
        indicators = pd.DataFrame({"ind1": [100]})
        result = parse_sqids_indicators(indicators, self.make_meta())
        assert "sess_possible" in result.columns
    
    def test_unknown_indicators_kept_as_is(Self):
        indicators = pd.DataFrame({"Unknown_id": [100]})
        result = parse_sqids_indicators(indicators, Self.make_meta())
        assert "Unknown_id" in result.columns

    def test_empty_meta_returns_copy(self):
        indicators = pd.DataFrame({"ind1": [100]})
        result = parse_sqids_indicators(indicators, {})
        assert isinstance(result, pd.DataFrame)
        assert "ind1" in result.columns
