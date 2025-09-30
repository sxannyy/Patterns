import os
import unittest

from Src.settings_manager import settings_manager

"""
    Unit-тесты для класса settings_manager из модуля Src.
    Проверяются:
    - загрузка файла настроек из другой директории
"""

BASE = r"/home/sxannyy/Desktop/Patterns"

class TestSettingsManager(unittest.TestCase):
    def test_load_different_settings(self):
        # Подготовка
        filename1 = os.path.join(BASE, "settings.json")
        filename2 = os.path.join("company_folder", "settings_2.json")

        # Действие
        sm1 = settings_manager(filename1)
        sm1.load_settings()
        model1 = sm1.company_settings()

        sm2 = settings_manager(filename2)
        sm2.load_settings()
        model2 = sm2.company_settings()

        # Проверка
        self.assertEqual(model1.name, "TechData")
        self.assertEqual(model1.inn, 123456789012)

        self.assertEqual(model2.name, "PieceofInfo")
        self.assertEqual(model2.bik, 123123123)
    
if __name__ == '__main__':
    unittest.main()