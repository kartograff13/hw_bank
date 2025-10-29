from datetime import datetime
from typing import Any

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: Any) -> str:
    """Функция обработки информации карт и счетов"""
    if account_info is None:
        return "Неизвестный отправитель"

    if not isinstance(account_info, str):
        account_info = str(account_info)

    account_info = account_info.strip()

    if not account_info:
        return "Неизвестный отправитель"

    parts = account_info.split()
    if len(parts) < 2:
        return "Неизвестный отправитель"

    type_of_account = " ".join(parts[:-1])
    card_number = parts[-1]
    card_number_clean = "".join([char for char in card_number if char.isdigit()])

    if not card_number_clean.isdigit():
        return "Неизвестный отправитель"

    type_lower = type_of_account.lower()

    if type_lower in ["maestro", "mastercard", "мир", "mir", "discover", "american express"]:
        if len(card_number_clean) != 16:
            return "Неизвестный отправитель"
        return f"{type_of_account} {get_mask_card_number(card_number_clean)}"
    elif type_lower.startswith("visa"):
        if len(card_number_clean) != 16:
            return "Неизвестный отправитель"
        return f"{type_of_account} {get_mask_card_number(card_number_clean)}"
    elif type_lower == "счет":
        if len(card_number_clean) != 20:
            return "Неизвестный отправитель"
        return f"{type_of_account} {get_mask_account(card_number_clean)}"
    else:
        return "Неизвестный отправитель"


def get_date(date_str: str) -> str:
    """Функция, которая возвращает строку с датой в формате 'ДД.ММ.ГГГГ'"""
    try:
        transform_date = datetime.fromisoformat(date_str)
        return transform_date.strftime("%d.%m.%Y")
    except ValueError:
        return "Неверный ввод даты"
