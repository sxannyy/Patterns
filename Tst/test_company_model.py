import os
import unittest

from Src.Models.company_model import company_model
from Src.settings_manager import settings_manager

"""
    Unit-тесты для класса company_model из модуля Models.
    Проверяются:
    - создание пустой модели компании
    - создание непустой модели компании
    - создание модели по файлу настроек
    - создание и сравнение моделей одного файла настроек
"""

class TestCompanyModel(unittest.TestCase):
    def test_check_create_company_model(self):
        # Подготовка
        model = company_model()

        # Действие

        # Проверка
        self.assertEqual(model.name, "")

    def test_not_empty_create_model_company_model(self):
        # Подготовка
        model = company_model()

        # Действие
        model.name = "test"

        # Проверка
        self.assertEqual(model.name, "test")

    def test_load_createmodel_companymodel(self):
        # Подготовка
        filename = os.path.join('settings.json')
        sm = settings_manager(filename)

        # Действие
        result = sm.load_settings()

        # Проверка
        self.assertTrue(result)

    def test_compare_createmodel_companymodel(self):
        # Подготовка
        filename = os.path.join("..\settings.json")
        sm1 = settings_manager(filename)
        sm2 = settings_manager(filename)

        # Действие
        sm1.load_settings()
        sm2.load_settings()

        model1 = sm1.company_settings()
        model2 = sm2.company_settings()

        # Проверка
        self.assertEqual(model1, model2)

if __name__ == '__main__':
    unittest.main()