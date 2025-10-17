from unittest.mock import Mock, mock_open, patch

from src.utils import load_transactions_file


@patch("os.path.exists")
@patch("os.path.getsize")
def test_load_transactions_file_not_exists_returns_empty_list(mock_getsize: Mock, mock_exists: Mock) -> None:
    """Файл не существует -> возвращается пустой список"""
    mock_exists.return_value = False
    result = load_transactions_file("fake_path.json")
    assert result == []
    mock_exists.assert_called_once_with("fake_path.json")
    mock_getsize.assert_not_called()


@patch("os.path.exists")
@patch("os.path.getsize")
def test_load_transactions_file_empty_file_returns_empty_list(mock_getsize: Mock, mock_exists: Mock) -> None:
    """Файл существует, но пустой -> возвращается пустой список"""
    mock_exists.return_value = True
    mock_getsize.return_value = 0
    result = load_transactions_file("empty_file.json")
    assert result == []
    mock_getsize.assert_called_once_with("empty_file.json")


@patch("builtins.open", new_callable=mock_open, read_data="invalid json")
@patch("os.path.exists")
@patch("os.path.getsize")
def test_load_transactions_file_invalid_json_returns_empty_list(
    mock_getsize: Mock, mock_exists: Mock, mock_file: Mock
) -> None:
    """Ошибка парсинга JSON -> возвращается пустой список"""
    mock_exists.return_value = True
    mock_getsize.return_value = 100
    result = load_transactions_file("invalid.json")
    assert result == []
    mock_file.assert_called_once_with("invalid.json", "r", encoding="utf-8")


@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
@patch("os.path.exists")
@patch("os.path.getsize")
def test_load_transactions_file_non_list_json_returns_empty_list(
    mock_getsize: Mock, mock_exists: Mock, mock_file: Mock
) -> None:
    """JSON есть, но это не список -> возвращается пустой список"""
    mock_exists.return_value = True
    mock_getsize.return_value = 100
    result = load_transactions_file("not_list.json")
    assert result == []
    mock_file.assert_called_once_with("not_list.json", "r", encoding="utf-8")


@patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1}, {"id": 2}]')
@patch("os.path.exists")
@patch("os.path.getsize")
def test_load_transactions_file_valid_list_returns_data(
    mock_getsize: Mock, mock_exists: Mock, mock_file: Mock
) -> None:
    """Успешная загрузка списка -> возвращается список транзакций"""
    mock_exists.return_value = True
    mock_getsize.return_value = 100
    expected = [{"id": 1}, {"id": 2}]
    result = load_transactions_file("valid.json")
    assert result == expected
    mock_file.assert_called_once_with("valid.json", "r", encoding="utf-8")
