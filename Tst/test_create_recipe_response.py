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
        
        expected_header = "ingredients;name;steps"
        self.assertIn(expected_header, content)
        self.assertIn("Простые лепешки", content)
        self.assertIn("Пшеничная мука", content)
        self.assertIn("400", content)

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
        
        self.assertEqual(data[0]["name"], "Простые лепешки")
        self.assertIn("Пшеничная мука", [ing["nomenclature"] for ing in data[0]["ingredients"]])
        self.assertIn("Подготовка ингредиентов", data[0]["steps"][0])

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
        
        self.assertIn("# Простые лепешки", content)
        self.assertIn("## Ингредиенты:", content)
        self.assertIn("Пшеничная мука", content)
        self.assertIn("400", content)
        self.assertIn("## Шаги приготовления:", content)
        self.assertIn("Подготовка ингредиентов", content)

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
        
        self.assertIn('<?xml version="1.0" encoding="UTF-8"?>', content)
        self.assertIn("<name>Простые лепешки</name>", content)
        self.assertIn("Пшеничная мука", content)
        self.assertIn("400", content)
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

        # Проверка
        self.assertIn("Простые лепешки", csv_content)
        self.assertIn("Простые лепешки", json_content)
        self.assertIn("Простые лепешки", md_content)
        self.assertIn("Простые лепешки", xml_content)
        
        for ingredient in ingredients_to_check:
            self.assertIn(ingredient, csv_content)
            self.assertIn(ingredient, json_content)
            self.assertIn(ingredient, md_content)
            self.assertIn(ingredient, xml_content)
        
        for step in steps_to_check:
            self.assertIn(step, csv_content)
            self.assertIn(step, json_content)
            self.assertIn(step, md_content)
            self.assertIn(step, xml_content)

if __name__ == '__main__':
    unittest.main()