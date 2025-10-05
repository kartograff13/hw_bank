from typing import Iterator


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]:
    """Возвращает итератор, который выдает транзакции с заданной валютой"""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions: list[dict]) -> Iterator[dict]:
    """Генератор, который возвращает описание каждой операции"""
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Генератор, который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX в заданном диапазоне"""
    for number in range(start, end + 1):
        formatted_number = f"{number:016d}"
        yield " ".join([formatted_number[i: i + 4] for i in range(0, 16, 4)])
