import pytest 
from api_url_query import build_query_body, query

Absence_session_id = "a0d20bb7-a919-456c-ae44-83815cc8515a"
Persistent_abs_id = "46d7be7f-0bf1-4092-a019-97164cba00d1"
Apprentice_inyr_id = "12192cf4-98d5-4479-abb5-b18e3961b601"
Apprentice_full_id = "26f76d9a-8700-4776-bbf6-9a1c963e607b"
Alevel_nat_id = "09c2dace-cd2f-4638-8098-7ca60eb1d228"
Alevel_mat_perf_id = "08d4edb3-828b-4cf6-ad1c-beee263b64f5"

Environments = ["prod","dev","preprod"]

class TestBuildQueryBody:
    def test_always_has_criteria(self):
        body = build_query_body()
        assert "criteria" in body

    def test_always_has_indicators(self):
        body = build_query_body()
        assert "indicators" in body

    def test_always_has_page(self):
        body = build_query_body()
        assert "page" in body

    def test_always_has_page_size(self):
        body = build_query_body()
        assert "pageSize" in body

    def test_default_page_is_1(self):
        body = build_query_body()
        assert body["page"] == 1

    def test_default_page_size_is_100(self):
        body = build_query_body()
        assert body["pageSize"] == 100

    def test_custom_page(self):
        body = build_query_body(page=3)
        assert body["page"] == 3

    def test_custom_page_size(self):
        body = build_query_body(page_size=50)
        assert body["pageSize"] == 50
  
    def test_empty_criteria_when_no_filters(self):
        body = build_query_body()
        assert body["criteria"] == {}

    def test_empty_indicators_list(self):
        body = build_query_body()
        assert body["indicators"] == []

    def test_indicators_in_body(self):
        body = build_query_body(indicators=["ind1","ind2"])
        assert body["indicators"] == ["ind1","ind2"]

    def test_geographic_levels_in_criteria(self):
        body = build_query_body(geographic_levels=["National", "Regional"])
        assert body["criteria"]["geographicLevels"] == {"in": ["National", "Regional"]}

    def test_locations_in_criteria(self):
        body = build_query_body(locations=["E92000001"])
        assert body["criteria"]["locations"] == {"in": ["E92000001"]}
    
    def test_time_periods_in_criteria(self):
        body = build_query_body(time_periods=["2024|AY"])
        assert "timePeriods" in body["criteria"]
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
            geographic_levels=["National"],
            locations=["E92000001"],
            filters=[{"field": "type","values": ["abc"]}],
            page=2,
            page_size=50
        )

        assert body["indicators"] == ["ind1"]
        assert body["page"] == 2
        assert body["pageSize"] == 50
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
            query(dataset_id=Absence_session_id, page_size=0)
    
    def test_negative_page_size_raises(self):
        with pytest.raises(ValueError, match="page_size must be greater than 0"):
            query(dataset_id=Absence_session_id,page_size=10)

class TestQueryProd:
    def test_returns_list(self):
        results = query(
            dataset_id=Alevel_mat_perf_id,
            ees_environment="prod",
            page_size=5,
            paginate=False,)
        assert isinstance(results, list)

    def test_returns_results(self):
        results = query(
            dataset_id=Alevel_mat_perf_id,
            ees_environment="prod",
            page_size=5,
            paginate=False)
        assert len(results) > 0

    def test_results_are_dicts(self):
        results = query(
            dataset_id=Alevel_mat_perf_id,
            ees_environment="prod",
            page_size=3,
            paginate=False
        )

        for row in results:
            assert isinstance(row, dict)

    def test_page_size_respected(self):
        results = query(
            dataset_id=Alevel_mat_perf_id,
            ees_environment="prod",
            page_size=3,
            paginate=False
        )

        assert len(results) <= 3
    
    def test_absence_sessions_national(self):
        results = query(
            dataset_id=Absence_session_id,
            ees_environment="prod",
            geographic_levels=["National"],
            time_periods=["2024|AY"],
            page_size=5,
            paginate=False
        )

        assert isinstance(results, list)
        assert len(results) <= 5

    def test_persistent_absence_national(self):
        results = query(
            dataset_id=Persistent_abs_id,
            ees_environment="prod",
            geographic_levels=["National"],
            page_size=5,
            paginate=False
        )
        assert len(results) > 0
    
    def test_apprenticeships_inyr_national(self):
        results = query(
            dataset_id=Apprentice_inyr_id,
            ees_environment="prod",
            geographic_levels=["National"],
            page_size=5,
            paginate=False
        )

        assert isinstance(results, list)
    
    def test_apprenticeships_full_national(self):
        results = query(
            dataset_id= Apprentice_full_id,
            ees_environment="prod",
            geographic_levels=["National"],
            page_size=5,
            paginate=False
        )
        assert isinstance(results, list)
    
    def test_alevel_national_performance(self):
        results = query(
            dataset_id=Alevel_nat_id,
            ees_environment="prod",
            geographic_levels=["National"],
            page_size=5,
            paginate=False
        )
        assert len(results) > 0
    
    def test_pagination_fetches_more(self):
        single_page = query(
            dataset_id = Alevel_mat_perf_id,
            ees_environment="prod",
            page_size=3,
            paginate=False
        )
        all_pages = query(
            dataset_id=Alevel_mat_perf_id,
            ees_environment="prod",
            page_size=3,
            paginate=True

        )
        assert len(all_pages) >= len(single_page)
    
    def test_pagination_false_stops_at_one_page(self):
        results = query(
            dataset_id=Alevel_mat_perf_id,
            ees_environment="prod",
            page_size=5,
            paginate=False
        )

        assert len(results) <= 5
    
    def test_invalid_dataset_raises(self):
        with pytest.raises(Exception):
            query(
                dataset_id="00000000-0000-0000-0000-000000000000",
                ees_environment="prod",
                paginate=False)

    def test_verbose_prints_output(self, capsys):
        query(
            dataset_id=Alevel_mat_perf_id,
            ees_environment="prod",
            page_size=3, 
            paginate=False,
            verbose=True
        )

        captured = capsys.readouterr()
        assert "QUERY" in captured.out or "POST" in captured.out
    
    def test_with_time_periods(self):
        results = query(
            dataset_id=Absence_session_id,
            ees_environment="prod",
            time_periods=["2023|AY", "2024|AY"],
            page_size=5,
            paginate=False
        )

        assert isinstance(results, list)


