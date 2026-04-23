import pytest 
import requests
from api_url_query import build_query_body, query


APPRENTICE_FULL_ID = "1d419801-a90e-f970-9335-a13623faccbe"

APPRENTICE_INYR_ID = "1d419801-435d-c676-b428-1217e08290c3"

KS4_ID = "019d4320-2bde-7059-8d7a-b685013eb1e6"

KS2_ID = "019d431f-c129-73e6-917e-6998bfe4d88d"

ABSENCE_SESSIONS_ID = "019d209b-b031-7497-8205-af255b581d91"

PERSISTENT_ABS_ID = "019d209c-08dc-74b6-9edb-52d521406fcf"

PHONICS_DIST_ID = "b3bd9901-88ea-8575-aa70-579c2636caf4"

PHONICS_CHAR_ID = "b3bd9901-96b6-1a77-b288-0a6ab2ad1496"

DEV_DATASET = "7c0e9201-c7c0-ff73-bee4-304e731ec0e6"

TEST_DATASET = "7ca99501-d160-2570-b4cd-122834d433f3"



Environments = ["prod","dev","preprod"]


def is_reachable(url):
    try:
        requests.get(url, timeout=5)
        return True
    except Exception:
        return False
skip_dev = pytest.mark.skipif(
    not is_reachable("https://pp-api.education.gov.uk/statistics-dev/v1/publications")
)

skip_preprod = pytest.mark.skipif(
    not is_reachable("https://pp-api.education.gov.uk/statistics-preprod/v1/publications")
)
class TestBuildQueryBody:
    def test_always_has_criteria(self):
        assert "criteria" in build_query_body()

    def test_always_has_indicators(self):
        assert "indicators" in build_query_body()

    def test_always_has_page_in_body(self):
        assert "page" in build_query_body()
    
    def test_always_has_pagesize_in_body(self):
        assert "pageSize" in build_query_body()

    def test_default_page_is_1(self):
        assert build_query_body()["page"] == 1

    def test_default_page_size_is_100(self):
        assert build_query_body()["pageSize"] == 100
    
    def test_custom_page(self):
        assert build_query_body(page=3)["page"] == 3

    def test_custom_page_size(self):
        assert build_query_body(page_size=50)["pageSize"] == 50
    
    def test_empty_criteria_when_no_filters(self):
        assert build_query_body()["criteria"] == {}

    def test_empty_indicators_list(self):
        assert build_query_body()["indicators"] == []    

    def test_indicators_in_body(self):
        body = build_query_body(indicators=["ind1","ind2"])
        assert body["indicators"] == ["ind1","ind2"]

    def test_geographic_levels_in_criteria(self):
        body = build_query_body(geographic_levels=["NAT", "REG"])
        assert body["criteria"]["geographicLevels"] == {"in": ["NAT", "REG"]}

    def test_locations_in_criteria(self):
        body = build_query_body(locations=["E92000001"])
        assert body["criteria"]["locations"] == {"in": ["E92000001"]}
    
    def test_time_periods_parsed(self):
        body = build_query_body(time_periods=["2024|AY"])
        assert body["criteria"]["timePeriods"] == {
            "in": [{"period": "2024","code":"AY"}]
        }

    def test_time_periods_mutliple(self):
        body = build_query_body(time_periods=["2022|AY","2023|AY"])
        periods = body["criteria"]["timePeriods"]["in"]
        assert {"period": "2022", "code": "AY"} in periods
        assert {"period": "2023", "code":"AY"} in periods

    def test_filters_in_criteria(self):
        filters = [{"field": "absence_type", "values":["abc123"]}]
        body = build_query_body(filters=filters)
        assert "filters" in body["criteria"]
        assert "abc123" in body["criteria"]["filters"]["in"]

    def test_none_params_not_in_criteria(self):
        body = build_query_body(time_periods=None)
        assert "timePeriods" not in body["criteria"]

    def test_empty_list_not_in_criteria(self):
        body = build_query_body(geographic_levels=[])
        assert "geographicLevels" not in body["criteria"]

    def test_all_params_combined(self):
        body = build_query_body(
            indicators=["ind1"],
            time_periods=["2024|AY"],
            geographic_levels=["NAT"],
            locations=["E92000001"],
            filters=[{"field": "type","values": ["abc"]}],
            page=2,
            page_size=50
        )
        assert body["page"] == 2
        assert body["pageSize"] == 50
        assert body["indicators"] == ["ind1"]
        assert "timePeriods" in body["criteria"]
        assert "geographicLevels" in body["criteria"]
        assert "locations" in body["criteria"]
        assert "filters" in body["criteria"]

    def test_return_dict(self):
        assert isinstance(build_query_body(), dict)


class TestQueryValidation:
    def test_empty_dataset_id_raises(self):
        with pytest.raises(ValueError, match="dataset_id must be provided"):
            query(dataset_id="")
    
    def test_none_dataset_id_raises(self):
        with pytest.raises(ValueError, match="dataset_id must be provided"):
            query(dataset_id=None)
    
    def test_zero_page_size_raises(self):
        with pytest.raises(ValueError, match="page_size must be greater than 0"):
            query(dataset_id=APPRENTICE_FULL_ID, page_size=0)
    
    def test_negative_page_size_raises(self):
        with pytest.raises(ValueError, match="page_size must be greater than 0"):
            query(dataset_id=APPRENTICE_FULL_ID,page_size=-10)

