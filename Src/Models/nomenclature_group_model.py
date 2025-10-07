from Src.Core.abstract_model import abstract_model
from Src.Core.validator import validator

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
    _instances = {}

    def __init__(self, name = ""):
        super().__init__(name)

    """ Универсальный метод - фабричный. Упрощает переиспользование и использование распространенных групп ном-уры """
    @staticmethod
    def create(name:str):
        validator.validate(name, str)
        if name in nomenclature_group_model._instances.keys():
            return nomenclature_group_model._instances[name]
        item = nomenclature_group_model()
        item.name = name
        nomenclature_group_model._instances[name] = item
        return item
    