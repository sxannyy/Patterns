from datetime import datetime
from Src.Core.validator import validator
from Src.Core.abstract_model import abstract_model
from Src.Dto.transaction_dto import transaction_dto
from Src.Models.storage_model import storage_model
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_model import nomenclature_model

class transaction_model(abstract_model):
    """
    Модель транзакции в предметной области.
    
    Представляет собой операцию движения товарно-материальных ценностей:
    приход (положительное количество) или расход (отрицательное количество).
    Наследует от abstract_model базовые поля: id, name, unique_code.
    """
    
    # Приватные поля модели
    __storage: storage_model = None           # Склад, на котором происходит операция
    __nomenclature: nomenclature_model = None # Номенклатура товара
    __measure: measure_model = None          # Единица измерения
    __quantity: float = 0.0            # Количество (положительное - приход, отрицательное - расход)
    __date: datetime = None                   # Дата и время операции

    @property
    def storage(self) -> storage_model:
        """Возвращает объект склада транзакции"""
        return self.__storage

    @storage.setter
    def storage(self, value: storage_model):
        """
        Устанавливает склад для транзакции.
        
        Аргументы:
            value (storage_model): Объект склада
            
        Ошибки:
            Validation error: Если переданный параметр не является storage_model
        """
        validator.validate(value, storage_model)
        self.__storage = value

    @property
    def nomenclature(self) -> nomenclature_model:
        """Возвращает объект номенклатуры транзакции"""
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        """
        Устанавливает номенклатуру для транзакции.
        
        Аргументы:
            value (nomenclature_model): Объект номенклатуры
            
        Ошибки:
            Validation error: Если переданный параметр не является nomenclature_model
        """
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    @property
    def measure(self) -> measure_model:
        """Возвращает объект единицы измерения транзакции"""
        return self.__measure

    @measure.setter
    def measure(self, value: measure_model):
        """
        Устанавливает единицу измерения для транзакции.
        
        Аргументы:
            value (measure_model): Объект единицы измерения
            
        Ошибки:
            Validation error: Если переданный параметр не является measure_model
        """
        validator.validate(value, measure_model)
        self.__measure = value

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
            
        Ошибки:
            Validation error: Если переданный параметр не является float
        """
        validator.validate(value, float)
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
            # Преобразуем строку в объект datetime
            self.__date = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        if isinstance(value, datetime):
            # Используем переданный объект datetime напрямую
            self.__date = value

    def to_dto(self) -> transaction_dto:
        """
        Преобразует модель домена transaction_model в транспортный объект transaction_dto.
        
        Возвращает:
            transaction_dto: Транспортный объект для передачи данных между слоями приложения
            
        Примечание:
            Метод извлекает уникальные идентификаторы связанных объектов (measure, storage, nomenclature)
            для сериализации в DTO формат.
        """
        dto = transaction_dto()
        dto.id = self.unique_code  # Уникальный идентификатор транзакции
        dto.measure_id = self.measure.unique_code if self.measure else None  # ID единицы измерения
        dto.storage_id = self.storage.unique_code if self.storage else None  # ID склада
        dto.nomenclature_id = self.nomenclature.unique_code if self.nomenclature else None  # ID номенклатуры
        dto.quantity = self.quantity  # Количество товара
        dto.date = self.date  # Дата и время операции
        
        return dto