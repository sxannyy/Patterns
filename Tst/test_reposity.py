import unittest
from Src.reposity import reposity

"""
    Unit-тесты для класса reposity.
    Проверяются:
    - создание репозитория
    - статические методы ключей
    - инициализация структур данных
    - доступ к данным
"""

class TestReposity(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных"""
        self.repo = reposity()

    def test_create_reposity(self):
        # Подготовка

        # Действие
        
        # Проверка
        self.assertIsNotNone(self.repo)
        self.assertIsInstance(self.repo, reposity)

    def test_measure_key(self):
        # Подготовка

        # Действие
        key = reposity.measure_key()

        # Проверка
        self.assertEqual(key, "measures")
        self.assertIsInstance(key, str)

    def test_recipe_key(self):
        # Подготовка

        # Действие
        key = reposity.recipe_key()

        # Проверка
        self.assertEqual(key, "recipes")
        self.assertIsInstance(key, str)

    def test_nomenclature_key(self):
        # Подготовка

        # Действие
        key = reposity.nomenclature_key()

        # Проверка
        self.assertEqual(key, "nomenclature")
        self.assertIsInstance(key, str)

    def test_nomenclature_group_key(self):
        # Подготовка

        # Действие
        key = reposity.nomenclature_group_key()

        # Проверка
        self.assertEqual(key, "nomenclature_groups")
        self.assertIsInstance(key, str)

    def test_storage_key(self):
        # Подготовка

        # Действие
        key = reposity.storage_key()

        # Проверка
        self.assertEqual(key, "storages")
        self.assertIsInstance(key, str)

    def test_transaction_key(self):
        # Подготовка

        # Действие
        key = reposity.transaction_key()

        # Проверка
        self.assertEqual(key, "transactions")
        self.assertIsInstance(key, str)

    def test_keys_method(self):
        # Подготовка
        expected_keys = [
            "measures",
            "recipes", 
            "nomenclature",
            "nomenclature_groups",
            "storages",
            "transactions"
        ]

        # Действие
        keys = reposity.keys()

        # Проверка
        self.assertIsInstance(keys, list)
        self.assertEqual(len(keys), len(expected_keys))
        for expected_key in expected_keys:
            self.assertIn(expected_key, keys)

    def test_initialize_method(self):
        # Подготовка

        # Действие
        self.repo.initalize()
        data = self.repo.data

        # Проверка
        self.assertIsInstance(data, dict)
        self.assertIn("measures", data)
        self.assertIn("recipes", data)
        self.assertIn("nomenclature", data)
        self.assertIn("nomenclature_groups", data)
        self.assertIn("storages", data)
        self.assertIn("transactions", data)
        
        # Проверяем, что все значения - пустые словари
        for key in data:
            self.assertIsInstance(data[key], dict)
            self.assertEqual(len(data[key]), 0)

    def test_data_property(self):
        # Подготовка
        self.repo.initalize()

        # Действие
        data = self.repo.data

        # Проверка
        self.assertIsInstance(data, dict)
        self.assertIs(data, self.repo._reposity__data)

    def test_multiple_initialization(self):
        # Подготовка
        self.repo.initalize()
        initial_data = self.repo.data.copy()

        # Действие
        self.repo.initalize()  # Повторная инициализация
        new_data = self.repo.data

        # Проверка
        # Данные должны быть сброшены к пустым словарям
        for key in new_data:
            self.assertIsInstance(new_data[key], dict)
            self.assertEqual(len(new_data[key]), 0)

    def test_keys_consistency(self):
        # Подготовка
        self.repo.initalize()

        # Действие
        data = self.repo.data
        static_keys = reposity.keys()

        # Проверка
        self.assertEqual(len(data), len(static_keys))
        for key in static_keys:
            self.assertIn(key, data)

    def test_data_modification(self):
        # Подготовка
        self.repo.initalize()

        # Действие
        self.repo.data["measures"]["test_measure"] = "test_value"

        # Проверка
        self.assertIn("test_measure", self.repo.data["measures"])
        self.assertEqual(self.repo.data["measures"]["test_measure"], "test_value")

    def test_empty_repository_after_initialization(self):
        # Подготовка

        # Действие
        self.repo.initalize()

        # Проверка
        for key in self.repo.data:
            self.assertEqual(len(self.repo.data[key]), 0)

if __name__ == '__main__':
    unittest.main()