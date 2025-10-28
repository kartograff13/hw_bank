import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")


def get_amount_rub(transaction: dict[str, Any]) -> float:
    """Функция конвертирует сумму транзакции в рубли"""

    if "operationAmount" in transaction:
        operation_amount = transaction["operationAmount"]
        amount_str = operation_amount.get("amount")
        currency_info = operation_amount.get("currency", {})
    else:
        amount_str = transaction.get("amount")
        currency_info = (
            transaction.get("currency", {})
            if "currency" in transaction
            else {"code": transaction.get("currency_code", "RUB")}
        )

    if amount_str is None:
        raise ValueError("Транзакция должна содержать 'amount'")

    try:
        amount = float(amount_str)
    except (TypeError, ValueError):
        raise ValueError("Сумма транзакции должна быть числом")

    if isinstance(currency_info, dict):
        currency = str(currency_info.get("code", "RUB")).upper()
    else:
        currency = str(currency_info).upper()

    if currency == "RUB":
        return amount

    if currency in ["USD", "EUR"]:
        if not api_key:
            raise ValueError("API ключ не найден в переменных окружения")

        url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}&symbols=RUB"
        headers = {"apikey": api_key}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            if not data.get("success", True):
                error_info = data.get("error", {}).get("info", "Неизвестная ошибка API")
                raise Exception(f"Ошибка в ответе API: {error_info}")

            if "rates" not in data or "RUB" not in data["rates"]:
                raise Exception("В ответе API отсутствует курс RUB")

            rate = data["rates"]["RUB"]
            return float(amount * rate)

        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросe к API: {e}")
        except ValueError as e:
            raise Exception(f"Ошибка при разборе JSON ответа: {e}")

    raise ValueError(f"Неподдерживаемая валюта: {currency}")
