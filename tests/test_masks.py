import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number():
    """Тест функции get_mask_card_number при корректном вводе данных"""
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"
    assert get_mask_card_number("7000 7922 8960 6361") == "7000 79** **** 6361"


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("123", "Вы ввели не существующий номер карты."),
        ("", "Вы ввели не существующий номер карты."),
        ("7OOO79228960636i", "Вы ввели не существующий номер карты."),
        ("{*jks/-+]", "Вы ввели не существующий номер карты."),
    ],
)
def test_get_mask_card_number_wrong_numbers(card_number, expected):
    """Тест функции get_mask_card_number при некорректном вводе данных"""
    assert get_mask_card_number(card_number) == expected


def test_get_mask_account():
    """Тест функции get_mask_account при корректном вводе данных"""
    assert get_mask_account("73654108430135874305") == "**4305"
    assert get_mask_account("7365 4108 4301 3587 4305") == "**4305"


@pytest.mark.parametrize(
    "account, expected",
    [
        ("24645", "Вы ввели не существующий номер счёта."),
        ("", "Вы ввели не существующий номер счёта."),
        ("73654i08430i358743O5", "Вы ввели не существующий номер счёта."),
        ("&%wrf$-.", "Вы ввели не существующий номер счёта."),
    ],
)
def test_get_mask_account_wrong_numbers(account, expected):
    """Тест функции get_mask_account при некорректном вводе данных"""
    assert get_mask_account(account) == expected
