import unittest
import os
import json
from Src.Logics.response_csv import response_csv
from Src.Logics.response_json import response_json
from Src.Logics.response_markdown import response_markdown
from Src.Logics.response_xml import response_xml
from Src.reposity import reposity
from Src.start_service import start_service

"""
    Unit-тесты для модуля Logics:
    Проверяется:
    - Формирование ответов в различных форматах (CSV, JSON, Markdown, XML)
    - Сохранение ответов в необходимый формат
    - Корректность выполнения
"""

class TestRecipeFiles(unittest.TestCase):
    __start_service = start_service()
    
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.__start_service.start()
        self.test_output_dir = "test_output"
        
    def setUp(self):
        # Подготовка
        if not os.path.exists(self.test_output_dir):
            os.makedirs(self.test_output_dir)
        
        self.responder_csv = response_csv()
        self.responder_json = response_json()
        self.responder_markdown = response_markdown()
        self.responder_xml = response_xml()

    def test_create_recipe_csv_file(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Простые лепешки"]
        filename = "простые_лепешки.csv"
        filepath = os.path.join(self.test_output_dir, filename)

        # Действие
        result = self.responder_csv.create(recipe)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result)

        # Проверка
        self.assertTrue(os.path.exists(filepath))
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем структуру CSV
        expected_header = "id;ingredients;name;steps"
        self.assertIn(expected_header, content)
        self.assertIn("Простые лепешки", content)
        self.assertIn("Пшеничная мука", content)
        self.assertIn("400", content)
        self.assertIn("Яйца куриные", content)
        self.assertIn("Молоко", content)

    def test_create_recipe_json_file(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Простые лепешки"]
        filename = "простые_лепешки.json"
        filepath = os.path.join(self.test_output_dir, filename)

        # Действие
        result = self.responder_json.create(recipe)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result)

        # Проверка
        self.assertTrue(os.path.exists(filepath))
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            data = json.loads(content)
        
        # Проверяем структуру JSON
        self.assertIsInstance(data, list)
        recipe_data = data[0]
        self.assertEqual(recipe_data["name"], "Простые лепешки")
        self.assertIn("id", recipe_data)
        self.assertIn("ingredients", recipe_data)
        self.assertIn("steps", recipe_data)
        
        # Проверяем ингредиенты
        ingredient_names = [ing["nomenclature_name"] for ing in recipe_data["ingredients"]]
        self.assertIn("Пшеничная мука", ingredient_names)
        self.assertIn("Яйца куриные", ingredient_names)
        
        # Проверяем шаги
        self.assertIn("Подготовка ингредиентов", recipe_data["steps"][0])

    def test_create_recipe_markdown_file(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Простые лепешки"]
        filename = "простые_лепешки.md"
        filepath = os.path.join(self.test_output_dir, filename)

        # Действие
        result = self.responder_markdown.create(recipe)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result)

        # Проверка
        self.assertTrue(os.path.exists(filepath))
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем структуру Markdown
        self.assertIn("# Простые лепешки", content)
        self.assertIn("## Свойства:", content)
        self.assertIn("| Свойство | Значение |", content)
        self.assertIn("Пшеничная мука", content)
        self.assertIn("400", content)
        self.assertIn("ingredients", content)
        self.assertIn("steps", content)

    def test_create_recipe_xml_file(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Простые лепешки"]
        filename = "простые_лепешки.xml"
        filepath = os.path.join(self.test_output_dir, filename)

        # Действие
        result = self.responder_xml.create(recipe)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result)

        # Проверка
        self.assertTrue(os.path.exists(filepath))
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем структуру XML
        self.assertIn('<?xml version="1.0" encoding="UTF-8"?>', content)
        self.assertIn("<name>Простые лепешки</name>", content)
        self.assertIn("<ingredients>", content)
        self.assertIn("<nomenclature_name>Пшеничная мука</nomenclature_name>", content)
        self.assertIn("<quantity>400</quantity>", content)
        self.assertIn("<steps>", content)
        self.assertIn("Подготовка ингредиентов", content)

    def test_create_all_recipe_formats(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Простые лепешки"]
        formats = [
            ('csv', self.responder_csv),
            ('json', self.responder_json),
            ('md', self.responder_markdown),
            ('xml', self.responder_xml)
        ]
        created_files = []

        # Действие
        for ext, responder in formats:
            result = responder.create(recipe)
            filename = f"простые_лепешки.{ext}"
            filepath = os.path.join(self.test_output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(result)
            
            created_files.append(filepath)

        # Проверка
        for filepath in created_files:
            self.assertTrue(os.path.exists(filepath))
            file_size = os.path.getsize(filepath)
            self.assertGreater(file_size, 0, f"Файл {filepath} пустой")
        
        files_in_dir = os.listdir(self.test_output_dir)
        self.assertEqual(len(files_in_dir), 4)

    def test_recipe_content_consistency(self):
        # Подготовка
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Простые лепешки"]
        ingredients_to_check = ["Пшеничная мука", "Яйца куриные", "Молоко"]
        steps_to_check = ["Подготовка ингредиентов", "Замес теста", "Выпекание"]

        # Действие
        csv_content = self.responder_csv.create(recipe)
        json_content = self.responder_json.create(recipe)
        md_content = self.responder_markdown.create(recipe)
        xml_content = self.responder_xml.create(recipe)

        # Проверка для CSV
        self.assertIn("Простые лепешки", csv_content)
        for ingredient in ingredients_to_check:
            self.assertIn(ingredient, csv_content)
        for step in steps_to_check:
            self.assertIn(step, csv_content)

        # Проверка для JSON
        json_data = json.loads(json_content)
        recipe_json = json_data[0]
        self.assertEqual(recipe_json["name"], "Простые лепешки")
        ingredient_names = [ing["nomenclature_name"] for ing in recipe_json["ingredients"]]
        for ingredient in ingredients_to_check:
            self.assertIn(ingredient, ingredient_names)
        for step in steps_to_check:
            step_found = any(step in s for s in recipe_json["steps"])
            self.assertTrue(step_found, f"Шаг '{step}' не найден в JSON")

        # Проверка для Markdown
        self.assertIn("# Простые лепешки", md_content)
        for ingredient in ingredients_to_check:
            self.assertIn(ingredient, md_content)
        for step in steps_to_check:
            self.assertIn(step, md_content)

        # Проверка для XML
        self.assertIn("<name>Простые лепешки</name>", xml_content)
        for ingredient in ingredients_to_check:
            self.assertIn(ingredient, xml_content)
        for step in steps_to_check:
            self.assertIn(step, xml_content)

if __name__ == '__main__':
    unittest.main()