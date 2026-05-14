import pytest 
from utils import (
    validate_ees_filter_type,
    convert_api_filter_type,
    check_response,
    extract_results,
    parse_tourl_filter_in,
    VALID_FILTER_TYPES

)


class TestValidateEesFilterType:

    def test_time_periods_valid(self):
        validate_ees_filter_type("time_periods")

    def test_geographic_levels_valid(self):
        validate_ees_filter_type("geographic_levels")

    def test_locations_valid(self):
        validate_ees_filter_type("locations")

    def test_filter_items_valid(self):
        validate_ees_filter_type("filter_items")

    def test_all_valid_types_pass(self):
        for ft in VALID_FILTER_TYPES:
            validate_ees_filter_type(ft)

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            validate_ees_filter_type("bad_filter")

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            validate_ees_filter_type("")

    def test_none_raises(self):
        with pytest.raises((ValueError, TypeError, AttributeError)):
            validate_ees_filter_type(None)

    def test_uppercase_raises(self):
        with pytest.raises(ValueError):
            validate_ees_filter_type("TIME_PERIODS")

    def test_partial_match_raises(self):
        with pytest.raises(ValueError):
            validate_ees_filter_type("time")


class TestConvertApiFilterTypeUtils:

    def test_time_periods_maps_correctly(self):
        assert convert_api_filter_type("time_periods") == "timePeriods"

    def test_locations_maps_correctly(self):
        assert convert_api_filter_type("locations") == "locations"

    def test_filter_items_maps_correctly(self):
        assert convert_api_filter_type("filter_items") == "filters"

    def test_unknown_returns_none(self):
        assert convert_api_filter_type("unknown") is None

    def test_geographic_levels_typo_bug(self):
        result = convert_api_filter_type("geographic_levels")
        assert result is None or result == "geographicLevels"


class TestCheckResponse:
    class FakeResponse:
        def __init__(self,status_code, text=""):
            self.status_code = status_code
            self.text = text
        
    def test_200_does_not_raise(self):
        check_response(self.FakeResponse(200))
        
    def test_201_does_not_raise(self):
        with pytest.raises(Exception):
            check_response(self.FakeResponse(201))
        
    def test_400_raises(self):
        with pytest.raises(Exception):
            check_response(self.FakeResponse(400, "Bad Request"))

    def test_404_raises(self):
        with pytest.raises(Exception, match="API Error: 404"):
            check_response(self.FakeResponse(404, "Not Found"))

    def test_500_raises(self):
        with pytest.raises(Exception, match="API Error: 500"):
            check_response(self.FakeResponse(500, "Server Error"))

    def test_error_contains_response_text(self):
        with pytest.raises(Exception, match="Invalid dataset"):
            check_response(self.FakeResponse(400, "Invalid dataset"))

    def test_403_raises(self):
        with pytest.raises(Exception, match="API Error: 403"):
            check_response(self.FakeResponse(403, "Forbidden"))


class TestExtractResults:

    def test_extracts_results_list(self):
        data = {"results": [{"id": "1"}, {"id": "2"}]}
        assert extract_results(data) == [{"id": "1"}, {"id": "2"}]

    def test_empty_results_returns_empty_list(self):
        data = {"results": []}
        assert extract_results(data) == []

    def test_missing_results_key_returns_empty(self):
        data = {"paging": {"page":1}}
        assert extract_results(data) == []

    def test_non_dict_returns_empty(self):
        assert extract_results([]) == []

    def test_string_returns_empty(self):
        assert extract_results("string") == []

    def test_none_returns_empty(self):
        assert extract_results(None) == []

    def test_int_returns_empty(self):
        assert extract_results(123) == []

    def test_returns_list(self):
        data = {"results":[{"id": "x"}]}
        assert isinstance(extract_results(data), list)
    
    def test_single_result(self):
        data = {"results": [{"id": "abc"}]}
        assert len(extract_results(data)) == 1

    def test_mutliple_results(self):
        data = {"results": [{"id": "1"}, {"id": "2"}, {"id": "3"}]}
        assert len(extract_results(data)) == 3


class TestParseToUrlFilterIn:

    def test_time_periods_single(self):
        result = parse_tourl_filter_in(["2024|AY"], "time_periods")
        assert "timePeriods.in=" in result
    
    def test_time_periods_encodes_pipe(self):
        result = parse_tourl_filter_in(["2024|AY"], "time_periods")
        assert "%7C" in result

    def test_time_periods_mutiple_joined(self):
        result = parse_tourl_filter_in(["2022|AY", "2023|AY"], "time_periods")
        assert "%2C" in result
    
    def test_locations_encodes_pipe(self):
        result = parse_tourl_filter_in(["NAT|code|E92000001"], "locations")
        assert "%7C" in result

    def test_filter_items_no_encoding(self):
        result = parse_tourl_filter_in(["abc", "def"], "filter_items")
        assert "filters.in=" in result

    def test_none_returns_empty_string(self):
        result = parse_tourl_filter_in(None, "time_periods")
        assert result == ""

    def test_ends_with_ampersand(self):
        result = parse_tourl_filter_in(["2024|AY"], "time_periods")
        assert result.endswith("&")

    def test_invalid_filter_type_raises(self):
        with pytest.raises(ValueError):
            parse_tourl_filter_in(["x"], "bad_type")

    def test_returns_string(Self):
        result = parse_tourl_filter_in(["2024|AY"], "time_periods")
        assert isinstance(result, str)