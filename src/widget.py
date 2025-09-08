from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """Функция обработки информации карт и счетов"""
    account_info = account_info.strip()
    type_of_account = ""
    card_number = ""
    for item in account_info:
        if item.isalpha():
            type_of_account += item
        else:
            card_number += item

    if type_of_account == "Maestro" or type_of_account == "MasterCard":
        return f"{type_of_account} {get_mask_card_number(card_number)}"
    elif type_of_account[0:4] == "Visa":
        return f"{type_of_account[0:4]} {type_of_account[4:]} {get_mask_card_number(card_number)}"
    elif type_of_account == "Счет":
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


if __name__ == "__main__":
    print(mask_account_card(input("Введите номер своей карты либо счёта: ")))
    print(get_date(input("Введите дату в формате (2024-03-11T02:26:18.671407): ")))
