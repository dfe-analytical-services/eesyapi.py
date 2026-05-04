import pytest
from convert_api_filter_type import convert_api_filter_type, convert_single_filter

class TestConvertSingleFilter:

    def test_string_value_becomes_list(Self):
        result = convert_single_filter("absence_type","Authorised")
        assert result == {"field": "absence_type","values": ["Authorised"]}
    
    def test_list_value_unchanged(self):
        result = convert_single_filter("absence_type", ["Authorised", "Unauthorised"])
        assert result == {"field": "absence_type", "values": ["Authorised", "Unauthorised"]}
    
    def test_returns_dict(self):
        result = convert_single_filter("field","value")
        assert isinstance(result, dict)
    
    def test_has_field_key(self):
        result = convert_single_filter("absence_type","Authorised")
        assert "field" in result
    
    def test_has_values_key(self):
        result = convert_single_filter("absence_type","Authorised")
        assert "values" in result

    def test_field_name_correct(self):
        result = convert_single_filter("school_type","Primary")
        assert result["field"] == "school_type"

    def test_single_string_wrapped_in_list(self):
        result = convert_single_filter("type","abc")
        assert result["values"] == ["abc"]
    
    def test_list_with_single_item(self):
        result = convert_single_filter("type",["abc"])
        assert result["values"] == ["abc"]
    
    def test_list_with_multiple_items(self):
        result = convert_single_filter("type", ["a","b","c"])
        assert result["values"] == ["a","b","c"]
    
    def test_empty_string_value(self):
        result = convert_single_filter("field", "")
        assert result["values"] == [""]

    def test_empty_list_values(self):
        result = convert_single_filter("field", [])
        assert result["values"] == []

    def test_invalid_type_raises(self):
        with pytest.raises(ValueError):
            convert_single_filter("field", 123)

    def test_invalid_dict_raises(self):
        with pytest.raises(ValueError):
            convert_single_filter("field", {"key": "value"})

    def test_invalid_none_raises(self):
        with pytest.raises(ValueError):
            convert_single_filter("field", None)


class TestConvertApiFilterType:

    def test_none_returns_empty_list(self):
        assert convert_api_filter_type(None) == []

    def test_empty_dict_returns_empty_list(self):
        assert convert_api_filter_type({}) == []

    def test_empty_list_returns_empty_list(Self):
        assert convert_api_filter_type([]) == []

    def test_valid_list_passthrough(self):
        filters = [{"field": "type", "values": ["x"]}]
        assert convert_api_filter_type(filters) == filters

    def test_dict_single_key_converted(self):
        result = convert_api_filter_type({"absence_type": "Authorised"})
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["field"] == "absence_type"
        assert result[0]["values"] == ["Authorised"]

    def test_dict_multiple_keys_converted(self):
        result = convert_api_filter_type({
            "absence_type": "Authorised",
            "school_type": "Primary"
        })
        assert len(result) == 2
        fields = [r["field"] for r in result]
        assert "absence_type" in fields
        assert "school_type" in fields

    def test_dict_with_list_values(self):
        result = convert_api_filter_type({
            "absence_type": ["Authorised", "Unauthorised"]
        })
        assert result[0]["values"] == ["Authorised","Unauthorised"]

    def test_dict_with_string_value_wrapped(self):
        result = convert_api_filter_type({"type": "abc"})
        assert result[0]["values"] == ["abc"]
    
    def test_valid_list_with_field_and_values(self):
        filters = [
            {"field": "absence_type", "values": ["Authorised"]},
            {"field": "school_type", "values": ["Primary","Secondary"]}
        ]
        result = convert_api_filter_type(filters)
        assert len(result) == 2

    def test_invalid_list_missing_values_raises(self):
        with pytest.raises(ValueError, match="Invalid filter format"):
            convert_api_filter_type([{"values": ["x"]}])

    def test_invalid_list_missing_values_raises(self):
        with pytest.raises(ValueError, match="Invalid filter format"):
            convert_api_filter_type([{"field": "x"}])
    
    def test_invalid_string_raises(self):
        with pytest.raises(ValueError):
            convert_api_filter_type("bad_input")

    def test_invalid_int_raises(self):
        with pytest.raises(ValueError):
            convert_api_filter_type(123)

    def test_invalid_tuple_raises(self):
        with pytest.raises(ValueError):
            convert_api_filter_type(("field","value"))

    def test_returns_list(Self):
        assert isinstance(convert_api_filter_type(None), list)
        assert isinstance(convert_api_filter_type({}), list)
        assert isinstance(convert_api_filter_type([]), list)

    def test_list_mutiple_filters_all_valid(self):
        filters = [
            {"field": "f1", "values": ["a" ,"b"]},
            {"field": "f2", "values": ["c"]},
            {"field": "f3", "values": ["d", "e","f"]}
        ]
        result = convert_api_filter_type(filters)
        assert len(result) == 3

    def test_dict_result_has_correct_structure(self):
        result = convert_api_filter_type({"school_type": "Primary"})
        for item in result:
            assert "field" in item 
            assert "values" in item
            assert isinstance(item["values"],list)


