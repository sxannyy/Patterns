import unittest
from datetime import datetime, date, time
from Src.Convertors.datetime_convertor import datetime_convertor

"""
    Unit-тесты для модуля datetime_convertor:
    Проверяется:
    - Преобразование объектов datetime, date, time
    - Корректность структуры возвращаемых словарей
    - Проверка возможности конвертации различных типов
    - Обработка неподдерживаемых типов
"""

class TestDatetimeConvertor(unittest.TestCase):

    def setUp(self):
        self.convertor = datetime_convertor()

    def test_can_convert_datetime(self):
        # Подготовка
        dt = datetime(2023, 12, 25, 14, 30, 45)

        # Действие
        result = self.convertor.can_convert(dt)

        # Проверка
        self.assertTrue(result)

    def test_can_convert_date(self):
        # Подготовка
        d = date(2023, 12, 25)

        # Действие
        result = self.convertor.can_convert(d)

        # Проверка
        self.assertTrue(result)

    def test_can_convert_time(self):
        # Подготовка
        t = time(14, 30, 45)

        # Действие
        result = self.convertor.can_convert(t)

        # Проверка
        self.assertTrue(result)

    def test_cannot_convert_other_types(self):
        # Подготовка
        test_cases = ["string", 123, 45.67, True, None, {"key": "value"}]

        # Действие и проверка
        for test_case in test_cases:
            result = self.convertor.can_convert(test_case)
            self.assertFalse(result, f"Не должен конвертировать тип: {type(test_case)}")

    def test_convert_datetime(self):
        # Подготовка
        dt = datetime(2023, 12, 25, 14, 30, 45)

        # Действие
        result = self.convertor.convert(dt)

        # Проверка
        self.assertEqual(result['type'], 'datetime')
        self.assertEqual(result['year'], 2023)
        self.assertEqual(result['month'], 12)
        self.assertEqual(result['day'], 25)
        self.assertEqual(result['hour'], 14)
        self.assertEqual(result['minute'], 30)
        self.assertEqual(result['second'], 45)
        self.assertIn('iso_format', result)
        self.assertEqual(result['iso_format'], '2023-12-25T14:30:45')

    def test_convert_date(self):
        # Подготовка
        d = date(2023, 12, 25)

        # Действие
        result = self.convertor.convert(d)

        # Проверка
        self.assertEqual(result['type'], 'date')
        self.assertEqual(result['year'], 2023)
        self.assertEqual(result['month'], 12)
        self.assertEqual(result['day'], 25)
        self.assertIn('iso_format', result)
        self.assertEqual(result['iso_format'], '2023-12-25')

    def test_convert_time(self):
        # Подготовка
        t = time(14, 30, 45)

        # Действие
        result = self.convertor.convert(t)

        # Проверка
        self.assertEqual(result['type'], 'time')
        self.assertEqual(result['hour'], 14)
        self.assertEqual(result['minute'], 30)
        self.assertEqual(result['second'], 45)
        self.assertIn('iso_format', result)
        self.assertEqual(result['iso_format'], '14:30:45')

    def test_convert_unconvertible_object(self):
        # Подготовка
        unconvertible_obj = "not_a_datetime"

        # Действие
        result = self.convertor.convert(unconvertible_obj)

        # Проверка
        expected = {'value': 'not_a_datetime', 'type': 'other'}
        self.assertEqual(result, expected)

    def test_convert_none_object(self):
        # Подготовка
        none_obj = None

        # Действие
        result = self.convertor.convert(none_obj)

        # Проверка
        expected = {'value': None, 'type': 'other'}
        self.assertEqual(result, expected)

    def test_datetime_edge_cases(self):
        # Подготовка
        edge_cases = [
            datetime(1, 1, 1, 0, 0, 0),  # Минимальная дата
            datetime(9999, 12, 31, 23, 59, 59),  # Максимальная дата
            datetime(2023, 2, 28, 0, 0, 0),  # Февраль не високосный
            datetime(2024, 2, 29, 0, 0, 0)   # Февраль високосный
        ]

        # Действие и проверка
        for dt in edge_cases:
            result = self.convertor.convert(dt)
            self.assertEqual(result['type'], 'datetime')
            self.assertEqual(result['year'], dt.year)
            self.assertEqual(result['month'], dt.month)
            self.assertEqual(result['day'], dt.day)

if __name__ == '__main__':
    unittest.main()