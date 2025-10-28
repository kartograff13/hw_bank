import os
import sys

from src.decorators import log
from src.financial_reader import read_financial_csv, read_financial_excel
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions_file
from src.widget import get_date, mask_account_card
from utils.bank_operations import process_bank_search

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), "utils"))


@log("logs/main.log")
def main() -> None:
    """Основная функция программы для работы с банковскими транзакциями"""

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_choice = input().strip()
    transactions = []

    if file_choice == "1":
        print("Для обработки выбран JSON-файл.")
        transactions = load_transactions_file()
    elif file_choice == "2":
        print("Для обработки выбран CSV-файл.")
        try:
            transactions = read_financial_csv("data/transactions.csv")
        except FileNotFoundError:
            print("Файл transactions.csv не найден.")
            return
        except Exception as e:
            print(f"Ошибка при чтении CSV файла: {e}")
            return
    elif file_choice == "3":
        print("Для обработки выбран XLSX-файл.")
        try:
            transactions = read_financial_excel("data/transactions_excel.xlsx")
        except FileNotFoundError:
            print("Файл transactions_excel.xlsx не найден.")
            return
        except Exception as e:
            print(f"Ошибка при чтении Excel файла: {e}")
            return
    else:
        print("Неверный выбор.")
        return

    if not transactions:
        print("Не удалось загрузить транзакции или файл пуст.")
        return

    available_states = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(available_states)}")
        state_input = input().strip().upper()

        if state_input in available_states:
            filtered_transactions = filter_by_state(transactions, state_input)
            print(f'Операции отфильтрованы по статусу "{state_input}"')
            break
        else:
            print(f'Статус операции "{state_input}" недоступен.')

    sort_answer = input("Отсортировать операции по дате? Да/Нет\n").strip().lower()
    if sort_answer == "да":
        order_answer = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        reverse = order_answer == "по убыванию"
        filtered_transactions = sort_by_date(filtered_transactions, reverse)

    rub_answer = input("Выводить только рублевые транзакции? Да/Нет\n").strip().lower()
    if rub_answer == "да":
        filtered_transactions = [
            t for t in filtered_transactions if t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]

    search_answer = (
        input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n").strip().lower()
    )
    if search_answer == "да":
        search_word = input("Введите слово для поиска в описании: ").strip()
        filtered_transactions = process_bank_search(filtered_transactions, search_word)

    print("Распечатываю итоговый список транзакций...")
    print()

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")
    print()

    for transaction in filtered_transactions:
        date_str = get_date(transaction["date"]) if "date" in transaction else "Дата не указана"
        description = transaction.get("description", "Описание отсутствует")
        from_account = mask_account_card(transaction["from"]) if "from" in transaction else None
        to_account = mask_account_card(transaction["to"]) if "to" in transaction else None

        amount_info = transaction.get("operationAmount", {})
        amount = amount_info.get("amount", "0")
        currency = amount_info.get("currency", {}).get("code", "RUB")

        print(f"{date_str} {description}")

        if from_account and to_account:
            print(f"{from_account} -> {to_account}")
        elif from_account:
            print(f"{from_account}")
        elif to_account:
            print(f"-> {to_account}")

        print(f"Сумма: {amount} {currency}")
        print()


if __name__ == "__main__":
    main()
