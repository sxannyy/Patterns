import unittest
from Src.Convertors.basic_convertor import basic_convertor

"""
    Unit-тесты для модуля basic_convertor:
    Проверяется:
    - Преобразование простых типов данных (str, int, float, bool, None)
    - Проверка возможности конвертации различных типов
    - Обработка неподдерживаемых типов с выбросом исключения
    - Корректность возвращаемых значений
"""

class TestBasicConvertor(unittest.TestCase):

    def setUp(self):
        self.convertor = basic_convertor()
        
    def test_convert_string(self):
        # Подготовка
        string_obj = "hello world"

        # Действие
        result = self.convertor.convert(string_obj)

        # Проверка
        self.assertEqual(result, "hello world")

    def test_convert_integer(self):
        # Подготовка
        int_obj = 42

        # Действие
        result = self.convertor.convert(int_obj)

        # Проверка
        self.assertEqual(result, 42)

    def test_convert_float(self):
        # Подготовка
        float_obj = 3.14159

        # Действие
        result = self.convertor.convert(float_obj)

        # Проверка
        self.assertEqual(result, 3.14159)

    def test_convert_boolean(self):
        # Подготовка
        bool_obj = True

        # Действие
        result = self.convertor.convert(bool_obj)

        # Проверка
        self.assertEqual(result, True)

    def test_convert_none(self):
        # Подготовка
        none_obj = None

        # Действие
        result = self.convertor.convert(none_obj)

        # Проверка
        self.assertEqual(result, None)

    def test_convert_unsupported_type_raises_exception(self):
        # Подготовка
        list_obj = [1, 2, 3]

        # Действие и проверка
        with self.assertRaises(ValueError) as context:
            self.convertor.convert(list_obj)

        # Проверка
        self.assertIn("Basic_convertor не может обработать тип", str(context.exception))

    def test_convert_different_strings(self):
        # Подготовка
        test_cases = [
            "",
            " ",
            "hello",
            "123",
            "special chars !@#$%",
            "unicode тест"
        ]

        # Действие и проверка
        for test_case in test_cases:
            result = self.convertor.convert(test_case)
            self.assertEqual(result, test_case)

    def test_convert_numeric_boundaries(self):
        # Подготовка
        test_cases = [
            0,
            -1,
            999999,
            -999999,
            0.0,
            -3.14,
            1.7976931348623157e+308  # max float
        ]

        # Действие и проверка
        for test_case in test_cases:
            result = self.convertor.convert(test_case)
            self.assertEqual(result, test_case)

    def test_convert_boolean_variants(self):
        # Подготовка
        true_obj = True
        false_obj = False

        # Действие
        true_result = self.convertor.convert(true_obj)
        false_result = self.convertor.convert(false_obj)

        # Проверка
        self.assertEqual(true_result, True)
        self.assertEqual(false_result, False)

if __name__ == '__main__':
    unittest.main()