from Src.Core.validator import validator
from Src.Core.abstract_model import abstract_model

"""
    Доменная модель «Склад / Место хранения».
    Назначение:
        Представляет физическое или логическое место хранения номенклатуры.
    Свойства:
        name (str): Название склада/ячейки (унаследовано из abstract_model).
        unique_code (str): Уникальный код склада/ячейки (унаследовано).
        address (str): Адрес хранения.
    Особенности:
        - Может использоваться для привязки номенклатуры к конкретному складу.
        - Поддерживает сравнение объектов по unique_code.
        - Хранит в себе адрес.
"""

class storage_model(abstract_model):
    __address:str = ""

    """ Адрес """
    @property
    def address(self) -> str:
        return self.__address.strip()

    @address.setter
    def address(self, value:str):
        validator.validate(value, str)
        self.__address = value.strip()