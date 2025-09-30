from Src.Core.abstract_model import abstract_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.measure_model import measure_model
from Src.Core.validator import validator

class nomenclature_model(abstract_model):

    """
    Доменная модель «Номенклатура».
    Назначение:
        Представляет товар или услугу в системе.
    Свойства:
        name (str): Наименование товара или услуги (унаследовано из abstract_model).
        unique_code (str): Уникальный идентификатор позиции (унаследовано).
        measure (measure_model): Единица измерения для номенклатуры.
        group (nomenclature_group_model): Группа, к которой относится данная позиция.
    Особенности:
        - Может использоваться для учёта складских остатков.
        - Может быть связана с разными бизнес-процессами (продажа, закупка и т.д.).
    """

    __fullname: str
    __nomenclature_group: nomenclature_group_model
    __measure: measure_model
    
    def __init__(self, name: str, fullname: str, nomenclature_group: nomenclature_group_model, measure: measure_model):
        super().__init__(name)
        validator.validate(fullname, str, 255)
        validator.validate(nomenclature_group, nomenclature_group_model)
        validator.validate(measure, measure_model)
        
        self.__fullname = fullname
        self.__nomenclature_group = nomenclature_group
        self.__measure = measure

    @property
    def fullname(self) -> str:
        return self.__fullname
    
    @fullname.setter
    def fullname(self, value:str):
        validator.validate(value, str, 255)
        self.__fullname = value

    @property
    def nomenclature_group(self) -> nomenclature_group_model:
        return self.__nomenclature_group
    
    @nomenclature_group.setter
    def nomenclature_group(self, value: nomenclature_group_model):
        validator.validate(value, nomenclature_group_model)
        self.__nomenclature_group = value

    @property
    def measure(self) -> measure_model:
        return self.__measure
    
    @measure.setter
    def measure(self, value: measure_model):
        validator.validate(value, measure_model)
        self.__measure = value