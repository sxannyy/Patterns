import unittest
from datetime import datetime

from Src.Core.match_type import match_type
from Src.Core.validator import operation_exception, argument_exception
from Src.Logics.prototype_report import prototype_report
from Src.reposity import reposity
from Src.start_service import start_service
from Src.Dto.filter_dto import filter_dto
from Src.Dto.filter_sorting_dto import filter_sorting_dto


"""
    Тестирование прототипа и DTO-фильтров
"""

class TestPrototype(unittest.TestCase):
    def setUp(self):
        # Инициализируем сервис и загружаем данные
        self.svc = start_service()
        self.svc.start()
        self.repo = self.svc.repo

        transactions = list(self.repo.data[reposity.transaction_key()].values())
        self.start_prototype = prototype_report(transactions)

    def test_prototype_nomenclature_filter(self):
        """Тестирование фильтрации по номенклатуре через специализированный метод"""
        # Подготовка
        transactions = list(self.repo.data[reposity.transaction_key()].values())
        start_prototype = prototype_report(transactions)

        nomenclatures = self.repo.data[reposity.nomenclature_key()]
        self.assertGreater(len(nomenclatures), 0, 
                          "В репозитории нет номенклатур. Проверьте загрузку тестовых данных.")

        first_nomenclature_key = list(nomenclatures.keys())[0]
        first_nomenclature = nomenclatures[first_nomenclature_key]

        # Действие
        next_prototype_nomenclature = prototype_report.filter_by_nomenclature(
            start_prototype,
            first_nomenclature
        )

        # Проверка
        self.assertGreater(len(next_prototype_nomenclature.data), 0)
        self.assertGreater(len(start_prototype.data), 0)
        self.assertGreaterEqual(len(start_prototype.data), len(next_prototype_nomenclature.data))

    def test_prototype_storage_filter(self):
        """Тестирование фильтрации по складу через специализированный метод"""
        # Подготовка
        transactions = list(self.repo.data[reposity.transaction_key()].values())
        start_prototype = prototype_report(transactions)

        storages = self.repo.data[reposity.storage_key()]
        self.assertGreater(len(storages), 0, 
                          "В репозитории нет складов. Проверьте загрузку тестовых данных.")

        first_storage_key = list(storages.keys())[0]
        first_storage = storages[first_storage_key]

        # Действие
        next_prototype_storage = prototype_report.filter_by_storage(
            start_prototype,
            first_storage
        )

        # Проверка
        self.assertGreater(len(next_prototype_storage.data), 0)
        self.assertGreater(len(start_prototype.data), 0)
        self.assertGreaterEqual(len(start_prototype.data), len(next_prototype_storage.data))

    def test_prototype_date_filter(self):
        """Тестирование фильтрации по диапазону дат через специализированный метод"""
        # Подготовка
        transactions = list(self.repo.data[reposity.transaction_key()].values())
        start_prototype = prototype_report(transactions)

        self.assertGreater(len(transactions), 0, 
                          "Нет транзакций для тестирования. Проверьте загрузку тестовых данных.")

        dates = [t.date for t in transactions if hasattr(t, 'date') and t.date is not None]
        self.assertGreater(len(dates), 0, 
                          "Нет транзакций с датами для тестирования.")

        min_date = min(dates)
        max_date = max(dates)

        # Действие
        next_prototype_date = prototype_report.filter_by_date(
            start_prototype,
            min_date,
            max_date
        )

        # Проверка
        self.assertGreater(len(next_prototype_date.data), 0)
        self.assertGreater(len(start_prototype.data), 0)
        self.assertGreaterEqual(len(start_prototype.data), len(next_prototype_date.data))

        for transaction in next_prototype_date.data:
            self.assertTrue(min_date <= transaction.date <= max_date)

    def test_prototype_universal_filter(self):
        """Сравнение специализированной и универсальной фильтрации по номенклатуре"""
        # Подготовка
        transactions = list(self.repo.data[reposity.transaction_key()].values())
        start_prototype = prototype_report(transactions)

        nomenclatures = self.repo.data[reposity.nomenclature_key()]
        self.assertGreater(len(nomenclatures), 0, 
                          "В репозитории нет номенклатур для тестирования.")

        first_nomenclature = list(nomenclatures.values())[0]

        # Действие - фильтрация через специализированный метод
        proto_by_nom = prototype_report.filter_by_nomenclature(start_prototype, first_nomenclature)

        # Действие - фильтрация через универсальный DTO
        dto = filter_dto()
        dto.field_name = "nomenclature.name"
        dto.filter_value = first_nomenclature.name
        dto.operation = match_type.EQUALS

        proto_by_dto = prototype_report.filter(start_prototype, dto)

        # Проверка
        self.assertGreater(len(proto_by_dto.data), 0)
        self.assertEqual(len(proto_by_dto.data), len(proto_by_nom.data))
        for item in proto_by_dto.data:
            self.assertEqual(item.nomenclature.name, first_nomenclature.name)

    def test_prototype_filter_dto_equals(self):
        """Тестирование фильтрации через DTO с операцией EQUALS"""
        # Подготовка
        self.assertGreater(len(self.start_prototype.data), 0, 
                          "Нет данных для тестирования фильтрации EQUALS.")

        test_transaction = self.start_prototype.data[0]

        dto = filter_dto()
        dto.field_name = "nomenclature.name"
        dto.filter_value = test_transaction.nomenclature.name
        dto.operation = match_type.EQUALS

        # Действие
        filtered_prototype = prototype_report.filter(self.start_prototype, dto)

        # Проверка
        self.assertGreater(len(filtered_prototype.data), 0)
        for item in filtered_prototype.data:
            self.assertEqual(item.nomenclature.name, test_transaction.nomenclature.name)

    def test_prototype_filter_dto_like(self):
        """Тестирование фильтрации через DTO с операцией LIKE"""
        # Подготовка
        self.assertGreater(len(self.start_prototype.data), 0, 
                          "Нет данных для тестирования фильтрации LIKE.")

        test_transaction = self.start_prototype.data[0]
        name_part = test_transaction.nomenclature.name[:3]  # первые 3 символа

        dto = filter_dto()
        dto.field_name = "nomenclature.name"
        dto.filter_value = name_part
        dto.operation = match_type.LIKE

        # Действие
        filtered_prototype = prototype_report.filter(self.start_prototype, dto)

        # Проверка
        self.assertGreater(len(filtered_prototype.data), 0)
        for item in filtered_prototype.data:
            self.assertIn(name_part.lower(), item.nomenclature.name.lower())

    def test_prototype_filter_dto_in_range(self):
        """Тестирование фильтрации через DTO с операцией IN_RANGE"""
        # Подготовка
        self.assertGreater(len(self.start_prototype.data), 0, 
                          "Нет данных для тестирования фильтрации IN_RANGE.")

        dates = [t.date for t in self.start_prototype.data
                 if hasattr(t, 'date') and t.date is not None]
        self.assertGreater(len(dates), 0, 
                          "Нет транзакций с датами для тестирования IN_RANGE.")

        min_date = min(dates)
        max_date = max(dates)
        mid_date = min_date + (max_date - min_date) / 2

        dto = filter_dto()
        dto.field_name = "date"
        dto.filter_value = [min_date, mid_date]
        dto.operation = match_type.IN_RANGE

        # Действие
        filtered_prototype = prototype_report.filter(self.start_prototype, dto)

        # Проверка
        self.assertGreater(len(filtered_prototype.data), 0)
        for item in filtered_prototype.data:
            self.assertTrue(min_date <= item.date <= mid_date)

    def test_prototype_filter_empty_data(self):
        """Тестирование фильтрации пустых данных"""
        # Подготовка
        empty_prototype = prototype_report([])

        # Действие и проверка - фильтрация по номенклатуре
        nomenclatures = self.repo.data[reposity.nomenclature_key()]
        if len(nomenclatures) > 0:
            first_nomenclature = list(nomenclatures.values())[0]
            filtered = prototype_report.filter_by_nomenclature(empty_prototype, first_nomenclature)
            self.assertEqual(len(filtered.data), 0)

        # Действие и проверка - фильтрация через DTO
        dto = filter_dto()
        dto.field_name = "name"
        dto.filter_value = "test"
        dto.operation = match_type.EQUALS
        filtered = prototype_report.filter(empty_prototype, dto)
        self.assertEqual(len(filtered.data), 0)

    def test_prototype_filter_invalid_parameters(self):
        """Тестирование обработки невалидных параметров"""
        # Проверка
        with self.assertRaises(argument_exception):
            prototype_report.filter_by_nomenclature("invalid_source", None)

        with self.assertRaises(argument_exception):
            prototype_report.filter_by_date(self.start_prototype, "invalid_date", datetime.now())

        with self.assertRaises(argument_exception):
            prototype_report.filter_by_storage("invalid_source", None)

    def test_prototype_get_nested_value(self):
        """Тестирование получения вложенных значений"""
        # Подготовка
        self.assertGreater(len(self.start_prototype.data), 0, 
                          "Нет данных для тестирования получения вложенных значений.")

        test_transaction = self.start_prototype.data[0]

        # Действие и проверка - простое поле
        simple_value = prototype_report.get_nested_value(test_transaction, "date")
        self.assertEqual(simple_value, test_transaction.date)

        # Действие и проверка - вложенное поле
        nested_value = prototype_report.get_nested_value(test_transaction, "nomenclature.name")
        self.assertEqual(nested_value, test_transaction.nomenclature.name)

        # Действие и проверка - несуществующее поле
        non_existent = prototype_report.get_nested_value(test_transaction, "non.existent.field")
        self.assertIsNone(non_existent)

    def test_filter_sorting_dto_creation(self):
        """Тестирование создания DTO для фильтрации и сортировки"""
        # Подготовка
        f1 = filter_dto()
        f1.field_name = "nomenclature.name"
        f1.filter_value = "test"
        f1.operation = match_type.EQUALS

        f2 = filter_dto()
        f2.field_name = "storage.name"
        f2.filter_value = "warehouse"
        f2.operation = match_type.LIKE

        # Действие
        sorting_dto = filter_sorting_dto()
        sorting_dto.filters = [f1, f2]
        sorting_dto.sorting = ["date", "nomenclature.name"]

        # Проверка
        self.assertEqual(len(sorting_dto.filters), 2)
        self.assertEqual(len(sorting_dto.sorting), 2)
        self.assertEqual(sorting_dto.filters[0].field_name, "nomenclature.name")
        self.assertEqual(sorting_dto.sorting[0], "date")

    def test_filter_sorting_dto_create_from_dict(self):
        """Тестирование создания DTO из словаря"""
        # Подготовка
        data = {
            "filters": [
                {
                    "filter_name": "nomenclature.name",
                    "value": "test_product",
                    "type": "EQUALS"
                },
                {
                    "filter_name": "date",
                    "value": [datetime(2023, 1, 1), datetime(2023, 12, 31)],
                    "type": "IN_RANGE"
                }
            ],
            "sorting": ["date", "nomenclature.name"]
        }

        # Действие
        sorting_dto = filter_sorting_dto().create(data)

        # Проверка
        self.assertEqual(len(sorting_dto.filters), 2)
        self.assertEqual(len(sorting_dto.sorting), 2)
        self.assertEqual(sorting_dto.filters[0].field_name, "nomenclature.name")
        self.assertEqual(sorting_dto.filters[0].filter_value, "test_product")
        self.assertEqual(sorting_dto.filters[0].operation, match_type.EQUALS)
        self.assertEqual(sorting_dto.filters[1].operation, match_type.IN_RANGE)

    def test_prototype_combined_filters(self):
        """Тестирование комбинированной фильтрации"""
        # Подготовка
        self.assertGreater(len(self.start_prototype.data), 0, 
                          "Нет данных для тестирования комбинированной фильтрации.")

        nomenclatures = self.repo.data[reposity.nomenclature_key()]
        self.assertGreater(len(nomenclatures), 0, 
                          "Нет номенклатур для тестирования комбинированной фильтрации.")

        first_nomenclature = list(nomenclatures.values())[0]

        # Действие - первый фильтр по номенклатуре
        filtered_by_nomenclature = prototype_report.filter_by_nomenclature(
            self.start_prototype,
            first_nomenclature
        )

        # Действие - второй фильтр по дате
        dates = [
            t.date for t in filtered_by_nomenclature.data
            if hasattr(t, 'date') and t.date is not None
        ]
        if len(dates) > 0:
            min_date = min(dates)
            max_date = max(dates)
            mid_date = min_date + (max_date - min_date) / 2

            final_filtered = prototype_report.filter_by_date(
                filtered_by_nomenclature,
                min_date,
                mid_date
            )

            # Проверка
            for item in final_filtered.data:
                self.assertEqual(item.nomenclature, first_nomenclature)
                self.assertTrue(min_date <= item.date <= mid_date)

    def test_prototype_edge_cases(self):
        """Тестирование граничных случаев"""
        # Подготовка и действие - несуществующее поле
        dto = filter_dto()
        dto.field_name = "nonexistent.field"
        dto.filter_value = "test"
        dto.operation = match_type.EQUALS

        filtered = prototype_report.filter(self.start_prototype, dto)
        self.assertEqual(len(filtered.data), 0)

        # Подготовка и действие - пустой LIKE по существующему полю
        dto.field_name = "nomenclature.name"
        dto.filter_value = ""
        dto.operation = match_type.LIKE

        filtered = prototype_report.filter(self.start_prototype, dto)
        self.assertEqual(len(filtered.data), len(self.start_prototype.data))


if __name__ == '__main__':
    unittest.main()