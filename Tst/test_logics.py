import unittest
from Src.Logics.response_csv import response_csv
from Src.Logics.factory_entities import factory_entities
from Src.Core.validator import operation_exception
from Src.Logics.response_json import response_json
from Src.Logics.response_markdown import response_markdown
from Src.Logics.response_xml import response_xml
from Src.Models.settings_model import settings_model
from Src.Core.response_format import response_formats
from Src.reposity import reposity
from Src.start_service import start_service
import json

"""
    Unit-тесты для модуля Logics:
    Проверяется:
    - Фабрика создания обработчиков ответов (factory_entities)
    - Формирование ответов в различных форматах (CSV, JSON, Markdown, XML)
    - Обработка одиночных рецептов и списков рецептов
    - Валидация входных параметров и обработка ошибок
    - Корректность преобразования данных рецептов в целевые форматы
"""

class TestLogics(unittest.TestCase):
    __start_service = start_service()

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.__start_service.start()

    def setUp(self):
        self.factory = factory_entities()
        self.responder = response_csv()
        self.responder_json = response_json()
        self.responder_markdown = response_markdown()
        self.responder_xml = response_xml()

    def test_response_formats(self):
        # Подготовка
        expected_formats = {
            response_formats.csv(): response_csv,
            response_formats.json(): response_json,
            response_formats.markdown(): response_markdown,
            response_formats.xml(): response_xml
        }

        # Действие

        # Проверка
        self.assertEqual(self.factory.response_formats, expected_formats)

    def test_create_valid_csv(self):
        # Подготовка

        # Действие
        responder = self.factory.create(response_formats.csv())

        # Проверка
        self.assertIsInstance(responder(), response_csv)

    def test_create_invalid_format(self):
        # Подготовка

        # Действие

        # Проверка
        with self.assertRaises(operation_exception):
            self.factory.create('invalid_format')
            
    def test_create_default_none_settings(self):
        # Подготовка

        # Действие

        # Проверка
        with self.assertRaises(operation_exception):
            self.factory.create_default(None)

    def test_create_default_valid(self):
        # Подготовка
        settings = settings_model()
        settings.response_format = response_formats.csv()

        # Действие
        responder = self.factory.create_default(settings)

        # Проверка
        self.assertIsInstance(responder(), response_csv)

    def test_create_single_recipe_csv(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]

        # Действие
        result = self.responder.create(recipe)

        # Проверка - проверяем структуру CSV
        lines = result.split('\n')
        self.assertGreater(len(lines), 1, "CSV должен содержать заголовок и данные")
        
        # Проверяем заголовок
        header = lines[0]
        expected_headers = ['id', 'name', 'ingredients', 'steps']
        for expected_header in expected_headers:
            self.assertIn(expected_header, header)
        
        # Проверяем данные
        if len(lines) > 1:
            data_line = lines[1]
            self.assertIn("Омлет с молоком", data_line)

    def test_create_list_recipes_csv(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]
        data = [recipe]

        # Действие
        result = self.responder.create(data)

        # Проверка
        lines = result.split('\n')
        self.assertGreater(len(lines), 1, "CSV должен содержать заголовок и данные")
        self.assertIn("Омлет с молоком", result)

    def test_create_valid_json(self):
        # Подготовка

        # Действие
        responder = self.factory.create(response_formats.json())

        # Проверка
        self.assertIsInstance(responder(), response_json)

    def test_create_default_valid_json(self):
        # Подготовка
        settings = settings_model()
        settings.response_format = response_formats.json()

        # Действие
        responder = self.factory.create_default(settings)

        # Проверка
        self.assertIsInstance(responder(), response_json)

    def test_create_single_recipe_json(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]

        # Действие
        result = self.responder_json.create(recipe)

        # Проверка
        data = json.loads(result)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        
        recipe_data = data[0]
        self.assertIn("name", recipe_data)
        self.assertIn("ingredients", recipe_data)
        self.assertIn("steps", recipe_data)
        self.assertEqual(recipe_data["name"], "Омлет с молоком")

    def test_create_list_recipes_json(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]
        data = [recipe]

        # Действие
        result = self.responder_json.create(data)

        # Проверка
        json_data = json.loads(result)
        self.assertIsInstance(json_data, list)
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]["name"], "Омлет с молоком")

    def test_create_valid_markdown(self):
        # Подготовка

        # Действие
        responder = self.factory.create(response_formats.markdown())

        # Проверка
        self.assertIsInstance(responder(), response_markdown)

    def test_create_default_valid_markdown(self):
        # Подготовка
        settings = settings_model()
        settings.response_format = response_formats.markdown()

        # Действие
        responder = self.factory.create_default(settings)

        # Проверка
        self.assertIsInstance(responder(), response_markdown)

    def test_create_single_recipe_markdown(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]

        # Действие
        result = self.responder_markdown.create(recipe)

        # Проверка
        self.assertIn("# Омлет с молоком", result)
        self.assertIn("## Свойства:", result)
        self.assertIn("| Свойство | Значение |", result)
        self.assertIn("name", result)
        self.assertIn("ingredients", result)
        self.assertIn("steps", result)

    def test_create_list_recipes_markdown(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]
        data = [recipe]

        # Действие
        result = self.responder_markdown.create(data)

        # Проверка
        self.assertIn("# Омлет с молоком", result)
        self.assertIn("## Свойства:", result)

    def test_create_valid_xml(self):
        # Подготовка

        # Действие
        responder = self.factory.create(response_formats.xml())

        # Проверка
        self.assertIsInstance(responder(), response_xml)

    def test_create_default_valid_xml(self):
        # Подготовка
        settings = settings_model()
        settings.response_format = response_formats.xml()

        # Действие
        responder = self.factory.create_default(settings)

        # Проверка
        self.assertIsInstance(responder(), response_xml)

    def test_create_single_recipe_xml(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]

        # Действие
        result = self.responder_xml.create(recipe)

        # Проверка
        self.assertIn('<?xml version="1.0" encoding="UTF-8"?>', result)
        self.assertIn("<name>Омлет с молоком</name>", result)
        self.assertIn("<ingredients>", result)
        self.assertIn("<steps>", result)

    def test_create_list_recipes_xml(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]
        data = [recipe]

        # Действие
        result = self.responder_xml.create(data)

        # Проверка
        self.assertIn('<?xml version="1.0" encoding="UTF-8"?>', result)
        self.assertIn("<name>Омлет с молоком</name>", result)

    def test_json_structure_validation(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]

        # Действие
        result = self.responder_json.create(recipe)
        data = json.loads(result)

        # Проверка
        recipe_data = data[0]
        required_fields = ["id", "name", "ingredients", "steps"]
        for field in required_fields:
            self.assertIn(field, recipe_data)
        
        # Проверяем структуру ингредиентов
        ingredients = recipe_data["ingredients"]
        self.assertIsInstance(ingredients, list)
        if ingredients:
            ingredient_fields = ["nomenclature_id", "nomenclature_name", "quantity", "measure_unit"]
            for field in ingredient_fields:
                self.assertIn(field, ingredients[0])

    def test_markdown_structure_validation(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]

        # Действие
        result = self.responder_markdown.create(recipe)

        # Проверка
        lines = result.split('\n')
        self.assertIn("# Омлет с молоком", lines[0])
        self.assertIn("## Свойства:", result)
        self.assertIn("| Свойство | Значение |", result)

    def test_csv_structure_validation(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]

        # Действие
        result = self.responder.create(recipe)

        # Проверка
        lines = result.split('\n')
        self.assertGreater(len(lines), 1)
        
        header = lines[0]
        data = lines[1] if len(lines) > 1 else ""
        
        # Проверяем основные поля в заголовке
        expected_fields = ["id", "name", "ingredients", "steps"]
        for field in expected_fields:
            self.assertIn(field, header)
        
        # Проверяем данные
        self.assertIn("Омлет с молоком", data)

    def test_xml_structure_validation(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]

        # Действие
        result = self.responder_xml.create(recipe)

        # Проверка
        self.assertIn('<?xml version="1.0" encoding="UTF-8"?>', result)
        self.assertIn("<name>Омлет с молоком</name>", result)
        self.assertIn("<ingredients>", result)
        self.assertIn("<steps>", result)

if __name__ == '__main__':
    unittest.main()