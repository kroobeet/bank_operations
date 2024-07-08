import json
import re
from datetime import datetime


def load_operations(file_path):
    """
    Загружает операции из указанного файла JSON.

    :param file_path: Путь к файлу с операциями в формате JSON
    :return: Список операций или None, если возникла ошибка
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            operations = json.load(f)
            return operations
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка: Не удалось прочитать файл {file_path} как JSON. Ошибка: {e}")
        return None
    except Exception as e:
        print(f"Произошла ошибка при загрузке операций из файла {file_path}: {e}")
        return None


def is_executed(op):
    """
    Проверяет, выполнена ли операция.

    :param op: Операция
    :return: True, если операция выполнена, иначе False
    """
    return op.get("state") == "EXECUTED"


def filter_executed_operations(operations):
    """
    Фильтрует операции, оставляя только выполненные.

    :param operations: Список операций
    :return: Генератор выполненных операций
    """
    try:
        return (op for op in operations if is_executed(op))
    except Exception as e:
        print(f"Произошла ошибка при фильтрации операций: {e}")
        return []


def sort_operations_by_date(operations):
    """
    Сортирует операции по дате в порядке убывания.

    :param operations: Список операций
    :return: Список отсортированных операций
    """
    try:
        return sorted(operations, key=lambda x: x["date"], reverse=True)
    except Exception as e:
        print(f"Произошла ошибка при сортировке операций по дате: {e}")
        return []


def mask_card(card_info):
    """
    Маскирует номер карты, показывая только первые 6 и последние 4 цифры.

    :param card_info: Информация о карте
    :return: Маскированная строка с номером карты
    """
    try:
        # Используем регулярное выражение для поиска номера карты
        pattern = r'(\b\d{4})(\d{2})(\d{2})(\d{4})(\d{4})\b'
        match = re.search(pattern, card_info)

        if match:
            first_four = match.group(1)
            second_two = match.group(2)
            last_four = match.group(5)
            masked_card_number = f"{first_four} {second_two}** **** {last_four}"
            return card_info.replace(match.group(0), masked_card_number)
        else:
            raise ValueError("Неверная длина номера карты")
    except Exception as e:
        print(f"Произошла ошибка при маскировке номера карты: {e}")
        return card_info


def mask_account(account_info):
    """
    Маскирует номер счета, показывая только последние 4 цифры.

    :param account_info: Информация о счете
    :return: Маскированная строка с номером счета
    """
    try:
        pattern = r'\b\d{20}\b'
        match = re.search(pattern, account_info)

        if match:
            masked_account_number = f"**{match.group(0)[-4:]}"
            return account_info.replace(match.group(0), masked_account_number)
        else:
            raise ValueError("Неверная длина номера счета")
    except Exception as e:
        print(f"Произошла ошибка при маскировке номера счета: {e}")
        return account_info


def format_date(date_str):
    """
    Форматирует дату из строки в формат ДД.ММ.ГГГГ.

    :param date_str: Строка с датой в формате ISO
    :return: Строка с датой в формате ДД.ММ.ГГГГ
    """
    try:
        date = datetime.fromisoformat(date_str)
        return date.strftime("%d.%m.%Y")
    except Exception as e:
        print(f"Произошла ошибка при форматировании даты: {e}")
        return date_str


def is_card_number(number):
    """
    Проверяет, является ли строка номером карты.

    :param number: Номер карты
    :return: True, если строка является номером карты, иначе False
    """
    return len(number) == 16


def is_account_number(number):
    """
    Проверяет, является ли строка номером счета.

    :param number: Номер счета
    :return: True, если строка является номером счета, иначе False
    """
    try:
        if len(number) != 20:
            print("Произошла ошибка при проверке номера счета:")
            raise ValueError("Неверная длина номера счета")
        return True
    except ValueError as e:
        raise e
    except Exception as e:
        print(f"Произошла ошибка при проверке номера счета: {e}")
        return False


def mask_account_or_card(info):
    """
    Маскирует номер счета или карты в зависимости от его длины.

    :param info: Информация о счете или карте
    :return: Маскированная строка или сообщение об ошибке
    """
    try:
        parts = info.split()
        name = " ".join(parts[:-1])
        number = parts[-1]

        if is_card_number(number):
            masked_info = mask_card(f"{name} {number}")
            return masked_info

        if is_account_number(number):
            masked_info = mask_account(f"{name} {number}")
            return masked_info

        raise ValueError("Неверный номер")
    except ValueError as e:
        return f"Произошла ошибка при маскировке номера: {str(e)}"
    except Exception as e:
        return f"Произошла ошибка при маскировке номера: {str(e)}"


def format_operation(operation):
    """
    Форматирует операцию в строку для вывода.

    :param operation: Операция
    :return: Строка с отформатированной операцией или сообщение об ошибке
    """
    try:
        if "date" not in operation or not operation["date"]:
            raise ValueError("Отсутствует дата операции")

        date = format_date(operation["date"])
        description = operation.get("description", "")
        amount = operation.get("operationAmount", {}).get("amount", "")
        currency = operation.get("operationAmount", {}).get("currency", {}).get("name", "")

        from_account = operation.get("from", "")
        to_account = operation.get("to", "")

        if from_account:
            from_account = mask_account_or_card(from_account)
            if "Ошибка" in from_account:
                return from_account

        if to_account:
            to_account = mask_account_or_card(to_account)
            if "Ошибка" in to_account:
                return to_account

        from_part = f"{from_account} -> " if from_account else ""
        to_part = to_account if to_account else ""

        return f"{date} {description}\n{from_part}{to_part}\n{amount} {currency}\n"

    except Exception as e:
        return f"Произошла ошибка при форматировании операции: {str(e)}"


def main(file_path):
    """
    Основная функция для загрузки, фильтрации, сортировки и вывода операций.

    :param file_path: Путь к файлу с операциями в формате JSON
    """
    try:
        operations_count = 5
        operations = load_operations(file_path)

        if not operations:
            print("Не удалось загрузить операции.")
            return

        sorted_operations_by_date = sort_operations_by_date(operations)
        filtered_and_sorted_executed_operations_by_date = filter_executed_operations(sorted_operations_by_date)

        last_actually_operations = filtered_and_sorted_executed_operations_by_date[:operations_count]

        for operation in last_actually_operations:
            result = format_operation(operation)
            if "Ошибка" in result:
                print(result)
            else:
                print(result)

    except Exception as e:
        print(f"Произошла ошибка в основной функции: {e}")


if __name__ == "__main__":
    file = 'operations.json'
    main(file)
