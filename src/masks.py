def get_mask_card_number(card_number: str) -> str:
    """Функция маскирует номер банковской карты"""
    card_number = card_number.replace(" ", "")
    if card_number.isdigit() and len(card_number) == 16:
        return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return "Вы ввели не существующий номер карты."


def get_mask_account(account_number: str) -> str:
    """Функция маскирует банковский счёт"""
    account_number = account_number.replace(" ", "")
    if account_number.isdigit() and len(account_number) == 20:
        return f"**{account_number[-4:]}"
    return "Вы ввели не существующий номер счёта."


if __name__ == "__main__":
    print(get_mask_card_number(input("Введите номер своей карты: ")))
    print(get_mask_account(input("Введите номер своего счёта: ")))
