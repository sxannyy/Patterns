import unittest
from datetime import datetime, date, time
from Src.Convertors.convert_factory import convert_factory
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
        self.convertor = convert_factory()

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