import unittest
from Src.reposity import reposity
from Src.start_service import start_service
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.recipe_model import recipe_model

class test_recipe_model(unittest.TestCase):
    __start_service = start_service()

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.__start_service.start()

    def test_add_ingredient_and_step(self):
        recipe = recipe_model("Вафли")
        recipe.add_ingredient(tuple(self.__start_service.repo.data[reposity.nomenclature_key]['Пшеничная мука'], 100))
        recipe.add_step("Смешайте ингредиенты")
        self.assertIn("Мука", recipe.ingredients)
        self.assertIn("Смешайте ингредиенты", recipe.steps)

    def test_create_recipe_waffles(self):
        recipe = recipe_model.create_recipe_waffles()
        self.assertGreater(len(recipe.ingredients()), 0)
        self.assertGreater(len(recipe.steps()), 0)

if __name__ == '__main__':
    unittest.main()