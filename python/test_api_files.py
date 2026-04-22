import pytest
from unittest.mock import Mock, patch

from api_url_query import build_query_body, query


class TestBuildQueryBody:

    def test_empty_body(self):
        body = build_query_body()
        assert body == {}

    def test_indicators_only(self):
        body = build_query_body(indicators=["authorised", "unauthorised"])
        assert body == {
            "indicators": ["authorised", "unauthorised"]
        }

    def test_time_periods_only(self):
        body = build_query_body(time_periods=["2024|AY", "2025|AY"])
        assert body == {
            "timePeriods": ["2024|AY", "2025|AY"]
        }

    def test_geographic_levels_only(self):
        body = build_query_body(geographic_levels=["National", "Regional"])
        assert body == {
            "geographicLevels": ["National", "Regional"]
        }

    def test_locations_only(self):
        body = build_query_body(locations=["E92000001", "E12000001"])
        assert body == {
            "locations": ["E92000001", "E12000001"]
        }

    def test_filters_only(self):
        filters = [
            {"field": "attendance_status", "values": ["Authorised absence"]}
        ]
        body = build_query_body(filters=filters)
        assert body == {
            "filters": filters
        }

    def test_full_body(self):
        filters = [
            {"field": "attendance_status", "values": ["Authorised absence"]},
            {"field": "education_phase", "values": ["Primary", "Secondary"]},
        ]

        body = build_query_body(
            indicators=["sessions"],
            time_periods=["2024|AY"],
            geographic_levels=["National"],
            locations=["E92000001"],
            filters=filters,
        )

        assert body == {
            "indicators": ["sessions"],
            "timePeriods": ["2024|AY"],
            "geographicLevels": ["National"],
            "locations": ["E92000001"],
            "filters": filters,
        }


