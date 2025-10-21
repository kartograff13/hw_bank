import logging
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

logger_card = logging.getLogger("card_number_logger")
logger_card.setLevel(logging.INFO)
card_handler = logging.FileHandler("logs/card_number_logger.log", mode="w", encoding="utf-8")
card_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)
card_handler.setFormatter(card_formatter)
logger_card.addHandler(card_handler)

logger_account = logging.getLogger("account_number_logger")
logger_account.setLevel(logging.INFO)
account_handler = logging.FileHandler("logs/account_number_logger.log", mode="w", encoding="utf-8")
account_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)
account_handler.setFormatter(account_formatter)
logger_account.addHandler(account_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция маскирует номер банковской карты"""
    card_number = card_number.replace(" ", "")
    if card_number.isdigit() and len(card_number) == 16:
        masked_card_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        logger_card.info(f"Успешная маскировка карты: {card_number}")
        return masked_card_number
    error_message = "Вы ввели не существующий номер карты."
    logger_card.error(f"Ошибка маскировки карты: {card_number}")
    return error_message


def get_mask_account(account_number: str) -> str:
    """Функция маскирует банковский счёт"""
    account_number = account_number.replace(" ", "")
    if account_number.isdigit() and len(account_number) == 20:
        masked_account_number = f"**{account_number[-4:]}"
        logger_account.info(f"Успешная маскировка счёта: {account_number}")
        return masked_account_number
    error_message = "Вы ввели не существующий номер счёта."
    logger_account.error(f"Ошибка маркировки счёта: {account_number}")
    return error_message
