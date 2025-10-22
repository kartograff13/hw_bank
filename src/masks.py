import logging
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

logger_card = logging.getLogger("card_number_logger")
logger_card.setLevel(logging.INFO)
card_handler = logging.FileHandler(os.path.join(LOGS_DIR, "card_number_logger.log"), mode="w", encoding="utf-8")
card_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)
card_handler.setFormatter(card_formatter)
logger_card.addHandler(card_handler)

logger_account = logging.getLogger("account_number_logger")
logger_account.setLevel(logging.INFO)
account_handler = logging.FileHandler(os.path.join(LOGS_DIR, "account_number_logger.log"), mode="w", encoding="utf-8")
account_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)
account_handler.setFormatter(account_formatter)
logger_account.addHandler(account_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция маскирует номер банковской карты"""
    try:
        card_number_str = card_number.replace(" ", "")

        if card_number_str.isdigit() and len(card_number_str) == 16:
            masked_card_number = f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"
            logger_card.info(f"Успешная маскировка карты: {card_number_str}")
            return masked_card_number

        error_message = "Вы ввели не существующий номер карты."
        logger_card.error(f"Ошибка маскировки номера счёта: {card_number}")
        return error_message

    except Exception as e:
        error_message = f"Ошибка обработки номера карты: {str(e)}"
        logger_card.error(f"Ошибка маскировки карты: {card_number}")
        return error_message


def get_mask_account(account_number: str) -> str:
    """Функция маскирует банковский счёт"""
    try:
        account_number_str = account_number.replace(" ", "")

        if account_number_str.isdigit() and len(account_number_str) == 20:
            masked_account_number = f"**{account_number_str[-4:]}"
            logger_account.info(f"Успешная маскировка счёта: {account_number_str}")
            return masked_account_number

        error_message = "Вы ввели не существующий номер счёта."
        logger_account.error(f"Ошибка маскировки счёта: {account_number}")
        return error_message

    except Exception as e:
        error_message = f"Ошибка обработки счёта: {str(e)}"
        logger_account.error(f"Ошибка маскировки счёта: {account_number} - {str(e)}")
        return error_message
