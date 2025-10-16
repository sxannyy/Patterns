import unittest
from Src.Models.nomenclature_group_model import nomenclature_group_model

"""
    Проверяет создание группы 'специи и пряности'.
    Проверяет, что название группы содержит строку 'специи и пряности'.
"""

class TestNomenclatureGroupModel(unittest.TestCase):
    def test_create_spices_and_herbs(self):
        # Подготовка
        group = nomenclature_group_model.create("специи и пряности")

        # Действие

        # Проверка
        self.assertTrue("специи и пряности" in group.name.lower())

if __name__ == '__main__':
    unittest.main()