from Src.Core.validator import validator
from Src.Core.abstract_model import abstract_model

class storage_model(abstract_model):

    """
    Доменная модель «Склад / Место хранения».
    Назначение:
        Представляет физическое или логическое место хранения номенклатуры.
    Свойства:
        name (str): Название склада/ячейки (унаследовано из abstract_model).
        unique_code (str): Уникальный код склада/ячейки (унаследовано).
    Особенности:
        - Может использоваться для привязки номенклатуры к конкретному складу.
        - Поддерживает сравнение объектов по unique_code.
    """

    pass