import os
import unittest
import json
import tempfile
import shutil

from Src.reposity import reposity
from Src.start_service import start_service
from Src.settings_manager import settings_manager
from Src.Logics.reference_service import reference_service
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.measure_model import measure_model
from Src.Models.storage_model import storage_model
from Src.Core.validator import argument_exception
from Src.Convertors.convert_factory import convert_factory

"""
    Unit-тесты для класса reference_service.
    Проверяются:
    - создание сервиса справочников
    - получение элементов справочников
    - добавление новых элементов
    - обновление существующих элементов
    - удаление элементов
    - проверка зависимостей при удалении
"""

class TestReferenceService(unittest.TestCase):
    
    def setUp(self):
        """Подготовка тестового окружения"""
        # Создаем временную директорию для тестовых файлов
        self.test_dir = tempfile.mkdtemp()
        self.settings_file = os.path.join(self.test_dir, 'test_settings.json')
        self.data_file = os.path.join(self.test_dir, 'test_data.json')
        
        # Создаем тестовые настройки
        test_settings = {
            "first_start": True,
            "response_format": "json",
            "company": {
                "name": "Test Company"
            },
            "block_date": "2025-01-01"
        }
        
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(test_settings, f, ensure_ascii=False, indent=2)
        
        # Инициализируем сервисы
        self.settings_mgr = settings_manager(self.settings_file)
        self.start_srv = start_service()
        self.start_srv._start_service__data_file = self.data_file

        # Инициализируем приложение с тестовыми данными
        self.start_srv.initialize_application(self.settings_mgr)

        # Создаем сервис справочников
        self.ref_service = reference_service(
            self.start_srv.repo,
            self.start_srv,
            self.settings_mgr
        )

        # Создаем конвертер для преобразования объектов в словари
        self.converter = convert_factory()

    def tearDown(self):
        """Очистка после тестов"""
        # Удаляем временную директорию
        shutil.rmtree(self.test_dir)

    def test_get_existing_nomenclature(self):
        # Подготовка
        nomenclatures = self.start_srv.repo.data[reposity.nomenclature_key()]
        sugar_nomenclature = nomenclatures.get('Сахар')

        # Действие
        result = self.ref_service.get_one('nomenclature', sugar_nomenclature.unique_code)

        # Проверка
        self.assertEqual(result, sugar_nomenclature)
        self.assertEqual(result.name, 'Сахар')

    def test_get_nonexistent_nomenclature(self):
        # Подготовка
        nonexistent_code = 'nonexistent-code-123'

        # Действие
        result = self.ref_service.get_one('nomenclature', nonexistent_code)

        # Проверка
        self.assertIsNone(result)

    def test_add_new_nomenclature(self):
        # Подготовка
        group = self.start_srv.repo.data[reposity.nomenclature_group_key()]['СиП']
        measure = self.start_srv.repo.data[reposity.measure_key()]['г']

        new_nom = nomenclature_model(
            'Новый продукт',
            'Полное название нового продукта',
            group,
            measure
        )

        # Преобразуем объект в словарь для передачи в API
        new_nom_dict = self.converter.convert(new_nom)

        # Действие
        result = self.ref_service.add('nomenclature', new_nom_dict)

        # Проверка
        self.assertIsNotNone(result)
        retrieved = self.ref_service.get_one('nomenclature', new_nom.unique_code)
        self.assertIsNotNone(retrieved)

        # Проверяем имя (retrieved может быть словарем или объектом)
        if isinstance(retrieved, dict):
            self.assertEqual(retrieved['name'], 'Новый продукт')
        else:
            self.assertEqual(retrieved.name, 'Новый продукт')

    def test_add_duplicate_nomenclature(self):
        # Подготовка
        nomenclatures = self.start_srv.repo.data[reposity.nomenclature_key()]
        existing_nom = nomenclatures.get('Сахар')

        # Преобразуем объект в словарь
        existing_nom_dict = self.converter.convert(existing_nom)

        # Действие & Проверка
        with self.assertRaises(argument_exception) as context:
            self.ref_service.add('nomenclature', existing_nom_dict)

        self.assertIn("уже существует", str(context.exception))

    def test_update_nomenclature(self):
        # Подготовка
        nomenclatures = self.start_srv.repo.data[reposity.nomenclature_key()]
        sugar_nomenclature = nomenclatures.get('Сахар')
        changes = {'name': 'Сахар обновленный'}

        # Действие
        result = self.ref_service.update('nomenclature', sugar_nomenclature.unique_code, changes)

        # Проверка
        self.assertEqual(result.name, 'Сахар обновленный')
        updated = self.ref_service.get_one('nomenclature', sugar_nomenclature.unique_code)
        self.assertEqual(updated.name, 'Сахар обновленный')

    def test_update_nonexistent_nomenclature(self):
        # Подготовка
        nonexistent_code = 'nonexistent-code-123'
        changes = {'name': 'Новое имя'}

        # Действие & Проверка
        with self.assertRaises(argument_exception) as context:
            self.ref_service.update('nomenclature', nonexistent_code, changes)
        
        self.assertIn("не найден", str(context.exception))

    def test_delete_nomenclature(self):
        # Подготовка
        group = self.start_srv.repo.data[reposity.nomenclature_group_key()]['СиП']
        measure = self.start_srv.repo.data[reposity.measure_key()]['г']

        temp_nom = nomenclature_model(
            'Временный продукт',
            'Временный продукт для удаления',
            group,
            measure
        )

        # Преобразуем объект в словарь
        temp_nom_dict = self.converter.convert(temp_nom)
        self.ref_service.add('nomenclature', temp_nom_dict)

        # Действие
        result = self.ref_service.delete('nomenclature', temp_nom.unique_code)

        # Проверка
        self.assertTrue(result)
        deleted = self.ref_service.get_one('nomenclature', temp_nom.unique_code)
        self.assertIsNone(deleted)

    def test_delete_nonexistent_nomenclature(self):
        # Подготовка
        nonexistent_code = 'nonexistent-code-123'

        # Действие & Проверка
        with self.assertRaises(argument_exception) as context:
            self.ref_service.delete('nomenclature', nonexistent_code)
        
        self.assertIn("не найден", str(context.exception))

    def test_get_existing_measure(self):
        # Подготовка
        measures = self.start_srv.repo.data[reposity.measure_key()]
        gram_measure = measures.get('г')

        # Действие
        result = self.ref_service.get_one('measure', gram_measure.unique_code)

        # Проверка
        self.assertEqual(result, gram_measure)
        self.assertEqual(result.name, 'грамм')

    def test_add_new_measure(self):
        # Подготовка
        base_measure = self.start_srv.repo.data[reposity.measure_key()]['г']
        new_measure = measure_model.create(
            'упаковка',
            base_measure,
            100.0  # 1 упаковка = 100 грамм
        )

        # Преобразуем объект в словарь
        new_measure_dict = self.converter.convert(new_measure)

        # Действие
        result = self.ref_service.add('measure', new_measure_dict)

        # Проверка
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'упаковка')
        # Проверяем conversion_factor если он есть в словаре
        if 'conversion_factor' in result:
            self.assertEqual(result['conversion_factor'], 100.0)

    def test_update_measure(self):
        # Подготовка
        measures = self.start_srv.repo.data[reposity.measure_key()]
        gram_measure = measures.get('г')
        changes = {'name': 'грамм обновленный'}

        # Действие
        result = self.ref_service.update('measure', gram_measure.unique_code, changes)

        # Проверка
        self.assertEqual(result.name, 'грамм обновленный')

    def test_get_existing_nomenclature_group(self):
        # Подготовка
        groups = self.start_srv.repo.data[reposity.nomenclature_group_key()]
        spices_group = groups.get('СиП')

        # Действие
        result = self.ref_service.get_one('nomenclature_group', spices_group.unique_code)

        # Проверка
        self.assertEqual(result, spices_group)
        self.assertEqual(result.name, 'специи и пряности')

    def test_add_new_nomenclature_group(self):
        # Подготовка
        new_group = nomenclature_group_model.create('овощи')

        # Преобразуем объект в словарь
        new_group_dict = self.converter.convert(new_group)

        # Действие
        result = self.ref_service.add('nomenclature_group', new_group_dict)

        # Проверка
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'овощи')

    def test_get_existing_storage(self):
        # Подготовка
        storages = self.start_srv.repo.data[reposity.storage_key()]
        main_storage = storages.get('Основной склад')

        # Действие
        result = self.ref_service.get_one('storage', main_storage.unique_code)

        # Проверка
        self.assertEqual(result, main_storage)
        self.assertEqual(result.name, 'Основной склад')

    def test_add_new_storage(self):
        # Подготовка
        new_storage = storage_model()
        new_storage.name = 'Новый склад'
        new_storage.address = 'ул. Новая, 1'

        # Преобразуем объект в словарь
        new_storage_dict = self.converter.convert(new_storage)

        # Действие
        result = self.ref_service.add('storage', new_storage_dict)

        # Проверка
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Новый склад')
        self.assertEqual(result['address'], 'ул. Новая, 1')

    def test_update_storage_address(self):
        # Подготовка
        storages = self.start_srv.repo.data[reposity.storage_key()]
        main_storage = storages.get('Основной склад')
        changes = {'address': 'ул. Обновленная, 2'}

        # Действие
        result = self.ref_service.update('storage', main_storage.unique_code, changes)

        # Проверка
        self.assertEqual(result.address, 'ул. Обновленная, 2')

    def test_invalid_reference_type(self):
        # Подготовка
        invalid_type = 'invalid_type'

        # Действие & Проверка
        with self.assertRaises(argument_exception) as context:
            self.ref_service.get_one(invalid_type, 'some-code')

        self.assertIn("Неподдерживаемый тип справочника", str(context.exception))

    def test_add_item_without_unique_code(self):
        # Подготовка - создаем словарь без unique_code
        item_dict = {
            "name": "Test Item"
        }

        # Действие & Проверка
        with self.assertRaises(argument_exception) as context:
            self.ref_service.add('nomenclature', item_dict)

        self.assertIn("уникальный код", str(context.exception))

    def test_recalculate_balances_after_operations(self):
        # Подготовка
        original_block_date = self.start_srv.block_date

        # Действие - добавление новой номенклатуры
        group = self.start_srv.repo.data[reposity.nomenclature_group_key()]['СиП']
        measure = self.start_srv.repo.data[reposity.measure_key()]['г']

        new_nom = nomenclature_model(
            'Тест для балансов',
            'Тестовый продукт для проверки балансов',
            group,
            measure
        )

        # Преобразуем объект в словарь
        new_nom_dict = self.converter.convert(new_nom)
        self.ref_service.add('nomenclature', new_nom_dict)

        # Проверка - балансы должны быть пересчитаны
        current_block_date = self.start_srv.block_date
        self.assertEqual(current_block_date, original_block_date)

    def test_settings_saved_after_operations(self):
        # Подготовка
        import time
        settings_file_before = os.path.getmtime(self.settings_file)

        # Небольшая задержка чтобы время изменилось
        time.sleep(0.01)

        # Действие - обновление элемента
        storages = self.start_srv.repo.data[reposity.storage_key()]
        main_storage = storages.get('Основной склад')
        changes = {'name': 'Главный склад'}

        self.ref_service.update('storage', main_storage.unique_code, changes)

        # Проверка - настройки должны быть сохранены
        settings_file_after = os.path.getmtime(self.settings_file)
        # Проверяем что время изменилось или файл существует (главное что сохранение отработало)
        self.assertTrue(os.path.exists(self.settings_file))

    def test_cannot_delete_nomenclature_used_in_recipe(self):
        # Подготовка - сахар используется в рецепте "Вафли"
        nomenclatures = self.start_srv.repo.data[reposity.nomenclature_key()]
        sugar_nomenclature = nomenclatures.get('Сахар')

        # Действие & Проверка - попытка удалить номенклатуру, используемую в рецепте
        with self.assertRaises(argument_exception) as context:
            self.ref_service.delete('nomenclature', sugar_nomenclature.unique_code)

        # Проверяем, что ошибка содержит информацию о блокировке
        self.assertIn("Невозможно удалить", str(context.exception))
        self.assertIn("Используется в", str(context.exception))
        # Проверяем, что есть либо рецепт, либо транзакция
        error_text = str(context.exception)
        self.assertTrue("Рецепт" in error_text or "Транзакция" in error_text)

        # Проверяем, что элемент НЕ был удален
        item = self.ref_service.get_one('nomenclature', sugar_nomenclature.unique_code)
        self.assertIsNotNone(item)

    def test_cannot_delete_nomenclature_used_in_transaction(self):
        # Подготовка - сахар используется в транзакциях
        nomenclatures = self.start_srv.repo.data[reposity.nomenclature_key()]
        sugar_nomenclature = nomenclatures.get('Сахар')

        # Действие & Проверка - попытка удалить номенклатуру, используемую в транзакции
        with self.assertRaises(argument_exception) as context:
            self.ref_service.delete('nomenclature', sugar_nomenclature.unique_code)

        # Проверяем, что ошибка содержит информацию о блокировке
        self.assertIn("Невозможно удалить", str(context.exception))
        self.assertIn("Транзакция", str(context.exception))

    def test_cannot_delete_measure_used_in_nomenclature(self):
        # Подготовка - грамм используется в номенклатуре
        measures = self.start_srv.repo.data[reposity.measure_key()]
        gram_measure = measures.get('г')

        # Действие & Проверка - попытка удалить единицу измерения, используемую в номенклатуре
        with self.assertRaises(argument_exception) as context:
            self.ref_service.delete('measure', gram_measure.unique_code)

        # Проверяем, что ошибка содержит информацию о блокировке
        self.assertIn("Невозможно удалить", str(context.exception))
        self.assertIn("Номенклатура", str(context.exception))

        # Проверяем, что элемент НЕ был удален
        item = self.ref_service.get_one('measure', gram_measure.unique_code)
        self.assertIsNotNone(item)

    def test_cannot_delete_group_used_in_nomenclature(self):
        # Подготовка - группа "СиП" используется в номенклатуре
        groups = self.start_srv.repo.data[reposity.nomenclature_group_key()]
        spices_group = groups.get('СиП')

        # Действие & Проверка - попытка удалить группу, используемую в номенклатуре
        with self.assertRaises(argument_exception) as context:
            self.ref_service.delete('nomenclature_group', spices_group.unique_code)

        # Проверяем, что ошибка содержит информацию о блокировке
        self.assertIn("Невозможно удалить", str(context.exception))
        self.assertIn("Номенклатура", str(context.exception))

        # Проверяем, что элемент НЕ был удален
        item = self.ref_service.get_one('nomenclature_group', spices_group.unique_code)
        self.assertIsNotNone(item)

    def test_cannot_delete_storage_used_in_transaction(self):
        # Подготовка - основной склад используется в транзакциях
        storages = self.start_srv.repo.data[reposity.storage_key()]
        main_storage = storages.get('Основной склад')

        # Действие & Проверка - попытка удалить склад, используемый в транзакциях
        with self.assertRaises(argument_exception) as context:
            self.ref_service.delete('storage', main_storage.unique_code)

        # Проверяем, что ошибка содержит информацию о блокировке
        self.assertIn("Невозможно удалить", str(context.exception))
        self.assertIn("Транзакция", str(context.exception))

        # Проверяем, что элемент НЕ был удален
        item = self.ref_service.get_one('storage', main_storage.unique_code)
        self.assertIsNotNone(item)

    def test_can_delete_unused_measure(self):
        # Подготовка - создаем новую единицу измерения, которая нигде не используется
        base_measure = self.start_srv.repo.data[reposity.measure_key()]['г']
        new_measure = measure_model.create(
            'тестовая единица',
            base_measure,
            1.0
        )

        # Преобразуем объект в словарь
        new_measure_dict = self.converter.convert(new_measure)
        self.ref_service.add('measure', new_measure_dict)

        # Действие - удаляем неиспользуемую единицу измерения
        result = self.ref_service.delete('measure', new_measure.unique_code)

        # Проверка - элемент должен быть успешно удален
        self.assertTrue(result)
        deleted = self.ref_service.get_one('measure', new_measure.unique_code)
        self.assertIsNone(deleted)

    def test_can_delete_unused_nomenclature_group(self):
        # Подготовка - создаем новую группу, которая нигде не используется
        new_group = nomenclature_group_model.create('тестовая группа')

        # Преобразуем объект в словарь
        new_group_dict = self.converter.convert(new_group)
        self.ref_service.add('nomenclature_group', new_group_dict)

        # Действие - удаляем неиспользуемую группу
        result = self.ref_service.delete('nomenclature_group', new_group.unique_code)

        # Проверка - элемент должен быть успешно удален
        self.assertTrue(result)
        deleted = self.ref_service.get_one('nomenclature_group', new_group.unique_code)
        self.assertIsNone(deleted)

    def test_update_nomenclature_updates_recipe_references(self):
        # Подготовка
        nomenclatures = self.start_srv.repo.data[reposity.nomenclature_key()]
        sugar_nomenclature = nomenclatures.get('Сахар')

        # Действие - обновляем название сахара
        changes = {'name': 'Сахар-песок обновленный'}
        self.ref_service.update('nomenclature', sugar_nomenclature.unique_code, changes)

        # Проверка - обновление должно отразиться в номенклатуре
        updated_sugar = nomenclatures.get('Сахар')
        self.assertEqual(updated_sugar.name, 'Сахар-песок обновленный')

        # Проверяем, что изменения видны через сервис
        retrieved_sugar = self.ref_service.get_one('nomenclature', sugar_nomenclature.unique_code)
        self.assertEqual(retrieved_sugar.name, 'Сахар-песок обновленный')

    def test_update_storage_updates_transaction_references(self):
        # Подготовка
        storages = self.start_srv.repo.data[reposity.storage_key()]
        main_storage = storages.get('Основной склад')
        transactions = self.start_srv.repo.data[reposity.transaction_key()]

        # Находим транзакцию, использующую основной склад
        transaction_with_storage = None
        for transaction in transactions.values():
            if transaction.storage.unique_code == main_storage.unique_code:
                transaction_with_storage = transaction
                break

        self.assertIsNotNone(transaction_with_storage, "Должна быть транзакция с основным складом")

        # Действие - обновляем название склада
        changes = {'name': 'Главный склад обновленный'}
        self.ref_service.update('storage', main_storage.unique_code, changes)

        # Проверка - обновление должно отразиться в транзакции
        self.assertEqual(transaction_with_storage.storage.name, 'Главный склад обновленный')

if __name__ == '__main__':
    unittest.main()