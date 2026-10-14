
from unittest.mock import Mock, patch

from monitor import check_website


def test_invalid_url():
    result = check_website("not-a-url")

    assert result["status"] == "DOWN"
    assert result["status_code"] == 0


@patch("monitor.requests.get")
def test_successful_website(mock_get):
    mock_get.return_value = Mock(status_code=200)

    result = check_website("https://example.com")

    assert result["status"] == "UP"
    assert result["status_code"] == 200


@patch("monitor.requests.get")
def test_server_error(mock_get):
    mock_get.return_value = Mock(status_code=500)

    result = check_website("https://example.com")

    assert result["status"] == "DOWN"
    assert result["status_code"] == 500


@patch("monitor.requests.get")
def test_connection_failure(mock_get):
    mock_get.side_effect = Exception("Unexpected error")

    # This test is replaced below with the expected requests exception.
@patch("monitor.requests.get")
def test_connection_failure(mock_get):
    import requests

    mock_get.side_effect = requests.ConnectionError("Connection failed")

    result = check_website("https://example.com")

    assert result["status"] == "DOWN"
    assert result["status_code"] == 0