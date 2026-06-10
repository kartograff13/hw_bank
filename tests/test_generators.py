import pytest

from src.generators import (card_number_generator, filter_by_currency,
                            transaction_descriptions)


@pytest.fixture
def sample_transactions() -> list[dict]:
    """Фикстура с примером списка транзакций для тестирования"""
    return [
        {"operationAmount": {"currency": {"code": "USD"}}},
        {"operationAmount": {"currency": {"code": "RUB"}}},
        {"operationAmount": {"currency": {"code": "USD"}}},
    ]


def test_filter_by_currency_single_currency(sample_transactions: list[dict]) -> None:
    """Тест filter_by_currency фильтрации транзакций по валюте USD"""
    result = list(filter_by_currency(sample_transactions, "USD"))
    expected = [
        sample_transactions[0],
        sample_transactions[2],
    ]
    assert result == expected


def test_filter_by_currency_other_currency(sample_transactions: list[dict]) -> None:
    """Тест filter_by_currency фильтрации транзакций по валюте RUB"""
    result = list(filter_by_currency(sample_transactions, "RUB"))
    expected = [sample_transactions[1]]
    assert result == expected


def test_filter_by_currency_no_matching_currency(sample_transactions: list[dict]) -> None:
    """Тест filter_by_currency для случая, когда подходящих транзакций нет"""
    result = list(filter_by_currency(sample_transactions, "GBP"))
    assert result == []


def test_filter_by_currency_empty_transactions() -> None:
    """Тест filter_by_currency обработки пустого списка транзакций."""
    result = list(filter_by_currency([], "USD"))
    assert result == []


def test_transaction_descriptions_multiple_transactions() -> None:
    """Тест transaction_descriptions с несколькими транзакциями"""
    transactions = [
        {"description": "Payment for groceries"},
        {"description": "ATM withdrawal"},
        {"description": "Online transfer"},
    ]
    result = list(transaction_descriptions(transactions))
    expected = ["Payment for groceries", "ATM withdrawal", "Online transfer"]
    assert result == expected


def test_transaction_descriptions_single_transaction() -> None:
    """Тест transaction_descriptions с одной транзакцией"""
    transactions = [{"description": "Initial deposit"}]
    result = list(transaction_descriptions(transactions))
    expected = ["Initial deposit"]
    assert result == expected


def test_transaction_descriptions_empty_list() -> None:
    """Тест transaction_descriptions с пустым списком транзакций"""
    result = list(transaction_descriptions([]))
    expected: list[str] = []
    assert result == expected


def test_transaction_descriptions_generator_behavior() -> None:
    """
    Тест transaction_descriptions проверяет ленивые вычисления (генератор не должен сразу обрабатывать все элементы)
    """
    transactions = [{"description": "First"}, {"description": "Second"}]
    generator = transaction_descriptions(transactions)

    assert next(generator) == "First"
    assert next(generator) == "Second"

    with pytest.raises(StopIteration):
        next(generator)


def test_card_number_generator_single_number() -> None:
    """Тест card_number_generator проверяет генерацию одного номера карты"""
    generator = card_number_generator(1, 1)
    assert next(generator) == "0000 0000 0000 0001"


def test_card_number_generator_range_formatting() -> None:
    """Тест card_number_generator проверяет форматирование номеров в диапазоне"""
    generator = card_number_generator(1, 3)
    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003"
    ]
    assert list(generator) == expected


def test_card_number_generator_large_numbers() -> None:
    """Тест card_number_generator проверяет генерацию больших номеров"""
    generator = card_number_generator(9999999999999998, 9999999999999999)
    expected = [
        "9999 9999 9999 9998",
        "9999 9999 9999 9999"
    ]
    assert list(generator) == expected


def test_card_number_generator_zero_range() -> None:
    """Тест card_number_generator проверяет обработку диапазона с нулем"""
    generator = card_number_generator(0, 1)
    expected = ["0000 0000 0000 0000", "0000 0000 0000 0001"]
    assert list(generator) == expected


def test_card_number_generator_stop_iteration() -> None:
    """Тест card_number_generator проверяет корректное завершение генерации"""
    generator = card_number_generator(1, 1)
    next(generator)
    with pytest.raises(StopIteration):
        next(generator)


def test_card_number_generator_reverse_range() -> None:
    """Тест card_number_generator проверяет пустой результат при обратном диапазоне"""
    generator = card_number_generator(5, 1)
    assert list(generator) == []
