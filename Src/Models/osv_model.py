from Src.Core.validator import validator
from Src.Core.abstract_model import abstract_model
from Src.Models.osv_unit_model import osv_unit_model
from Src.Dto.osv_dto import osv_dto
from datetime import datetime
from typing import List

from Src.Models.storage_model import storage_model

class osv_model(abstract_model):
    """
    Модель оборотно-сальдовой ведомости (ОСВ) в предметной области.
    
    Представляет собой отчет по остаткам и движениям номенклатуры на складе за определенный период.
    Содержит информацию о начальных и конечных остатках, приходе и расходе товаров.
    
    Наследует от abstract_model базовые поля: id, name, unique_code.
    """
    
    # Приватные поля модели
    __start_date: datetime = None      # Дата начала отчетного периода
    __end_date: datetime = None        # Дата окончания отчетного периода
    __storage: storage_model = None    # Склад, для которого формируется ведомость
    __rows: List[osv_unit_model] = []  # Список строк ведомости по каждой номенклатуре

    def __init__(self, name: str = ""):
        """
        Конструктор модели оборотно-сальдовой ведомости.
        
        Аргументы:
            name (str): Наименование отчета ОСВ (по умолчанию пустая строка)
        """
        super().__init__(name)

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
    
    @staticmethod
    def create(start_date: datetime, end_date: datetime, storage: storage_model) -> 'osv_model':
        """
        Фабричный метод для создания отчета оборотно-сальдовой ведомости.
        
        Аргументы:
            start_date (datetime): Дата начала отчетного периода
            end_date (datetime): Дата окончания отчетного периода
            storage (storage_model): Склад, для которого формируется ведомость
            
        Возвращает:
            osv_model: Созданный экземпляр отчета ОСВ
            
        Ошибки:
            Validation error: Если параметры не соответствуют ожидаемым типам
        """
        # Валидация входных параметров
        validator.validate(start_date, datetime)
        validator.validate(end_date, datetime)
        validator.validate(storage, storage_model)

        # Создание и настройка экземпляра ведомости
        item = osv_model()
        item.start_date = start_date
        item.end_date = end_date
        item.storage = storage

        return item
    
    def to_dto(self) -> osv_dto:
        """
        Преобразует модель домена osv_model в транспортный объект osv_dto.
        
        Возвращает:
            osv_dto: Транспортный объект для передачи данных между слоями приложения
        """
        # Преобразуем каждую строку ведомости в DTO формат
        rows_dto = [row.to_dto() for row in self.rows]
        
        # Создаем и заполняем DTO объект
        dto = osv_dto()
        dto.id = self.unique_code          # Уникальный идентификатор ведомости
        dto.start_date = self.start_date   # Дата начала периода
        dto.end_date = self.end_date       # Дата окончания периода
        dto.storage = self.storage         # Объект склада
        dto.rows = rows_dto                # Список строк ведомости в DTO формате
        
        return dto