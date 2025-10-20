import unittest
from Src.Logics.response_csv import response_csv
from Src.Logics.factory_entities import factory_entities
from Src.Core.validator import operation_exception
from Src.Logics.response_json import response_json
from Src.Logics.response_markdown import response_markdown
from Src.Logics.response_xml import response_xml
from Src.Models.settings_model import settings_model
from Src.Core.response_format import response_formats
from Src.Logics.factory_entities import factory_entities
from Src.Core.response_format import response_formats

from Src.reposity import reposity
from Src.start_service import start_service
import json

"""
    Unit-тесты для модуля Logics приложения кулинарных рецептов.
    Проверяется:
    - Фабрика создания обработчиков ответов (factory_entities)
    - Формирование ответов в различных форматах (CSV, JSON, Markdown, XML)
    - Обработка одиночных рецептов и списков рецептов
    - Валидация входных параметров и обработка ошибок
    - Корректность преобразования данных рецептов в целевые форматы
"""

class test_logics(unittest.TestCase):
    __start_service = start_service()

    def __init__(self, methodName="runTest"):
        """
        Инициализация тестового класса.
        
        Args:
            methodName (str): Название метода тестирования
        """
        super().__init__(methodName)
        self.__start_service.start()

    def setUp(self):
        """
        Подготовка тестового окружения перед каждым тестом.
        Инициализирует фабрику и обработчики различных форматов ответов.
        """
        self.factory = factory_entities()
        self.responder = response_csv()
        self.responder_json = response_json()
        self.responder_markdown = response_markdown()
        self.responder_xml = response_xml()

    def test_response_formats(self):
        """
        Проверка корректности сопоставления форматов ответов с классами обработчиков.
        Тестирует, что фабрика правильно связывает каждый формат с соответствующим классом.
        """
        expected_formats = {
            response_formats.csv(): response_csv,
            response_formats.json(): response_json,
            response_formats.markdown(): response_markdown,
            response_formats.xml(): response_xml
        }
        self.assertEqual(self.factory.response_formats, expected_formats)

    def test_create_valid_csv(self):
        """
        Проверка создания обработчика CSV формата через фабрику.
        Убеждается, что фабрика возвращает корректный тип объекта для CSV формата.
        """
        responder = self.factory.create(response_formats.csv())
        self.assertIsInstance(responder, type(response_csv))

    def test_create_invalid_format(self):
        """
        Проверка обработки некорректного формата фабрикой.
        Ожидается выброс исключения operation_exception при передаче невалидного формата.
        """
        with self.assertRaises(operation_exception):
            self.factory.create('invalid_format')
            
    def test_create_default_none_settings(self):
        """
        Проверка обработки пустых настроек в методе create_default.
        Ожидается исключение при передаче None в качестве параметра настроек.
        """
        with self.assertRaises(operation_exception):
            self.factory.create_default(None)

    def test_create_default_valid(self):
        """
        Проверка создания обработчика по умолчанию на основе валидных настроек.
        Тестирует создание CSV обработчика при соответствующих настройках формата ответа.
        """
        settings = settings_model()
        settings.response_format = response_formats.csv()
        responder = self.factory.create_default(settings)
        self.assertIsInstance(responder, type(response_csv))

    def test_create_single_recipe(self):
        """
        Проверка преобразования одиночного рецепта в CSV формат.
        Тестирует корректность формирования структуры CSV с разделителями-точками с запятой.
        """
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]
        result = self.responder.create(recipe)
        expected = "Название;Ингредиенты;Шаги приготовления\nОмлет с молоком;Яйца куриные: 3, Молоко: 150, Соль: 3, Сливочное масло: 20, Перец черный: 2;1. Подготовка яиц: Яйца куриные достаньте заранее, чтобы они достигли комнатной температуры | 2. Взбивание основы: В миске взбейте яйца с солью и черным перцем до легкой пены и однородной консистенции | 3. Добавление молока: Постепенно влейте молоко, аккуратно перемешивая. Избегайте интенсивного взбивания | 4. Подготовка сковороды: В сковороде растопите сливочное масло, равномерно распределите по всей поверхности | 5. Выпекание: Вылейте яично-молочную смесь в разогретую сковороду. Накройте крышкой | 6. Приготовление: Готовьте на среднем огне 7-10 минут. Омлет готов, когда края золотятся, а середина пропечена | 7. Подача: Немного дайте омлету остыть в сковороде, затем аккуратно сверните или разрежьте на порции. Подавайте сразу после приготовления\n"
        self.assertEqual(result, expected)

    def test_create_list_recipes(self):
        """
        Проверка преобразования списка рецептов в CSV формат.
        Тестирует обработку массива рецептов и формирование корректной CSV структуры.
        """
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]
        data = [recipe]
        result = self.responder.create(data)
        expected = "Название;Ингредиенты;Шаги приготовления\nОмлет с молоком;Яйца куриные: 3, Молоко: 150, Соль: 3, Сливочное масло: 20, Перец черный: 2;1. Подготовка яиц: Яйца куриные достаньте заранее, чтобы они достигли комнатной температуры | 2. Взбивание основы: В миске взбейте яйца с солью и черным перцем до легкой пены и однородной консистенции | 3. Добавление молока: Постепенно влейте молоко, аккуратно перемешивая. Избегайте интенсивного взбивания | 4. Подготовка сковороды: В сковороде растопите сливочное масло, равномерно распределите по всей поверхности | 5. Выпекание: Вылейте яично-молочную смесь в разогретую сковороду. Накройте крышкой | 6. Приготовление: Готовьте на среднем огне 7-10 минут. Омлет готов, когда края золотятся, а середина пропечена | 7. Подача: Немного дайте омлету остыть в сковороде, затем аккуратно сверните или разрежьте на порции. Подавайте сразу после приготовления\n"
        self.assertEqual(result, expected)

    def test_create_valid_json(self):
        """
        Проверка создания обработчика JSON формата через фабрику.
        Убеждается, что фабрика возвращает корректный тип объекта для JSON формата.
        """
        responder = self.factory.create(response_formats.json())
        self.assertIsInstance(responder, type(response_json))

    def test_create_default_valid_json(self):
        """
        Проверка создания JSON обработчика по умолчанию на основе настроек.
        Тестирует создание JSON обработчика при соответствующих настройках формата ответа.
        """
        settings = settings_model()
        settings.response_format = response_formats.json()
        responder = self.factory.create_default(settings)
        self.assertIsInstance(responder, type(response_json))

    def test_create_single_recipe_json(self):
        """
        Проверка преобразования одиночного рецепта в JSON формат.
        Тестирует корректность формирования JSON структуры с ингредиентами и шагами приготовления.
        """
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]
        result = self.responder_json.create(recipe)
        expected_data = [
            {
                "name": "Омлет с молоком",
                "ingredients": [
                    {"nomenclature": "Яйца куриные", "quantity": 3},
                    {"nomenclature": "Молоко", "quantity": 150},
                    {"nomenclature": "Соль", "quantity": 3},
                    {"nomenclature": "Сливочное масло", "quantity": 20},
                    {"nomenclature": "Перец черный", "quantity": 2}
                ],
                "steps": [
                    "Подготовка яиц: Яйца куриные достаньте заранее, чтобы они достигли комнатной температуры",
                    "Взбивание основы: В миске взбейте яйца с солью и черным перцем до легкой пены и однородной консистенции",
                    "Добавление молока: Постепенно влейте молоко, аккуратно перемешивая. Избегайте интенсивного взбивания",
                    "Подготовка сковороды: В сковороде растопите сливочное масло, равномерно распределите по всей поверхности",
                    "Выпекание: Вылейте яично-молочную смесь в разогретую сковороду. Накройте крышкой",
                    "Приготовление: Готовьте на среднем огне 7-10 минут. Омлет готов, когда края золотятся, а середина пропечена",
                    "Подача: Немного дайте омлету остыть в сковороде, затем аккуратно сверните или разрежьте на порции. Подавайте сразу после приготовления"
                ]
            }
        ]
        expected = json.dumps(expected_data, ensure_ascii=False, indent=2)
        self.assertEqual(result, expected)

    def test_create_list_recipes_json(self):
        """
        Проверка преобразования списка рецептов в JSON формат.
        Тестирует обработку массива рецептов и формирование корректной JSON структуры.
        """
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]
        data = [recipe]
        result = self.responder_json.create(data)
        expected_data = [
            {
                "name": "Омлет с молоком",
                "ingredients": [
                    {"nomenclature": "Яйца куриные", "quantity": 3},
                    {"nomenclature": "Молоко", "quantity": 150},
                    {"nomenclature": "Соль", "quantity": 3},
                    {"nomenclature": "Сливочное масло", "quantity": 20},
                    {"nomenclature": "Перец черный", "quantity": 2}
                ],
                "steps": [
                    "Подготовка яиц: Яйца куриные достаньте заранее, чтобы они достигли комнатной температуры",
                    "Взбивание основы: В миске взбейте яйца с солью и черным перцем до легкой пены и однородной консистенции",
                    "Добавление молока: Постепенно влейте молоко, аккуратно перемешивая. Избегайте интенсивного взбивания",
                    "Подготовка сковороды: В сковороде растопите сливочное масло, равномерно распределите по всей поверхности",
                    "Выпекание: Вылейте яично-молочную смесь в разогретую сковороду. Накройте крышкой",
                    "Приготовление: Готовьте на среднем огне 7-10 минут. Омлет готов, когда края золотятся, а середина пропечена",
                    "Подача: Немного дайте омлету остыть в сковороде, затем аккуратно сверните или разрежьте на порции. Подавайте сразу после приготовления"
                ]
            }
        ]
        expected = json.dumps(expected_data, ensure_ascii=False, indent=2)
        self.assertEqual(result, expected)

    def test_create_valid_markdown(self):
        """
        Проверка создания обработчика Markdown формата через фабрику.
        Убеждается, что фабрика возвращает корректный тип объекта для Markdown формата.
        """
        responder = self.factory.create(response_formats.markdown())
        self.assertIsInstance(responder, type(response_markdown))

    def test_create_default_valid_markdown(self):
        """
        Проверка создания Markdown обработчика по умолчанию на основе настроек.
        Тестирует создание Markdown обработчика при соответствующих настройках формата ответа.
        """
        settings = settings_model()
        settings.response_format = response_formats.markdown()
        responder = self.factory.create_default(settings)
        self.assertIsInstance(responder, type(response_markdown))

    def test_create_single_recipe_markdown(self):
        """
        Проверка преобразования одиночного рецепта в Markdown формат.
        Тестирует корректность формирования Markdown разметки с таблицей ингредиентов и нумерованным списком шагов.
        """
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]
        result = self.responder_markdown.create(recipe)
        expected = "# Омлет с молоком\n\n## Ингредиенты:\n| Ингредиент | Количество |\n|-------------|------------|\n| Яйца куриные | 3 |\n| Молоко | 150 |\n| Соль | 3 |\n| Сливочное масло | 20 |\n| Перец черный | 2 |\n\n## Шаги приготовления:\n1. Подготовка яиц: Яйца куриные достаньте заранее, чтобы они достигли комнатной температуры\n2. Взбивание основы: В миске взбейте яйца с солью и черным перцем до легкой пены и однородной консистенции\n3. Добавление молока: Постепенно влейте молоко, аккуратно перемешивая. Избегайте интенсивного взбивания\n4. Подготовка сковороды: В сковороде растопите сливочное масло, равномерно распределите по всей поверхности\n5. Выпекание: Вылейте яично-молочную смесь в разогретую сковороду. Накройте крышкой\n6. Приготовление: Готовьте на среднем огне 7-10 минут. Омлет готов, когда края золотятся, а середина пропечена\n7. Подача: Немного дайте омлету остыть в сковороде, затем аккуратно сверните или разрежьте на порции. Подавайте сразу после приготовления\n\n---\n\n"
        self.assertEqual(result, expected)

    def test_create_list_recipes_markdown(self):
        """
        Проверка преобразования списка рецептов в Markdown формат.
        Тестирует обработку массива рецептов и формирование корректной Markdown разметки.
        """
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]
        data = [recipe]
        result = self.responder_markdown.create(data)
        expected = "# Омлет с молоком\n\n## Ингредиенты:\n| Ингредиент | Количество |\n|-------------|------------|\n| Яйца куриные | 3 |\n| Молоко | 150 |\n| Соль | 3 |\n| Сливочное масло | 20 |\n| Перец черный | 2 |\n\n## Шаги приготовления:\n1. Подготовка яиц: Яйца куриные достаньте заранее, чтобы они достигли комнатной температуры\n2. Взбивание основы: В миске взбейте яйца с солью и черным перцем до легкой пены и однородной консистенции\n3. Добавление молока: Постепенно влейте молоко, аккуратно перемешивая. Избегайте интенсивного взбивания\n4. Подготовка сковороды: В сковороде растопите сливочное масло, равномерно распределите по всей поверхности\n5. Выпекание: Вылейте яично-молочную смесь в разогретую сковороду. Накройте крышкой\n6. Приготовление: Готовьте на среднем огне 7-10 минут. Омлет готов, когда края золотятся, а середина пропечена\n7. Подача: Немного дайте омлету остыть в сковороде, затем аккуратно сверните или разрежьте на порции. Подавайте сразу после приготовления\n\n---\n\n"
        self.assertEqual(result, expected)

    def test_create_valid_xml(self):
        """
        Проверка создания обработчика XML формата через фабрику.
        Убеждается, что фабрика возвращает корректный тип объекта для XML формата.
        """
        responder = self.factory.create(response_formats.xml())
        self.assertIsInstance(responder, type(response_xml))

    def test_create_default_valid_xml(self):
        """
        Проверка создания XML обработчика по умолчанию на основе настроек.
        Тестирует создание XML обработчика при соответствующих настройках формата ответа.
        """
        settings = settings_model()
        settings.response_format = response_formats.xml()
        responder = self.factory.create_default(settings)
        self.assertIsInstance(responder, type(response_xml))

    def test_create_single_recipe_xml(self):
        """
        Проверка преобразования одиночного рецепта в XML формат.
        Тестирует корректность формирования XML структуры с вложенными элементами ингредиентов и шагов.
        """
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]
        result = self.responder_xml.create(recipe)
        expected = '<recipes><recipe><name>Омлет с молоком</name><ingredients><ingredient><nomenclature>Яйца куриные</nomenclature><quantity>3</quantity></ingredient><ingredient><nomenclature>Молоко</nomenclature><quantity>150</quantity></ingredient><ingredient><nomenclature>Соль</nomenclature><quantity>3</quantity></ingredient><ingredient><nomenclature>Сливочное масло</nomenclature><quantity>20</quantity></ingredient><ingredient><nomenclature>Перец черный</nomenclature><quantity>2</quantity></ingredient></ingredients><steps><step number="1">Подготовка яиц: Яйца куриные достаньте заранее, чтобы они достигли комнатной температуры</step><step number="2">Взбивание основы: В миске взбейте яйца с солью и черным перцем до легкой пены и однородной консистенции</step><step number="3">Добавление молока: Постепенно влейте молоко, аккуратно перемешивая. Избегайте интенсивного взбивания</step><step number="4">Подготовка сковороды: В сковороде растопите сливочное масло, равномерно распределите по всей поверхности</step><step number="5">Выпекание: Вылейте яично-молочную смесь в разогретую сковороду. Накройте крышкой</step><step number="6">Приготовление: Готовьте на среднем огне 7-10 минут. Омлет готов, когда края золотятся, а середина пропечена</step><step number="7">Подача: Немного дайте омлету остыть в сковороде, затем аккуратно сверните или разрежьте на порции. Подавайте сразу после приготовления</step></steps></recipe></recipes>'
        self.assertEqual(result, expected)

    def test_create_list_recipes_xml(self):
        """
        Проверка преобразования списка рецептов в XML формат.
        Тестирует обработку массива рецептов и формирование корректной XML структуры.
        """
        recipe = self.__start_service.repo.data[reposity.recipe_key()]["Омлет с молоком"]
        data = [recipe]
        result = self.responder_xml.create(data)
        expected = '<recipes><recipe><name>Омлет с молоком</name><ingredients><ingredient><nomenclature>Яйца куриные</nomenclature><quantity>3</quantity></ingredient><ingredient><nomenclature>Молоко</nomenclature><quantity>150</quantity></ingredient><ingredient><nomenclature>Соль</nomenclature><quantity>3</quantity></ingredient><ingredient><nomenclature>Сливочное масло</nomenclature><quantity>20</quantity></ingredient><ingredient><nomenclature>Перец черный</nomenclature><quantity>2</quantity></ingredient></ingredients><steps><step number="1">Подготовка яиц: Яйца куриные достаньте заранее, чтобы они достигли комнатной температуры</step><step number="2">Взбивание основы: В миске взбейте яйца с солью и черным перцем до легкой пены и однородной консистенции</step><step number="3">Добавление молока: Постепенно влейте молоко, аккуратно перемешивая. Избегайте интенсивного взбивания</step><step number="4">Подготовка сковороды: В сковороде растопите сливочное масло, равномерно распределите по всей поверхности</step><step number="5">Выпекание: Вылейте яично-молочную смесь в разогретую сковороду. Накройте крышкой</step><step number="6">Приготовление: Готовьте на среднем огне 7-10 минут. Омлет готов, когда края золотятся, а середина пропечена</step><step number="7">Подача: Немного дайте омлету остыть в сковороде, затем аккуратно сверните или разрежьте на порции. Подавайте сразу после приготовления</step></steps></recipe></recipes>'
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()