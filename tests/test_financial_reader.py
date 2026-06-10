from unittest.mock import patch

import pandas as pd
import pytest

from src.financial_reader import read_financial_csv, read_financial_excel


def test_read_financial_csv_success() -> None:
    """Тест успешного чтения CSV-файла"""
    mock_data = pd.DataFrame(
        {
            "id": [1, 2],
            "state": ["EXECUTED", "PENDING"],
            "date": ["2023-01-01", "2023-01-02"],
            "amount": [100.0, -50.0],
            "currency_name": ["USD", "EUR"],
            "currency_code": ["USD", "EUR"],
            "description": ["Deposit", "Withdrawal"],
            "from": ["Account A", "Account B"],
            "to": ["Account C", "Account D"],
        }
    )

    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read_csv:
        mock_exists.return_value = True
        mock_read_csv.return_value = mock_data
        result = read_financial_csv("/fake/path/transactions.csv")

        mock_exists.assert_called_once_with("/fake/path/transactions.csv")
        mock_read_csv.assert_called_once_with("/fake/path/transactions.csv", sep=";")

        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["state"] == "EXECUTED"
        assert result[0]["date"] == "2023-01-01"
        assert result[0]["operationAmount"]["amount"] == "100.0"
        assert result[0]["operationAmount"]["currency"]["name"] == "USD"
        assert result[0]["operationAmount"]["currency"]["code"] == "USD"
        assert result[0]["description"] == "Deposit"
        assert result[0]["from"] == "Account A"
        assert result[0]["to"] == "Account C"


def test_read_financial_csv_file_not_found() -> None:
    """Тест обработки отсутствующего CSV-файла"""
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False

        with pytest.raises(FileNotFoundError) as exc_info:
            read_financial_csv("/fake/path/nonexistent.csv")

        assert "Файл /fake/path/nonexistent.csv не найден." in str(exc_info.value)


def test_read_financial_csv_empty_file() -> None:
    """Тест чтения пустого CSV-файла"""
    mock_data = pd.DataFrame()

    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read_csv:
        mock_exists.return_value = True
        mock_read_csv.return_value = mock_data
        result = read_financial_csv("/fake/path/empty.csv")

        assert result == []
        assert isinstance(result, list)


def test_read_financial_excel_success() -> None:
    """Тест успешного чтения Excel-файла"""
    mock_data = pd.DataFrame(
        {
            "id": [3, 4],
            "state": ["EXECUTED", "CANCELED"],
            "date": ["2023-01-01", "2023-01-02"],
            "amount": [200.0, -75.0],
            "currency_name": ["GBP", "JPY"],
            "currency_code": ["GBP", "JPY"],
            "description": ["Income", "Expense"],
            "from": ["Account X", "Account Y"],
            "to": ["Account Z", "Account W"],
        }
    )

    with patch("os.path.exists") as mock_exists, patch("pandas.read_excel") as mock_read_excel:
        mock_exists.return_value = True
        mock_read_excel.return_value = mock_data
        result = read_financial_excel("/fake/path/transactions.xlsx")

        mock_exists.assert_called_once_with("/fake/path/transactions.xlsx")
        mock_read_excel.assert_called_once_with("/fake/path/transactions.xlsx", sheet_name=0)

        assert len(result) == 2
        assert result[0]["id"] == 3
        assert result[0]["state"] == "EXECUTED"
        assert result[0]["date"] == "2023-01-01"
        assert result[0]["operationAmount"]["amount"] == "200.0"
        assert result[0]["operationAmount"]["currency"]["name"] == "GBP"
        assert result[0]["operationAmount"]["currency"]["code"] == "GBP"
        assert result[0]["description"] == "Income"
        assert result[0]["from"] == "Account X"
        assert result[0]["to"] == "Account Z"


def test_read_financial_excel_with_sheet_name() -> None:
    """Тест чтения Excel-файла с указанием имени листа"""
    mock_data = pd.DataFrame(
        {
            "id": [5, 6],
            "state": ["EXECUTED", "EXECUTED"],
            "date": ["2023-01-03", "2023-01-04"],
            "amount": [100.0, 200.0],
            "currency_name": ["USD", "USD"],
            "currency_code": ["USD", "USD"],
            "description": ["Transfer", "Transfer"],
            "from": ["Acc1", "Acc2"],
            "to": ["Acc3", "Acc4"],
        }
    )

    with patch("os.path.exists") as mock_exists, patch("pandas.read_excel") as mock_read_excel:
        mock_exists.return_value = True
        mock_read_excel.return_value = mock_data
        result = read_financial_excel("/fake/path/transactions.xlsx", sheet_name="Sheet2")
        mock_read_excel.assert_called_once_with("/fake/path/transactions.xlsx", sheet_name="Sheet2")

        assert len(result) == 2
        assert result[0]["id"] == 5
        assert result[0]["operationAmount"]["amount"] == "100.0"


