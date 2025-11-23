import unittest
from datetime import datetime, timedelta
from time import perf_counter

from Src.start_service import start_service
from Src.Models.storage_model import storage_model
from Src.Models.transaction_model import transaction_model
from Src.reposity import reposity
from Src.Core.validator import validator

"""
    Нагрузочный тест для расчета ОСВ с учетом даты блокировки.
    Проверяется:
    - работа сервиса при большом количестве транзакций (1000+)
    - время вычисления ОСВ при разных вариантах block_date
    - формирование Markdown-отчета с результатами замеров
"""

class TestOsvBlockDatePerformance(unittest.TestCase):

    def setUp(self):
        """
        Подготовка данных для нагрузочного теста:
        - инициализация start_service
        - создание базовых справочников и 5 тестовых транзакций
        - добавление 1000 дополнительных транзакций
        """
        self.service = start_service()
        self.service.start()

        # Доступ к репозиторию
        self.repo = self.service._start_service__repo

        self.transactions = self.repo.data[reposity.transaction_key()]
        self.storages = self.repo.data[reposity.storage_key()]
        self.nomenclatures = self.repo.data[reposity.nomenclature_key()]
        self.measures = self.repo.data[reposity.measure_key()]

        # Базовые сущности для генерации транзакций
        self.storage_main = self.storages.get("Основной склад")
        self.sugar = self.nomenclatures.get("Сахар")
        self.gram = self.measures.get("г")

        # Проверяем, что данные действительно есть
        self.assertIsNotNone(self.storage_main)
        self.assertIsNotNone(self.sugar)
        self.assertIsNotNone(self.gram)

        # Создаем не менее 1000 дополнительных транзакций
        self._create_test_transactions(count=1000)

        # Период для ОСВ
        self.start_date = datetime(2025, 10, 1, 0, 0, 0)
        self.end_date = datetime(2025, 10, 31, 23, 59, 59)

        self.storage_for_osv = storage_model()
        self.storage_for_osv.name = "Основной склад"

    def _create_test_transactions(self, count: int = 1000):
        """
        Создает указанное количество дополнительных транзакций
        по номенклатуре 'Сахар' на 'Основной склад'.
        """
        base_date = datetime(2025, 10, 1, 0, 0, 0)

        for i in range(count):
            t = transaction_model()
            t.name = f"Тестовая транзакция {i + 1}"
            # Распределяем транзакции по времени в пределах месяца
            t.date = (base_date + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S")
            t.nomenclature = self.sugar
            t.storage = self.storage_main
            t.measure = self.gram
            # Чередуем приход и расход
            t.quantity = 10.0 if i % 2 == 0 else -5.0

            # Добавляем в репозиторий по уникальному коду
            self.transactions[t.unique_code] = t

    def test_osv_performance_with_different_block_dates(self):
        """
        Нагрузочный тест:
        - измеряет время расчета ОСВ при разных датах блокировки
        - сохраняет результаты в Markdown-файл osv_block_date_performance.md
        """
        scenarios = [
            ("Блокировка в начале периода", datetime(2020, 10, 1, 0, 0, 0)),
            ("Блокировка в середине периода", datetime(2025, 10, 15, 0, 0, 0)),
            ("Блокировка в конце периода", datetime(2025, 10, 30, 0, 0, 0)),
        ]

        results = []

        for name, block_date in scenarios:
            # Подготовка
            self.service.block_date = block_date

            # Действие
            start_time = perf_counter()
            osv_build = self.service.create_osv(
                self.start_date,
                self.end_date,
                self.storage_for_osv
            )
            duration = perf_counter() - start_time

            # Базовые проверки корректности результата
            self.assertIsNotNone(osv_build)
            self.assertTrue(len(osv_build.rows) > 0)

            results.append(
                {
                    "name": name,
                    "block_date": block_date,
                    "duration": duration,
                    "rows_count": len(osv_build.rows),
                }
            )

        # Формируем Markdown-файл
        lines = []
        lines.append("# Результаты нагрузочного теста расчета ОСВ\n\n")
        lines.append("| Сценарий | Дата блокировки | Время расчета, сек | Количество строк ОСВ |\n")
        lines.append("|----------|-----------------|--------------------|-----------------------|\n")

        for item in results:
            date_str = item["block_date"].strftime("%Y-%m-%d %H:%M:%S")
            lines.append(
                f"| {item['name']} | {date_str} | {item['duration']:.6f} | {item['rows_count']} |\n"
            )

        # Сохраняем отчет в Markdown-файл
        output_file = "osv_block_date_performance.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(lines)

if __name__ == '__main__':
    unittest.main()