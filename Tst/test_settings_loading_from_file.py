import os
import unittest

from Src.settings_manager import settings_manager

BASE = r"/home/sxannyy/Desktop/Patterns"

"""
    Unit-тесты для класса settings_manager из модуля Src.
    Проверяются:
    - загрузка настроек через относительный путь
    - загрузка настроек через абсолютный путь
"""

class TestSettingsLoadingFromFile(unittest.TestCase):

    def test_relative_path(self):
        # Подготовка
        filename1 = os.path.join("..\settings.json")
        filename2 = os.path.join("settings.json")

        sm1 = settings_manager(filename1)
        sm2 = settings_manager(filename2)

        # Действие
        res1 = sm1.load_settings()
        res2 = sm2.load_settings()
        model1 = sm1.company_settings()
        model2 = sm2.company_settings()

        # Проверка
        self.assertEqual(model1, model2)
        self.assertTrue(res1)
        self.assertTrue(res2)

    def test_absolute_path(self):
        # Подготовка
        filename = os.path.join(BASE, "settings.json")
    
        sm1 = settings_manager(filename)

        # Действие
        res = sm1.load_settings()

        # Проверка
        self.assertTrue(res)

if __name__ == '__main__':
    unittest.main()