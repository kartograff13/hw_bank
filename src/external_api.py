import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')


def get_amount_rub(transaction):
    """Функция конвертирует сумму транзакции в рубли"""
    if not isinstance(transaction, dict):
        raise ValueError("Транзакция должна быть словарем")

    if "amount" not in transaction or "currency" not in transaction:
        raise ValueError("Транзакция должна содержать 'amount' и 'currency'")

    try:
        amount = float(transaction["amount"])
    except (TypeError, ValueError):
        raise ValueError("Сумма транзакции должна быть числом")

    currency = str(transaction["currency"]).upper()

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

            if not data.get('success', True):
                error_info = data.get('error', {}).get("info", "Неизвестная ошибка API")

                raise Exception(f"Ошибка в ответе API: {error_info}")

            if 'rates' not in data or "RUB" not in data["rates"]:
                raise Exception("В ответе API отсутствует курс RUB")

            rate = data["rates"]["RUB"]
            return amount * rate

        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе к API: {e}")
        except ValueError as e:
            raise Exception(f"Ошибка при разборе JSON ответа: {e}")

    raise ValueError(f"Неподдерживаемая валюта: {currency}")
