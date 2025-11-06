import unittest
from datetime import datetime
from Src.Dto.transaction_dto import transaction_dto
from Src.Core.validator import validator

"""
    Unit-тесты для класса transaction_dto.
    Проверяются:
    - создание DTO
    - установка и получение свойств
    - обработка дат
    - валидация свойств
"""

class TestTransactionDto(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных"""
        self.dto = transaction_dto()

    def test_create_transaction_dto(self):
        # Подготовка

        # Действие
        
        # Проверка
        self.assertIsNotNone(self.dto)
        self.assertIsInstance(self.dto, transaction_dto)

    def test_storage_id_property(self):
        # Подготовка
        test_storage_id = "storage_001"

        # Действие
        self.dto.storage_id = test_storage_id

        # Проверка
        self.assertEqual(self.dto.storage_id, test_storage_id)
        self.assertIsInstance(self.dto.storage_id, str)

    def test_nomenclature_id_property(self):
        # Подготовка
        test_nomenclature_id = "nomenclature_001"

        # Действие
        self.dto.nomenclature_id = test_nomenclature_id

        # Проверка
        self.assertEqual(self.dto.nomenclature_id, test_nomenclature_id)
        self.assertIsInstance(self.dto.nomenclature_id, str)

    def test_measure_id_property(self):
        # Подготовка
        test_measure_id = "measure_001"

        # Действие
        self.dto.measure_id = test_measure_id

        # Проверка
        self.assertEqual(self.dto.measure_id, test_measure_id)
        self.assertIsInstance(self.dto.measure_id, str)

    def test_quantity_property(self):
        # Подготовка
        test_quantity = 150.5

        # Действие
        self.dto.quantity = test_quantity

        # Проверка
        self.assertEqual(self.dto.quantity, test_quantity)
        self.assertIsInstance(self.dto.quantity, float)

    def test_negative_quantity(self):
        # Подготовка
        negative_quantity = -50.0

        # Действие
        self.dto.quantity = negative_quantity

        # Проверка
        self.assertEqual(self.dto.quantity, negative_quantity)

    def test_date_property_string(self):
        # Подготовка
        date_string = "2025-10-25 10:10:00"

        # Действие
        self.dto.date = date_string

        # Проверка
        self.assertIsInstance(self.dto.date, datetime)
        self.assertEqual(self.dto.date.year, 2025)
        self.assertEqual(self.dto.date.month, 10)
        self.assertEqual(self.dto.date.day, 25)

    def test_date_property_datetime(self):
        # Подготовка
        test_datetime = datetime(2025, 10, 25, 10, 10, 0)

        # Действие
        self.dto.date = test_datetime

        # Проверка
        self.assertEqual(self.dto.date, test_datetime)
        self.assertIsInstance(self.dto.date, datetime)

    def test_date_validation(self):
        # Подготовка

        # Действие и Проверка
        with self.assertRaises(Exception):  # Validation error
            self.dto.date = 12345  # Invalid type

    def test_invalid_date_string_format(self):
        # Подготовка
        invalid_date_string = "2025/10/25 10-10-00"

        # Действие и Проверка
        with self.assertRaises(ValueError):
            self.dto.date = invalid_date_string

    def test_transaction_dto_with_all_properties(self):
        # Подготовка
        dto = transaction_dto()
        dto.id = "test_id"
        dto.name = "Test Transaction DTO"
        dto.unique_code = "test_unique_code"
        dto.storage_id = "storage_001"
        dto.nomenclature_id = "nomenclature_001"
        dto.measure_id = "measure_001"
        dto.quantity = 100.0
        dto.date = datetime(2025, 10, 25, 10, 10, 0)

        # Действие

        # Проверка
        self.assertEqual(dto.id, "test_id")
        self.assertEqual(dto.name, "Test Transaction DTO")
        self.assertEqual(dto.unique_code, "test_unique_code")
        self.assertEqual(dto.storage_id, "storage_001")
        self.assertEqual(dto.nomenclature_id, "nomenclature_001")
        self.assertEqual(dto.measure_id, "measure_001")
        self.assertEqual(dto.quantity, 100.0)
        self.assertEqual(dto.date, datetime(2025, 10, 25, 10, 10, 0))

    def test_empty_ids(self):
        # Подготовка
        self.dto.storage_id = ""
        self.dto.nomenclature_id = ""
        self.dto.measure_id = ""

        # Действие

        # Проверка
        self.assertEqual(self.dto.storage_id, "")
        self.assertEqual(self.dto.nomenclature_id, "")
        self.assertEqual(self.dto.measure_id, "")

    def test_zero_quantity(self):
        # Подготовка
        zero_quantity = 0.0

        # Действие
        self.dto.quantity = zero_quantity

        # Проверка
        self.assertEqual(self.dto.quantity, zero_quantity)

    def test_large_quantity(self):
        # Подготовка
        large_quantity = 999999.99

        # Действие
        self.dto.quantity = large_quantity

        # Проверка
        self.assertEqual(self.dto.quantity, large_quantity)

if __name__ == '__main__':
    unittest.main()