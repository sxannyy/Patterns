import unittest
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_group_model import nomenclature_group_model

"""
    Проверяет правильность установки полного названия и единицы измерения.
    Проверяет, что полное название ингредиента соответствует ожидаемому значению, а также что единица измерения правильно связана с ингредиентом.
"""

class TestNomenclatureModel(unittest.TestCase):
    def test_fullname_and_measure(self):
        group = nomenclature_group_model.create_spices_and_herbs()
        measure = measure_model.create_gramm()
        nom = nomenclature_model("Перец", 'Перец', group, measure)
        self.assertIn("Перец", nom.fullname)
        self.assertEqual(nom.measure, measure)

if __name__ == '__main__':
    unittest.main()
