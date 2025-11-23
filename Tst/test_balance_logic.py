import unittest
from datetime import datetime

from Src.start_service import start_service
from Src.Models.storage_model import storage_model

"""
    Unit-тесты для проверки расчетов ОСВ с учетом даты блокировки.
    Проверяется:
    - создание ОСВ для склада
    - корректность формирования строк ОСВ
    - неизменность результата при изменении даты блокировки (кэш)
"""

class TestOsvBlockDate(unittest.TestCase):

    def setUp(self):
        """
        Подготовка тестовых данных:
        - инициализация start_service
        - загрузка справочников и транзакций
        - подготовка объекта склада для ОСВ
        """
        self.service = start_service()
        self.service.start()

        self.storage = storage_model()
        self.storage.name = "Основной склад"

    def _osv_to_dict(self, osv_build):
        """
        Вспомогательный метод:
        Преобразует результат ОСВ в словарь по номенклатуре.

        Формат:
        {
            "Сахар": {
                "start": ...,
                "income": ...,
                "outcome": ...,
                "end": ...
            },
            ...
        }
        """
        rows = getattr(osv_build, "rows", [])
        result = {}

        for row in rows:
            key = row.nomenclature.name
            result[key] = {
                "start": row.start_balance,
                "income": row.income,
                "outcome": row.outcome,
                "end": row.end_balance,
            }

        return result

    def test_osv_result_not_changed_when_block_date_changes(self):
        """
        При изменении даты блокировки (и, соответственно, кэша)
        конечный результат ОСВ по складу не должен меняться.
        """

        # Подготовка
        # Берем период, который начинается ПОСЛЕ дат транзакций и позволяет использовать кэш
        start_date = datetime(2025, 10, 27, 0, 0, 0)
        end_date = datetime(2025, 10, 30, 23, 59, 59)

        first_block_date = datetime(2025, 10, 24, 0, 0, 0)
        second_block_date = datetime(2025, 10, 26, 0, 0, 0)

        # Действие — первый расчет с первой датой блокировки
        self.service.block_date = first_block_date
        osv_first = self.service.create_osv(start_date, end_date, self.storage)
        osv_first_data = self._osv_to_dict(osv_first)

        # Базовые проверки
        self.assertIsNotNone(osv_first)
        self.assertTrue(len(osv_first.rows) > 0)

        # Действие — второй расчет с другой датой блокировки
        self.service.block_date = second_block_date
        osv_second = self.service.create_osv(start_date, end_date, self.storage)
        osv_second_data = self._osv_to_dict(osv_second)

        # Базовые проверки
        self.assertIsNotNone(osv_second)
        self.assertTrue(len(osv_second.rows) > 0)

        # Проверка — при изменении block_date результат не должен меняться
        self.assertEqual(osv_first_data, osv_second_data)


if __name__ == '__main__':
    unittest.main()