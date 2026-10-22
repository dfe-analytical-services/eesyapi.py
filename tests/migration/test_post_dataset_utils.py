"""Check geography criteria in POST query bodies."""

import json

from eesyapi.post_dataset_utils import parse_tojson_geographies, parse_tojson_params


class TestGeographyCriteria:

    def test_no_geographies_omits_criteria(self):
        assert parse_tojson_geographies(None) is None

    def test_level_without_location(self):
        result = json.loads(parse_tojson_geographies("NAT"))
        assert result == {"or": [{"and": [{"geographicLevels": {"eq": "NAT"}}]}]}

    def test_locations_stay_paired_with_their_levels(self):
        result = json.loads(parse_tojson_geographies([
            "NAT|code|E92000001",
            "REG|id|region1",
        ]))
        assert result == {"or": [
            {"and": [
                {"geographicLevels": {"eq": "NAT"}},
                {"locations": {"in": [{"level": "NAT", "code": "E92000001"}]}},
            ]},
            {"and": [
                {"geographicLevels": {"eq": "REG"}},
                {"locations": {"in": [{"level": "REG", "id": "region1"}]}},
            ]},
        ]}

    def test_geography_in_complete_query_body(self):
        result = json.loads(parse_tojson_params(
            indicators=["X9fKb"], geographies="NAT|code|E92000001", page_size=5,
        ))
        assert result == {
            "criteria": {"and": [{"or": [{"and": [
                {"geographicLevels": {"eq": "NAT"}},
                {"locations": {"in": [{"level": "NAT", "code": "E92000001"}]}},
            ]}]}]},
            "indicators": ["X9fKb"],
            "debug": False,
            "page": 1,
            "pageSize": 5,
        }