def test_read_financial_excel_with_sheet_index() -> None:
    """Тест чтения Excel-файла с указанием индекса листа"""
    mock_data = pd.DataFrame(
        {
            "id": [7],
            "state": ["PENDING"],
            "date": ["2023-01-05"],
            "amount": [150.0],
            "currency_name": ["EUR"],
            "currency_code": ["EUR"],
            "description": ["Test"],
            "from": ["Test1"],
            "to": ["Test2"],
        }
    )

    with patch("os.path.exists") as mock_exists, patch("pandas.read_excel") as mock_read_excel:
        mock_exists.return_value = True
        mock_read_excel.return_value = mock_data
        result = read_financial_excel("/fake/path/transactions.xlsx", sheet_name=2)
        mock_read_excel.assert_called_once_with("/fake/path/transactions.xlsx", sheet_name=2)

        assert len(result) == 1
        assert result[0]["id"] == 7
        assert result[0]["description"] == "Test"


def test_read_financial_excel_file_not_found() -> None:
    """Тест обработки отсутствующего Excel-файла"""
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False

        with pytest.raises(FileNotFoundError) as exc_info:
            read_financial_excel("/fake/path/nonexistent.xlsx")

        assert "Файл /fake/path/nonexistent.xlsx не найден." in str(exc_info.value)


def test_read_financial_excel_empty_file() -> None:
    """Тест чтения пустого Excel-файла"""
    mock_data = pd.DataFrame()

    with patch("os.path.exists") as mock_exists, patch("pandas.read_excel") as mock_read_excel:
        mock_exists.return_value = True
        mock_read_excel.return_value = mock_data
        result = read_financial_excel("/fake/path/empty.xlsx")

        assert result == []
        assert isinstance(result, list)


def test_return_type_consistency() -> None:
    """Тест на согласованность типов возвращаемых данных"""
    mock_data = pd.DataFrame(
        {
            "id": [1, 2],
            "state": ["EXECUTED", "PENDING"],
            "date": ["2023-01-01", "2023-01-02"],
            "amount": [100.0, 200.0],
            "currency_name": ["USD", "EUR"],
            "currency_code": ["USD", "EUR"],
            "description": ["Test1", "Test2"],
            "from": ["A", "B"],
            "to": ["C", "D"],
        }
    )

    with (
        patch("os.path.exists") as mock_exists,
        patch("pandas.read_csv") as mock_read_csv,
        patch("pandas.read_excel") as mock_read_excel,
    ):
        mock_exists.return_value = True
        mock_read_csv.return_value = mock_data
        mock_read_excel.return_value = mock_data
        csv_result = read_financial_csv("/fake/path/test.csv")
        excel_result = read_financial_excel("/fake/path/test.xlsx")

        assert isinstance(csv_result, list)
        assert isinstance(excel_result, list)
        assert all(isinstance(item, dict) for item in csv_result)
        assert all(isinstance(item, dict) for item in excel_result)

        assert len(csv_result) == len(excel_result) == 2
        assert "operationAmount" in csv_result[0]
        assert "operationAmount" in excel_result[0]
        assert isinstance(csv_result[0]["operationAmount"], dict)
        assert isinstance(excel_result[0]["operationAmount"], dict)


def test_safe_str_none() -> None:
    """Тест safe_str с None значением"""
    mock_data = pd.DataFrame(
        {
            "id": [1],
            "state": ["EXECUTED"],
            "date": ["2023-01-01"],
            "amount": [100.0],
            "currency_name": ["USD"],
            "currency_code": ["USD"],
            "description": ["Test"],
            "from": [None],
            "to": [None],
        }
    )

    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read_csv:
        mock_exists.return_value = True
        mock_read_csv.return_value = mock_data
        result = read_financial_csv("/fake/path/test.csv")

        assert result[0]["from"] is None
        assert result[0]["to"] is None


