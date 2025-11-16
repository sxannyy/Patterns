from Src.Core.abstract_dto import abstract_dto
from Src.Core.match_type import match_type
from Src.Core.validator import validator
from typing import Any

class filter_dto(abstract_dto):
    """
    DTO для представления параметров фильтрации.
    Используется для передачи критериев фильтрации между слоями приложения.
    Поддерживает различные типы сравнения: точное совпадение, частичный поиск, диапазон.
    """
    
    __field_name: str = ""                       # Название поля для фильтрации
    __filter_value: Any = None                   # Значение для фильтрации
    __operation: match_type = match_type.EQUALS  # Тип операции сравнения

    @property
    def field_name(self) -> str:
        """Возвращает название поля для фильтрации"""
        return self.__field_name
    
    @field_name.setter
    def field_name(self, value: str):
        """Устанавливает название поля для фильтрации"""
        self.__field_name = value
    
    @property
    def filter_value(self) -> Any:
        """Возвращает значение для фильтрации"""
        return self.__filter_value
    
    @filter_value.setter
    def filter_value(self, value: Any):
        """Устанавливает значение для фильтрации"""
        self.__filter_value = value

    @property
    def operation(self) -> match_type:
        """Возвращает тип операции """
        return self.__operation

    @operation.setter
    def operation(self, value: str):
        """Устанавливает тип операции из строки"""
        if isinstance(value, str):
            try:
                value = match_type[value.upper()]
            except KeyError:
                raise match_type(f"Недопустимый тип фильтра: {value}")
        validator.validate(value, match_type)
        self.__operation = value

    def create(self, data) -> "filter_dto":
        """
        Создает и инициализирует DTO из словаря с данными.
        
        Аргументы:
            data: Словарь с параметрами фильтра в формате:
                {
                    "filter_name": "название_поля",
                    "value": "значение_для_фильтрации", 
                    "type": "тип_операции"
                } 
        Возвращает:
            filter_dto: Текущий экземпляр DTO с установленными значениями
        Ошибки:
            ValueError: Если переданные данные не являются словарем
            KeyError: Если указан неверный тип операции
        """
        validator.validate(data, dict)
        self.field_name = data.get("filter_name", "")
        self.filter_value = data.get("value")
        op = data.get("type") or data.get("operation")
        if op:
            self.operation = op
        return self