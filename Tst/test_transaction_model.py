import unittest
from datetime import datetime
from Src.Models.transaction_model import transaction_model
from Src.Models.storage_model import storage_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.measure_model import measure_model
from Src.Dto.transaction_dto import transaction_dto
from Src.Core.validator import validator

"""
    Unit-тесты для класса transaction_model.
    Проверяются:
    - создание транзакции
    - установка и получение свойств
    - валидация свойств
    - преобразование в DTO
    - обработка дат
"""

class TestTransactionModel(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных"""
        self.storage = storage_model()
        self.storage.name = "Test Storage"
        
        self.nomenclature = nomenclature_model()
        self.nomenclature.name = "Test Nomenclature"
        
        self.measure = measure_model()
        self.measure.name = "Test Measure"
        
        self.transaction = transaction_model()

    def test_create_transaction(self):
        # Подготовка

        # Действие
        
        # Проверка
        self.assertIsNotNone(self.transaction)
        self.assertIsInstance(self.transaction, transaction_model)

    def test_storage_property(self):
        # Подготовка

        # Действие
        self.transaction.storage = self.storage

        # Проверка
        self.assertEqual(self.transaction.storage, self.storage)
        self.assertIsInstance(self.transaction.storage, storage_model)

    def test_storage_validation(self):
        # Подготовка

        # Действие и Проверка
        with self.assertRaises(Exception):  # Validation error
            self.transaction.storage = "invalid_storage"

    def test_nomenclature_property(self):
        # Подготовка

        # Действие
        self.transaction.nomenclature = self.nomenclature

        # Проверка
        self.assertEqual(self.transaction.nomenclature, self.nomenclature)
        self.assertIsInstance(self.transaction.nomenclature, nomenclature_model)

    def test_nomenclature_validation(self):
        # Подготовка

        # Действие и Проверка
        with self.assertRaises(Exception):  # Validation error
            self.transaction.nomenclature = "invalid_nomenclature"

    def test_measure_property(self):
        # Подготовка

        # Действие
        self.transaction.measure = self.measure

        # Проверка
        self.assertEqual(self.transaction.measure, self.measure)
        self.assertIsInstance(self.transaction.measure, measure_model)

    def test_measure_validation(self):
        # Подготовка

        # Действие и Проверка
        with self.assertRaises(Exception):  # Validation error
            self.transaction.measure = "invalid_measure"

    def test_quantity_property(self):
        # Подготовка
        test_quantity = 150.5

        # Действие
        self.transaction.quantity = test_quantity

        # Проверка
        self.assertEqual(self.transaction.quantity, test_quantity)
        self.assertIsInstance(self.transaction.quantity, float)

    def test_negative_quantity(self):
        # Подготовка
        negative_quantity = -50.0

        # Действие
        self.transaction.quantity = negative_quantity

        # Проверка
        self.assertEqual(self.transaction.quantity, negative_quantity)

    def test_quantity_validation(self):
        # Подготовка

        # Действие и Проверка
        with self.assertRaises(Exception):  # Validation error
            self.transaction.quantity = "invalid_quantity"

    def test_date_property_string(self):
        # Подготовка
        date_string = "2025-10-25 10:10:00"

        # Действие
        self.transaction.date = date_string

        # Проверка
        self.assertIsInstance(self.transaction.date, datetime)
        self.assertEqual(self.transaction.date.year, 2025)
        self.assertEqual(self.transaction.date.month, 10)
        self.assertEqual(self.transaction.date.day, 25)

    def test_date_property_datetime(self):
        # Подготовка
        test_datetime = datetime(2025, 10, 25, 10, 10, 0)

        # Действие
        self.transaction.date = test_datetime

        # Проверка
        self.assertEqual(self.transaction.date, test_datetime)
        self.assertIsInstance(self.transaction.date, datetime)

    def test_date_validation(self):
        # Подготовка

        # Действие и Проверка
        with self.assertRaises(Exception):  # Validation error
            self.transaction.date = 12345  # Invalid type

    def test_invalid_date_string_format(self):
        # Подготовка
        invalid_date_string = "2025/10/25 10-10-00"

        # Действие и Проверка
        with self.assertRaises(ValueError):
            self.transaction.date = invalid_date_string

    def test_to_dto_conversion(self):
        # Подготовка
        self.transaction.storage = self.storage
        self.transaction.nomenclature = self.nomenclature
        self.transaction.measure = self.measure
        self.transaction.quantity = 100.0
        self.transaction.date = "2025-10-25 10:10:00"
        self.transaction.unique_code = "test_unique_code"

        # Действие
        dto = self.transaction.to_dto()

        # Проверка
        self.assertIsInstance(dto, transaction_dto)
        self.assertEqual(dto.id, "test_unique_code")
        self.assertEqual(dto.storage_id, self.storage.unique_code)
        self.assertEqual(dto.nomenclature_id, self.nomenclature.unique_code)
        self.assertEqual(dto.measure_id, self.measure.unique_code)
        self.assertEqual(dto.quantity, 100.0)
        self.assertIsInstance(dto.date, datetime)

    def test_to_dto_with_none_values(self):
        # Подготовка
        transaction = transaction_model()
        transaction.unique_code = "test_code"
        transaction.quantity = 50.0
        transaction.date = "2025-10-25 10:10:00"

        # Действие
        dto = transaction.to_dto()

        # Проверка
        self.assertIsInstance(dto, transaction_dto)
        self.assertEqual(dto.id, "test_code")
        self.assertIsNone(dto.storage_id)
        self.assertIsNone(dto.nomenclature_id)
        self.assertIsNone(dto.measure_id)
        self.assertEqual(dto.quantity, 50.0)

    def test_transaction_with_all_properties(self):
        # Подготовка
        transaction = transaction_model()
        transaction.name = "Test Transaction"
        transaction.unique_code = "test_code_123"
        transaction.storage = self.storage
        transaction.nomenclature = self.nomenclature
        transaction.measure = self.measure
        transaction.quantity = 75.5
        transaction.date = datetime(2025, 10, 25, 10, 10, 0)

        # Действие

        # Проверка
        self.assertEqual(transaction.name, "Test Transaction")
        self.assertEqual(transaction.unique_code, "test_code_123")
        self.assertEqual(transaction.storage, self.storage)
        self.assertEqual(transaction.nomenclature, self.nomenclature)
        self.assertEqual(transaction.measure, self.measure)
        self.assertEqual(transaction.quantity, 75.5)
        self.assertEqual(transaction.date, datetime(2025, 10, 25, 10, 10, 0))

if __name__ == '__main__':
    unittest.main()