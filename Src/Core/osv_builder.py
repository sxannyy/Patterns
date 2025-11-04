from datetime import datetime
from typing import List
from Src.Core.abstract_model import abstract_model
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
        
        Аргументы:
            transactions (list[transaction_model]): Список всех транзакций
            nomenclatures (list[nomenclature_model]): Справочник номенклатур
        """
        # Инициализация строк ОСВ: создаем по одной строке для каждой номенклатуры с начальными значениями
        self.__rows = [
            osv_unit_model.create_default(nomenclature, nomenclature.measure.base_measure or nomenclature.measure)
            for nomenclature in dict(nomenclatures).values()
        ]

        # Обработка транзакций до начала периода для определения начальных остатков
        for transaction in transactions:
            # Проверка, относится ли транзакция к правильному складу и к периоду до start_date
            is_correct_storage = transaction.storage.unique_code == self.__storage.unique_code
            is_before_start_date = transaction.date < self.__start_date
            
            if not (is_correct_storage and is_before_start_date):
                continue
                
            try:
                # Находим строку по номенклатуре транзакции
                item = self.find_row(transaction.nomenclature)
                quantity = transaction.quantity
                
                # Корректируем количество по коэффициенту преобразования измерений
                if transaction.measure.base_measure and transaction.measure.base_measure == item.measure:
                    quantity *= transaction.measure.conversion_factor
                
                # Обновляем начальный остаток
                item.start_balance += quantity
                
                # Обновляем конечный остаток (для учета всех транзакций)
                item.end_balance += quantity
            
            except operation_exception:
                # Если номенклатура отсутствует в текущем списке, пропускаем транзакцию
                continue

        # Обработка транзакций в диапазоне даты (учет операций за период)
        for transaction in transactions:
            # Проверка, что транзакция относится к правильному складу и попадает в диапазон дат
            is_correct_storage = transaction.storage.unique_code == self.__storage.unique_code
            is_in_date_range = self.__start_date <= transaction.date <= self.__end_date
            
            if not (is_correct_storage and is_in_date_range):
                continue
                
            try:
                # Находим строку по номенклатуре транзакции
                item = self.find_row(transaction.nomenclature)
                quantity = transaction.quantity
                
                # Корректируем количество, если измерение отличается от базового
                if transaction.measure.base_measure and transaction.measure.base_measure == item.measure:
                    quantity *= transaction.measure.conversion_factor
                
                # Обновляем показатели по приходу/расходу
                if transaction.quantity > 0:
                    item.income += quantity
                else:
                    # Для расхода берем абсолютное значение
                    item.outcome += abs(quantity)
                
                # Обновляем конечный остаток
                item.end_balance += quantity
            
            except operation_exception:
                # Пропускаем транзакции без соответствующей номенклатуры
                continue