class TestQueryProd:
    def test_apprenticeships_full_returns_list(self):
        results = query(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=5,
            paginate=False)
        assert isinstance(results, list)

    def test_apprenticeships_full_returns_results(self):
        results = query(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=5,
            paginate=False)
        assert len(results) > 0

    def test_apprenticeships_inyr(self):
        results = query(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=3,
            paginate=False
        )
        assert isinstance(results, list)
        assert len(results) > 0

    def test_ks4_dataset(self):
        results = query(
            dataset_id=KS4_ID,
            ees_environment="prod",
            page_size=5,
            paginate=False
        )   
        assert isinstance(results, list)

    def test_ks2_dataset(self):
        results = query(
            dataset_id=KS2_ID,
            ees_environment="prod",
            page_size=5,
            paginate=False
        )
        assert isinstance(results, list)


    def test_absence_sessions(self):
        results = query(
            dataset_id=ABSENCE_SESSIONS_ID,
            ees_environment="prod",
            page_size=5,
            paginate=False
        )
        assert isinstance(results, list)
        assert len(results) > 0

    def test_persistent_absence(self):
        results = query(
            dataset_id = PERSISTENT_ABS_ID,
            ees_environment="prod",
            page_size=5,
            paginate=False)
        assert isinstance(results, list)

    def test_phonics_distribution(self):
        results = query(
            dataset_id=PHONICS_DIST_ID,
            ees_environment="prod",
            geographic_levels=["NAT"],
            page_size=5,
            paginate=False
        )
        assert isinstance(results, list)

    def test_phonics_characteristics(self):
        results = query(
            dataset_id=PHONICS_CHAR_ID,
            ees_environment="prod",
            page_size=5,
            paginate=False
        )
        assert isinstance(results, list)

    def test_results_are_dicts(self):
        results = query(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=3,
            paginate=False)
        for row in results:
              assert isinstance(row, dict)
    
    def test_page_size_respected(self):
        results = query(
             dataset_id=APPRENTICE_FULL_ID,
             ees_environment="prod",
             page_size=3,
             paginate=False)
        assert len(results) <= 3

    def test_with_national_geo_level(self):
        results = query(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            geographic_levels=["NAT"],
            page_size=5,
            paginate=False
            )
        assert isinstance(results, list)

    def test_with_time_period(self):
        results = query(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            time_periods=["2024|AY"],
            page_size=5,
            paginate=False
        )
        assert isinstance(results, list)
    
    def test_paginate_false_stops_at_one_page(self):
        results = query(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=5,
            paginate=False
        )
        assert len(results) <= 5
    
    def test_pagination_with_max_pages(self):
        page1 = query(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=3,
            paginate=False
        )

        both_pages = query(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=3,
            paginate=True,
            max_pages=2
        )
        assert len(both_pages) >= len(page1)
    
    def test_invalid_dataset_raises(self):
        with pytest.raises(Exception):
            query(
                dataset_id="00000000-0000-0000-000000000000",
                ees_environment="prod",
                paginate=False
            )
    
    def test_verbose_prints_output(self, capsys):
        query(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=3,
            paginate=False,
            verbose=True
        )
        captured = capsys.readouterr()
        assert "QUERY" in captured.out or "POST" in captured.out
 

class TestQuerDev:

    def test_returns_list(self):
        results = query(
            dataset_id=DEV_DATASET,
            ees_environment="dev",
            page_size=5,
            paginate=False
        )
        assert isinstance(results, list)
    
    def test_returns_results(self):
        results = query(
            dataset_id=DEV_DATASET,
            ees_environment="dev",
            page_size=5,
            paginate=False
        )
        assert len(results) > 0
    
    def test_page_size_respected(self):
        results = query(
            dataset_id=DEV_DATASET,
            ees_environment="dev",
            page_size=3,
            paginate=False
        )
        assert len(results) <= 3

    def test_with_national_geo_level(self):
        results = query(
            dataset_id=DEV_DATASET,
            ees_environment="dev",
            geographic_levels=["NAT"],
            page_size=5,
            paginate=False
        )
        assert isinstance(results, list)

    def test_invalid_dataset_raises(self):
         with pytest.raises(Exception):
             query(
                 dataset_id="00000000-0000-0000-000000000000",
                 ees_environment="dev",
                 paginate=False
              )
       

class TestQueryPreprod:

    def test_returns_list(self):
        results = query(
            dataset_id=TEST_DATASET,
            ees_environment="preprod",
            page_size=5,
            paginate=False
        )
        assert isinstance(results, list)

    def test_returns_results(self):
        results = query(
            dataset_id=TEST_DATASET,
            ees_environment="preprod",
            page_size=5,
            paginate=False
        )
        assert len(results) > 0
    
    def test_page_size_respected(self):
        results = query(
            dataset_id=TEST_DATASET,
            ees_environment="preprod",
            page_size=3,
            paginate=False
        )
        assert len(results) <= 3

    def test_invalid_dataset_raises(self):
        with pytest.raises(Exception):
            query(
                dataset_id="00000000-0000-0000-000000000000",
                ees_environment="preprod",
                paginate=False
            )

 
