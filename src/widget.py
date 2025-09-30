from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """Функция обработки информации карт и счетов"""
    if not account_info or not account_info.strip():
        return "Вы ввели не существующий номер карты либо счёта."

    account_info = account_info.strip()

    parts = account_info.split()
    if len(parts) < 2:
        return "Вы ввели не существующий номер карты либо счёта."

    type_of_account = " ".join(parts[:-1])
    card_number = parts[-1]

    if not card_number.isdigit():
        return "Вы ввели не существующий номер карты либо счёта."

    if type_of_account in ["Maestro", "MasterCard"]:
        if len(card_number) != 16:
            return "Вы ввели не существующий номер карты либо счёта."
        return f"{type_of_account} {get_mask_card_number(card_number)}"
    elif type_of_account.startswith("Visa"):
        if len(card_number) != 16:
            return "Вы ввели не существующий номер карты либо счёта."
        return f"{type_of_account} {get_mask_card_number(card_number)}"
    elif type_of_account == "Счет":
        if len(card_number) != 20:
            return "Вы ввели не существующий номер карты либо счёта."
        return f"{type_of_account} {get_mask_account(card_number)}"
    else:
        return "Вы ввели не существующий номер карты либо счёта."


def get_date(date_str: str) -> str:
    """Функция, которая возвращает строку с датой в формате 'ДД.ММ.ГГГГ'"""
    try:
        transform_date = datetime.fromisoformat(date_str)
        return transform_date.strftime("%d.%m.%Y")
    except ValueError:
        return "Неверный ввод даты"
