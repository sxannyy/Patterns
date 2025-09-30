import unittest
from Src.Models.measure_model import measure_model

"""
    Unit-тесты для класса measure_model из модуля Models.
    Проверяется:
    - создание базовой единицы измерения
    - создание производной единицы измерения
    - изменение коэффициента преобразования
    - удаление базовой единицы измерения
    - проверка обработки ошибок
"""

class TestMeasureModel(unittest.TestCase):
    def test_measure_model_basic_and_derived(self):
        # Подготовка
        piece = measure_model("шт", 1)
        pack = measure_model("упаковка", 10, base_measure=piece)

        # Действие

        # Проверка
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

if __name__ == '__main__':
    unittest.main()