from datetime import datetime
from Src.Core.abstract_dto import abstract_dto
from Src.Core.validator import validator

class transaction_dto(abstract_dto):
    """
    Транспортный объект (DTO) для передачи данных о транзакции между слоями приложения.
    
    Содержит идентификаторы связанных сущностей вместо полных объектов для оптимизации передачи данных.
    Наследует от abstract_dto базовые поля: id, name, unique_code.
    """
    
    # Приватные поля DTO
    __storage_id: str          # Уникальный идентификатор склада
    __nomenclature_id: str     # Уникальный идентификатор номенклатуры
    __measure_id: str          # Уникальный идентификатор единицы измерения
    __quantity: float = 0.0    # Количество товара (положительное - приход, отрицательное - расход)
    __date: datetime           # Дата и время операции

    @property
    def storage_id(self) -> str:
        """Возвращает уникальный идентификатор склада"""
        return self.__storage_id

    @storage_id.setter
    def storage_id(self, value: str):
        """
        Устанавливает идентификатор склада.
        
        Аргументы:
            value (str): Уникальный идентификатор склада
        """
        self.__storage_id = value

    @property
    def nomenclature_id(self) -> str:
        """Возвращает уникальный идентификатор номенклатуры"""
        return self.__nomenclature_id

    @nomenclature_id.setter
    def nomenclature_id(self, value: str):
        """
        Устанавливает идентификатор номенклатуры.
        
        Аргументы:
            value (str): Уникальный идентификатор номенклатуры
        """
        self.__nomenclature_id = value

    @property
    def measure_id(self) -> str:
        """Возвращает уникальный идентификатор единицы измерения"""
        return self.__measure_id

    @measure_id.setter
    def measure_id(self, value: str):
        """
        Устанавливает идентификатор единицы измерения.
        
        Аргументы:
            value (str): Уникальный идентификатор единицы измерения
        """
        self.__measure_id = value

    @property
    def quantity(self) -> float:
        """Возвращает количество товара в транзакции"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        """
        Устанавливает количество товара.
        
        Аргументы:
            value (float): Количество товара (положительное - приход, отрицательное - расход)
        """
        self.__quantity = value

    @property
    def date(self) -> datetime:
        """Возвращает дату и время транзакции"""
        return self.__date

    @date.setter
    def date(self, value):
        """
        Устанавливает дату и время транзакции.
        Поддерживает установку как из строки, так и из объекта datetime.
        
        Аргументы:
            value (str|datetime): Дата и время в формате строки "ГГГГ-ММ-ДД ЧЧ:ММ:СС" или объект datetime
            
        Ошибки:
            Validation error: Если переданный параметр не является строкой или datetime
            ValueError: Если строка не соответствует формату "ГГГГ-ММ-ДД ЧЧ:ММ:СС"
        """
        validator.validate(value, str | datetime)
        if isinstance(value, str):
            # Преобразуем строку в объект datetime по заданному формату
            self.__date = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        if isinstance(value, datetime):
            # Используем переданный объект datetime напрямую
            self.__date = value