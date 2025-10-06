import unittest
from Src.Models.storage_model import storage_model

"""
    Unit-тесты для класса storage_model из модуля Models.
    Проверяется:
    - создание хранилища с именем и без
    - создание адреса хранилища
"""

class TestStorageModel(unittest.TestCase):
    def test_empty_storage_create(self):
        store = storage_model()

        # Действие

        # Проверка
        self.assertEqual(store.name, "")
    

    def test_not_empty_create_storage(self):
        # Подготовка
        store = storage_model()

        # Действие
        store.name = "test"

        # Проверка
        self.assertEqual(store.name, "test")

    def test_address_set_get(self):
        # Подготовка
        storage = storage_model()

        # Действие
        storage.address = "Test address"

        # Проверка
        self.assertEqual(storage.address, "Test address")

if __name__ == '__main__':
    unittest.main()
