import unittest
from Src.Models.storage_model import storage_model
from Src.Dto.storage_dto import storage_dto
from Src.Core.validator import validator

"""
    Unit-тесты для класса storage_model.
    Проверяются:
    - создание склада
    - установка и получение свойств
    - валидация свойств
    - преобразование в DTO
    - обработка адреса
"""

class TestStorageModel(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных"""
        self.storage = storage_model()

    def test_create_storage(self):
        # Подготовка

        # Действие
        
        # Проверка
        self.assertIsNotNone(self.storage)
        self.assertIsInstance(self.storage, storage_model)

    def test_address_property(self):
        # Подготовка
        test_address = "ул. Тестовая, 123"

        # Действие
        self.storage.address = test_address

        # Проверка
        self.assertEqual(self.storage.address, test_address)
        self.assertIsInstance(self.storage.address, str)

    def test_address_stripping(self):
        # Подготовка
        address_with_spaces = "   ул. Тестовая, 123   "

        # Действие
        self.storage.address = address_with_spaces

        # Проверка
        self.assertEqual(self.storage.address, "ул. Тестовая, 123")

    def test_address_validation(self):
        # Подготовка

        # Действие и Проверка
        with self.assertRaises(Exception):  # Validation error
            self.storage.address = 12345  # Invalid type

    def test_to_dto_conversion(self):
        # Подготовка
        self.storage.name = "Test Storage"
        self.storage.unique_code = "test_unique_code"
        self.storage.address = "ул. Тестовая, 123"

        # Действие
        dto = self.storage.to_dto()

        # Проверка
        self.assertIsInstance(dto, storage_dto)
        self.assertEqual(dto.id, "test_unique_code")
        self.assertEqual(dto.name, "Test Storage")
        self.assertEqual(dto.address, "ул. Тестовая, 123")

    def test_storage_with_all_properties(self):
        # Подготовка
        storage = storage_model()
        storage.name = "Main Storage"
        storage.unique_code = "storage_001"
        storage.address = "ул. Центральная, 1"

        # Действие

        # Проверка
        self.assertEqual(storage.name, "Main Storage")
        self.assertEqual(storage.unique_code, "storage_001")
        self.assertEqual(storage.address, "ул. Центральная, 1")

    def test_address_with_special_characters(self):
        # Подготовка
        special_address = "ул. Ленина, д. 15/2, кв. 45"

        # Действие
        self.storage.address = special_address

        # Проверка
        self.assertEqual(self.storage.address, special_address)

    def test_multiple_address_changes(self):
        # Подготовка
        address1 = "Первый адрес"
        address2 = "Второй адрес"

        # Действие
        self.storage.address = address1
        first_address = self.storage.address
        self.storage.address = address2
        second_address = self.storage.address

        # Проверка
        self.assertEqual(first_address, address1)
        self.assertEqual(second_address, address2)

if __name__ == '__main__':
    unittest.main()