import unittest
from datetime import datetime

from Src.start_service import start_service
from Src.reposity import reposity
from Src.Models.balance_model import balance_model
from Src.Models.storage_model import storage_model
from Src.Models.nomenclature_model import nomenclature_model

"""
    Unit-тесты для проверки формирования кэша остатков.
    Проверяется:
    - корректная генерация кэша при установке block_date
    - корректные значения end_balance по тестовым данным
"""

class TestBalanceCacheGeneration(unittest.TestCase):

    def setUp(self):
        """Подготовка тестового сервиса и данных."""
        self.service = start_service()
        # создаём стандартные справочники и транзакции
        self.service.start()

        self.repo = self.service.repo
        self.storages = self.repo.data[reposity.storage_key()]
        self.nomenclatures = self.repo.data[reposity.nomenclature_key()]

    def test_balance_cache_on_block_date(self):
        """
        Проверяем, что при установке block_date формируется кэш с ожидаемыми остатками.
        """
        # Подготовка
        block_date = datetime(2025, 10, 27, 0, 0, 0)

        main_storage: storage_model = self.storages.get("Основной склад")
        sugar: nomenclature_model = self.nomenclatures.get("Сахар")
        eggs: nomenclature_model = self.nomenclatures.get("Яйца куриные")

        # Действие
        self.service.block_date = block_date

        balance_cache = self.service.balance_cache

        # Проверка типа
        self.assertIsInstance(balance_cache, dict)

        # Формируем ключи кэша
        sugar_key = f"{main_storage.unique_code}:{sugar.unique_code}"
        eggs_key = f"{main_storage.unique_code}:{eggs.unique_code}"

        # Проверка наличия записей
        self.assertIn(sugar_key, balance_cache)
        self.assertIn(eggs_key, balance_cache)

        sugar_balance: balance_model = balance_cache[sugar_key]
        eggs_balance: balance_model = balance_cache[eggs_key]

        # Проверка типов и значений
        self.assertIsInstance(sugar_balance, balance_model)
        self.assertIsInstance(eggs_balance, balance_model)

        self.assertEqual(sugar_balance.end_balance, 1000.0)
        self.assertEqual(eggs_balance.end_balance, 30.0)

        # Проверка даты блокировки внутри balance_model
        self.assertEqual(sugar_balance.block_date, block_date)
        self.assertEqual(eggs_balance.block_date, block_date)

if __name__ == '__main__':
    unittest.main()