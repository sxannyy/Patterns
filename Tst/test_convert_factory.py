import unittest
from Src.Convertors.convert_factory import convert_factory
from datetime import datetime, date, time
from Src.Core.abstract_model import abstract_model
from Src.Core.abstract_dto import abstract_dto

"""
    Unit-тесты для модуля convert_factory:
    Проверяется:
    - Преобразование объектов различных типов через фабрику
    - Работа с цепочкой конвертеров
    - Обработка списков и словарей
    - Получение информации о конвертерах
    - Обработка граничных случаев (None, неизвестные типы)
"""

class TestConvertFactory(unittest.TestCase):

    def setUp(self):
        self.factory = convert_factory()

    def test_convert_none(self):
        # Подготовка
        none_obj = None

        # Действие
        result = self.factory.convert(none_obj)

        # Проверка
        expected = None
        self.assertEqual(result, expected)

    def test_convert_basic_types(self):
        # Подготовка
        test_cases = [
            ("string", "string"),
            (123, 123),
            (45.67, 45.67),
            (True, True)
        ]

        # Действие и проверка
        for input_obj, expected in test_cases:
            result = self.factory.convert(input_obj)
            self.assertEqual(result, expected)

    def test_convert_datetime(self):
        # Подготовка
        dt = datetime(2023, 12, 25, 14, 30, 45)

        # Действие
        result = self.factory.convert(dt)

        # Проверка
        self.assertEqual(result['type'], 'datetime')
        self.assertEqual(result['year'], 2023)

    def test_convert_date(self):
        # Подготовка
        d = date(2023, 12, 25)

        # Действие
        result = self.factory.convert(d)

        # Проверка
        self.assertEqual(result['type'], 'date')
        self.assertEqual(result['year'], 2023)

    def test_convert_time(self):
        # Подготовка
        t = time(14, 30, 45)

        # Действие
        result = self.factory.convert(t)

        # Проверка
        self.assertEqual(result['type'], 'time')
        self.assertEqual(result['hour'], 14)

    def test_convert_list(self):
        # Подготовка
        test_list = [1, "hello", True, None]

        # Действие
        result = self.factory.convert_list(test_list)

        # Проверка
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], "hello")
        self.assertEqual(result[2], True)

    def test_convert_dict(self):
        # Подготовка
        test_dict = {
            "number": 42,
            "string": "hello",
            "boolean": True
        }

        # Действие
        result = self.factory.convert_dict(test_dict)

        # Проверка
        self.assertIsInstance(result, dict)
        self.assertEqual(result["number"], 42)
        self.assertEqual(result["string"], "hello")
        self.assertEqual(result["boolean"], True)

    def test_get_converters_info(self):
        # Действие
        result = self.factory.get_converters_info()

        # Проверка
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        
        # Проверяем структуру информации о конвертерах
        for converter_info in result:
            self.assertIn('name', converter_info)
            self.assertIn('module', converter_info)
            self.assertIn('description', converter_info)
            
        # Проверяем порядок конвертеров
        converter_names = [info['name'] for info in result]
        expected_order = ['basic_convertor', 'datetime_convertor', 'reference_convertor']
        self.assertEqual(converter_names, expected_order)

if __name__ == '__main__':
    unittest.main()