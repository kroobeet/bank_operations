import unittest
from operations import *


class TestBankOperations(unittest.TestCase):

    def setUp(self):
        self.operations_data = [
            {
                "id": 431131847,
                "state": "EXECUTED",
                "date": "2018-05-05T01:38:56.538074",
                "operationAmount": {
                    "amount": "56071.02",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод с карты на счет",
                "from": "MasterCard 9454780748494532",
                "to": "Счет 51958934737718181351"
            },
            {
                "id": 15948212,
                "state": "EXECUTED",
                "date": "2018-12-23T11:47:52.403285",
                "operationAmount": {
                    "amount": "47408.20",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод с карты на карту",
                "from": "МИР 8665240839126074",
                "to": "Maestro 3000704277834087"
            },
            {
                "id": 114832369,
                "state": "EXECUTED",
                "date": "2019-12-07T06:17:14.634890",
                "operationAmount": {
                    "amount": "48150.39",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод организации",
                "from": "Visa Classic 28428728893689012",
                "to": "Счет 35158586384610753655"
            },
            {
                "id": 176798279,
                "state": "CANCELED",
                "date": "2019-04-18T11:22:18.800453",
                "operationAmount": {
                    "amount": "73778.48",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Открытие вклада",
                "to": "Счет 90417871337969064865"
            }
        ]

    def test_load_operations_file_not_found(self):
        operations = load_operations('non_existing_file.json')
        self.assertIsNone(operations)

    def test_load_operations_json_decode_error(self):
        operations = load_operations('invalid_json.json')
        self.assertIsNone(operations)

    def test_is_executed_true(self):
        op = {"state": "EXECUTED"}
        self.assertTrue(is_executed(op))

    def test_is_executed_false(self):
        op = {"state": "PENDING"}
        self.assertFalse(is_executed(op))

    def test_filter_executed_operations(self):
        filtered_operations = list(filter_executed_operations(self.operations_data))
        self.assertEqual(len(filtered_operations), 3)
        self.assertTrue(all(op["state"] == "EXECUTED" for op in filtered_operations))

    def test_sort_operations_by_date(self):
        sorted_operations = sort_operations_by_date(self.operations_data)
        self.assertEqual(sorted_operations[0]["id"], 114832369)
        self.assertEqual(sorted_operations[-1]["id"], 431131847)

    def test_mask_card(self):
        masked_card = mask_card("MasterCard 9454780748494532")
        self.assertEqual(masked_card, "MasterCard 9454 78** **** 4532")

    def test_format_date(self):
        formatted_date = format_date("2018-05-05T01:38:56.538074")
        self.assertEqual(formatted_date, "05.05.2018")

    def test_is_card_number_true(self):
        result = is_card_number("9454780748494532")
        self.assertTrue(result)

    def test_is_card_number_false(self):
        result = is_card_number("123456789012345")
        self.assertFalse(result)

    def test_is_account_number_true(self):
        result = is_account_number("51958934737718181351")
        self.assertTrue(result)

    def test_mask_account_or_card_card(self):
        masked_info = mask_account_or_card("MasterCard 9454780748494532")
        self.assertEqual(masked_info, "MasterCard 9454 78** **** 4532")

    def test_mask_account_or_card_invalid_number(self):
        masked_info = mask_account_or_card("Invalid Number")
        self.assertIn("Произошла ошибка при маскировке номера", masked_info)

    def test_format_operation(self):
        formatted_operation = format_operation(self.operations_data[0])
        expected_output = "05.05.2018 Перевод с карты на счет\nMasterCard 9454 78** **** 4532 -> Счет **1351\n56071.02 руб.\n"
        self.assertEqual(formatted_operation, expected_output)


if __name__ == '__main__':
    unittest.main()
