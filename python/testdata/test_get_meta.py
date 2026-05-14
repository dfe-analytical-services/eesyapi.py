import pytest
import requests
import pandas as pd
from get_meta import (
    get_meta,
    get_meta_response,
    parse_meta_time_periods,
    parse_meta_filter_columns,
    parse_meta_filter_item_ids,
    parse_meta_location_ids
)


APPRENTICE_FULL_ID = "1d419801-a90e-f970-9335-a13623faccbe"

APPRENTICE_INYR_ID = "1d419801-435d-c676-b428-1217e08290c3"

KS4_ID = "019d4320-2bde-7059-8d7a-b685013eb1e6"

KS2_ID = "019d431f-c129-73e6-917e-6998bfe4d88d"

PHONICS_DIST_ID = "b3bd9901-88ea-8575-aa70-579c2636caf4"

PHONICS_CHAR_ID = "b3bd9901-96b6-1a77-b288-0a6ab2ad1496"

DEV_DATASET = "7c0e9201-c7c0-ff73-bee4-304e731ec0e6"

TEST_DATASET = "7ca99501-d160-2570-b4cd-122834d433f3"


def is_reachable(url):
    try:
        requests.get(url, timeout=5)
        return True
    except Exception:
        return False

skip_dev = pytest.mark.skipif(
    not is_reachable("http://pp-api.education.gov.uk/statistics-dev/v1/publications"),
    reason = "Dev not reachable - connect to DFE VPN"

)

skip_preprod = pytest.mark.skipif(
    not is_reachable("http://pp-api.education.gov.uk/statistics-preprod/v1/publications"),
    reason ="Preprod not reachable - connect to DFE VPN"
)

class TestParseMetaFilterColumns:

    def test_returns_dataframe(self):
        data =[{"id": "1", "column": "absence_type", "label": "Absence type"}]
        result = parse_meta_filter_columns(data)
        assert isinstance(result, pd.DataFrame)
    
    def test_has_col_id_column(self):
        data =[{"id":"1", "column": "absence_type", "label": "Absence type"}]
        result = parse_meta_filter_columns(data)
        assert "col_id" in result.columns
    
    def test_has_col_name_column(self):
        data =[{"id":"1", "column": "absence_type", "label": "Absence type"}]
        result = parse_meta_filter_columns(data)
        assert "col_name" in result.columns
    
    def test_has_label_column(self):
        data =[{"id":"1", "column": "absence_type", "label": "Absence type"}]
        result = parse_meta_filter_columns(data)
        assert "label" in result.columns
    
    def test_empty_input_returns_empty_df(self):
        result = parse_meta_filter_columns([])
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_mutliple_filters(self):
        data = [
            {"id": "1", "column": "absence_type", "label": "Absence type"},
            {"id": "2", "column": "school_type", "label": "School type"}
        ]
        result = parse_meta_filter_columns(data)
        assert len(result) == 2

class TestParseMetaFilteItemIds:

    def test_returns_dataframe(self):
        data = [{
            "id": "f1",
            "column":"absence_type",
            "label":"Absence type",
            "options": [{"id": "opt1", "label": "Authorised", "isAggregate": False}]

        }]
        result = parse_meta_filter_item_ids(data)
        assert isinstance(result, pd.DataFrame)
    
    def test_has_item_id_column(self):
        data = [{
            "id": "f1",
            "column":"absence_type",
            "label":"Absence type",
            "options": [{"id": "opt1", "label": "Authorised", "isAggregate": False}]

        }]
        result = parse_meta_filter_item_ids(data)
        assert "item_id" in result.columns
    
    def test_has_item_label_column(self):
        data = [{
            "id": "f1",
            "column":"absence_type",
            "label":"Absence type",
            "options": [{"id": "opt1", "label": "Authorised", "isAggregate": False}]

        }]
        result = parse_meta_filter_item_ids(data)
        assert "item_label" in result.columns

    def test_empty_returns_empty_df(self):
        result = parse_meta_filter_item_ids([])
        assert isinstance(result, pd.DataFrame)
    
    def test_multiple_options(self):
        data = [{
            "id": "f1",
            "column":"absence_type",
            "label":"Absence type",
            "options": [
                {"id": "opt1", "label": "Authorised", "isAggregate": False},
                {"id": "opt1", "label": "Authorised", "isAggregate": False}]

        }]
        result = parse_meta_filter_item_ids(data)
        assert len(result) == 2
    
    def test_has_is_aggregate_columns(self):
        data = [{
            "id": "f1",
            "column":"absence_type",
            "label":"Absence type",
            "options": [
                {"id": "opt1", "label": "Authorised", "isAggregate": False}]
        
        }]
        result = parse_meta_filter_item_ids(data)
        assert "isAggregate" in result.columns
        

