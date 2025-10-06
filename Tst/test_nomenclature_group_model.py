import unittest
from Src.Models.nomenclature_group_model import nomenclature_group_model

class TestNomenclatureGroupModel(unittest.TestCase):
    def test_create_spices_and_herbs(self):
        group = nomenclature_group_model.create_spices_and_herbs()
        self.assertTrue("специи и пряности" in group.name.lower())

if __name__ == '__main__':
    unittest.main()