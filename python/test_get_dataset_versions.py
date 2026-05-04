import pytest
import requests
from get_dataset_versions import (
    get_dataset_versions,
    validate_ees_id,
    validate_page_size,
    warning_max_pages
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
    not is_reachable("https://pp-api.education.gov.uk/statistics-dev/v1/publications"),
    reason = "Dev not reachable - connect to DFE VPN"

)

skip_preprod = pytest.mark.skipif(
    not is_reachable("https://pp-api.education.gov.uk/statistics-preprod/v1/publications"),
    reason = "Preprod not reachable - Connect to DFE VPN"

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

    def test_int_id_raises(Self):
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

    def test_with_total_no_warning(self, capsys):
        warning_max_pages({"paging": {"totalPages": 5, "page": 3}})
        assert "Warning" not in capsys.readouterr().out

    def test_exceeds_total_warns(self, capsys):
        warning_max_pages({"paging": {"totalPages": 3, "page":5}})
        assert "Warning" in capsys.readouterr().out

    def test_eqaul_pages_no_warning(self, capsys):
        warning_max_pages({"paging": {"totalPages": 3, "page": 3}})
        assert "Warning" not in capsys.readouterr().out

class TestGetDatasetVersionsProd:

    def test_apprenticeships_full_returns_list(self):
        results = get_dataset_versions(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
    
    def test_apprenticeships_full_has_versions(self):
        results = get_dataset_versions(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert len(results) >= 1
    
    def test_apprenticeships_inyr_versions(self):
        results = get_dataset_versions(
            dataset_id=APPRENTICE_INYR_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) >= 1

    
    def test_ks4_version(self):
        results = get_dataset_versions(
            dataset_id=KS4_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)


    def test_apprenticeships_full_has_version(self):
        results = get_dataset_versions(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert len(results) >= 1

    def test_apprenticeships_inyr_version(self):
        results = get_dataset_versions(
            dataset_id=APPRENTICE_INYR_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) >= 1
    
    def test_ks4_versions(self):
        results = get_dataset_versions(
            dataset_id=KS4_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
    
    def test_ks4_version(self):
        results = get_dataset_versions(
            dataset_id=KS2_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)

    def test_phonics_dist_versions(self):
        results = get_dataset_versions(
            dataset_id=PHONICS_DIST_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
    
    def test_phonics_char_versions(self):
        results = get_dataset_versions(
            dataset_id=PHONICS_CHAR_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
    
    def test_results_are_dicts(self):
        results = get_dataset_versions(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        for r in results:
            assert isinstance(r, dict)
    
    def test_version_has_version_field(self):
        results = get_dataset_versions(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert len(results) > 0
        assert "version" in results[0]

    def test_page_size_1_respected(self):
        results = get_dataset_versions(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=1,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) >= 1

    def test_page_size_3_respected(self):
        results = get_dataset_versions(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=3,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) >= 1
    
    def test_empty_dataset_id_raises(self):
        with pytest.raises(ValueError):
            get_dataset_versions(
                dataset_id="",
                ees_environment="prod"
            )
    
    def test_invalid_dataset_id_raises(self):
        with pytest.raises(Exception):
            get_dataset_versions(
                dataset_id="00000000-0000-0000-0000-000000000000",
                ees_environment="prod"
            )

    def test_zero_page_size_raises(self):
        with pytest.raises(ValueError):
            get_dataset_versions(
                dataset_id=APPRENTICE_FULL_ID,
                ees_environment="prod",
                page_size=0
            )

    def test_verbose_prints_url(self, capsys):
        get_dataset_versions(
            dataset_id=APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=3,
            page=1,
            verbose=True
        )
        captured = capsys.readouterr()
        assert "http" in captured.out.lower()

class TestGoDatasetVersionDev:

    def test_returns_list(self):
        results = get_dataset_versions(
            dataset_id=DEV_DATASET,
            ees_environment="dev",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)

    def test_has_versions(self):
        results = get_dataset_versions(
            dataset_id=DEV_DATASET,
            ees_environment="dev",
            page_size=5,
            page=1

        )
        assert len(results) >= 1

    def test_page_size_respected(self):
        results = get_dataset_versions(
            dataset_id=DEV_DATASET,
            ees_environment="dev",
            page_size=1,
            page=1
        )
        assert len(results) <= 1


class TestGetDatasetVersionsPreprod:

    def test_returns_list(self):
        results = get_dataset_versions(
            dataset_id=TEST_DATASET,
            ees_environment="preprod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)

    def test_has_versions(self):
        results = get_dataset_versions(
            dataset_id=TEST_DATASET,
            ees_environment="preprod",
            page_size=5,
            page=1
        )
        assert len(results) >= 1
    
    def test_page_size_respected(self):
        results = get_dataset_versions(
            dataset_id=TEST_DATASET,
            ees_environment="preprod",
            page_size=1,
            page=1
        )

        assert len(results) <= 1