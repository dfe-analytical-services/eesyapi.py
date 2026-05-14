import pytest

"""
api_url.py

Url builder for Explore     Education Statistics (EES) API 

"""

from urllib.parse import urlparse, parse_qs
from api_url import api_url


ABSENCE_SESSIONS_DATASET_ID = "a0d20bb7-a919-456c-ae44-83815cc8515a"

PERSISENT_ABSENTEES_DATASET_ID = "46d7be7f-0bf1-4092-a019-97164cba00d1"

APPRENTICESHIPS_INYR_DATASET_ID = "12192cf4-98d5-4479-abb5-b18e3961b601"

APPRENTICESHIPS_FULL_DATASET_ID = "26f76d9a-8700-4776-bbf6-9a1c963e607b"

ALEVEL_PERF_DATASET_ID = "eb2322e3-5976-42f2-ae83-900f26e92bd9"

ALEVEL_INST_DATASET_ID = "4e6da9be-0c0f-46a5-b9f8-fc09c6cad8fb"

ALEVEL_NAT_PERF_DATASET_ID = "09c2dace-cd2f-4638-8098-7ca60eb1d228"

ALEVEL_SUBJ_DATASET_ID = "9a275c77-4325-4ac8-aa9e-b1a2bd3ab63b"

PUPIL_ABSENCE_PUBLICATION_ID = "8b7474f9-5870-4ecc-7557-08da5f64dcf1"


def parse_url(url: str):
    "return (base_without_query, query_dict) for easy assertions."
    parsed = urlparse(url)
    base = parsed.scheme + "://" + parsed.netloc + parsed.path
    params = parse_qs(parsed.query)
    return base, params


class TestGetPublications:
    
    def test_default_url(self):
         url = api_url()
         assert url == "https://api.education.gov.uk/statistics/v1/publications"

    def test_with_search(self):
         url = api_url(search="absence")
         base, params = parse_url(url)
         assert base.endswith("/publications")
         assert params["search"] == ["absence"]

    def test_with_pagination(self):
         url = api_url(page=2, page_size=5)
         _, params = parse_url(url)
         assert params["page"] == ["2"]
         assert params["pageSize"] == ["5"]
    
    def test_dev_environment(self):
        url = api_url(ees_environment="dev")

        base, _ = parse_url(url)
        assert base == "https://pp-api.education.gov.uk/statistics-dev/v1/publications"

    def test_preprod_environment(self):
        url = api_url(ees_environment="preprod")
        base, _ = parse_url(url)
        assert base == "https://pp-api.education.gov.uk/statistics-preprod/v1/publications"
    
    def test_test_environment(self):
          url = api_url(ees_environment="test")
          base, _ = parse_url(url)
          assert base == "https://pp-api.education.gov.uk/statistics-test/v1/publications"

    def test_prod_environment(self):
          url = api_url(ees_environment="prod")
          base, _ = parse_url(url)
          assert base == "https://api.education.gov.uk/statistics/v1/publications"
     
    def test_invalid_environment_raises(self):
          url = api_url(ees_environment="stagging")
          base, _ = parse_url(url)
          assert base == "https://api.education.gov.uk/statistics/v1/publications"

    def test_api_version(self):
          url = api_url(api_version="2")
          assert "/v2/" in url 
     
    def test_no_params_no_query_string(self):
          url = api_url()
          assert "?" not in url 


class TestGetDataCatalogue:
    
    def test_basic_url(self):
        url = api_url(
            endpoint="get-data-catalogue",
            publication_id=PUPIL_ABSENCE_PUBLICATION_ID)

        assert f"publications/{PUPIL_ABSENCE_PUBLICATION_ID}/data-sets" in url

    def test_missing_publication_id_raises(self):
        with pytest.raises(ValueError, match="publication_id is required"):
            api_url(endpoint="get-data-catalogue")

    def test_pagination(self):
        url = api_url(
            endpoint="get-data-catalogue",
               publication_id=PUPIL_ABSENCE_PUBLICATION_ID,
               page=1,
               page_size=10)

        _, params = parse_url(url)
        assert params["page"] == ["1"]
        assert params["pageSize"] == ["10"]


    def test_no_extra_params(self):
        url = api_url(
            endpoint="get-data-catalogue",
               publication_id=PUPIL_ABSENCE_PUBLICATION_ID)

        assert "?" not in url


class TestGetSummary:
    
    def test_absence_sessions(self):
        url = api_url(
               endpoint="get-summary",
               dataset_id=ABSENCE_SESSIONS_DATASET_ID)

        base, _ = parse_url(url)
        assert base.endswith(f"data-sets/{ABSENCE_SESSIONS_DATASET_ID}")
        assert "?" not in url

    def test_persistent_absentees(self):
        url = api_url(
            endpoint="get-summary",
               dataset_id=PERSISENT_ABSENTEES_DATASET_ID)

        assert f"data-sets/{PERSISENT_ABSENTEES_DATASET_ID}" in url

    
    def test_missing_dataset_id_raises(self):
          with pytest.raises(ValueError, match="dataset_id is required"):
               api_url(endpoint="get-summary")


