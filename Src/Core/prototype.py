from abc import ABC, abstractmethod
from Src.Core.validator import validator
from Src.Dto.filter_dto import filter_dto
from Src.Core.match_type import match_type

class prototype(ABC):
    """
    Абстрактный базовый класс для реализации Прототипа.
    
    Позволяет создавать копии объектов и фильтровать коллекции данных
    по различным критериям с поддержкой вложенных полей.
    """
    __data = []

    @property
    def data(self):
        """Возвращает внутренние данные прототипа"""
        return self.__data

    def __init__(self, data:list):
        """
        Инициализирует прототип с данными
        
        Аргументы:
            data: Список объектов для работы
            
        Ошибки:
            ValueError: Если данные не являются списком
        """
        validator.validate(data, list)
        self.__data = data

    @abstractmethod
    def clone(self, data:list = None) -> 'prototype':
        """
        Абстрактный метод для создания копии прототипа
        
        Аргументы:
            data: Новые данные для клонирования. Если None, используются текущие данные   
        Возвращает:
            prototype: Новый экземпляр прототипа
        """
        inner_data = None
        if data is None:
            inner_data = self.__data
        else:
            inner_data = data
        instance = prototype(inner_data)
        return instance
    
    @staticmethod
    def get_nested_value(obj, field_path: str):
        """
        Получает значение вложенного поля объекта по точечному пути
        
        Аргументы:
            obj: Объект для получения значения
            field_path: Путь к полю в формате
        Возвращает:
            Значение поля или None если поле не существует
        """
        parts = field_path.split(".")
        current = obj
        for part in parts:
            if current is None or not hasattr(current, part):
                return None
            current = getattr(current, part)
        return current

    @staticmethod
    def filter(data: list, flt: filter_dto):
        """
        Фильтрует список объектов по заданному критерию
        
        Аргументы:
            data: Список объектов для фильтрации
            flt: DTO с параметрами фильтрации (поле, значение, тип операции)
        Возвращает:
            list: Отфильтрованный список объектов, удовлетворяющих условиям
            
        Ошибки:
            TypeError: Если данные не являются списком или словарем
            ValueError: Если фильтр содержит некорректные параметры
        """
        if not data:
            return data

        result = []
        # Поддержка словарей - преобразуем в список значений
        if isinstance(data, dict):
            data = data.values()
            
        for item in data:
            raw_value = prototype.get_nested_value(item, flt.field_name)
            if raw_value is None:
                continue

            # 1. Диапазон (IN_RANGE) — работаем с "сырым" значением (датой, числом и т.п.)
            if flt.operation == match_type.IN_RANGE:
                range_val = flt.filter_value

                # ожидаем кортеж/список из двух значений
                try:
                    start, end = range_val
                except Exception:
                    # некорректное значение фильтра — просто пропускаем элемент
                    continue

                # допускаем "открытые" границы: None вместо начала/конца диапазона
                if start is not None and raw_value < start:
                    continue
                if end is not None and raw_value > end:
                    continue

                result.append(item)
                continue  # переходим к следующему элементу

            # 2. Остальные операции — работаем как и раньше через строки
            value = str(raw_value)
            pattern = str(flt.filter_value or "")

            if flt.operation == match_type.EQUALS:
                if value == pattern:
                    result.append(item)

            elif flt.operation == match_type.LIKE:
                # Частичное совпадение без учета регистра
                if pattern.lower() in value.lower():
                    result.append(item)

        return result