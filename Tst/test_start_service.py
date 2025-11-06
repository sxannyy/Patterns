import unittest
from datetime import datetime
from Src.Core.osv_builder import osv_builder
from Src.Core.validator import argument_exception
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.reposity import reposity
from Src.Models.measure_model import measure_model
from Src.Models.recipe_model import recipe_model
from Src.start_service import start_service
from Src.Models.storage_model import storage_model
from Src.Models.transaction_model import transaction_model
from Src.Models.osv_model import osv_model
import os

"""
    Unit-тесты для класса start_service.
    Проверяются:
    - создание сервиса и Singleton
    - инициализация репозитория с пустыми данными
    - создание стандартных единиц измерения
    - создание стандартных групп номенклатуры
    - создание стандартной номенклатуры
    - создание рецептов
    - создание складов
    - создание транзакций
    - создание оборотно-сальдовой ведомости
    - выгрузка данных в файл
    - запуск полной инициализации данных
"""

class TestStartService(unittest.TestCase):
    __start_service = start_service()

    def setUp(self):
        """Инициализация сервиса перед каждым тестом"""
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
        self.assertIn(reposity.storage_key(), data)
        self.assertIn(reposity.transaction_key(), data)
        
        # Проверяем, что данные созданы (не пустые словари)
        self.assertGreater(len(data[reposity.measure_key()]), 0)
        self.assertGreater(len(data[reposity.nomenclature_key()]), 0)
        self.assertGreater(len(data[reposity.nomenclature_group_key()]), 0)
        self.assertGreater(len(data[reposity.recipe_key()]), 0)
        self.assertGreater(len(data[reposity.storage_key()]), 0)
        self.assertGreater(len(data[reposity.transaction_key()]), 0)

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
        # Проверяем меры - должно быть 5 единиц измерения
        self.assertEqual(len(data[reposity.measure_key()]), 5)
        # Проверяем группы номенклатуры - должно быть 3 группы
        self.assertEqual(len(data[reposity.nomenclature_group_key()]), 3)
        # Проверяем номенклатуру - должно быть 8 позиций
        self.assertEqual(len(data[reposity.nomenclature_key()]), 8)
        # Проверяем рецепты - должно быть 3 рецепта
        self.assertEqual(len(data[reposity.recipe_key()]), 3)
        # Проверяем склады - должно быть 2 склада
        self.assertEqual(len(data[reposity.storage_key()]), 2)
        # Проверяем транзакции - должно быть 5 транзакций
        self.assertEqual(len(data[reposity.transaction_key()]), 5)
        
        # Проверяем конкретные рецепты
        self.assertIn('Вафли', data[reposity.recipe_key()])
        self.assertIn('Омлет с молоком', data[reposity.recipe_key()])
        self.assertIn('Простые лепешки', data[reposity.recipe_key()])
        
        # Проверяем конкретные склады
        self.assertIn('Основной склад', data[reposity.storage_key()])
        self.assertIn('Резервный склад', data[reposity.storage_key()])

    def test_check_create_storages(self):
        # Подготовка
        storages = self.__start_service.data()[reposity.storage_key()]

        # Действия

        # Проверка
        self.assertIn('Основной склад', storages)
        self.assertIn('Резервный склад', storages)
        self.assertIsInstance(storages['Основной склад'], storage_model)
        self.assertIsInstance(storages['Резервный склад'], storage_model)
        
        # Проверка атрибутов складов
        main_storage = storages['Основной склад']
        self.assertEqual(main_storage.name, "Основной склад")
        self.assertEqual(main_storage.address, "ул. Центральная, 1")
        
        reserve_storage = storages['Резервный склад']
        self.assertEqual(reserve_storage.name, "Резервный склад")
        self.assertEqual(reserve_storage.address, "ул. Крестьянская, 47")

    def test_check_create_transactions(self):
        # Подготовка
        transactions = self.__start_service.data()[reposity.transaction_key()]

        # Действия

        # Проверка
        self.assertEqual(len(transactions), 5)
        
        # Проверяем, что все транзакции являются transaction_model
        for transaction_key, transaction in transactions.items():
            self.assertIsInstance(transaction, transaction_model)
            self.assertIsNotNone(transaction.unique_code)
            self.assertIsNotNone(transaction.name)
            self.assertIsNotNone(transaction.date)
            self.assertIsNotNone(transaction.nomenclature)
            self.assertIsNotNone(transaction.storage)
            self.assertIsNotNone(transaction.measure)
            self.assertIsNotNone(transaction.quantity)

    def test_check_transaction_quantities(self):
        # Подготовка
        transactions = self.__start_service.data()[reposity.transaction_key()]

        # Действия
        # Ищем транзакции по имени для проверки количеств
        receipt_transactions = [t for t in transactions.values() if "Поступление" in t.name]
        expense_transactions = [t for t in transactions.values() if "Расход" in t.name]

        # Проверка
        self.assertEqual(len(receipt_transactions), 3)  # 3 приходные транзакции
        self.assertEqual(len(expense_transactions), 2)  # 2 расходные транзакции
        
        # Проверяем знаки количеств
        for transaction in receipt_transactions:
            self.assertGreater(transaction.quantity, 0)
        
        for transaction in expense_transactions:
            self.assertLess(transaction.quantity, 0)

    def test_check_create_osv(self):
        # Подготовка
        start_date = datetime(2025, 10, 1)
        end_date = datetime(2025, 10, 31)
        
        # Получаем объект склада из репозитория
        storage = self.__start_service.repo.data[reposity.storage_key()]["Основной склад"]
        
        # Действия
        osv = self.__start_service.create_osv(start_date, end_date, storage)

        # Проверка
        self.assertIsInstance(osv, osv_builder)
        self.assertEqual(osv.start_date, start_date)
        self.assertEqual(osv.end_date, end_date)
        self.assertEqual(osv.storage.name, "Основной склад")
        self.assertIsInstance(osv.rows, list)

    def test_check_dump_method(self):
        # Подготовка
        filename = "test_dump.json"

        # Действия
        self.__start_service.dump(filename)

        # Проверка
        self.assertTrue(os.path.exists(filename))
        
        # Проверяем, что файл не пустой
        file_size = os.path.getsize(filename)
        self.assertGreater(file_size, 0)
        
        # Очистка
        if os.path.exists(filename):
            os.remove(filename)

    def test_check_dump_method_invalid_filename(self):
        # Подготовка
        invalid_filename = "/invalid/path/test_dump.json"

        # Проверка
        with self.assertRaises(argument_exception):
            self.__start_service.dump(invalid_filename)

    def test_check_repository_keys_completeness(self):
        # Подготовка
        data = self.__start_service.data()
        expected_keys = [
            reposity.measure_key(),
            reposity.recipe_key(),
            reposity.nomenclature_key(),
            reposity.nomenclature_group_key(),
            reposity.storage_key(),
            reposity.transaction_key()
        ]

        # Действия

        # Проверка
        for key in expected_keys:
            self.assertIn(key, data)
            self.assertIsInstance(data[key], dict)

    def test_check_transaction_dates(self):
        # Подготовка
        transactions = self.__start_service.data()[reposity.transaction_key()]

        # Действия

        # Проверка
        for transaction in transactions.values():
            self.assertIsInstance(transaction.date, datetime)
            # Проверяем, что дата в разумных пределах (не будущее и не слишком далекое прошлое)
            self.assertLess(transaction.date.year, 2030)
            self.assertGreater(transaction.date.year, 2020)

    def test_check_recipe_ingredients_connections(self):
        # Подготовка
        recipes = self.__start_service.data()[reposity.recipe_key()]
        nomenclature = self.__start_service.data()[reposity.nomenclature_key()]

        # Действия

        # Проверка
        for recipe_name, recipe_obj in recipes.items():
            self.assertGreater(len(recipe_obj.ingredients), 0, f"Рецепт '{recipe_name}' не имеет ингредиентов")
            for ingredient in recipe_obj.ingredients:
                nom_obj, quantity = ingredient
                self.assertIsNotNone(nom_obj, f"Ингредиент в рецепте '{recipe_name}' не имеет номенклатуры")
                self.assertIsInstance(quantity, (int, float), f"Количество ингредиента в рецепте '{recipe_name}' не является числом")

    def test_check_singleton_after_multiple_instances(self):
        # Подготовка
        service1 = start_service()
        service2 = start_service()
        service3 = start_service()

        # Действия
        data1 = service1.data()
        data2 = service2.data()
        data3 = service3.data()

        # Проверка
        self.assertIs(service1, service2)
        self.assertIs(service2, service3)
        self.assertIs(service1, service3)
        self.assertIs(data1, data2)
        self.assertIs(data2, data3)

    def test_check_service_data_consistency(self):
        # Подготовка
        data = self.__start_service.data()

        # Действия

        # Проверка
        # Все ключи должны быть строками
        for key in data:
            self.assertIsInstance(key, str)
            
        # Все значения по ключам должны быть словарями
        for key, value_dict in data.items():
            self.assertIsInstance(value_dict, dict)
            
        # Проверяем, что во всех словарях ключи - строки
        for key, value_dict in data.items():
            for sub_key in value_dict:
                self.assertIsInstance(sub_key, str)

if __name__ == '__main__':
    unittest.main()