class TestGetMeta:
    
    def test_absence_sessions_meta(self):
        url = api_url(
               endpoint="get-meta",
               dataset_id=ABSENCE_SESSIONS_DATASET_ID
          )

        base, _=parse_url(url)
        assert base.endswith(f"data-sets/{ABSENCE_SESSIONS_DATASET_ID}/meta")


    def test_apprenticeships_meta(self):
        url = api_url(
               endpoint="get-meta",
               dataset_id=APPRENTICESHIPS_INYR_DATASET_ID
               )
        assert "/meta" in url

    def test_meta_with_version(self):
        url = api_url(
               endpoint="get-meta",
               dataset_id=ABSENCE_SESSIONS_DATASET_ID,
               dataset_version="2.0")

        _, params = parse_url(url)
        assert params["dataSetVersion"] == ["2.0"]


class TestGetCsv:

    def test_csv_url_structure(self):
        url = api_url(
               endpoint="get-csv",
               dataset_id=ALEVEL_PERF_DATASET_ID
               )

        base, _ = parse_url(url)
        assert base.endswith(f"data-sets/{ALEVEL_PERF_DATASET_ID}/csv")

    def test_csv_with_version(self):
        url = api_url(
               endpoint="get-csv",
               dataset_id=ALEVEL_PERF_DATASET_ID,
               dataset_version="1.1")

        _, params = parse_url(url)
        assert params["dataSetVersion"] == ["1.1"]


class TestGetDatasetVersions:

    def test_version_url(self):
        url = api_url(
               endpoint = "get-dataset-versions",
               dataset_id = ABSENCE_SESSIONS_DATASET_ID)

        base, _=parse_url(url)
        assert base.endswith(f"data-sets/{ABSENCE_SESSIONS_DATASET_ID}/versions")

    def test_alevel_nat_versions(self):
        url = api_url(
               endpoint = "get-dataset-versions",
               dataset_id=ALEVEL_NAT_PERF_DATASET_ID)

        assert "/versions" in url

class TestGetData:
    
    def test_basic_get_data(self):
        url = api_url(
               endpoint="get-data",
               dataset_id=ABSENCE_SESSIONS_DATASET_ID)

        base, _ = parse_url(url)
        assert base.endswith(f"data-sets/{ABSENCE_SESSIONS_DATASET_ID}/query")

    def test_indicators(self):
        url = api_url(
            endpoint = "get-data",
               dataset_id=ABSENCE_SESSIONS_DATASET_ID,
               indicators=["number_of_sessions","percentage_of_sessions"])

        _, params = parse_url(url)
        assert "number_of_sessions" in params["indicators"][0]
        assert "percentage_of_sessions" in params["indicators"][0]

    def test_time_periods(self):
        url = api_url(
               endpoint="get-data",
               dataset_id=ABSENCE_SESSIONS_DATASET_ID,
               time_periods=["2022|AY", "2023|AY", "2024|AY"]
          )

        _, params = parse_url(url)
        assert "2022|AY" in params["timeperiods"][0]

    def test_geographic_levels(self):
        url = api_url(
               endpoint="get-data",
               dataset_id=ABSENCE_SESSIONS_DATASET_ID,
               geographic_levels=["National","Regional","LocalAuthority"]
          )

        _, params = parse_url(url)

        assert "National" in params["geographicLevels"][0]

    def test_filter_items_absence_reason(self):
        url = api_url(
               endpoint="get-data",
               dataset_id=ABSENCE_SESSIONS_DATASET_ID,
               filter_items=["Authorised absence", "Unauthorised absence"]
          )
        _, params = parse_url(url)
        assert "Authorised absence" in params["filters"][0]

    def test_locations(self):
        url = api_url(
               endpoint="get-data",
               dataset_id=ALEVEL_NAT_PERF_DATASET_ID,
               locations=["E92000001"])

        _, params = parse_url(url)
        assert "E92000001" in params["locations"][0]

    def test_pagination_auto_defaults_page_only(self):
        url = api_url(
               endpoint="get-data",
               dataset_id=ABSENCE_SESSIONS_DATASET_ID,
               page=2
          )

        _, params = parse_url(url)
        assert params["page"] == ["2"]
        assert params["pageSize"] == ["1000"]

    def test_pagination_auto_defaults_page_size_only(self):
        url = api_url(
               endpoint = "get-data",
               dataset_id=ABSENCE_SESSIONS_DATASET_ID,
               page_size=500
          )

        _, params = parse_url(url)
        assert params["pageSize"] == ["500"]
        assert params["page"] == ["1"]


    def test_explict_pagination(self):
        url = api_url(
               endpoint="get-data",
               dataset_id=APPRENTICESHIPS_FULL_DATASET_ID,
               page=3,
               page_size=200
          )

        _, params = parse_url(url)
        assert params["page"] == ["3"]
        assert params["pageSize"] == ["200"]

    def test_combined_filters_apprenticeships(self):
        url = api_url(
               endpoint="get-data",
               dataset_id=APPRENTICESHIPS_INYR_DATASET_ID,
               indicators=["starts","achievements","participation"],
               geographic_levels=["National", "Regional"],
               filter_items=["Intermediate","Advanced"],
               time_periods=["2024|AY"]
          )

        _, params = parse_url(url)
        assert "starts" in params["indicators"][0]
        assert "National" in params["geographicLevels"][0]
        assert "Intermediate" in params["filters"][0]


    def test_versions_with_get_data(self):
        url = api_url(
               endpoint="get-data",
               dataset_id=ABSENCE_SESSIONS_DATASET_ID,
               dataset_version="3.0"
          )

        _, params = parse_url(url)
        assert params["dataSetVersion"] == ["3.0"]

    def test_missing_dataset_id_raises(self):
        with pytest.raises(ValueError, match="dataset_id is required"):
            api_url(endpoint="get-data")
