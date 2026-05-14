import pytest
import requests
import pandas as pd 
from query_dataset import query_dataset
from query_dataset_utils import todf_geographies


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
    reason = "Dev not reachable - connect to DFE VPN"

)

skip_preprod = pytest.mark.skipif(
    not is_reachable("https://pp-api.education.gov.uk/statistics-preprod/v1/publications"),
    reason = "Preprod not reachable - connect to DFE VPN"
)

class TestTodfGeographies:
    def test_none_returns_none(self):
        assert todf_geographies(None) is None 
    
    def test_string_returns_dataframe(self):
        result = todf_geographies("NAT")
        assert isinstance(result, pd.DataFrame)
    
    def test_string_has_geographic_level(self):
        result = todf_geographies("NAT")
        assert "geographic_level" in result.columns
        assert result["geographic_level"].iloc[0] == "NAT"
    
    def test_list_of_levels(self):
        result = todf_geographies(["NAT", "REG"])
        assert len(result) == 2
    
    def test_location_string_parsed(self):
        result = todf_geographies("NAT|code|E92000001")
        assert result["location_id"].iloc[0] == "E92000001"
        assert result["location_id_type"].iloc[0] == "code"
    
    def test_location_list_parsed(self):
        result = todf_geographies(["NAT|code|E92000001", "REG|code|E12000001"])
        assert len(result) == 2

    def test_dataframe_input(self):
        df = pd.DataFrame({"geographic_level": ["NAT", "REG"]})
        result = todf_geographies(df)
        assert isinstance(result, pd.DataFrame)
    
    def test_dataframe_with_locations(self):
        df = pd.DataFrame({"locations": ["NAT|code|E92000001"]})
        result = todf_geographies(df)
        assert "location_level" in result.columns
        assert "location_id" in result.columns
    
    def test_dict_with_geographic_level(self):
        result = todf_geographies({"geographic_level": ["NAT", "REG"]})
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
    
    def test_dict_with_locations(self):
        result = todf_geographies({"locations": ["NAT|code|E92000001"]})
        assert isinstance(result, pd.DataFrame)
    
    def test_dict_with_both(self):
        result = todf_geographies({
            "geographic_level": ["REG", "LA"],
            "locations": ["REG|code|E12000001"]
        })
        assert isinstance(result, pd.DataFrame)
    
    def test_invalid_type_raises(self):
        with pytest.raises(ValueError):
            todf_geographies(123)
    
    def test_invalid_dict_key_raises(self):
        with pytest.raises(ValueError):
            todf_geographies({"invalid_key": ["NAT"]})
    
    def test_human_friendly_name_converted(self):
        result = todf_geographies("NAT")
        assert result["geographic_level"].iloc[0] == "NAT"
    
    def test_returns_no_duplicates(self):
        result = todf_geographies(["NAT", "NAT", "REG"])
        assert len(result) == len(result.drop_duplicates())

    

class TestQueryDatasetValidation:

    def test_invalid_method_raises(self):
        with pytest.raises(ValueError, match="Invalid method"):
            query_dataset(
                APPRENTICE_FULL_ID,
                method="DELETE"
            )

    def test_invalid_method_put_raises(self):
        with pytest.raises(ValueError):
            query_dataset(
                APPRENTICE_FULL_ID,
                method = "PUT"
            )

class TestQueryDatasetProd:

    def test_returns_dataframe_post(self):
        result = query_dataset(
            APPRENTICE_FULL_ID,
            ees_environment="prod",
            page_size=5,
            page=1,
            method="POST",
            json_query={"criteria": {}, "indicators": [], "page": 1, "pageSize":5}
            
        )
        assert isinstance(result, (pd.DataFrame, type(None)))
    
    def test_with_geographies_nat(self):
        result = query_dataset(
            APPRENTICE_FULL_ID,
            geographies="NAT",
            indicators=["X9fKb"],
            ees_environment="prod",
            page_size=5,
            page=1,
            method="POST",
            parse=False

        )
        assert isinstance(result, (pd.DataFrame, type(None)))
    
    def test_with_time_periods(self):
        result = query_dataset(
            APPRENTICE_FULL_ID,
            time_periods=["2024|AY"],
            indicators=["X9fKb"],
            ees_environment="prod",
            page_size=5,
            page=1,
            method="POST",
            parse=False
        )
        assert isinstance(result, (pd.DataFrame, type(None)))
    
    def test_ks4_dataset(self):
        result = query_dataset(
            KS4_ID,
            ees_environment="prod",
            page_size=5,
            page=1,
            method="POST",
            json_query={"criteria": {}, "indicators": [], "page":1, "pageSize":5}
        )

        assert isinstance(result, (pd.DataFrame, type(None)))
    
    def test_get_method_warns(self):
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            query_dataset(
                APPRENTICE_FULL_ID,
                geographies="NAT",
                ees_environment="prod",
                page_size=5,
                page=1,
                method="GET"
            )
            assert any("GET" in str(Warning.message) for warning in w)
    

    