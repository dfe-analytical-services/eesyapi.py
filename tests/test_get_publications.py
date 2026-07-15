import pytest
import requests
from eesyapi import (
    get_publications,
    validate_page_size,
    validate_environment,
    warning_max_pages,
)


EARLY_YEARS_PUB_ID = "fcda2962-82a6-4052-afa2-ea398c53c85f"  # Early yeras foundation stage

APPRENTICESHIPS_PUB_ID = "412d8090-ab45-455a-c17a-08dbf5ab522b" # Apprenticeships

OUTCOMES_PUB_ID = "f51895df-c682-45e6-b23e-3138ddbfdaeb" #Outcomes for children in need 

PHONICS_PUB_ID = "5becb18e-852b-4cdf-e2e8-08dcc3489646" #Phonics screening

PUPIL_ABSENCE_PUB_ID = "cbbd299f-8297-44bc-92ac-558bcf51f8ad" #Pupil absence



def is_reachable(url):
    try:
        requests.get(url, timeout=5)
        return True
    except Exception:
        return False

skip_dev = pytest.mark.skipif(
    not is_reachable("http://pp-api.education.gov.uk/statistics-dev/v1/publications")
    
)

skip_preprod = pytest.mark.skipif(
    not is_reachable("https://pp-api.education.gov.uk/statistics-preprod/v1/publications")
)

class TestValidation:
    def test_none_passes(self):
        validate_page_size(None)

    def test_positive_passes(self):
        validate_page_size(10)

    def test_zero_raises(self):
        with pytest.raises(ValueError, match="page_size must be greater than 0"):
            validate_page_size(0)

    def test_negative_raises(self):
        with pytest.raises(ValueError, match="page_size must be greater than 0"):
            validate_page_size(-5)

    def test_one_passes(self):
        validate_page_size(1)

    def test_large_passes(self):
        validate_page_size(1000)

class TestEnvironmentValidation:

    def test_none_passes(self):
        validate_environment(None)

    def test_dev_passes(self):
        validate_environment("dev")

    def test_test_passes(self):
        validate_environment("test")

    def test_preprod_passes(self):
        validate_environment("preprod")

    def test_prod_passes(self):
        validate_environment("prod")

    def test_invalid_fails(self):
        with pytest.raises(ValueError, match="ees_environment must be one of the following: dev, test, preprod or prod"):
            validate_environment("pvh")

    def test_invalid_environment_raises(self):
        with pytest.raises(
            ValueError,
            match="ees_environment must be one of the following"
        ):
            validate_environment("production")

class TestWarningMaxPages:

    def test_no_paging_key_no_warning(self, capsys):
        warning_max_pages({})
        assert "Warning" not in capsys.readouterr().out
    
    def test_current_within_total_no_warning(self, capsys):
        warning_max_pages({"paging": {"totalPages":5, "page":3}})
        assert "Warning" not in capsys.readouterr().out
    
    def test_current_exceeds_total_warns(self, capsys):
        warning_max_pages({"paging": {"totalPages": 3, "page": 5}})
        assert "Warning" in capsys.readouterr().out
    
    def test_equal_pages_no_warning(self, capsys):
        warning_max_pages({"paging": {"totalPages": 3,"page": 3}})
        captured = capsys.readouterr()
        assert "Warning" not in capsys.readouterr().out

class TestGetPublicationsProd:
    def test_returns_list(self):
        results = get_publications(
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)

    def test_returns_results(self):
        results = get_publications(
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert len(results) > 0

    def test_results_are_dicts(self):
        results = get_publications(
            ees_environment="prod",
            page_size=5,
            page=1
        )
        for r in results:
            assert isinstance(r,dict)
    
    def test_page_size_respected(self):
        results = get_publications(
            ees_environment="prod",
            page_size=3,
            page=1
        )
        assert len(results) <= 3 

    def test_search_absence(self):
        results = get_publications(
            search="absence",
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) > 0 
    
    def test_search_apprenticeships(self):
        results = get_publications(
            search="apprenticeships",
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) > 0
    
    def test_search_phonics(self):
        results = get_publications(
            search="phonics",
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
    
    def test_search_no_results(self):
        results = get_publications(
            search="xyznoneistentpublication12345",
            ees_environment="prod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
        assert len(results) == 0

    def test_page_1_and_page_2_different(self):
        page1 = get_publications(
            ees_environment="prod",
            page_size=1,
            page=1
        )
        page2 = get_publications(
            ees_environment="prod",
            page_size=1,
            page=2
        )
        assert page1 != page2

    def test_invalid_page_size_raises(self):
        with pytest.raises(ValueError, match="page_size must be greater than 0"):
            get_publications(
                ees_environment="prod",
                page_size=0
            )

    def test_negative_page_size_raises(Self):
        with pytest.raises(ValueError, match="page_size must be greater than 0"):
            get_publications(
                ees_environment="prod",
                page_size=-1
            )

    def test_verbose_prints_url(self, capsys):
        get_publications(
            ees_environment="prod",
            page_size=3,
            page=1,
            verbose=True
        )
        captured = capsys.readouterr()
        assert "GET" in captured.out

    def test_results_have_id_failed(self):
        results = get_publications(
            ees_environment="prod",
            page_size=5,
            page=1
        )
        for r in results:
            assert "id" in r 

    def test_results_have_title_field(self):
        results = get_publications(
            ees_environment="prod",
            page_size=5,
            page=1
        )

        for r in results:
            assert "title" in r

class TestGetPublicationDev:

    def test_returns_list(len):
        results = get_publications(
            ees_environment="dev",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)

    def test_returns_results(self):
        results = get_publications(
            ees_environment="dev",
            page_size=5,
            page=1
        )
        assert len(results) > 0

    def test_page_size_respected(self):
        results = get_publications(
            ees_environment="dev",
            page_size=3,
            page=1
        )
        assert len(results) <=3

    def test_search_works(self):
        results = get_publications(
            search="attendance",
            ees_environment="dev",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)

class TestGetPublicationsPreprod:

    def test_returns_list(self):
        results = get_publications(
            ees_environment="preprod",
            page_size=5,
            page=1
        )
        assert isinstance(results, list)
    
    def test_returns_results(Self):
        results = get_publications(
            ees_environment="preprod",
            page_size=5,
            page=1
        )
        assert len(results) > 0
    
    def test_page_size_respected(self):
        results = get_publications(
            ees_environment="preprod",
            page_size=3,
            page=1
        )
        assert len(results) <= 3
