from Src.Core.abstract_model import abstract_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.measure_model import measure_model
from Src.Core.validator import validator
from Src.Dto.nomenclature_dto import nomenclature_dto

class nomenclature_model(abstract_model):

    """
    Модель номенклатуры (товара/продукта) в бизнес-логике приложения.
    Наследует от абстрактной модели и содержит бизнес-логику для работы с номенклатурой.
    """

    # Приватные поля модели
    __fullname: str  # Полное наименование товара
    __nomenclature_group: nomenclature_group_model  # Группа номенклатуры
    __measure: measure_model  # Единица измерения
    
    def __init__(self, name: str = "", fullname: str = "", nomenclature_group: nomenclature_group_model = None, measure: measure_model = None):
        
        """
        Конструктор модели номенклатуры.
        
        Аргументы:
            name (str): Краткое наименование товара
            fullname (str): Полное наименование товара
            nomenclature_group (nomenclature_group_model): Группа номенклатуры
            measure (measure_model): Единица измерения
        """

        super().__init__(name)  # Инициализация базового класса
        self.__fullname = fullname
        self.__nomenclature_group = nomenclature_group
        self.__measure = measure

    @property
    def fullname(self) -> str:
        """Возвращает полное наименование товара"""
        return self.__fullname
    
    @fullname.setter
    def fullname(self, value: str):
        """Устанавливает полное наименование товара с валидацией"""
        validator.validate(value, str, 255)  # Валидация: строка, макс. 255 символов
        self.__fullname = value

    @property
    def nomenclature_group(self) -> nomenclature_group_model:
        """Возвращает группу номенклатуры"""
        return self.__nomenclature_group
    
    @nomenclature_group.setter
    def nomenclature_group(self, value: nomenclature_group_model):
        """Устанавливает группу номенклатуры с валидацией"""
        validator.validate(value, nomenclature_group_model)  # Валидация типа
        self.__nomenclature_group = value

    @property
    def measure(self) -> measure_model:
        """Возвращает единицу измерения"""
        return self.__measure
    
    @measure.setter
    def measure(self, value: measure_model):
        """Устанавливает единицу измерения с валидацией"""
        validator.validate(value, measure_model)  # Валидация типа
        self.__measure = value

    @staticmethod
    def create(name: str, group: nomenclature_group_model, measure: measure_model, fullname: str = ""):

        """
        Статический метод для создания экземпляра номенклатуры.
        Аргументы:
            name (str): Краткое наименование
            group (nomenclature_group_model): Группа номенклатуры
            measure (measure_model): Единица измерения
            fullname (str): Полное наименование (опционально)  
        Возвращает:
            nomenclature_model: Созданный экземпляр модели
        """

        validator.validate(name, str)  # Валидация обязательных параметров
        validator.validate(group, nomenclature_group_model)
        validator.validate(measure, measure_model)
        
        if not fullname:
            fullname = name  # Если полное имя не указано, используем краткое
            
        item = nomenclature_model(name, fullname, group, measure)
        return item

    @staticmethod
    def from_dto(dto: nomenclature_dto, cache: dict):

        """
        Создает модель номенклатуры из DTO объекта.
        Аргументы:
            dto (nomenclature_dto): DTO объект с данными
            cache (dict): Кэш для поиска связанных объектов (measure и group)
        Возвращает:
            nomenclature_model: Созданная модель номенклатуры
        """

        validator.validate(dto, nomenclature_dto)
        validator.validate(cache, dict)
        
        # Получаем связанные объекты из кэша по ID
        measure = cache.get(dto.range_id)  # range_id соответствует measure
        category = cache.get(dto.category_id)  # category_id соответствует nomenclature_group
        
        item = nomenclature_model.create(
            name=dto.name,
            group=category,
            measure=measure,
            fullname=dto.name  # В текущей реализации используется name как fullname
        )
        
        return item
    
    def to_dto(self) -> nomenclature_dto:

        """
        Преобразует модель номенклатуры в DTO объект для передачи данных.
        Возвращает:
            nomenclature_dto: DTO объект с данными модели
        """

        dto = nomenclature_dto()
        dto.id = self.unique_code  # ID из базового класса
        dto.name = self.name  # Наименование из базового класса
        dto.range_id = self.measure.unique_code if self.measure else None  # ID единицы измерения
        dto.category_id = self.nomenclature_group.unique_code if self.nomenclature_group else None  # ID группы
        return dto