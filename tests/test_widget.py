import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "account_info, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Maestro 15968378687051991", "Вы ввели не существующий номер карты либо счёта."),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Счет 6468647367889477958", "Вы ввели не существующий номер карты либо счёта."),
        ("", "Вы ввели не существующий номер карты либо счёта."),
        ("MasterVisa 7i583OO7347267581", "Вы ввели не существующий номер карты либо счёта."),
        ("Visa Classic 683198247673765", "Вы ввели не существующий номер карты либо счёта."),
        ("{*jks/-+]123", "Вы ввели не существующий номер карты либо счёта.")
    ],
)
def test_mask_account_card(account_info: str, expected: str) -> None:
    """Тест функции mask_account_card"""
    assert mask_account_card(account_info) == expected


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2024-04-10T12:30:00", "10.04.2024"),
        ("2023-12-31T23:59:59", "31.12.2023"),
        ("2020-01-01T00:00:00", "01.01.2020"),
        ("2023-12-31", "31.12.2023"),
        ("23-12-11", "Неверный ввод даты"),
        ("", "Неверный ввод даты"),
        ("2023-13-45", "Неверный ввод даты"),
    ],
)
def test_get_date(date_str: str, expected: str) -> None:
    """Тест функции get_date"""
    assert get_date(date_str) == expected
