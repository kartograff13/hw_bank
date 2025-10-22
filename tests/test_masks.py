from typing import Any, Tuple

import pytest

from src.masks import get_mask_account, get_mask_card_number

CardTestCase = Tuple[str, str]
AccountTestCase = Tuple[str, str]


@pytest.fixture(
    params=[
        ("7000792289606361", "7000 79** **** 6361"),
        ("7000 7922 8960 6361", "7000 79** **** 6361"),
    ]
)
def valid_card_cases(request: pytest.FixtureRequest) -> CardTestCase:
    case: CardTestCase = request.param
    return case


@pytest.fixture(
    params=[
        ("123", "Вы ввели не существующий номер карты."),
        ("", "Вы ввели не существующий номер карты."),
        ("7OOO79228960636i", "Вы ввели не существующий номер карты."),
    ]
)
def invalid_card_cases(request: pytest.FixtureRequest) -> CardTestCase:
    case: CardTestCase = request.param
    return case


@pytest.fixture(
    params=[
        ("73654108430135874305", "**4305"),
        ("7365 4108 4301 3587 4305", "**4305"),
    ]
)
def valid_account_cases(request: pytest.FixtureRequest) -> AccountTestCase:
    case: AccountTestCase = request.param
    return case


@pytest.fixture(
    params=[
        ("24645", "Вы ввели не существующий номер счёта."),
        ("", "Вы ввели не существующий номер счёта."),
        ("73654i08430i358743O5", "Вы ввели не существующий номер счёта."),
    ]
)
def invalid_account_cases(request: pytest.FixtureRequest) -> AccountTestCase:
    case: AccountTestCase = request.param
    return case


@pytest.fixture(
    params=[
        (1234567812345678, "Ошибка обработки номера карты: 'int' object has no attribute 'replace'"),
        (7000.792289606361, "Ошибка обработки номера карты: 'float' object has no attribute 'replace'"),
        (None, "Ошибка обработки номера карты: 'NoneType' object has no attribute 'replace'"),
        (True, "Ошибка обработки номера карты: 'bool' object has no attribute 'replace'"),
        (["7000792289606361"], "Ошибка обработки номера карты: 'list' object has no attribute 'replace'"),
        ({"card": "7000792289606361"}, "Ошибка обработки номера карты: 'dict' object has no attribute 'replace'"),
    ]
)
def different_types_card_cases(request: pytest.FixtureRequest) -> Tuple[Any, str]:
    case: Tuple[Any, str] = request.param
    return case


@pytest.fixture(
    params=[
        ("73654108430135874305", "**4305"),
        ("7365 4108 4301 3587 4305", "**4305"),
        ("24645", "Вы ввели не существующий номер счёта."),
        ("", "Вы ввели не существующий номер счёта."),
        ("73654i08430i358743O5", "Вы ввели не существующий номер счёта."),
        (1234567812345678, "Ошибка обработки счёта: 'int' object has no attribute 'replace'"),
        (73654108430135874305, "Ошибка обработки счёта: 'int' object has no attribute 'replace'"),
        (73654108430135874305.0, "Ошибка обработки счёта: 'float' object has no attribute 'replace'"),
        (None, "Ошибка обработки счёта: 'NoneType' object has no attribute 'replace'"),
        (True, "Ошибка обработки счёта: 'bool' object has no attribute 'replace'"),
        (False, "Ошибка обработки счёта: 'bool' object has no attribute 'replace'"),
        (["73654108430135874305"], "Ошибка обработки счёта: 'list' object has no attribute 'replace'"),
        ({"account": "73654108430135874305"}, "Ошибка обработки счёта: 'dict' object has no attribute 'replace'"),
    ]
)
def different_types_account_cases(request: pytest.FixtureRequest) -> Tuple[Any, str]:
    case: Tuple[Any, str] = request.param
    return case


def test_valid_card_cases(valid_card_cases: CardTestCase) -> None:
    card_number, expected = valid_card_cases
    assert get_mask_card_number(card_number) == expected


def test_invalid_card_cases(invalid_card_cases: CardTestCase) -> None:
    card_number, expected = invalid_card_cases
    assert get_mask_card_number(card_number) == expected


def test_valid_account_cases(valid_account_cases: AccountTestCase) -> None:
    account_number, expected = valid_account_cases
    assert get_mask_account(account_number) == expected


def test_invalid_account_cases(invalid_account_cases: AccountTestCase) -> None:
    account_number, expected = invalid_account_cases
    assert get_mask_account(account_number) == expected


def test_different_types_card_cases(different_types_card_cases: Tuple[Any, str]) -> None:
    card_number, expected = different_types_card_cases
    assert get_mask_card_number(card_number) == expected


def test_different_types_account_cases(different_types_account_cases: Tuple[Any, str]) -> None:
    account_number, expected = different_types_account_cases
    assert get_mask_account(account_number) == expected
