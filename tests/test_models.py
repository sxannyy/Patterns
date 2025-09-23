import os
import unittest

from src.models.CompanyModel import CompanyModel
from src.settings_manager import SettingsManager

BASE = r"/home/sxannyy/Desktop/Patterns"

class TestModels(unittest.TestCase):
    def test_check_create_company_model(self):
        model = CompanyModel()
        self.assertEqual(model.name, "")

    def test_not_empty_create_model_company_model(self):
        model = CompanyModel()
        model.name = "test"
        self.assertEqual(model.name, "test")

    def test_load_createmodel_companymodel(self):
        filename = os.path.join(BASE, 'settings.json')
        sm = SettingsManager(filename)
        result = sm.load_settings()
        self.assertTrue(result)

    def test_compare_createmodel_companymodel(self):
        filename = os.path.join(BASE, "settings.json")
        sm1 = SettingsManager(filename)
        sm2 = SettingsManager(filename)
        sm1.load_settings()
        sm2.load_settings()
        model1 = sm1.company_settings()
        model2 = sm2.company_settings()
        self.assertEqual(model1, model2)

    def test_load_different_settings(self):
        filename1 = os.path.join(BASE, "settings.json")
        filename2 = os.path.join("company_folder", "settings_2.json")
        sm1 = SettingsManager(filename1)
        sm1.load_settings()
        model1 = sm1.company_settings()

        sm2 = SettingsManager(filename2)
        sm2.load_settings()
        model2 = sm2.company_settings()

        self.assertEqual(model1.name, "TechData")
        self.assertEqual(model2.name, "PieceofInfo")
        self.assertEqual(model1.inn, 123456789012)
        self.assertEqual(model2.bik, 123123123)

if __name__ == '__main__':
    unittest.main()