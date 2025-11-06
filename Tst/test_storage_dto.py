import unittest
from Src.Dto.storage_dto import storage_dto

"""
    Unit-тесты для класса storage_dto.
    Проверяются:
    - создание DTO
    - установка и получение свойств
    - обработка строковых значений
"""

class TestStorageDto(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных"""
        self.dto = storage_dto()

    def test_create_storage_dto(self):
        # Подготовка

        # Действие
        
        # Проверка
        self.assertIsNotNone(self.dto)
        self.assertIsInstance(self.dto, storage_dto)

    def test_name_property(self):
        # Подготовка
        test_name = "Test Storage"

        # Действие
        self.dto.name = test_name

        # Проверка
        self.assertEqual(self.dto.name, test_name)
        self.assertIsInstance(self.dto.name, str)

    def test_address_property(self):
        # Подготовка
        test_address = "ул. Тестовая, 123"

        # Действие
        self.dto.address = test_address

        # Проверка
        self.assertEqual(self.dto.address, test_address)
        self.assertIsInstance(self.dto.address, str)

    def test_empty_name_and_address(self):
        # Подготовка
        empty_string = ""

        # Действие
        self.dto.name = empty_string
        self.dto.address = empty_string

        # Проверка
        self.assertEqual(self.dto.name, "")
        self.assertEqual(self.dto.address, "")

    def test_storage_dto_with_all_properties(self):
        # Подготовка
        dto = storage_dto()
        dto.id = "test_id"
        dto.name = "Main Storage"
        dto.unique_code = "storage_001"
        dto.address = "ул. Центральная, 1"

        # Действие

        # Проверка
        self.assertEqual(dto.id, "test_id")
        self.assertEqual(dto.name, "Main Storage")
        self.assertEqual(dto.unique_code, "storage_001")
        self.assertEqual(dto.address, "ул. Центральная, 1")

    def test_name_with_special_characters(self):
        # Подготовка
        special_name = "Склад №1 (Основной)"

        # Действие
        self.dto.name = special_name

        # Проверка
        self.assertEqual(self.dto.name, special_name)

    def test_address_with_special_characters(self):
        # Подготовка
        special_address = "ул. Ленина, д. 15/2, кв. 45"

        # Действие
        self.dto.address = special_address

        # Проверка
        self.assertEqual(self.dto.address, special_address)

    def test_multiple_property_changes(self):
        # Подготовка
        name1 = "Первое название"
        address1 = "Первый адрес"
        name2 = "Второе название"
        address2 = "Второй адрес"

        # Действие
        self.dto.name = name1
        self.dto.address = address1
        first_name = self.dto.name
        first_address = self.dto.address
        
        self.dto.name = name2
        self.dto.address = address2
        second_name = self.dto.name
        second_address = self.dto.address

        # Проверка
        self.assertEqual(first_name, name1)
        self.assertEqual(first_address, address1)
        self.assertEqual(second_name, name2)
        self.assertEqual(second_address, address2)

    def test_long_strings(self):
        # Подготовка
        long_name = "Очень длинное название склада которое может содержать много символов"
        long_address = "Очень длинный адрес склада который содержит много информации о местоположении и может занимать несколько строк"

        # Действие
        self.dto.name = long_name
        self.dto.address = long_address

        # Проверка
        self.assertEqual(self.dto.name, long_name)
        self.assertEqual(self.dto.address, long_address)

if __name__ == '__main__':
    unittest.main()