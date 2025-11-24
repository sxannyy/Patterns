from datetime import datetime
from Src.Core.validator import validator
from Src.Core.abstract_model import abstract_model
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.Dto.balance_dto import balance_dto

class balance_model(abstract_model):
    
    """
    Модель остатка товара на складе.
    Наследуется от абстрактной модели и содержит информацию об остатках номенклатуры.
    """
    
    __nomenclature: nomenclature_model      # Номенклатура
    __measure: measure_model                # Единица измерения
    __storage: storage_model                # Склад
    __end_balance: float                    # Конечный остаток
    __block_date: datetime                  # Фиксированная (закрытая) дата

    @property
    def nomenclature(self) -> nomenclature_model:
        """Возвращает номенклатуру"""
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        """Устанавливает номенклатуру с валидацией типа"""
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    @property
    def measure(self) -> measure_model:
        """Возвращает единицу измерения"""
        return self.__measure
    
    @measure.setter
    def measure(self, value: measure_model):
        """Устанавливает единицу измерения с валидацией типа"""
        validator.validate(value, measure_model)
        self.__measure = value

    @property
    def storage(self) -> storage_model:
        """Возвращает склад"""
        return self.__storage
    
    @storage.setter
    def storage(self, value: storage_model):
        """Устанавливает склад с валидацией типа"""
        validator.validate(value, storage_model)
        self.__storage = value

    @property
    def end_balance(self) -> float:
        """Возвращает конечный остаток"""
        return self.__end_balance
    
    @end_balance.setter
    def end_balance(self, value: float):
        """Устанавливает конечный остаток с валидацией типа"""
        validator.validate(value, float)
        self.__end_balance = value

    @property
    def block_date(self) -> datetime:
        """Возвращает фиксированную (закрытую) дату"""
        return self.__block_date
    
    @block_date.setter
    def block_date(self, value: datetime):
        """Устанавливает фиксированную (закрытую) дату"""
        self.__block_date = value

    @staticmethod
    def create(nomenclature: nomenclature_model, measure: measure_model, end_balance: float, block_date: datetime) -> 'balance_model':
        """
        Фабричный метод создания модели остатка.
        
        Аргументы:
            nomenclature: Модель номенклатуры
            measure: Модель единицы измерения
            end_balance: Конечный остаток
            block_date: Фиксированная дата
            
        Возвращает:
            balance_model: Созданная модель остатка
        """
        item = balance_model()
        item.nomenclature = nomenclature
        item.measure = measure
        item.end_balance = end_balance
        item.block_date = block_date

        return item

    @staticmethod
    def from_dto(dto: balance_dto, cache: dict) -> 'balance_model':
        """
        Создает модель остатка из DTO объекта.

        Аргументы:
            dto (balance_dto): DTO объект с данными.
            cache (dict): Кэш для поиска связанных объектов:
                - dto.nomenclature_id -> nomenclature_model
                - dto.measure_id      -> measure_model
                - dto.storage_id      -> storage_model

        Возвращает:
            balance_model: Созданная модель остатка.
        """

        # Валидация входных параметров
        validator.validate(dto, balance_dto)
        validator.validate(cache, dict)

        # Получаем связанные объекты из кэша по ID
        nomenclature = cache.get(dto.nomenclature_id) if dto.nomenclature_id else None
        measure = cache.get(dto.measure_id) if dto.measure_id else None
        storage = cache.get(dto.storage_id) if dto.storage_id else None

        # Создаём модель (storage установим отдельно, т.к. фабричный метод его не принимает)
        item = balance_model.create(
            nomenclature=nomenclature,
            measure=measure,
            end_balance=dto.end_balance,
            block_date=dto.block_date
        )

        # Устанавливаем склад, если он найден в кэше
        if storage:
            item.storage = storage

        # Если в abstract_model есть поле unique_code, можно привязать id из DTO
        # (в зависимости от реализации базового класса)
        if hasattr(item, "unique_code") and dto.id:
            item.unique_code = dto.id

        return item

    def to_dto(self) -> balance_dto:
        """
        Преобразует модель остатка в DTO объект для передачи данных.

        Возвращает:
            balance_dto: DTO объект с данными модели.
        """

        dto = balance_dto()

        # ID из базового класса (если он есть в abstract_model)
        if hasattr(self, "unique_code"):
            dto.id = self.unique_code

        # ID связанных сущностей
        dto.nomenclature_id = (
            self.nomenclature.unique_code if getattr(self, "nomenclature", None) else None
        )
        dto.measure_id = (
            self.measure.unique_code if getattr(self, "measure", None) else None
        )
        dto.storage_id = (
            self.storage.unique_code if getattr(self, "storage", None) else None
        )

        # Остаток и дата
        dto.end_balance = self.end_balance
        dto.block_date = self.block_date

        return dto