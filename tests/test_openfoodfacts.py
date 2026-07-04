from unittest.mock import patch, Mock
import requests

from app import openfoodfacts


def _mock_response(json_data, status_code=200, raise_error=None):
    mock_resp = Mock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data
    if raise_error:
        mock_resp.raise_for_status.side_effect = raise_error
    else:
        mock_resp.raise_for_status.return_value = None
    return mock_resp


@patch("app.openfoodfacts.requests.get")
def test_fetch_by_barcode_found(mock_get):
    mock_get.return_value = _mock_response({
        "status": "success",
        "product": {
            "product_name": "Nutella",
            "brands": "Ferrero",
            "ingredients_text": "Sugar, palm oil, hazelnuts",
        },
    })

    result = openfoodfacts.fetch_by_barcode("3017620422003")

    assert result is not None
    assert result["product_name"] == "Nutella"
    assert result["brands"] == "Ferrero"
    assert result["barcode"] == "3017620422003"
    mock_get.assert_called_once()


@patch("app.openfoodfacts.requests.get")
def test_fetch_by_barcode_not_found(mock_get):
    mock_get.return_value = _mock_response({"status": "failure"})

    result = openfoodfacts.fetch_by_barcode("0000000000000")

    assert result is None


@patch("app.openfoodfacts.requests.get")
def test_fetch_by_barcode_missing_fields_uses_defaults(mock_get):
    mock_get.return_value = _mock_response({
        "status": "success",
        "product": {},
    })

    result = openfoodfacts.fetch_by_barcode("1234567890123")

    assert result["product_name"] == "Unknown"
    assert result["brands"] == "Unknown"
    assert result["ingredients_text"] == ""


@patch("app.openfoodfacts.requests.get")
def test_fetch_by_barcode_connection_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError("Network down")

    result = openfoodfacts.fetch_by_barcode("3017620422003")

    assert result is None


@patch("app.openfoodfacts.requests.get")
def test_fetch_by_barcode_http_error(mock_get):
    mock_get.return_value = _mock_response(
        {}, status_code=500, raise_error=requests.exceptions.HTTPError("Server error")
    )

    result = openfoodfacts.fetch_by_barcode("3017620422003")

    assert result is None