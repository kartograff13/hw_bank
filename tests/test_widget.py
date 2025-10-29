from typing import Any, Tuple

import pytest

from src.widget import get_date, mask_account_card


@pytest.fixture
def valid_card_data() -> list[Tuple[str, str]]:
    """Данные для валидных номеров карт"""
    return [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
        ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
        ("Discover 1234567890123456", "Discover 1234 56** **** 3456"),
        ("American Express 1234567890123456", "American Express 1234 56** **** 3456"),
        ("мир 1234567890123456", "мир 1234 56** **** 3456"),
        ("discover 1234567890123456", "discover 1234 56** **** 3456"),
        ("american express 1234567890123456", "american express 1234 56** **** 3456"),
        ("maestro 1596837868705199", "maestro 1596 83** **** 5199"),
    ]


@pytest.fixture
def valid_account_data() -> list[Tuple[str, str]]:
    """Данные для валидных номеров счетов"""
    return [
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Счет 12345678901234567890", "Счет **7890"),
        ("счет 64686473678894779589", "счет **9589"),
    ]


@pytest.fixture
def invalid_data() -> list[Tuple[Any, str]]:
    """Данные для невалидных входных данных"""
    return [
        (None, "Неизвестный отправитель"),
        ("", "Неизвестный отправитель"),
        ("   ", "Неизвестный отправитель"),
        ("Mastro 1596837868705199", "Неизвестный отправитель"),
        ("Maestro 15968378687051991", "Неизвестный отправитель"),
        ("Maestro 159683786870519", "Неизвестный отправитель"),
        ("Счет 6468647367889477958", "Неизвестный отправитель"),
        ("Счет 646864736788947795890", "Неизвестный отправитель"),
        ("MasterVisa 7i583OO7347267581", "Неизвестный отправитель"),
        ("Visa Classic 683198247673765", "Неизвестный отправитель"),
        ("{*jks/-+]123", "Неизвестный отправитель"),
        ("CardOnly", "Неизвестный отправитель"),
        ("1234567890123456", "Неизвестный отправитель"),
    ]


@pytest.fixture
def edge_cases_data() -> list[Tuple[str, str]]:
    """Данные для граничных случаев"""
    return [
        ("  Maestro  1596837868705199  ", "Maestro 1596 83** **** 5199"),
        ("  Счет  64686473678894779589  ", "Счет **9589"),
    ]


def test_mask_account_card_valid_cards(valid_card_data: list[Tuple[str, str]]) -> None:
    """Тест для валидных номеров карт"""
    for account_info, expected in valid_card_data:
        assert mask_account_card(account_info) == expected


def test_mask_account_card_valid_accounts(valid_account_data: list[Tuple[str, str]]) -> None:
    """Тест для валидных номеров счетов"""
    for account_info, expected in valid_account_data:
        assert mask_account_card(account_info) == expected


def test_mask_account_card_invalid_data(invalid_data: list[Tuple[Any, str]]) -> None:
    """Тест для невалидных входных данных"""
    for account_info, expected in invalid_data:
        assert mask_account_card(account_info) == expected


def test_mask_account_card_edge_cases(edge_cases_data: list[Tuple[str, str]]) -> None:
    """Тест для граничных случаев"""
    for account_info, expected in edge_cases_data:
        assert mask_account_card(account_info) == expected


@pytest.fixture
def valid_dates() -> list[Tuple[str, str]]:
    """Данные для валидных дат"""
    return [
        ("2024-04-10T12:30:00", "10.04.2024"),
        ("2023-12-31T23:59:59", "31.12.2023"),
        ("2020-01-01T00:00:00", "01.01.2020"),
        ("2023-12-31", "31.12.2023"),
        ("2024-02-29T00:00:00", "29.02.2024"),
    ]


@pytest.fixture
def invalid_dates() -> list[Tuple[str, str]]:
    """Данные для невалидных дат"""
    return [
        ("23-12-11", "Неверный ввод даты"),
        ("", "Неверный ввод даты"),
        ("2023-13-45", "Неверный ввод даты"),
        ("2023-02-29", "Неверный ввод даты"),
        ("invalid-date", "Неверный ввод даты"),
    ]


def test_get_date_valid_dates(valid_dates: list[Tuple[str, str]]) -> None:
    """Тест для валидных дат"""
    for date_str, expected in valid_dates:
        assert get_date(date_str) == expected


def test_get_date_invalid_dates(invalid_dates: list[Tuple[str, str]]) -> None:
    """Тест для невалидных дат"""
    for date_str, expected in invalid_dates:
        assert get_date(date_str) == expected
