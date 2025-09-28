import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("7000 7922 8960 6361", "7000 79** **** 6361"),
        ("123", "Вы ввели не существующий номер карты."),
        ("", "Вы ввели не существующий номер карты."),
        ("7OOO79228960636i", "Вы ввели не существующий номер карты."),
        ("{*jks/-+]", "Вы ввели не существующий номер карты."),
    ],
)
def test_get_mask_card_number(card_number: str, expected: str) -> None:
    """Тест функции get_mask_card_number"""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "account_info, expected",
    [
        ("73654108430135874305", "**4305"),
        ("7365 4108 4301 3587 4305", "**4305"),
        ("24645", "Вы ввели не существующий номер счёта."),
        ("", "Вы ввели не существующий номер счёта."),
        ("73654i08430i358743O5", "Вы ввели не существующий номер счёта."),
        ("&%wrf$-.", "Вы ввели не существующий номер счёта."),
    ],
)
def test_get_mask_account(account_info: str, expected: str) -> None:
    """Тест функции get_mask_account"""
    assert get_mask_account(account_info) == expected
