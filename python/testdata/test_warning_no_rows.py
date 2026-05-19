import pytest
import warnings
from warning_no_rows import warning_no_rows

class TestWarningNoRows:

    def test_returns_input_unchanged(self):
        data = {"paging": {"totalResults":5, "page": 1, "totalPages": 1}}
        result = warning_no_rows(data)
        assert result == data
    
    def test_no_warning_when_results_exist(self):
        data = {"paging": {"totalResults": 10}}
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warning_no_rows(data)
            assert len(w) == 0
    
    def test_warning_when_zero_results(self):
        data = {"paging":  {"totalResults": 0}}
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warning_no_rows(data)
            assert len(w) == 1
            assert "zero rows" in str(w[0].message).lower()

    def test_no_warning_when_one_result(self):
        data = {"paging": {"totalResults": 1}}
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warning_no_rows(data)
            assert len(w) == 0

    def test_no_paging_key_no_warning(self):
        data = {"results": []}
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warning_no_rows(data)
            assert len(w) == 0

    def test_empty_paging_no_warning(self):
        data = {"paging": {}}
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warning_no_rows(data)
            assert len(w) == 0

    def test_returns_original_dict(self):
        data = {"paging": {"totalResults": 0}, "results": []}
        result = warning_no_rows(data)
        assert "results" in result 
        assert result["results"] == []

    def test_large_result_count_no_warning(self):
        data = {"paging": {"totalResults": 100000}}
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warning_no_rows(data)
            assert len(w) == 0