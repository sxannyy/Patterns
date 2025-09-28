import os
import unittest
import uuid

from Src.Core.abstract_model import not_abstract_exception
from Src.Core.validator import validator, argument_exception
from Src.settings_manager import settings_manager
from Src.Models.company_model import company_model
from Src.Models.storage_model import storage_model
from Src.Models.measure_model import measure_model

BASE = r"/home/sxannyy/Desktop/Patterns"

class TestModels(unittest.TestCase):
    def test_check_create_company_model(self):
        model = company_model()
        self.assertEqual(model.name, "")

    def test_not_empty_create_model_company_model(self):
        model = company_model()
        model.name = "test"
        self.assertEqual(model.name, "test")

    def test_load_createmodel_companymodel(self):
        filename = os.path.join('settings.json')
        sm = settings_manager(filename)
        result = sm.load_settings()
        self.assertTrue(result)

    def test_compare_createmodel_companymodel(self):
        filename = os.path.join("..\settings.json")
        sm1 = settings_manager(filename)
        sm2 = settings_manager(filename)
        sm1.load_settings()
        sm2.load_settings()
        model1 = sm1.company_settings()
        model2 = sm2.company_settings()
        self.assertEqual(model1, model2)

    def test_load_different_settings(self):
        filename1 = os.path.join(BASE, "settings.json")
        filename2 = os.path.join("company_folder", "settings_2.json")
        sm1 = settings_manager(filename1)
        sm1.load_settings()
        model1 = sm1.company_settings()

        sm2 = settings_manager(filename2)
        sm2.load_settings()
        model2 = sm2.company_settings()

        self.assertEqual(model1.name, "TechData")
        self.assertEqual(model2.name, "PieceofInfo")
        self.assertEqual(model1.inn, 123456789012)
        self.assertEqual(model2.bik, 123123123)
    
    def test_relative_path(self):
        filename1 = os.path.join("..\settings.json")
        filename2 = os.path.join("settings.json")
        sm1 = settings_manager(filename1)
        sm2 = settings_manager(filename2)
        res1 = sm1.load_settings()
        res2 = sm2.load_settings()
        model1 = sm1.company_settings()
        model2 = sm2.company_settings()
        self.assertEqual(model1, model2)
        self.assertTrue(res1)
        self.assertTrue(res2)

    def test_absolute_path(self):
        filename = os.path.join(BASE, "settings.json")
        sm1 = settings_manager(filename)
        res = sm1.load_settings()
        model1 = sm1.company_settings()
        self.assertTrue(res)

    def test_equals_storage_model_create(self):
        # Подготовка
        id = uuid.uuid4().hex
        storage1 = storage_model()
        storage2 = storage_model()   
        
        # Действие GUID
        storage1.unique_code = id
        storage2.unique_code = id

        # Проверки
        assert storage1 == storage2

    def test_measure_model_basic_and_derived(self):
        # Подготовка
        piece = measure_model("шт", 1)
        pack = measure_model("упаковка", 10, base_measure=piece)

        # Действие

        # Проверки
        self.assertEqual(piece.name, "шт")
        self.assertEqual(piece.conversion_factor, 1)
        self.assertIsNone(piece.base_measure)

        self.assertEqual(pack.name, "упаковка")
        self.assertEqual(pack.conversion_factor, 10)
        self.assertIs(pack.base_measure, piece)

        pack.conversion_factor = 20
        self.assertEqual(pack.conversion_factor, 20)

        pack.base_measure = None
        self.assertIsNone(pack.base_measure)

        with self.assertRaises(Exception):
            pack.conversion_factor = "ten"

    def test_not_abstract_exception_on_eq(self):
        # Подготовка
        org = company_model("Test LLC")

        # Проверка
        with self.assertRaises(not_abstract_exception):
            _ = (org == 123)

    def test_validate_string_ok(self):
        self.assertTrue(validator.validate("hello", str))

    def test_validate_string_with_len_ok(self):
        self.assertTrue(validator.validate("abcd", str, 4))

    def test_validate_int_ok(self):
        self.assertTrue(validator.validate(123, int))

    def test_validate_custom_type_ok(self):
        class MyType: ...
        obj = MyType()
        self.assertTrue(validator.validate(obj, MyType))

    def test_validate_list_ok(self):
        self.assertTrue(validator.validate([1, 2, 3], list))

    def test_validate_len_ok(self):
        self.assertTrue(validator.validate(12345, int, 5))

    def test_validate_none_raises(self):
        with self.assertRaises(argument_exception):
            validator.validate(None, str)

    def test_validate_empty_string_raises(self):
        with self.assertRaises(argument_exception):
            validator.validate("", str)

    def test_validate_whitespace_string_raises(self):
        with self.assertRaises(argument_exception):
            validator.validate("   \t\n  ", str)

    def test_validate_wrong_type_raises(self):
        with self.assertRaises(argument_exception):
            validator.validate(123, str)

    def test_validate_custom_type_wrong_raises(self):
        class A: ...
        class B: ...
        with self.assertRaises(argument_exception):
            validator.validate(A(), B)

    def test_validate_string_too_long_raises(self):
        with self.assertRaises(argument_exception):
            validator.validate("abcdef", str, 5)

    def test_validate_numeric_len_bound_too_long_raises(self):
        with self.assertRaises(argument_exception):
            validator.validate(123456, int, 5)

    def test_validate_string_trimmed_passes_if_within_limit(self):
        self.assertTrue(validator.validate("  abc  ", str, 3))

    def test_validate_bool_type_check(self):
        self.assertTrue(validator.validate(True, int))

if __name__ == '__main__':
    unittest.main()