import argparse
from unittest.mock import patch, Mock

import requests

from cli import cli as cli_module


def _mock_response(json_data, status_code=200):
    mock_resp = Mock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data
    mock_resp.raise_for_status.return_value = None
    return mock_resp

@patch("cli.cli.requests.request")
def test_handle_request_connection_error(mock_request, capsys):
    mock_request.side_effect = requests.exceptions.ConnectionError("refused")

    result = cli_module.handle_request("GET", cli_module.BASE_URL)

    assert result is None
    captured = capsys.readouterr()
    assert "Error connecting to server" in captured.out


@patch("cli.cli.requests.request")
def test_handle_request_404(mock_request, capsys):
    mock_request.return_value = _mock_response({"error": "not found"}, status_code=404)

    result = cli_module.handle_request("GET", cli_module.BASE_URL)

    assert result is None
    captured = capsys.readouterr()
    assert "Not found." in captured.out


@patch("cli.cli.requests.request")
def test_view_all_items_prints_inventory(mock_request, capsys):
    mock_request.return_value = _mock_response([
        {"id": 1, "product_name": "Almond Milk"},
        {"id": 2, "product_name": "Peanut Butter"},
    ])

    cli_module.view_all_items(argparse.Namespace())

    mock_request.assert_called_once_with("GET", cli_module.BASE_URL, timeout=5)
    captured = capsys.readouterr()
    assert "Almond Milk" in captured.out


@patch("cli.cli.requests.request")
def test_view_all_items_empty_inventory(mock_request, capsys):
    mock_request.return_value = _mock_response([])

    cli_module.view_all_items(argparse.Namespace())

    captured = capsys.readouterr()
    assert "Inventory is empty" in captured.out


@patch("cli.cli.requests.request")
def test_view_specific_item_found(mock_request, capsys):
    mock_request.return_value = _mock_response({"id": 1, "product_name": "Almond Milk"})

    cli_module.view_specific_item(argparse.Namespace(id=1))

    mock_request.assert_called_once_with("GET", f"{cli_module.BASE_URL}/1", timeout=5)
    captured = capsys.readouterr()
    assert "Almond Milk" in captured.out


@patch("cli.cli.requests.request")
def test_view_specific_item_not_found(mock_request, capsys):
    mock_request.return_value = _mock_response({"error": "Item not found"}, status_code=404)

    cli_module.view_specific_item(argparse.Namespace(id=999))

    captured = capsys.readouterr()
    assert "Not found." in captured.out


@patch("cli.cli.requests.request")
def test_add_item_sends_correct_payload(mock_request, capsys):
    mock_request.return_value = _mock_response({"id": 3, "product_name": "Oat Milk"}, status_code=201)

    args = argparse.Namespace(
        name="Oat Milk", brand="Oatly", ingredients="Oats, water",
        barcode="123", price=3.99, stock=10,
    )
    cli_module.add_item(args)

    mock_request.assert_called_once_with(
        "POST",
        cli_module.BASE_URL,
        timeout=5,
        json={
            "product_name": "Oat Milk",
            "brands": "Oatly",
            "ingredients_text": "Oats, water",
            "barcode": "123",
            "price": 3.99,
            "stock_quantity": 10,
        },
    )
    captured = capsys.readouterr()
    assert "Item added" in captured.out


@patch("cli.cli.requests.request")
def test_edit_item_only_sends_provided_fields(mock_request, capsys):
    mock_request.return_value = _mock_response({"id": 1, "price": 5.49})

    args = argparse.Namespace(
        id=1, name=None, brand=None, ingredients=None,
        barcode=None, price=5.49, stock=None,
    )
    cli_module.edit_item(args)

    mock_request.assert_called_once_with(
        "PATCH", f"{cli_module.BASE_URL}/1", timeout=5, json={"price": 5.49}
    )
    captured = capsys.readouterr()
    assert "Item updated" in captured.out


def test_edit_item_no_fields_does_not_call_api(capsys):
    args = argparse.Namespace(
        id=1, name=None, brand=None, ingredients=None,
        barcode=None, price=None, stock=None,
    )
    with patch("cli.cli.requests.request") as mock_request:
        cli_module.edit_item(args)
        mock_request.assert_not_called()

    captured = capsys.readouterr()
    assert "Provide at least one field" in captured.out


@patch("cli.cli.requests.request")
def test_delete_item(mock_request, capsys):
    mock_request.return_value = _mock_response({"id": 2, "product_name": "Peanut Butter"})

    cli_module.delete_item(argparse.Namespace(id=2))

    mock_request.assert_called_once_with("DELETE", f"{cli_module.BASE_URL}/2", timeout=5)
    captured = capsys.readouterr()
    assert "Item deleted" in captured.out


@patch("cli.cli.requests.request")
def test_fetch_and_add_success(mock_request, capsys):
    mock_request.return_value = _mock_response({"id": 3, "product_name": "Nutella"}, status_code=201)

    args = argparse.Namespace(barcode="3017620422003", price=5.99, stock=8)
    cli_module.fetch_and_add(args)

    mock_request.assert_called_once_with(
        "POST",
        f"{cli_module.BASE_URL}/lookup/3017620422003",
        timeout=5,
        json={"price": 5.99, "stock_quantity": 8},
    )
    captured = capsys.readouterr()
    assert "Item added from OpenFoodFacts" in captured.out


@patch("cli.cli.requests.request")
def test_fetch_and_add_not_found(mock_request, capsys):
    mock_request.return_value = _mock_response({"error": "not found"}, status_code=404)

    args = argparse.Namespace(barcode="000", price=None, stock=None)
    cli_module.fetch_and_add(args)

    captured = capsys.readouterr()
    assert "Not found." in captured.out