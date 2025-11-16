from datetime import datetime
from typing import List
from Src.Core.abstract_model import abstract_model
from Src.Dto.filter_dto import filter_dto
from Src.Logics.prototype_report import prototype_report
from Src.Models.nomenclature_model import nomenclature_model
from Src.Core.validator import operation_exception, validator
from Src.Models.osv_model import osv_model
from Src.Models.osv_unit_model import osv_unit_model
from Src.Models.storage_model import storage_model
from Src.Models.transaction_model import transaction_model

class osv_builder(abstract_model):

    __start_date: datetime
    __end_date: datetime
    __storage: storage_model
    __rows: List[osv_unit_model]

    def __init__(self, osv: osv_model):
        self.__start_date = osv.start_date
        self.__end_date = osv.end_date
        self.__storage = osv.storage
        self.__rows: List[osv_unit_model] = []

    @property
    def start_date(self) -> datetime:
        """Возвращает дату начала отчетного периода"""
        return self.__start_date

    @start_date.setter
    def start_date(self, start_date: datetime):
        """
        Устанавливает дату начала периода с валидацией типа данных.
        
        Аргументы:
            start_date (datetime): Дата начала отчетного периода
            
        Ошибки:
            Validation error: Если переданный параметр не является datetime
        """
        validator.validate(start_date, datetime)
        self.__start_date = start_date

    @property
    def end_date(self) -> datetime:
        """Возвращает дату окончания отчетного периода"""
        return self.__end_date
        
    @end_date.setter
    def end_date(self, end_date: datetime):
        """
        Устанавливает дату окончания периода с валидацией типа данных.
        
        Аргументы:
            end_date (datetime): Дата окончания отчетного периода
            
        Ошибки:
            Validation error: Если переданный параметр не является datetime
        """
        validator.validate(end_date, datetime)
        self.__end_date = end_date

    @property
    def storage(self) -> storage_model:
        """Возвращает объект склада, для которого формируется ведомость"""
        return self.__storage
        
    @storage.setter
    def storage(self, storage: storage_model):
        """
        Устанавливает склад для ведомости с валидацией типа данных.
        
        Аргументы:
            storage (storage_model): Объект склада
            
        Ошибки:
            Validation error: Если переданный параметр не является storage_model
        """
        validator.validate(storage, storage_model)
        self.__storage = storage

    @property
    def rows(self) -> List[osv_unit_model]:
        """Возвращает список строк оборотно-сальдовой ведомости"""
        return self.__rows
        
    @rows.setter
    def rows(self, rows: List[osv_unit_model]):
        """
        Устанавливает список строк ведомости с валидацией типа данных.
        
        Аргументы:
            rows (List[osv_unit_model]): Список строк отчета ОСВ
            
        Ошибки:
            Validation error: Если параметр не является списком или элементы не osv_unit_model
        """
        validator.validate(rows, list)
        for row in rows:
            validator.validate(row, osv_unit_model)
        self.__rows = rows

    def find_row(self, nomenclature):
        """
        Находит строку ведомости по номенклатуре.
        
        Аргументы:
            nomenclature: Номенклатура для поиска
            
        Возвращает:
            osv_unit_model: Найденная строка ведомости
            
        Ошибки:
            operation_exception: Если строка с указанной номенклатурой не найдена
        """
        # Итерируем по всем строкам ведомости
        for item in self.__rows:
            if item.nomenclature == nomenclature:
                return item
        # Если не найдено - генерируем исключение
        raise operation_exception("Элемент ОСВ не найден!")

    def generate_rows(self, transactions: list[transaction_model], nomenclatures: list[nomenclature_model]):
        """
        Генерирует строки ведомости на основе транзакций и справочника номенклатур.
        
        Алгоритм:
        1. Фильтрация транзакций по складу
        2. Разделение транзакций на периоды (до начала и внутри периода отчета)
        3. Для каждой номенклатуры рассчитываются:
        - Остаток на начало периода
        - Обороты за период (приход и расход)
        - Остаток на конец периода
        
        Аргументы:
            transactions: Список всех транзакций
            nomenclatures: Справочник номенклатур в формате словаря
        """
        
        # Создаем прототипы для работы с фильтрами
        # Прототипы позволяют применять фильтры к коллекциям объектов
        transactions_prototype = prototype_report(transactions)
        nomenclatures_prototype = prototype_report(list(nomenclatures.values()))
        
        # 1. Фильтрация транзакций по складу - оставляем только транзакции нужного склада
        filter_storage = filter_dto().create(
            {
                "filter_name": "storage.name",  # Поле для фильтрации
                "value": self.__storage.name,   # Название склада
                "type": "EQUALS"                # Точное совпадение
            }
        )
        transactions_by_storage = transactions_prototype.filter(
            transactions_prototype,
            filter_storage
        )

        # 2. Фильтр транзакций до начала периода - для расчета разницы между приходомами и расходами счета
        filter_before_period = filter_dto().create(
            {
                "filter_name": "date",
                "value": (datetime.min, self.__start_date),  # Диапазон от минимальной даты до начала периода
                "type": "IN_RANGE"
            }
        )
        transactions_before_period = transactions_by_storage.filter(
            transactions_by_storage,
            filter_before_period
        )

        # 3. Фильтр транзакций внутри отчетного периода. Рассматриваются операции за период [start_date; end_date]
        filter_in_period = filter_dto().create(
            {
                "filter_name": "date",
                "value": (self.__start_date, self.__end_date),  # Отчетный период
                "type": "IN_RANGE"
            }
        )
        transactions_in_period = transactions_by_storage.filter(
            transactions_by_storage,
            filter_in_period
        )

        # 4. Инициализация строк ОСВ - для каждой номенклатуры создаем строку
        self.__rows = []
        for nomenclature in nomenclatures.values():
            # Фильтруем транзакции по конкретной номенклатуре до периода
            filter_nomenclature = filter_dto().create(
                {
                    "filter_name": "nomenclature",
                    "value": nomenclature,  # Текущая номенклатура
                    "type": "EQUALS"
                }
            )
            nomenclature_before = transactions_before_period.filter(
                transactions_before_period,
                filter_nomenclature
            )
            
            # Фильтруем транзакции по номенклатуре внутри периода
            nomenclature_in_period = transactions_in_period.filter(
                transactions_in_period,
                filter_nomenclature
            )
            
            # Создаем строку ОСВ для этой номенклатуры
            osv_row = osv_unit_model.create_default(
                nomenclature,
                nomenclature.measure.base_measure or nomenclature.measure  # Базовая единица измерения
            )
            
            # Рассчитываем начальный остаток на основе транзакций до периода
            start_balance = 0.0
            for transaction in nomenclature_before.data:
                quantity = transaction.quantity
                # Конвертируем в базовые единицы измерения если нужно
                if transaction.measure.base_measure and transaction.measure.base_measure == osv_row.measure:
                    quantity *= transaction.measure.conversion_factor
                start_balance += quantity  # Суммируем все операции
            
            # Рассчитываем обороты за период
            income = 0.0   # Приход (положительные количества)
            outcome = 0.0  # Расход (отрицательные количества, берем по модулю)
            for transaction in nomenclature_in_period.data:
                quantity = transaction.quantity
                # Конвертируем в базовые единицы измерения
                if transaction.measure.base_measure and transaction.measure.base_measure == osv_row.measure:
                    quantity *= transaction.measure.conversion_factor
                
                # Разделяем на приход и расход
                if quantity > 0:
                    income += quantity
                else:
                    outcome += abs(quantity)  # Берем модуль для расхода
            
            # Устанавливаем рассчитанные значения в строку ОСВ
            osv_row.start_balance = start_balance                    # Стартовый счет
            osv_row.income = income                                  # Приход за период
            osv_row.outcome = outcome                                # Расход за период
            osv_row.end_balance = start_balance + income - outcome   # Конечный счет
            
            self.__rows.append(osv_row)