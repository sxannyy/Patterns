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
    - проверка грамм-килограмм, литр-миллилитр, штука
"""

class TestMeasureModel(unittest.TestCase):
    def test_measure_model_basic_and_derived(self):
        # Подготовка
        piece = measure_model("шт", 1.0)
        pack = measure_model("упаковка", 10.0, base_measure=piece)

        # Действие

        # Проверка
        self.assertEqual(piece.name, "шт")
        self.assertEqual(piece.conversion_factor, 1)
        self.assertIsNone(piece.base_measure)

        self.assertEqual(pack.name, "упаковка")
        self.assertEqual(pack.conversion_factor, 10)
        self.assertIs(pack.base_measure, piece)

        pack.conversion_factor = 20.0
        self.assertEqual(pack.conversion_factor, 20)

        pack.base_measure = None
        self.assertIsNone(pack.base_measure)

        with self.assertRaises(Exception):
            pack.conversion_factor = "ten"
    
    def test_gramm_equal(self):
        # Подготовка
        kilo: measure_model = measure_model.create_kilogramm()
        gram: measure_model = measure_model.create_gramm()

        # Действие

        # Проверка
        self.assertEqual(kilo.base_measure, gram)
        self.assertEqual(measure_model.create_kilogramm().base_measure, measure_model.create_gramm())

    def test_milliliter_equal(self):
        # Подготовка
        liter: measure_model = measure_model.create_liter()
        milli: measure_model = measure_model.create_milliliter()

        # Действие

        # Проверка
        self.assertEqual(liter, milli.base_measure)
        self.assertEqual(measure_model.create_liter(), measure_model.create_milliliter().base_measure)

    def test_piece_create(self):
        # Подготовка
        thing: measure_model = measure_model.create_piece()

        # Действие

        # Проверка
        self.assertEqual(thing, measure_model.create_piece())

if __name__ == '__main__':
    unittest.main()