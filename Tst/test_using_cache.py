import unittest
from datetime import datetime

from Src.start_service import start_service
from Src.reposity import reposity
from Src.Models.storage_model import storage_model
from Src.Models.osv_unit_model import osv_unit_model

"""
    Unit-тесты для проверки использования кэша остатков при формировании ОСВ.
    Проверяется:
    - что start_balance берётся из кэша (с учётом block_date)
    - что конечный end_balance не зависит от block_date
"""

class TestBalanceCacheUsageInOSV(unittest.TestCase):

    def setUp(self):
        """Подготовка тестового сервиса, данных и склада."""
        self.service = start_service()
        self.service.start()

        self.repo = self.service.repo
        self.storages = self.repo.data[reposity.storage_key()]
        self.nomenclatures = self.repo.data[reposity.nomenclature_key()]

        # Основной склад для теста
        self.main_storage: storage_model = self.storages.get("Основной склад")

    def _get_osv_row(self, osv_build, nomenclature_name: str):
        """
        Вспомогательный метод: найти строку ОСВ по названию номенклатуры.
        """
        for row in osv_build.rows:
            if row.nomenclature.name == nomenclature_name:
                return row
        return None

    def test_osv_uses_cache_for_start_balance(self):
        """
        Проверяем, что при установленной block_date:
        - start_balance для "Сахар" равен остатку из кэша
        - обороты считаются только после даты блокировки
        - конечный остаток совпадает с прямым расчётом по транзакциям
        """
        # Подготовка
        block_date = datetime(2025, 10, 27, 0, 0, 0)
        self.service.block_date = block_date  # пересчёт кэша

        # Период отчёта — начинается с даты блокировки
        start_date = datetime(2025, 10, 27, 0, 0, 0)
        end_date = datetime(2025, 10, 30, 23, 59, 59)

        # Действие — строим ОСВ
        osv_build = self.service.create_osv(start_date, end_date, self.main_storage)

        # Проверка — строка по Сахару
        sugar_row = self._get_osv_row(osv_build, "Сахар")
        self.assertIsNotNone(sugar_row)

        self.assertAlmostEqual(sugar_row.start_balance, 1000.0)
        self.assertAlmostEqual(sugar_row.income, 0.0)
        self.assertAlmostEqual(sugar_row.outcome, 200.0)
        self.assertAlmostEqual(sugar_row.end_balance, 800.0)

    def test_osv_end_balance_not_changed_with_different_block_dates(self):
        """
        Проверяем, что при изменении block_date:
        - конечный остаток (end_balance) не меняется,
          меняется только распределение между start_balance и оборотами.
        """
        # Период отчёта для ОСВ
        start_date = datetime(2025, 10, 24, 0, 0, 0)
        end_date = datetime(2025, 10, 30, 23, 59, 59)

        # 1. Без кэша (block_date = None)
        self.service.block_date = None
        osv_no_cache = self.service.create_osv(start_date, end_date, self.main_storage)
        sugar_row_no_cache = self._get_osv_row(osv_no_cache, "Сахар")
        self.assertIsNotNone(sugar_row_no_cache)

        # 2. С кэшем на 27.10
        self.service.block_date = datetime(2025, 10, 27, 0, 0, 0)
        osv_with_cache = self.service.create_osv(start_date, end_date, self.main_storage)
        sugar_row_with_cache = self._get_osv_row(osv_with_cache, "Сахар")
        self.assertIsNotNone(sugar_row_with_cache)

        # Проверяем, что конечный остаток одинаковый
        self.assertAlmostEqual(
            sugar_row_no_cache.end_balance,
            sugar_row_with_cache.end_balance
        )

        # Но распределение по start_balance / оборотам отличается
        self.assertNotEqual(
            sugar_row_no_cache.start_balance,
            sugar_row_with_cache.start_balance
        )

if __name__ == '__main__':
    unittest.main()