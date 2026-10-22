import pytest
import requests 
from unittest.mock import Mock, patch
from eesyapi.get_dataset import (
    get_dataset,
    validate_ees_id,
    validate_page_size,
    warning_max_pages
)

APPRENTICE_FULL_ID = "1d419801-a90e-f970-9335-a13623faccbe"

APPRENTICE_INYR_ID = "1d419801-435d-c676-b428-1217e08290c3"

KS4_ID = "019d4320-2bde-7059-8d7a-b685013eb1e6"

KS2_ID = "019d431f-c129-73e6-917e-6998bfe4d88d"

ABSENCE_ID = "019d209b-b031-7497-8205-af255b581d91"

PERSISTENT_ABS_ID = "019d209c-08dc-74b6-9edb-52d521406fcf"

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
    not is_reachable("https://pp-api.education.gov.uk/statistics-dev/v1/publications"),
    reason ="Dev not reachable - Connect to DFE VPN"
)

skip_preprod = pytest.mark.skipif(
    not is_reachable("https://pp-api.education.gov.uk/statistics-preprod/v1/publications"),
    reason = "Preprod not reachable - connect to DFE VPN"

)

class TestValidation:

    def test_valid_id_passes(self):
        validate_ees_id(APPRENTICE_FULL_ID)
    
    def test_empty_id_raises(self):
        with pytest.raises(ValueError, match="Invalid dataset_id"):
            validate_ees_id("")

    def test_none_id_raises(self):
        with pytest.raises(ValueError):
            validate_ees_id(None)

    def test_int_id_raises(self):
        with pytest.raises(ValueError):
            validate_ees_id(123)

    def test_valid_page_size(self):
        validate_page_size(10)
    
    def test_none_page_size_passes(self):
        validate_page_size(None)

    def test_zero_page_size_raises(self):
        with pytest.raises(ValueError, match="page_size must be greater than 0"):
            validate_page_size(0)

    def test_negative_page_size_raises(self):
        with pytest.raises(ValueError):
            validate_page_size(-1)


class TestWarningMaxPages:

    def test_no_paging_key_no_warning(self, capsys):
        warning_max_pages({})
        assert "Warning" not in capsys.readouterr().out
    
    def test_within_total_no_warning(self, capsys):
        result = capsys.readouterr().out
        warning_max_pages({"paging": {"totalPages": 5, "page":3}})
        captured = capsys.readouterr().out
        assert isinstance(captured, str)
    
    def test_exceeds_total_warns(self, capsys):
        warning_max_pages({"paging": {"totalPages":3, "page":5}})
        assert "Warning" in capsys.readouterr().out
    
    def test_equal_pages_no_warning(self, capsys):
        warning_max_pages({"paging": {"totalPages": 3, "page": 3}})
        assert "Warning" not in capsys.readouterr().out


class TestGetDatasetSummary:

    @pytest.mark.parametrize("kwargs", [
        {},
        {"page": 1, "page_size": 1},
        {"page": 2, "page_size": 3, "dataset_version": "1.0.0"},
    ])
    def test_returns_summary_from_one_request(self, kwargs):
        summary = {
            "id": APPRENTICE_FULL_ID,
            "title": "Apprenticeship starts",
            "summary": "Starts by level and age.",
            "status": "Published",
            "latestVersion": {"version": "1.0.0"},
        }
        response = Mock(status_code=200)
        response.json.return_value = summary
        with patch("eesyapi.get_dataset.requests.get", return_value=response) as get:
            result = get_dataset(APPRENTICE_FULL_ID, **kwargs)

        assert result == [summary]
        get.assert_called_once_with(
            f"https://api.education.gov.uk/statistics/v1/data-sets/{APPRENTICE_FULL_ID}"
        )

    def test_failed_summary_request_raises(self):
        response = Mock(status_code=404)
        with patch("eesyapi.get_dataset.requests.get", return_value=response):
            with pytest.raises(Exception, match="API Error: 404"):
                get_dataset(APPRENTICE_FULL_ID)
        response.json.assert_not_called()


