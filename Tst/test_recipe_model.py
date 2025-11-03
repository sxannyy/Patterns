import unittest
from Src.reposity import reposity
from Src.start_service import start_service
from Src.Models.recipe_model import recipe_model

class TestRecipeModel(unittest.TestCase):
    def setUp(self):
        # Инициализируем сервис и загружаем дефолтные данные
        self.svc = start_service()
        self.svc.start()  # важно: чтобы появились дефолтные номенклатуры
        self.repo = self.svc.repo

    def test_add_ingredient_and_step(self):
        # Подготовка
        recipe = recipe_model("Вафли")

        # Достаём муку из репозитория
        nomenclature = self.repo.data.get(reposity.nomenclature_key(), {})
        flour = nomenclature.get('Пшеничная мука')
        self.assertIsNotNone(
            flour,
            "В репозитории нет номенклатуры 'Пшеничная мука'. "
            "Проверьте, что start_service.start() действительно создаёт дефолтные данные "
            "и что в settings.json флаг 'Первый старт' (first_start) = True для тестов."
        )

        # Действие
        recipe.add_ingredient(flour, 100)
        recipe.add_step("Смешайте ингредиенты")

        # Проверка
        self.assertIn("Пшеничная мука", recipe.ingredients[0][0].name)
        self.assertIn("Смешайте ингредиенты", recipe.steps)

if __name__ == '__main__':
    unittest.main()