def test_safe_str_nan_float() -> None:
    """Тест safe_str с NaN float значением"""
    mock_data = pd.DataFrame(
        {
            "id": [1],
            "state": ["EXECUTED"],
            "date": ["2023-01-01"],
            "amount": [100.0],
            "currency_name": ["USD"],
            "currency_code": ["USD"],
            "description": ["Test"],
            "from": [float("nan")],
            "to": [float("nan")],
        }
    )

    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read_csv:
        mock_exists.return_value = True
        mock_read_csv.return_value = mock_data
        result = read_financial_csv("/fake/path/test.csv")

        assert result[0]["from"] is None
        assert result[0]["to"] is None


def test_safe_str_float_integer() -> None:
    """Тест safe_str с float, представляющим целое число"""
    mock_data = pd.DataFrame(
        {
            "id": [1],
            "state": ["EXECUTED"],
            "date": ["2023-01-01"],
            "amount": [100.0],
            "currency_name": ["USD"],
            "currency_code": ["USD"],
            "description": ["Test"],
            "from": [100.0],
            "to": [200.0],
        }
    )

    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read_csv:
        mock_exists.return_value = True
        mock_read_csv.return_value = mock_data
        result = read_financial_csv("/fake/path/test.csv")

        assert result[0]["from"] == "100"
        assert result[0]["to"] == "200"


def test_safe_str_float_decimal() -> None:
    """Тест safe_str с float, имеющим дробную часть"""
    mock_data = pd.DataFrame(
        {
            "id": [1],
            "state": ["EXECUTED"],
            "date": ["2023-01-01"],
            "amount": [100.0],
            "currency_name": ["USD"],
            "currency_code": ["USD"],
            "description": ["Test"],
            "from": [100.5],
            "to": [200.75],
        }
    )

    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read_csv:
        mock_exists.return_value = True
        mock_read_csv.return_value = mock_data
        result = read_financial_csv("/fake/path/test.csv")

        assert result[0]["from"] == "100.5"
        assert result[0]["to"] == "200.75"


def test_safe_str_integer() -> None:
    """Тест safe_str с целыми числами"""
    mock_data = pd.DataFrame(
        {
            "id": [1],
            "state": ["EXECUTED"],
            "date": ["2023-01-01"],
            "amount": [100.0],
            "currency_name": ["USD"],
            "currency_code": ["USD"],
            "description": ["Test"],
            "from": [123],
            "to": [456],
        }
    )

    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read_csv:
        mock_exists.return_value = True
        mock_read_csv.return_value = mock_data
        result = read_financial_csv("/fake/path/test.csv")

        assert result[0]["from"] == "123"
        assert result[0]["to"] == "456"


def test_safe_str_string() -> None:
    """Тест safe_str со строковыми значениями"""
    mock_data = pd.DataFrame(
        {
            "id": [1],
            "state": ["EXECUTED"],
            "date": ["2023-01-01"],
            "amount": [100.0],
            "currency_name": ["USD"],
            "currency_code": ["USD"],
            "description": ["Test"],
            "from": ["Account 123"],
            "to": ["Account 456"],
        }
    )

    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read_csv:
        mock_exists.return_value = True
        mock_read_csv.return_value = mock_data
        result = read_financial_csv("/fake/path/test.csv")

        assert result[0]["from"] == "Account 123"
        assert result[0]["to"] == "Account 456"


def test_safe_str_mixed_types() -> None:
    """Тест safe_str с различными типами данных в одном наборе"""
    mock_data = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "state": ["EXECUTED"] * 5,
            "date": ["2023-01-01"] * 5,
            "amount": [100.0] * 5,
            "currency_name": ["USD"] * 5,
            "currency_code": ["USD"] * 5,
            "description": ["Test"] * 5,
            "from": [None, 100.0, 100.5, 200, "Account A"],
            "to": ["Account B", None, 300.75, 400, None],
        }
    )

    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read_csv:
        mock_exists.return_value = True
        mock_read_csv.return_value = mock_data
        result = read_financial_csv("/fake/path/test.csv")

        assert result[0]["from"] is None
        assert result[0]["to"] == "Account B"

        assert result[1]["from"] == "100"
        assert result[1]["to"] is None

        assert result[2]["from"] == "100.5"
        assert result[2]["to"] == "300.75"

        assert result[3]["from"] == "200"
        assert result[3]["to"] == "400"

        assert result[4]["from"] == "Account A"
        assert result[4]["to"] is None
