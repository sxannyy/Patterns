from datetime import datetime
from Src.Core.prototype import prototype
from Src.Models.nomenclature_model import nomenclature_model
from Src.Core.validator import validator
from Src.Models.storage_model import storage_model
from Src.Dto.filter_dto import filter_dto

class prototype_report(prototype):
    """
    Класс-прототип для работы с отчетами.
    Наследует базовый функционал прототипа и добавляет специализированные методы
    для фильтрации данных отчетов по номенклатуре, датам и складам.
    """
    
    def __init__(self, data):
        """
        Инициализирует прототип отчета с данными
        
        Аргументы:
            data: Список объектов для работы в отчете
        """
        self._prototype__data = data

    def clone(self, data = None):
        """
        Создает копию прототипа отчета
        
        Аргументы:
            data: Новые данные для клонирования. Если None, используются текущие данные
        Возвращает:
            prototype_report: Новый экземпляр прототипа отчета с указанными данными
        """
        if data is None:
            data = self.data
        return prototype_report(data)
    
    @staticmethod
    def filter_by_nomenclature(source: prototype, nomenclature: nomenclature_model) -> prototype:
        """
        Фильтрует данные по указанной номенклатуре
        
        Аргументы:
            source: Прототип с исходными данными для фильтрации
            nomenclature: Модель номенклатуры для фильтрации
            
        Возвращает:
            prototype: Новый прототип с отфильтрованными данными
            
        Ошибки:
            ValueError: Если source не является prototype или nomenclature не является nomenclature_model
        """
        validator.validate(source, prototype)
        validator.validate(nomenclature, nomenclature_model)

        result = []
        for item in source.data:
            if item.nomenclature == nomenclature:
                result.append(item)
        
        return source.clone(result)

    @staticmethod
    def filter_by_date(source: prototype, first_date: datetime, second_date: datetime) -> prototype:
        """
        Фильтрует данные по диапазону дат (включительно)
        
        Аргументы:
            source: Прототип с исходными данными для фильтрации
            first_date: Начальная дата диапазона
            second_date: Конечная дата диапазона
        Возвращает:
            prototype: Новый прототип с данными, попадающими в указанный диапазон дат
        Ошибки:
            ValueError: Если source не является prototype или даты не являются datetime
        """
        validator.validate(source, prototype)
        validator.validate(first_date, datetime)
        validator.validate(second_date, datetime)

        result = []
        for item in source.data:
            if hasattr(item, 'date') and first_date <= item.date <= second_date:
                result.append(item)
        
        return source.clone(result)

    @staticmethod
    def filter_by_storage(source: prototype, storage: storage_model) -> prototype:
        """
        Фильтрует данные по указанному складу
        
        Аргументы:
            source: Прототип с исходными данными для фильтрации
            storage: Модель склада для фильтрации
        Возвращает:
            prototype: Новый прототип с данными, связанными с указанным складом
        Ошибки:
            ValueError: Если source не является prototype или storage не является storage_model
        """
        validator.validate(source, prototype)
        validator.validate(storage, storage_model)

        result = []
        for item in source.data:
            if hasattr(item, 'storage') and item.storage == storage:
                result.append(item)
        
        return source.clone(result)
    
    @staticmethod
    def filter(source: prototype, filter: filter_dto) -> prototype:
        """
        Фильтрует данные по произвольному критерию с использованием filter_dto
        
        Аргументы:
            source: Прототип с исходными данными для фильтрации
            filter: DTO с параметрами фильтрации (поле, значение, тип операции)
        Возвращает:
            prototype: Новый прототип с данными, удовлетворяющими критериям фильтра
        Ошибки:
            ValueError: Если source не является prototype
        """
        validator.validate(source, prototype)
        result = prototype.filter(source.data, filter)
        return source.clone(result)