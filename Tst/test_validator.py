import unittest
from Src.Core.validator import validator, argument_exception

"""
Unit-тесты для класса validator из модуля Core.
Проверяются:
  - корректная работа при валидных данных,
  - выброс исключений при пустых/неверных значениях,
  - граничные условия (максимальная длина).
"""

class TestValidator(unittest.TestCase):

    """ Каждый тест отражает конкретный сценарий валидации """

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