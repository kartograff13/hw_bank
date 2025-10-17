from typing import Any, Generator
from unittest.mock import Mock, patch

import pytest
from requests import RequestException

from src.external_api import get_amount_rub


@pytest.fixture(autouse=True)
def mock_api_key() -> Generator[None, Any, None]:
    """Фикстура для мока API ключа во всех тестах"""
    with patch("src.external_api.api_key", "test-api-key"):
        yield


def test_get_amount_rub() -> None:
    """Тест транзакции в рублях без конвертации"""
    transaction = {"amount": 1000, "currency": "RUB"}
    assert get_amount_rub(transaction) == 1000


@patch("src.external_api.requests.get")
def test_get_amount_rub_usd_transaction(mock_get: Mock) -> None:
    """Тест конвертации USD в RUB"""
    # Мок успешного ответа API
    mock_response = Mock()
    mock_response.json.return_value = {"success": True, "rates": {"RUB": 92.5}}
    mock_get.return_value = mock_response

    transaction = {"amount": 100, "currency": "USD"}
    result = get_amount_rub(transaction)

    assert result == 9250.0
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/latest?base=USD&symbols=RUB", headers={"apikey": "test-api-key"}
    )


@patch("src.external_api.requests.get")
def test_get_amount_rub_eur_transaction(mock_get: Mock) -> None:
    """Тест конвертации EUR в RUB"""
    mock_response = Mock()
    mock_response.json.return_value = {"success": True, "rates": {"RUB": 99.3}}
    mock_get.return_value = mock_response

    transaction = {"amount": 50, "currency": "EUR"}
    result = get_amount_rub(transaction)

    assert result == 4965.0


def test_get_amount_rub_missing_currency() -> None:
    """Тест отсутствия валюты в транзакции"""
    transaction = {"amount": 100}
    with pytest.raises(ValueError, match="Транзакция должна содержать 'amount' и 'currency'"):
        get_amount_rub(transaction)


def test_get_amount_rub_missing_amount() -> None:
    """Тест отсутствия суммы в транзакции"""
    transaction = {"currency": "USD"}
    with pytest.raises(ValueError, match="Транзакция должна содержать 'amount' и 'currency'"):
        get_amount_rub(transaction)


def test_get_amount_rub_invalid_amount() -> None:
    """Тест нечисловой суммы в транзакции"""
    transaction = {"amount": "invalid", "currency": "USD"}
    with pytest.raises(ValueError, match="Сумма транзакции должна быть числом"):
        get_amount_rub(transaction)


def test_get_amount_rub_unsupported_currency() -> None:
    """Тест неподдерживаемой валюты"""
    transaction = {"amount": 100, "currency": "GBP"}
    with pytest.raises(ValueError, match="Неподдерживаемая валюта: GBP"):
        get_amount_rub(transaction)


@patch("src.external_api.requests.get")
def test_get_amount_rub_api_request_exception(mock_get: Mock) -> None:
    """Тест обработки сетевой ошибки"""
    mock_get.side_effect = RequestException("Connection error")

    transaction = {"amount": 100, "currency": "USD"}
    with pytest.raises(Exception, match="Ошибка при запросе к API: Connection error"):
        get_amount_rub(transaction)


@patch("src.external_api.requests.get")
def test_get_amount_rub_api_response_not_successful(mock_get: Mock) -> None:
    """Тест неуспешного ответа от API"""
    mock_response = Mock()
    mock_response.json.return_value = {"success": False, "error": {"info": "Invalid API key"}}
    mock_get.return_value = mock_response

    transaction = {"amount": 100, "currency": "USD"}
    with pytest.raises(Exception, match="Ошибка в ответе API: Invalid API key"):
        get_amount_rub(transaction)


@patch("src.external_api.requests.get")
def test_get_amount_rub_api_missing_rates(mock_get: Mock) -> None:
    """Тест отсутствия курса в ответе API"""
    mock_response = Mock()
    mock_response.json.return_value = {"success": True, "rates": {}}
    mock_get.return_value = mock_response

    transaction = {"amount": 100, "currency": "USD"}
    with pytest.raises(Exception, match="В ответе API отсутствует курс RUB"):
        get_amount_rub(transaction)


@patch("src.external_api.api_key", None)
def test_get_amount_rub_missing_api_key() -> None:
    """Тест отсутствия API-ключа"""
    transaction = {"amount": 100, "currency": "USD"}
    with pytest.raises(ValueError, match="API ключ не найден в переменных окружения"):
        get_amount_rub(transaction)


@patch("src.external_api.requests.get")
def test_get_amount_rub_api_json_decode_error(mock_get: Mock) -> None:
    """Тест ошибки декодирования JSON"""
    mock_response = Mock()
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_get.return_value = mock_response

    transaction = {"amount": 100, "currency": "USD"}
    with pytest.raises(Exception, match="Ошибка при разборе JSON ответа: Invalid JSON"):
        get_amount_rub(transaction)


@patch("src.external_api.requests.get")
def test_get_amount_rub_api_http_error(mock_get: Mock) -> None:
    """Тест HTTP ошибки от API"""
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = RequestException("HTTP Error")
    mock_get.return_value = mock_response

    transaction = {"amount": 100, "currency": "USD"}
    with pytest.raises(Exception, match="Ошибка при запросе к API: HTTP Error"):
        get_amount_rub(transaction)