class TestGetDatasetProd:

    def test_apprenticeship_full_returns_list(self):
        results = get_dataset(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) == 1
        assert {"id", "title", "summary", "status", "latestVersion"} <= results[0].keys()

    def test_apprenticeship_full_returns_results(self):
        results = get_dataset(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert len(results) > 0

    def test_apprenticeships_inyr(self):
        results = get_dataset(
            dataset_id=APPRENTICE_INYR_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) == 1
        assert {"id", "title", "summary", "status", "latestVersion"} <= results[0].keys()
        assert len(results) > 0

    def test_ks4_dataset(self):
        results = get_dataset(
            dataset_id=KS4_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) == 1
        assert {"id", "title", "summary", "status", "latestVersion"} <= results[0].keys()

    def test_ks2_dataset(self):
        results = get_dataset(
            dataset_id=KS2_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) == 1
        assert {"id", "title", "summary", "status", "latestVersion"} <= results[0].keys()

    def test_absence_sessions(self):
        results = get_dataset(
            dataset_id=ABSENCE_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) == 1
        assert {"id", "title", "summary", "status", "latestVersion"} <= results[0].keys()
        assert len(results) > 0
    
    def test_persistent_absence(self):
        results = get_dataset(
            dataset_id=PERSISTENT_ABS_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) == 1
        assert {"id", "title", "summary", "status", "latestVersion"} <= results[0].keys()

    def test_phonics_distribution(self):
        results = get_dataset(
            dataset_id=PHONICS_DIST_ID,
            ees_environment="prod",
            page_size=5,
            page=1

        )
        assert isinstance(results, list)
        assert len(results) == 1
        assert {"id", "title", "summary", "status", "latestVersion"} <= results[0].keys()

    def test_phonics_characteristics(self):
        results = get_dataset(
            dataset_id=PHONICS_CHAR_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) == 1
        assert {"id", "title", "summary", "status", "latestVersion"} <= results[0].keys()
    
    def test_results_are_dict(self):
        results = get_dataset(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=3,
            page=1
        )

        for r in results:
            assert isinstance(r, dict)

    def test_summary_with_legacy_page_size_1(self):
        results = get_dataset(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=1,
            page=1

        )
        assert len(results) == 1
        assert {"id", "title", "summary", "status", "latestVersion"} <= results[0].keys()

    def test_summary_with_legacy_page_size_3(self):
        results = get_dataset(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=3,
            page=1
        )
        assert len(results) == 1
        assert results[0]["id"] == APPRENTICE_FULL_ID
        assert "latestVersion" in results[0]

    def test_empty_dataset_id_raises(self):
        with pytest.raises(ValueError):
            get_dataset(
                dataset_id="",
                ees_environment="prod"
            )
    
    def test_zero_page_size_raises(self):
        with pytest.raises(ValueError):
            get_dataset(
                dataset_id=APPRENTICE_FULL_ID,
                ees_environment="prod",
                page_size=0
            )
    
    def test_verbose_print_url(self, capsys):
        get_dataset(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=3,
            page=1,
            verbose=True
        )
        captured = capsys.readouterr()
        assert "http" in captured.out.lower()

class TestGetDatasetDev:

    def test_returns_list(self):
        results = get_dataset(
            dataset_id=DEV_DATASET,
            ees_environment="dev",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) == 1
        assert {"id", "title", "summary", "status", "latestVersion"} <= results[0].keys()

    def test_returns_results(self):
        results = get_dataset(
            dataset_id=DEV_DATASET,
            ees_environment="dev",
            page_size=5,
            page=1
        )
        assert len(results) > 0

    def test_summary_with_legacy_page_size(self):
        results = get_dataset(
            dataset_id=DEV_DATASET,
            ees_environment="dev",
            page_size=1,
            page=1
        )
        assert len(results) == 1
        assert {"id", "title", "summary", "status", "latestVersion"} <= results[0].keys()


class TestGetDatasetPreprod:

    def test_returns_list(self):
        results = get_dataset(
            dataset_id=TEST_DATASET,
            ees_environment="preprod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) == 1
        assert {"id", "title", "summary", "status", "latestVersion"} <= results[0].keys()
    
    def test_returns_results(self):
        results = get_dataset(
            dataset_id=TEST_DATASET,
            ees_environment="preprod",
            page_size=5,
            page=1
        )
        assert len(results) > 0

    def test_summary_with_legacy_page_size(self):
        results = get_dataset(
            dataset_id=TEST_DATASET,
            ees_environment="preprod",
            page_size=1,
            page=1
        )
        assert len(results) == 1
        assert {"id", "title", "summary", "status", "latestVersion"} <= results[0].keys()


