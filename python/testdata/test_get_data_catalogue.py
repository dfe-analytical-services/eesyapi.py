import pytest 
import requests
from get_data_catalogue import (
    get_data_catalogue, 
    validate_ees_id, 
    validate_page_size, 
    warning_max_pages
)


EARLY_YEARS_PUB_ID = "fcda2962-82a6-4052-afa2-ea398c53c85f"

APPRENTICESHIPS_PUB_ID = "412d8090-ab45-455a-c176-08dbf5ab522b"

PHONICS_PUB_ID = "5becb18e-852b-4cdf-e2e8-08dcc3489646"

PUPIL_ABSENCE_PUB_ID = "cbbd299f-8297-44bc-92ac-558bcf51f8ad"

CHILDREN_NEEDS_PUB_ID = "89869bba-0c00-40f7-b7d6-e28cb904ad37"

KS4_PUB_ID = "c8756008-ed50-4632-9b96-01b5ca002a43"


def is_reachable(url):
    try:
        requests.get(url, timeout=5)
        return True
    except Exception:
        return False
    
skip_dev = pytest.mark.skipif(
    not is_reachable("http://pp-api.education.gov.uk/statistics-dev/v1/publications"),
    reason ="Dev not reachable - Connect o DFE VPN"

)

skip_preprod = pytest.mark.skipif(
    not is_reachable("https://pp-api.education.gov.uk/statistics-preprod/v1/publications"),
    reason = "Preprod not reachable - Connect to DFE VPN"
)


class TestValidation:


    def test_valid_id_passes(self):
        validate_ees_id("PUPIL_ABSENCE_PUB_ID")

    def test_empty_id_raises(self):
        with pytest.raises(ValueError, match="Invalid publication_id"):
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

class TestWarningMaxPage:

    def test_no_paging_key_no_warning(self, capsys):
        warning_max_pages({})
        assert "Warning" not in capsys.readouterr().out
    
    def test_within_total_no_warning(self, capsys):
        warning_max_pages({"paging": {"totalPages": 5, "page": 3}})
        assert "Warning" not in capsys.readouterr().out

    def test_exceeds_total_warns(self, capsys):
        warning_max_pages({"paging": {"totalPages": 3, "page": 5}})
        assert "Warning" in capsys.readouterr().out

    def test_equal_pages_no_warning(self, capsys):
        warning_max_pages({"paging" : {"totalPages": 3, "page":3}})
        assert "Warning" not in capsys.readouterr().out  

class TestGetDataCatalogueProd:

    def test_early_years_returns_list(self):
        results = get_data_catalogue(
            publication_id=EARLY_YEARS_PUB_ID,
            ees_environment="prod",
            page_size=5, 
            page=1
        )      
        assert isinstance(results, list)
    
    def test_early_years_returns_results(self):
        results = get_data_catalogue(
            publication_id=EARLY_YEARS_PUB_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert len(results) > 0

    def test_apprenticeship_returns_results(self):
        results = get_data_catalogue(
            publication_id=APPRENTICESHIPS_PUB_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) > 0
    
    def test_phonics_returns_results(self):
        results = get_data_catalogue(
            publication_id=PHONICS_PUB_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) > 0

    def test_pupil_absence_returns_results(self):
        results = get_data_catalogue(
            publication_id=PUPIL_ABSENCE_PUB_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) > 0
    
    def test_children_needs_returns_results(self):
        results = get_data_catalogue(
            publication_id=CHILDREN_NEEDS_PUB_ID,
            ees_environment="prod",
            page_size=5, 
            page=1
        )
        assert isinstance(results, list)
        assert len(results) > 0
    
    def test_ks4_returns_results(self):
        results = get_data_catalogue(
            publication_id=KS4_PUB_ID, 
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) > 0
    
    def test_results_have_id_field(self):
        results = get_data_catalogue(
            publication_id=PUPIL_ABSENCE_PUB_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        for r in results:
            assert "id" in r
    
    def test_results_are_dicts(self):
        results = get_data_catalogue(
            publication_id=PUPIL_ABSENCE_PUB_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        for r in results:
            assert isinstance(r, dict)
    
    def test_results_have_title_field(self):
        results = get_data_catalogue(
            publication_id=PUPIL_ABSENCE_PUB_ID,
            ees_environment="prod",
            page_size=5,
            page=1
        )
        for r in results:
            assert "title" in r
    
    def test_page_size_1_respected(self):
        results = get_data_catalogue(
            publication_id=PUPIL_ABSENCE_PUB_ID,
            ees_environment="prod",
            page_size=1,
            page=1
        )
        assert len(results) <= 1

    def test_page_size_3_respected(self):
        results = get_data_catalogue(
            publication_id=PUPIL_ABSENCE_PUB_ID,
            ees_environment="prod",
            page_size=3,
            page=1
        )
        assert len(results) <= 3
    
    def test_invalid_publication_id_raises(self):
        with pytest.raises(Exception):
            get_data_catalogue(
                publication_id="00000000-0000-0000-0000-000000000000",
                ees_environment="prod"

            )
            assert results == []
    
    def test_empty_publication_id_raises(self):
        with pytest.raises(ValueError):
            get_data_catalogue(
                publication_id="",
                ees_environment="prod"
            )

    def test_zero_page_size_raises(self):
        with pytest.raises(ValueError):
            get_data_catalogue(
                publication_id=PUPIL_ABSENCE_PUB_ID,
                ees_environment="prod",
                page_size=0
            )

    
    def test_negative_page_size_raises(self):
        with pytest.raises(ValueError):
            get_data_catalogue(
                publication_id=PUPIL_ABSENCE_PUB_ID,
                ees_environment="prod",
                page_size=-1
            )

    def test_verbose_print_url(self, capsys):
        get_data_catalogue(
            publication_id=PUPIL_ABSENCE_PUB_ID,
            ees_environment="prod",
            page_size=3,
            page=1,
            verbose=True
        )

        captured = capsys.readouterr()
        assert "http" in captured.out.lower()



DEV_PUB_ID = "cbbd299f-8297-44bc-92ac-558bcf51f8ad"

class TestGetDataCatalogueDev:

    def test_returns_list(self):
        results = get_data_catalogue(
            publication_id=PUPIL_ABSENCE_PUB_ID,
            ees_environment="dev",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
    

    def test_page_size_respected(self):
        results = get_data_catalogue(
            publication_id=PUPIL_ABSENCE_PUB_ID,
            ees_environment="dev",
            page_size=1,
            page=1
        )
        assert len(results) <= 1

class TestGetDataCataloguePreprod:

    def test_returns_list(self):
        results = get_data_catalogue(
            publication_id=PUPIL_ABSENCE_PUB_ID,
            ees_environment="preprod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
    

    def test_page_size_respected(self):
        results = get_data_catalogue(
            publication_id=PUPIL_ABSENCE_PUB_ID,
            ees_environment="preprod",
            page_size=1,
            page=1
        )
        assert len(results) <=1


