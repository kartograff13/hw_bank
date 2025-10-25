from unittest.mock import patch

import pandas as pd
import pytest

from src.financial_reader import read_financial_csv, read_financial_excel


def test_read_financial_csv_success() -> None:
    """Тест успешного чтения CSV файла"""
    mock_data = pd.DataFrame(
        {"date": ["2023-01-01", "2023-01-02"], "amount": [100.0, -50.0], "description": ["Deposit", "Withdrawal"]}
    )

    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read_csv:
        mock_exists.return_value = True
        mock_read_csv.return_value = mock_data
        result = read_financial_csv("/fake/path/transactions.csv")
        mock_exists.assert_called_once_with("/fake/path/transactions.csv")
        mock_read_csv.assert_called_once_with("/fake/path/transactions.csv")

        expected = [
            {"date": "2023-01-01", "amount": 100.0, "description": "Deposit"},
            {"date": "2023-01-02", "amount": -50.0, "description": "Withdrawal"},
        ]

        assert result == expected
        assert isinstance(result, list)
        assert all(isinstance(item, dict) for item in result)


def test_read_financial_csv_file_not_found() -> None:
    """Тест обработки отсутствующего CSV файла"""
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False

        with pytest.raises(FileNotFoundError) as exc_info:
            read_financial_csv("/fake/path/nonexistent.csv")

        assert "Файл /fake/path/nonexistent.csv не найден." in str(exc_info.value)


def test_read_financial_csv_empty_file() -> None:
    """Тест чтения пустого CSV файла"""
    mock_data = pd.DataFrame()

    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read_csv:
        mock_exists.return_value = True
        mock_read_csv.return_value = mock_data
        result = read_financial_csv("/fake/path/empty.csv")

        assert result == []
        assert isinstance(result, list)


def test_read_financial_excel_success() -> None:
    """Тест успешного чтения Excel файла"""
    mock_data = pd.DataFrame(
        {"date": ["2023-01-01", "2023-01-02"], "amount": [200.0, -75.0], "category": ["Income", "Expense"]}
    )

    with patch("os.path.exists") as mock_exists, patch("pandas.read_excel") as mock_read_excel:
        mock_exists.return_value = True
        mock_read_excel.return_value = mock_data
        result = read_financial_excel("/fake/path/transactions.xlsx")
        mock_exists.assert_called_once_with("/fake/path/transactions.xlsx")
        mock_read_excel.assert_called_once_with("/fake/path/transactions.xlsx", sheet_name=0)

        expected = [
            {"date": "2023-01-01", "amount": 200.0, "category": "Income"},
            {"date": "2023-01-02", "amount": -75.0, "category": "Expense"},
        ]

        assert result == expected


def test_read_financial_excel_with_sheet_name() -> None:
    """Тест чтения Excel файла с указанием имени листа"""
    mock_data = pd.DataFrame({"transaction_id": [1, 2], "amount": [100.0, 200.0]})

    with patch("os.path.exists") as mock_exists, patch("pandas.read_excel") as mock_read_excel:
        mock_exists.return_value = True
        mock_read_excel.return_value = mock_data
        result = read_financial_excel("/fake/path/transactions.xlsx", sheet_name="Sheet2")
        mock_read_excel.assert_called_once_with("/fake/path/transactions.xlsx", sheet_name="Sheet2")

        expected = [{"transaction_id": 1, "amount": 100.0}, {"transaction_id": 2, "amount": 200.0}]

        assert result == expected


def test_read_financial_excel_with_sheet_index() -> None:
    """Тест чтения Excel файла с указанием индекса листа"""
    mock_data = pd.DataFrame({"data": ["test"]})

    with patch("os.path.exists") as mock_exists, patch("pandas.read_excel") as mock_read_excel:
        mock_exists.return_value = True
        mock_read_excel.return_value = mock_data
        result = read_financial_excel("/fake/path/transactions.xlsx", sheet_name=2)
        mock_read_excel.assert_called_once_with("/fake/path/transactions.xlsx", sheet_name=2)

        assert result == [{"data": "test"}]


def test_read_financial_excel_file_not_found() -> None:
    """Тест обработки отсутствующего Excel файла"""
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False

        with pytest.raises(FileNotFoundError) as exc_info:
            read_financial_excel("/fake/path/nonexistent.xlsx")

        assert "Файл /fake/path/nonexistent.xlsx не найден." in str(exc_info.value)


def test_read_financial_excel_empty_file() -> None:
    """Тест чтения пустого Excel файла"""
    mock_data = pd.DataFrame()

    with patch("os.path.exists") as mock_exists, patch("pandas.read_excel") as mock_read_excel:
        mock_exists.return_value = True
        mock_read_excel.return_value = mock_data
        result = read_financial_excel("/fake/path/empty.xlsx")

        assert result == []
        assert isinstance(result, list)


def test_return_type_consistency() -> None:
    """Тест на согласованность типов возвращаемых данных"""
    mock_data = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})

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
