import pytest 
from validation_rules import (
    validate_api_version, 
    validate_ees_environment,
    validate_endpoint,
    validate_time_periods,
    validate_ees_id,
    validate_ees_filter_type,
    validate_page_size,
    validate_dataset_version,
    VALID_FILTER_TYPES,
    VALID_ENDPOINTS,
    VALID_ENVIRONMENTS,
)

class TestValidateEesEnvironment:

    def test_prod_valid(self):
        validate_ees_environment("prod")
    
    def test_dev_valid(self):
        validate_ees_environment("dev")
    
    def test_test_valid(self):
        validate_ees_environment("test")
    
    def test_preprod_valid(self):
        validate_ees_environment("preprod")
    
    def test_all_valid_environments(self):
        for env in VALID_ENVIRONMENTS:
            validate_ees_environment(env)
    
    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            validate_ees_environment("staging")
    
    def test_empty_raises(self):
        with pytest.raises(ValueError):
            validate_ees_environment("")
    
    def test_uppercase_raises(self):
        with pytest.raises(ValueError):
            validate_ees_environment("PROD")


class TestValidateApiVersion:

    def test_numeric_string_valid(self):
        validate_api_version("1")
    
    def test_integer_valid(self):
        validate_api_version(1)
    
    def test_float_valid(self):
        validate_api_version(1.0)
    
    def test_version_2_valid(self):
        validate_api_version("2")
    
    def test_letter_raises(self):
        with pytest.raises(ValueError):
            validate_api_version("v1")
        
    def test_underscore_raises(self):
        with pytest.raises(ValueError):
            validate_api_version("1_0")
    
    def test_plus_raises(self):
        with pytest.raises(ValueError):
            validate_api_version("1+2")


class TestValidateEndpoint:

    def test_all_valid_endpoints(self):
        for ep in VALID_ENDPOINTS:
            validate_endpoint(ep)
    
    def test_none_raises(self):
        with pytest.raises(ValueError):
            validate_endpoint(None)
    
    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            validate_endpoint("get-invalid")
    
    def test_empty_raises(self):
        with pytest.raises(ValueError):
            validate_endpoint("")
    
    def test_get_publications_valid(self):
        validate_endpoint("get-publications")
    
    def test_get_data_valid(self):
        validate_endpoint("get-data")
    
    def test_post_data_valid(self):
        validate_endpoint("post-data")
        

class TestValidateTimePeriods:

    def test_valid_academic_year(Self):
        validate_time_periods(["2024|AY"])
    
    def test_valid_week(self):
        validate_time_periods(["2024|W23"])
    
    def test_valid_mutliple(self):
        validate_time_periods(["2024|AY", "2023|AY", "2022|AY"])
    
    def test_valid_financial_year(self):
        validate_time_periods(["2024|FY"])
    
    def test_no_pipe_raises(self):
        with pytest.raises(ValueError):
            validate_time_periods(["2024AY"])
    
    def test_multiple_pipes_raises(self):
        with pytest.raises(ValueError):
            validate_time_periods(["2024|AY|extra"])
    
    def test_mixed_valid_invalid_raises(self):
        with pytest.raises(ValueError):
            validate_time_periods(["2024|AY", "2023AY"])


class TestValidateEesId:

    def test_valid_publication_id(self):
        validate_ees_id("cbbd299f-8297-44bc-92ac-558bcf51f8ad", level="publication")
    
    def test_valid_dataset_id(self):
        validate_ees_id("a0d20bb7-a919-456c-ae44-83815cc8515a", level="dataset")
    
    def test_none_raises(self):
        with pytest.raises(ValueError):
            validate_ees_id(None, level="publications")
    
    def test_invalid_level_raises(self):
        with pytest.raises(ValueError):
            validate_ees_id("abc123", level="invalid_level")
    
    def test_valid_location_with_code(self):
        validate_ees_id("NAT|code|E92000001", level="location")
    
    def test_valid_location_with_id(self):
        validate_ees_id("NAT|id|dP0Zw", level="location")
    
    def test_valid_location_format_raises(self):
        with pytest.raises(ValueError):
            validate_ees_id("NAT|sqid|E92000001", level="location")
    
    def test_valid_indicator_id(self):
        validate_ees_id("abc123", level="indicator")
    
    def test_valid_filter_item_id(self):
        validate_ees_id("xyz456", level="filter_item")


class TestValidateEesFilterType:

    def test_all_valid_types(self):
        for ft in VALID_FILTER_TYPES:
            validate_ees_filter_type(ft)
    
    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            validate_ees_filter_type("bad_type")

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            validate_ees_filter_type("")
    
    def test_time_periods_valid(self):
        validate_ees_filter_type("time_periods")
    
    def test_geographic_levels_valid(self):
        validate_ees_filter_type("geographic_levels")
    
    def test_locations_valid(self):
        validate_ees_filter_type("locations")
    
    def test_filter_items_valid(Self):
        validate_ees_filter_type("filter_items")


class TestValidatePageSize:

    def test_valid_min(self):
        validate_page_size(1)

    def test_valid_max(self):
        validate_page_size(40)
    
    def test_valid_middle(self):
        validate_page_size(20)
    
    def test_none_passes(self):
        validate_page_size(None)
    
    def test_zero_raises(self):
        with pytest.raises(ValueError):
            validate_page_size(0)
    
    def test_negative_raises(self):
        with pytest.raises(ValueError):
            validate_page_size(-1)
    
    def test_over_max_raises(self):
        with pytest.raises(ValueError):
            validate_page_size(41)
    
    def test_bool_raises(self):
        with pytest.raises(ValueError):
            validate_page_size(True)
    
    def test_custom_max(self):
        validate_page_size(100, min_size=1, max_size=100)
    
    def test_custom_max_exceeded_raises(self):
        with pytest.raises(ValueError):
            validate_page_size(101, min_size=1, max_size=100)


class TestValidateDatasetVersion:

    def test_none_passes(self):
        validate_dataset_version(None)
    
    def test_wildcard_valid(self):
        validate_dataset_version("*")
    
    def test_major_minor_patch_valid(self):
        validate_dataset_version("8.2.3")
    
    def test_major_minor_valid(self):
        validate_dataset_version("2.3")
    
    def test_major_only_valid(self):
        validate_dataset_version("2")
    
    def test_wildcard_minor_valid(self):
        validate_dataset_version("2.*")
    
    def test_integer_valid(self):
        validate_dataset_version(1)
    
    def test_float_valid(self):
        validate_dataset_version(1.0)
    
    def test_invalid_string_raises(self):
        with pytest.raises(ValueError):
            validate_dataset_version("v1.0")
    
    def te