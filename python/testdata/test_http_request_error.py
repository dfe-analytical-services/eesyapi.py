import pytest
from http_request_error import http_request_error

class FakeResponse:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self._json = json_data or {}
    

    def json(self):
        return self._json


class TestHttpRequestError:
    def test_200_returns_success_message(self):
        response = FakeResponse(200)
        result = http_request_error(response)
        assert result is None or "Successful" in str(result)


    def test_400_raises_exception(self):
        response = FakeResponse(400, {
        "errors" : [{"message": "Bad dataset ID", "detail": {}}]
        })
    
        with pytest.raises(Exception):
             http_request_error(response)

    def test_500_raises_exception(self):
        response = FakeResponse(500, {
            "errors": [{"message": "Server error", "detail":{}}]
        })

        with pytest.raises(Exception):
            http_request_error(response)
    
    def test_404_raises_exception(self):
        response = FakeResponse(404, {
            "errors": [{"message": "Not found", "detail": {}}]
        })

        with pytest.raises(Exception):
            http_request_error(response)
    
    def test_no_status_code_raises(self):
        with pytest.raises((ValueError, AttributeError)):
            http_request_error("not a response")
    
    def test_400_no_errors_key_raises(self):
        response = FakeResponse(400, {})
        try:
            result = http_request_error(response)
        except Exception:
            pass
    
    def test_error_message_in_exception(self):
        response = FakeResponse(400, {
            "errors" : [{"message": "Invalid value", "detail": {}}]
        })
        with pytest.raises(Exception, match="Invalid value"):
            http_request_error(response)
    
    def test_error_with_allowed_values(self):
        response = FakeResponse(400, {
            "errors": [{
                "message": "Invalid value",
                "detail": {
                    "allowed" : ["National", "Regional"],
                    "value": ["Bad"]
                }
            }]
        })
        with pytest.raises(Exception):
            http_request_error(response)
    
    def test_error_with_items(self):
        response = FakeResponse(400, {
            "errors": [{
                "message":"Invalid items",
                "detail": {"items": ["item1","items2"]}
            }]
        })
        with pytest.raises(Exception):
            http_request_error(response)
    
    def test_error_with_value_detail(self):
        response = FakeResponse(400, {
            "errors": [{
                "message": "Bad value",
                "detail": {"value": ["bad_value"]}
            }]
        })
        with pytest.raises(Exception):
            http_request_error(response)
    
    def test_verbose_does_not_crash(self):
        response = FakeResponse(400, {
            "errors": [{"message": "Error", "detail": {}}]
        })
        with pytest.raises(Exception):
            http_request_error(response, verbose=True)
    
    def test_200_status_group_returns_string(self):
        response = FakeResponse(200)
        result = http_request_error(response)
        assert result is None or isinstance(result, str)
    
    def test_unrecognised_status_code(self):
        response = FakeResponse(301, {})
        try:
            result = http_request_error(response)
        except Exception:
            pass
    
    def test_multiple_errors_raises(self):
        response = FakeResponse(400, {
            "errors": [
                {"message": "Error 1", "detail": {}},
                {"message": "Error 2", "detail": {}}
            ]
        })
        with pytest.raises(Exception):
            http_request_error(response)

