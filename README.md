# 💳 HW Bank — личный кабинет для банка

#### Виджет для отображения последних успешных банковских операций клиента. Проект разработан для IT-отдела крупного банка. Показывает несколько последних транзакций в удобном и безопасном формате.

## 📋 Оглавление
- Возможности
- Стек технологий
- Установка и запуск
- Использование:
  - Маскировка номеров карт и счетов
  - Фильтрация и сортировка операций
  - Генераторы для работы с транзакциями
  - Чтение CSV / Excel
  - Поиск по операциям с помощью re
- Тестирование
- Структура проекта
- Лицензия

## ✨ Возможности
- 🔒 Безопасный вывод номеров карт и счетов (маскировка)
- 📅 Форматирование даты из ISO в удобный формат ДД.ММ.ГГГГ
- 🔍 Фильтрация операций по статусу (EXECUTED, CANCELED)
- 🗓 Сортировка по дате (по убыванию / возрастанию)
- ♻️ Генераторы для перебора транзакций по валюте, описаниям и номерам карт
- 📂 Поддержка CSV и Excel файлов с транзакциями
- 🔎 Поиск по описанию с помощью регулярных выражений

## 🧰 Стек технологий
- **Python 3.10+**	Основной язык
- **Poetry**	Управление зависимостями
- **pytest** + **pytest-cov**	Тестирование и оценка покрытия
- **flake8, mypy, black, isort**	Линтинг и форматирование кода
- **pandas, openpyxl**	Работа с CSV и Excel

## ⚙️ Установка и запуск

1. Клонирование репозитория

```
# через SSH
git clone git@github.com:kartograff13/hw_bank.git

# или через HTTPS
git clone https://github.com/kartograff13/hw_bank.git
```

2. Переход в директорию проекта

```
cd hw_bank
```

3. Установка зависимостей через Poetry

```
poetry install
```
Эта команда создаст виртуальное окружение и установит все зависимости из pyproject.toml.

4. Активация окружения (опционально)

```
poetry shell
```

5. Запуск основной программы

```
poetry run python main.py
```
Примечание: Если вы используете PyCharm, не забудьте настроить интерпретатор на виртуальное окружение Poetry.

## 🚀 Использование

### 🃏 Маскировка номеров карт и счетов
#### Модуль src/masks.py

```
from src.masks import get_mask_card_number, get_mask_account

# Карта: 7000 79** **** 6361
print(get_mask_card_number("7000792289606361"))

# Счёт: **4305
print(get_mask_account("73654108430135874305"))
```

#### Модуль src/widget.py

```
from src.widget import mask_account_card, get_date

# Распознаёт тип (карта / счёт) и маскирует
print(mask_account_card("Visa Platinum 7000792289606361"))
# Visa Platinum 7000 79** **** 6361

print(mask_account_card("Счет 73654108430135874305"))
# Счет **4305

# Преобразование даты
print(get_date("2024-03-11T02:26:18.671407"))
# 11.03.2024
```

### 📂 Фильтрация и сортировка операций
#### Модуль src/processing.py

```
from src.processing import filter_by_state, sort_by_date

data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
]

# Фильтр по умолчанию (state = 'EXECUTED')
executed = filter_by_state(data)

# Сортировка по дате (убывание)
sorted_data = sort_by_date(data)
```

### ♻️ Генераторы для работы с транзакциями
#### Модуль src/generators.py

```
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

transactions = [...]  # список словарей с транзакциями

# Итератор по USD-транзакциям
usd_trans = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_trans))

# Генератор описаний
descriptions = transaction_descriptions(transactions)
for _ in range(3):
    print(next(descriptions))

# Генератор номеров карт в диапазоне
for card in card_number_generator(1, 5):
    print(card)
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# ...
```

### 📊 Чтение CSV / Excel
#### Модуль src/financial_reader.py

```
from src.financial_reader import read_csv, read_excel

# Чтение CSV-файла
data_csv = read_csv("data/transactions.csv")

# Чтение Excel-файла
data_xlsx = read_excel("data/transactions.xlsx")
Для корректной работы установлены pandas и openpyxl.
```

### 🔎 Поиск по операциям с помощью re
#### Модуль src/bank_operations.py

```
from src.bank_operations import process_bank_search, process_bank_operations

# Фильтрация по совпадению в описании
filtered = process_bank_search(transactions, "перевод")

# Подсчёт операций по категориям (например, "Перевод", "Оплата")
counts = process_bank_operations(transactions, ["Перевод", "Оплата"])
```

### 🧪 Тестирование
Для запуска тестов используется pytest с отчётом о покрытии.

```
# Запуск всех тестов
poetry run pytest

# С оценкой покрытия по модулям src
poetry run pytest --cov=src

# Генерация HTML-отчёта о покрытии
poetry run pytest --cov=src --cov-report=html
```

## Настройка в PyCharm
1. Откройте Run → Edit Configurations
2. Нажмите + и выберите pytest
3. Укажите рабочую директорию (корень проекта) и директорию tests
4. Добавьте параметры, например --cov=src