class TestQuery:

    def test_missing_dataset_id_raises(self):
        with pytest.raises(ValueError, match="dataset_id must be provided"):
            query(dataset_id="")

    def test_page_size_zero_raises(self):
        with pytest.raises(ValueError, match="page_size must be greater than 0"):
            query(dataset_id="abc123", page_size=0)

    def test_page_size_negative_raises(self):
        with pytest.raises(ValueError, match="page_size must be greater than 0"):
            query(dataset_id="abc123", page_size=-5)

    @patch("api_url_query.convert_api_filter_type")
    @patch("api_url_query.extract_results")
    @patch("api_url_query.check_response")
    @patch("api_url_query.requests.post")
    @patch("api_url_query.api_url")
    def test_single_page_no_paginate(
        self,
        mock_api_url,
        mock_post,
        mock_check_response,
        mock_extract_results,
        mock_convert_filters,
    ):
        dataset_id = "test-dataset-id"
        converted_filters = [{"field": "phase", "values": ["Primary"]}]
        results = [{"row": 1}, {"row": 2}]

        mock_convert_filters.return_value = converted_filters
        mock_api_url.return_value = "https://fake-api/query?page=1&pageSize=100"

        mock_response = Mock()
        mock_response.json.return_value = {
            "results": results,
            "totalResults": 2
        }
        mock_post.return_value = mock_response
        mock_extract_results.return_value = results

        output = query(
            dataset_id=dataset_id,
            filters={"phase": "Primary"},
            paginate=False
        )

        assert output == results
        mock_convert_filters.assert_called_once_with({"phase": "Primary"})
        mock_api_url.assert_called_once_with(
            endpoint="get-data",
            dataset_id=dataset_id,
            dataset_version=None,
            ees_environment="prod",
            api_version="1",
            page=1,
            page_size=100,
        )
        mock_post.assert_called_once_with(
            "https://fake-api/query?page=1&pageSize=100",
            json={
                "filters": converted_filters
            },
        )
        mock_check_response.assert_called_once_with(mock_response)

    @patch("api_url_query.convert_api_filter_type")
    @patch("api_url_query.extract_results")
    @patch("api_url_query.check_response")
    @patch("api_url_query.requests.post")
    @patch("api_url_query.api_url")
    def test_multiple_pages_paginate_true(
        self,
        mock_api_url,
        mock_post,
        mock_check_response,
        mock_extract_results,
        mock_convert_filters,
    ):
        dataset_id = "test-dataset-id"

        mock_convert_filters.return_value = []

        mock_api_url.side_effect = [
            "https://fake-api/query?page=1&pageSize=2",
            "https://fake-api/query?page=2&pageSize=2",
        ]

        response_page_1 = Mock()
        response_page_1.json.return_value = {
            "results": [{"row": 1}, {"row": 2}],
            "totalResults": 4
        }

        response_page_2 = Mock()
        response_page_2.json.return_value = {
            "results": [{"row": 3}, {"row": 4}],
            "totalResults": 4
        }

        mock_post.side_effect = [response_page_1, response_page_2]
        mock_extract_results.side_effect = [
            [{"row": 1}, {"row": 2}],
            [{"row": 3}, {"row": 4}],
        ]

        output = query(
            dataset_id=dataset_id,
            page_size=2,
            paginate=True
        )

        assert output == [
            {"row": 1}, {"row": 2}, {"row": 3}, {"row": 4}
        ]

        assert mock_post.call_count == 2
        assert mock_check_response.call_count == 2
        assert mock_extract_results.call_count == 2

    @patch("api_url_query.convert_api_filter_type")
    @patch("api_url_query.extract_results")
    @patch("api_url_query.check_response")
    @patch("api_url_query.requests.post")
    @patch("api_url_query.api_url")
    def test_stops_when_no_results(
        self,
        mock_api_url,
        mock_post,
        mock_check_response,
        mock_extract_results,
        mock_convert_filters,
    ):
        dataset_id = "test-dataset-id"

        mock_convert_filters.return_value = []
        mock_api_url.return_value = "https://fake-api/query?page=1&pageSize=100"

        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [],
            "totalResults": 0
        }
        mock_post.return_value = mock_response
        mock_extract_results.return_value = []

        output = query(dataset_id=dataset_id)

        assert output == []
        mock_post.assert_called_once()

    @patch("api_url_query.convert_api_filter_type")
    @patch("api_url_query.requests.post")
    @patch("api_url_query.api_url")
    def test_query_passes_full_body_to_post(
        self,
        mock_api_url,
        mock_post,
        mock_convert_filters,
    ):
        dataset_id = "test-dataset-id"
        converted_filters = [
            {"field": "attendance_status", "values": ["Authorised absence"]}
        ]

        mock_convert_filters.return_value = converted_filters
        mock_api_url.return_value = "https://fake-api/query?page=1&pageSize=50"

        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [{"row": 1}],
            "totalResults": 1
        }
        mock_post.return_value = mock_response

        with patch("api_url_query.check_response") as mock_check_response, \
             patch("api_url_query.extract_results") as mock_extract_results:

            mock_extract_results.return_value = [{"row": 1}]

            output = query(
                dataset_id=dataset_id,
                indicators=["sessions"],
                time_periods=["2024|AY"],
                geographic_levels=["National"],
                locations=["E92000001"],
                filters={"attendance_status": "Authorised absence"},
                page_size=50,
                paginate=False,
            )

            assert output == [{"row": 1}]

            mock_post.assert_called_once_with(
                "https://fake-api/query?page=1&pageSize=50",
                json={
                    "indicators": ["sessions"],
                    "timePeriods": ["2024|AY"],
                    "geographicLevels": ["National"],
                    "locations": ["E92000001"],
                    "filters": converted_filters,
                },
            )
            mock_check_response.assert_called_once()

    @patch("api_url_query.convert_api_filter_type")
    @patch("api_url_query.check_response")
    @patch("api_url_query.requests.post")
    @patch("api_url_query.api_url")
    def test_query_propagates_check_response_exception(
        self,
        mock_api_url,
        mock_post,
        mock_check_response,
        mock_convert_filters,
    ):
        mock_convert_filters.return_value = []
        mock_api_url.return_value = "https://fake-api/query?page=1&pageSize=100"

        mock_response = Mock()
        mock_post.return_value = mock_response

        mock_check_response.side_effect = Exception("API Error: 500")

        with pytest.raises(Exception, match="API Error: 500"):
            query(dataset_id="test-dataset-id")

    @patch("api_url_query.convert_api_filter_type")
    @patch("api_url_query.extract_results")
    @patch("api_url_query.check_response")
    @patch("api_url_query.requests.post")
    @patch("api_url_query.api_url")
    def test_dataset_version_is_passed_to_api_url(
        self,
        mock_api_url,
        mock_post,
        mock_check_response,
        mock_extract_results,
        mock_convert_filters,
    ):
        mock_convert_filters.return_value = []
        mock_api_url.return_value = "https://fake-api/query?page=1&pageSize=100&dataSetVersion=2.0"

        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [{"row": 1}],
            "totalResults": 1
        }
        mock_post.return_value = mock_response
        mock_extract_results.return_value = [{"row": 1}]

        output = query(
            dataset_id="test-dataset-id",
            dataset_version="2.0",
            paginate=False
        )

        assert output == [{"row": 1}]
        mock_api_url.assert_called_once_with(
            endpoint="get-data",
            dataset_id="test-dataset-id",
            dataset_version="2.0",
            ees_environment="prod",
            api_version="1",
            page=1,
            page_size=100,
        )