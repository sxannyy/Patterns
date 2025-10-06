import unittest
from Src.reposity import reposity
from Src.start_service import start_service
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.recipe_model import recipe_model

"""
    Проверяет добавление ингредиента и шага в рецепт.
    Проверяет, что ингредиент был успешно добавлен в рецепт, а также что шаг приготовления был добавлен правильно.
"""

class TestRecipeModel(unittest.TestCase):
    __start_service = start_service()

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.__start_service.start()

    def test_add_ingredient_and_step(self):
        recipe = recipe_model("Вафли")
        recipe.add_ingredient(self.__start_service.repo.data[reposity.nomenclature_key]['Пшеничная мука'], 100)
        recipe.add_step("Смешайте ингредиенты")
        self.assertIn("Пшеничная мука", recipe.ingredients[0][0].name)
        self.assertIn("Смешайте ингредиенты", recipe.steps) 

if __name__ == '__main__':
    unittest.main()