class TestGetMetaResponseProd:

    def test_returns_dict(self):
        result = get_meta_response(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod"
        )
        assert isinstance(result, dict)
    
    def test_has_filters_key(self):
        result = get_meta_response(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod"
        )
        assert "filters" in result

    def test_has_indicators_key(self):
        result = get_meta_response(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod"
        ) 
        assert "indicators" in result

    def test_has_time_periods_key(self):
        result = get_meta_response(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod"
        )    
        assert "timePeriods" in result

    def test_has_locations_key(self):
        result = get_meta_response(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod"
        )   
        assert "locations" in result
    
    def test_apprenticeship_inyr(self):
        result = get_meta_response(
            dataset_id=APPRENTICE_INYR_ID,
            ees_environment="prod"

        )
        assert isinstance(result, dict)
    
    def test_ks4_meta(self):
        result = get_meta_response(
            dataset_id=KS4_ID,
            ees_environment="prod"
        )
        assert isinstance(result, dict)

    def test_phonics_meta(self):
        result = get_meta_response(
            dataset_id=PHONICS_DIST_ID,
            ees_environment="prod"
        )
        assert isinstance(result, dict)

    def test_parse_false_returns_response_object(self):
        result = get_meta_response(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            parse=False
        )
        assert hasattr(result, "status_code")
        assert result.status_code == 200
    
    def test_invalid_dataset_raises(self):
        with pytest.raises(Exception):
            get_meta_response(
                dataset_id="00000000-0000-0000-0000-000000000000",
                ees_environment="prod"
            )
    
    def test_filters_is_list(self):
        result = get_meta_response(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod"
        )
        assert isinstance(result["filters"], list)

    def test_indicators_is_list(self):
        result = get_meta_response(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod"
        )
        assert isinstance(result["indicators"], list)
    
    def test_time_periods_is_list(self):
        result = get_meta_response(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod"
        )
        assert isinstance(result["timePeriods"], list)


class TestGetMetaDev:

    def test_returns_dict(self):
        result = get_meta_response(
            dataset_id=DEV_DATASET,
            ees_environment="dev"
        )
        assert isinstance(result, dict)
    
    def test_has_filters_key(self):
        result = get_meta_response(
            dataset_id=DEV_DATASET,
            ees_environment="dev"
        )
        assert "filters" in result
    
    def test_has_indicators_key(self):
        result = get_meta_response(
            dataset_id=DEV_DATASET,
            ees_environment="dev"
        )
        assert "indicators" in result


class TestGetMetaPreprod:

    def test_returns_dict(self):
        result = get_meta_response(
            dataset_id=TEST_DATASET,
            ees_environment="preprod"
        )
        assert isinstance(result, dict)
    
    def test_has_filters_key(self):
        result = get_meta_response(
            dataset_id=TEST_DATASET,
            ees_environment="preprod"
        )
        assert "filters" in result
    
    def test_has_indicators_key(self):
        result = get_meta_response(
            dataset_id=TEST_DATASET,
            ees_environment="preprod"
        )
        assert "indicators" in result
    