import pytest 
import requests
import pandas as pd 
from preview_dataset import preview_dataset


APPRENTICE_FULL_ID = "1d419801-a90e-f970-9335-a13623faccbe"

KS4_ID = "019d4320-2bde-7059-8d7a-b685013eb1e6"

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
    reason="Dev not reachable - connect of DFE VPN"

)

skip_preprod = pytest.mark.skipif(
    not is_reachable("http://pp-api.education.gov.uk/statistics-preprod/v1/publications"),
    reason="Preprod not reachable - connect to DFE VPN"
)

class TestValidation:

    def test_invalid_verbose_raises(self):
        with pytest.raises(ValueError, match="verbose must be a boolean"):
            preview_dataset(APPRENTICE_FULL_ID, verbose="yes")
    
    def test_invalid_n_max_string_raises(self):
        with pytest.raises(ValueError):
            preview_dataset(APPRENTICE_FULL_ID, n_max="ten")
    
    def test_invalid_n_max_float_raises(self):
        with pytest.raises(ValueError):
            preview_dataset(APPRENTICE_FULL_ID, n_max=1.5)
    
    def test_invalid_n_max_zero_raises(self):
        with pytest.raises(ValueError):
            preview_dataset(APPRENTICE_FULL_ID, n_max=0)
    
    def test_invalid_dataset_id_raises(self):
        with pytest.raises(ValueError):
            preview_dataset("", ees_environment="prod")


class TestPreviewDatasetProd:

    def test_returns_dataframe(self):
        result = preview_dataset(
            APPRENTICE_FULL_ID,
            ees_environment="prod",
            n_max=5
        )
        assert isinstance(result, pd.DataFrame)
    
    def test_n_max_respected(self):
        result = preview_dataset(
            APPRENTICE_FULL_ID,
            ees_environment="prod",
            n_max=3
        )
        assert len(result) <= 3
    
    def test_default_n_max_10(self):
        result = preview_dataset(
            APPRENTICE_FULL_ID,
            ees_environment="prod"
        )

        assert len(result) <= 10
    
    def test_n_max_1(self):
        result = preview_dataset(
            APPRENTICE_FULL_ID,
            ees_environment="prod",
            n_max=1
        )

        assert len(result) == 1
    
    def test_ks4_dataset(self):
        result = preview_dataset(
            KS4_ID,
            ees_environment="prod",
            n_max=5

        )

        assert isinstance(result, pd.DataFrame)
    
    def test_has_columns(self):
        result = preview_dataset(
            APPRENTICE_FULL_ID,
            ees_environment="prod",
            n_max=3
        )
        assert len(result.columns) > 0
    
    def test_invalid_dataset_raises(self):
        with pytest.raises(Exception):
            preview_dataset(
                "00000000-0000-0000-0000-000000000000",
                ees_environment="prod"
            )


class TestPreviewDatasetDev:

    def test_returns_dataframe(self):
        result = preview_dataset(
            DEV_DATASET,
            ees_environment="dev",
            n_max=5
        )

        assert isinstance(result, pd.DataFrame)
    
    def test_n_max_respected(self):
        result = preview_dataset(
            DEV_DATASET,
            ees_environment="dev",
            n_max=3
        )

        assert len(result) <= 3

class TestPreviewDatasetPreprod:

    def test_returns_dataframe(self):
        result = preview_dataset(
            TEST_DATASET,
            ees_environment="preprod",
            n_max=5
        )

        assert isinstance(result, pd.DataFrame)

