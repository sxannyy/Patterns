from Src.Core.abstract_model import abstract_model
from Src.Core.validator import validator
from Src.Dto.category_dto import category_dto

"""
    Доменная модель «Группа номенклатуры».
    Назначение:
        Используется для классификации номенклатуры (товаров, услуг) по группам и категориям.
    Свойства:
        name (str): Название группы (унаследовано из abstract_model).
        unique_code (str): Уникальный идентификатор группы (унаследовано).
    Особенности:
        - Может быть использована для построения иерархии категорий товаров.
    Статические методы (группы, встречающиеся часто):
        Специи и пряности
        Продукты животного происхождения
        Мука и крупы
"""

class nomenclature_group_model(abstract_model):

    """
    Модель группы номенклатуры для классификации товаров/услуг
    """
    
    # Словарь для хранения созданных экземпляров (паттерн Flyweight)
    _instances = {}

    def __init__(self, name = ""):

        """
        Конструктор группы номенклатуры.
        Аргументы:
            name (str): Название группы
        """

        super().__init__(name)

    @staticmethod
    def create(name:str):

        """
        Фабричный метод для создания или получения существующего экземпляра группы.
        Реализует паттерн Flyweight - переиспользует существующие объекты с одинаковыми именами.
        Аргументы:
            name (str): Название группы
        Возвращает:
            nomenclature_group_model: Существующий или новый экземпляр группы
        """
        validator.validate(name, str)
        
        # Если группа с таким именем уже существует, возвращаем существующий экземпляр
        if name in nomenclature_group_model._instances.keys():
            return nomenclature_group_model._instances[name]
            
        # Создаем новый экземпляр
        item = nomenclature_group_model()
        item.name = name
        # Сохраняем в кэше для повторного использования
        nomenclature_group_model._instances[name] = item
        return item

    @staticmethod
    def from_dto(dto:abstract_model, cache:dict):

        """
        Создает модель группы номенклатуры из DTO объекта.
        Аргументы:
            dto (abstract_model): DTO объект с данными группы
            cache (dict): Кэш для хранения объектов (не используется в этом методе)
        Возвращает:
            nomenclature_group_model: Созданная модель группы
        """

        item  = nomenclature_group_model()
        item.name = dto.name
        item.unique_code = dto.id
        return item
    
    def to_dto(self) -> category_dto:

        """
        Преобразует nomenclature_group_model в category_dto для передачи данных
        """

        dto = category_dto()
        dto.id = self.unique_code
        dto.name = self.name
        return dto