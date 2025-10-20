import unittest

from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.reposity import reposity
from Src.Models.measure_model import measure_model
from Src.Models.recipe_model import recipe_model
from Src.start_service import start_service

"""
    Unit-тесты для класса start_service.
    Проверяются:
    - создание сервиса и Singleton
    - инициализация репозитория с пустыми данными
    - создание стандартных единиц измерения
    - создание стандартных групп номенклатуры
    - создание стандартной номенклатуры
    - создание рецептов
    - запуск полной инициализации данных
"""

class TestStartService(unittest.TestCase):
    __start_service = start_service()

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.__start_service.start()

    def test_check_create_start_service(self):
        # Подготовка

        # Действие
        
        # Проверка
        self.assertIsNotNone(self.__start_service)
        self.assertIsInstance(self.__start_service, start_service)

    def test_check_singleton_pattern(self):
        # Подготовка
        service1 = start_service()
        service2 = start_service()

        # Действие

        # Проверка
        self.assertIs(service1, service2)

    def test_check_repository_initialization(self):
        # Подготовка

        # Действие
        data = self.__start_service.data()

        # Проверка
        self.assertIn(reposity.measure_key(), data)
        self.assertIn(reposity.nomenclature_key(), data)
        self.assertIn(reposity.nomenclature_group_key(), data)
        self.assertIn(reposity.recipe_key(), data)
        self.assertEqual(len(data[reposity.measure_key()]), 5)
        self.assertEqual(len(data[reposity.nomenclature_key()]), 8)
        self.assertEqual(len(data[reposity.nomenclature_group_key()]), 3)
        self.assertEqual(len(data[reposity.recipe_key()]), 3)

    def test_check_default_create_measure(self):
        # подготовка
        measures = self.__start_service.data()[reposity.measure_key()]

        # Действия

        # Проверка
        self.assertIn('г', measures)
        self.assertIn('кг', measures)
        self.assertIn('л', measures)
        self.assertIn('мл', measures)
        self.assertIn('шт', measures)
        self.assertIsInstance(measures['г'], measure_model)
        self.assertIsInstance(measures['кг'], measure_model)
        self.assertIsInstance(measures['л'], measure_model)
        self.assertIsInstance(measures['мл'], measure_model)
        self.assertIsInstance(measures['шт'], measure_model)

    def test_check_default_create_nomenclature_group(self):
        # Подготовка
        groups = self.__start_service.data()[reposity.nomenclature_group_key()]

        # Действия

        # Проверка
        self.assertIn('СиП', groups)
        self.assertIn('ЖПП', groups)
        self.assertIn('МиК', groups)
        self.assertIsInstance(groups['СиП'], nomenclature_group_model)
        self.assertIsInstance(groups['ЖПП'], nomenclature_group_model)
        self.assertIsInstance(groups['МиК'], nomenclature_group_model)

    def test_check_default_create_nomenclature(self):
        # Подготовка
        nomenclature = self.__start_service.data()[reposity.nomenclature_key()]

        # Действия

        # Проверка
        self.assertIn('Сахар', nomenclature)
        self.assertIn('Пшеничная мука', nomenclature)
        self.assertIn('Сливочное масло', nomenclature)
        self.assertIn('Яйца куриные', nomenclature)
        self.assertIn('Ванилин', nomenclature)
        self.assertIn('Соль', nomenclature)
        self.assertIn('Перец черный', nomenclature)
        self.assertIn('Молоко', nomenclature)
        self.assertIsInstance(nomenclature['Сахар'], nomenclature_model)
        self.assertIsInstance(nomenclature['Пшеничная мука'], nomenclature_model)

    def test_check_default_create_recipe_waffles(self):
        # Подготовка
        recipe = self.__start_service.data()[reposity.recipe_key()]['Вафли']
        recipes = self.__start_service.data()[reposity.recipe_key()]

        # Действия

        # Проверка
        self.assertIn('Вафли', recipes)
        self.assertIsInstance(recipe, recipe_model)
        self.assertEqual(recipe.name, "Вафли")
        self.assertIsInstance(recipe.steps, list)
        self.assertIsInstance(recipe.ingredients, list)
        self.assertGreater(len(recipe.steps), 0)
        self.assertGreater(len(recipe.ingredients), 0)

    def test_check_create_omelette_recipe(self):
        # Подготовка
        recipe = self.__start_service.data()[reposity.recipe_key()]['Омлет с молоком']
        recipes = self.__start_service.data()[reposity.recipe_key()]

        # Действия

        # Проверка
        self.assertIn('Омлет с молоком', recipes)
        self.assertIsInstance(recipe, recipe_model)
        self.assertEqual(recipe.name, "Омлет с молоком")
        self.assertIsInstance(recipe.steps, list)
        self.assertIsInstance(recipe.ingredients, list)
        self.assertGreater(len(recipe.steps), 0)
        self.assertGreater(len(recipe.ingredients), 0)

    def test_check_create_flatjack_recipe(self):
        # Подготовка
        recipe = self.__start_service.data()[reposity.recipe_key()]['Простые лепешки']
        recipes = self.__start_service.data()[reposity.recipe_key()]

        # Действия

        # Проверка
        self.assertIn('Простые лепешки', recipes)
        self.assertIsInstance(recipe, recipe_model)
        self.assertEqual(recipe.name, "Простые лепешки")
        self.assertIsInstance(recipe.steps, list)
        self.assertIsInstance(recipe.ingredients, list)
        self.assertGreater(len(recipe.steps), 0)
        self.assertGreater(len(recipe.ingredients), 0)

    def test_check_full_start_method(self):
        # Подготовка
        data = self.__start_service.data()

        # Действия

        # Проверка
        # Проверяем меры
        self.assertGreater(len(data[reposity.measure_key()]), 0)
        # Проверяем группы номенклатуры
        self.assertGreater(len(data[reposity.nomenclature_group_key()]), 0)
        # Проверяем номенклатуру
        self.assertGreater(len(data[reposity.nomenclature_key()]), 0)
        # Проверяем рецепты
        self.assertGreater(len(data[reposity.recipe_key()]), 0)
        # Проверяем конкретные рецепты
        self.assertIn('Вафли', data[reposity.recipe_key()])
        self.assertIn('Омлет с молоком', data[reposity.recipe_key()])
        self.assertIn('Простые лепешки', data[reposity.recipe_key()])

if __name__ == '__main__':
    unittest.main()