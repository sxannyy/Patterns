from Src.Core.abstract_model import abstract_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.measure_model import measure_model
from Src.Dto.composition_dto import composition_dto
from Src.Core.validator import validator

# Модель элемента рецепта
class receipt_item_model(abstract_model):

    """
    Модель элемента рецепта (ингредиента в составе блюда/продукта).
    Представляет собой один ингредиент в рецепте с указанием количества и единицы измерения.
    Наследует от abstract_model (поля id, name, unique_code).
    """
    
    # Приватные поля модели
    __nomenclature: nomenclature_model  # Номенклатура (ингредиент)
    __range: measure_model              # Единица измерения (мера)
    __value: int                        # Количество

    @property
    def nomenclature(self) -> nomenclature_model:
        """Возвращает номенклатуру (ингредиент)"""
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        """Устанавливает номенклатуру с валидацией типа"""
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    @property
    def range(self) -> measure_model:
        """Возвращает единицу измерения"""
        return self.__range
    
    @range.setter
    def range(self, value: measure_model):
        """Устанавливает единицу измерения с валидацией типа"""
        validator.validate(value, measure_model)
        self.__range = value

    @property
    def value(self) -> int:
        """Возвращает количество ингредиента"""
        return self.__value
    
    @value.setter
    def value(self, value: int):
        """Устанавливает количество с валидацией типа"""
        validator.validate(value, int)
        self.__value = value

    # Фабричный метод
    @staticmethod
    def create(nomenclature: nomenclature_model, range: measure_model, value: int):

        """
        Фабричный метод для создания элемента рецепта.
        Аргументы:
            nomenclature (nomenclature_model): Ингредиент
            range (measure_model): Единица измерения
            value (int): Количество
        Возвращает:
            receipt_item_model: Созданный элемент рецепта
        """
        item = receipt_item_model()
        item.nomenclature = nomenclature
        item.range = range
        item.value = value
        return item

    @staticmethod
    def from_dto(dto: composition_dto, cache: dict):

        """
        Создает модель элемента рецепта из DTO объекта.
        Аргументы:
            dto (composition_dto): DTO с данными состава
            cache (dict): Кэш для поиска связанных объектов по ID
        Возвращает:
            receipt_item_model: Созданная модель элемента рецепта
        """
        validator.validate(dto, composition_dto)
        validator.validate(cache, dict)
        
        # Получаем связанные объекты из кэша по ID из DTO
        nomenclature = cache.get(dto.nomenclature_id)  # Находим номенклатуру по ID
        range = cache.get(dto.range_id)                # Находим единицу измерения по ID
        
        # Создаем элемент рецепта
        item = receipt_item_model.create(nomenclature, range, dto.value)
        return item
    
    def to_dto(self) -> composition_dto:

        """
        Преобразует receipt_item_model в composition_dto для передачи данных.
        """
        
        dto = composition_dto()
        dto.id = self.unique_code  # Уникальный идентификатор
        dto.name = self.name if hasattr(self, 'name') else f"Item_{self.unique_code}"  # Имя или значение по умолчанию
        dto.nomenclature_id = self.nomenclature.unique_code if self.nomenclature else None  # ID номенклатуры
        dto.range_id = self.range.unique_code if self.range else None  # ID единицы измерения
        dto.value = self.value  # Количество
        return dto