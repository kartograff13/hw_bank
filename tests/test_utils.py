import json
from unittest.mock import Mock, patch

from src.utils import load_transactions_file


@patch("src.utils.os.path.exists")
@patch("src.utils.os.path.getsize")
def test_load_transactions_file_file_not_exists(mock_getsize: Mock, mock_exists: Mock) -> None:
    """Тест когда файл не существует"""
    mock_exists.return_value = False
    result = load_transactions_file()
    assert result == []
    mock_exists.assert_called_once()
    mock_getsize.assert_not_called()


@patch("src.utils.os.path.exists")
@patch("src.utils.os.path.getsize")
def test_load_transactions_file_file_empty(mock_getsize: Mock, mock_exists: Mock) -> None:
    """Тест когда файл существует, но пустой"""
    mock_exists.return_value = True
    mock_getsize.return_value = 0
    result = load_transactions_file()
    assert result == []
    mock_exists.assert_called_once()
    mock_getsize.assert_called_once()


@patch("src.utils.os.path.exists")
@patch("src.utils.os.path.getsize")
@patch("src.utils.json.load")
@patch("src.utils.open")
def test_load_transactions_file_json_decode_error(
    mock_open_func: Mock, mock_json_load: Mock, mock_getsize: Mock, mock_exists: Mock
) -> None:
    """Тест с ошибкой декодирования JSON"""
    mock_exists.return_value = True
    mock_getsize.return_value = 100
    mock_json_load.side_effect = json.JSONDecodeError("Ошибка JSON", "doc", 0)

    result = load_transactions_file()
    assert result == []
    mock_open_func.assert_called_once()


@patch("src.utils.os.path.exists")
@patch("src.utils.os.path.getsize")
@patch("src.utils.json.load")
@patch("src.utils.open")
def test_load_transactions_file_file_not_found_error(
    mock_open_func: Mock, mock_json_load: Mock, mock_getsize: Mock, mock_exists: Mock
) -> None:
    """Тест случая, когда файл не найден после проверки exists"""
    mock_exists.return_value = True
    mock_getsize.return_value = 100
    mock_open_func.side_effect = FileNotFoundError()

    result = load_transactions_file()
    assert result == []
    mock_open_func.assert_called_once()


@patch("src.utils.os.path.exists")
@patch("src.utils.os.path.getsize")
@patch("src.utils.json.load")
@patch("src.utils.open")
def test_load_transactions_file_valid_json_list(
    mock_open_func: Mock, mock_json_load: Mock, mock_getsize: Mock, mock_exists: Mock
) -> None:
    """Тест случая с валидным JSON списком"""
    mock_exists.return_value = True
    mock_getsize.return_value = 100
    expected_data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    mock_json_load.return_value = expected_data

    result = load_transactions_file()
    assert result == expected_data
    mock_open_func.assert_called_once()

    @patch("src.utils.os.path.exists")
    @patch("src.utils.os.path.getsize")
    @patch("src.utils.json.load")
    @patch("src.utils.open")
    def test_load_transactions_file_valid_json_not_list(
        mock_open_func: Mock, mock_json_load: Mock, mock_getsize: Mock, mock_exists: Mock
    ) -> None:
        """Тест случая с валидным JSON, но не списком"""
        mock_exists.return_value = True
        mock_getsize.return_value = 100
        mock_json_load.return_value = {"not": "a list"}

        result = load_transactions_file()
        assert result == []
        mock_open_func.assert_called_once()
