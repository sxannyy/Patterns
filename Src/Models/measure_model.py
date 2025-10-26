from Src.Core.validator import validator
from Src.Core.abstract_model import abstract_model
from Src.Core.validator import argument_exception
from Src.Dto.measure_dto import measure_dto

"""
    Доменная модель «Единица измерения».

    Свойства:
        base_measure (measure_model|None): Базовая единица (например, штука).
        conversion_factor (float): Коэффициент пересчёта к базовой единице.
    Статические методы:
        Грамм - начальный метод (name: грамм, measure_model: None, conversion_factor: 1)
        Килограмм - основывается на методе грамм (name: килограмм, measure_model: gramm, conversion_factor: 1000)
        Штука - начальный метод (name: штука, measure_model: None, conversion_factor: 1)
        Литр - начальный метод (name: литр, measure_model: None, conversion_factor: 1)
        Миллилитр - основывается на методе литр (name: миллилитр, measure_model: liter, conversion_factor: 0.001)
    Примеры:
        - 'упаковка' с conversion_factor=10.0 и base_measure='шт'.
"""

class measure_model(abstract_model):
    
    __base_measure: 'measure_model'
    __conversion_factor: float
    _instances = {}

    def __init__(self, name:str = '', conversion_factor: float = 1.0, base_measure = None):
        super().__init__(name)
        if base_measure is not None:
            validator.validate(base_measure, measure_model)
        validator.validate(conversion_factor, float)
        self.__base_measure: measure_model = base_measure
        self.__conversion_factor: float = float(conversion_factor)

    @property
    def base_measure(self):
        """ Базовая единица измерения или None (если текущая - базовая) """
        return self.__base_measure
        
    @base_measure.setter
    def base_measure(self, base_measure):
        """ Задаёт базовую единицу; допускается None или другой measure_model """
        if base_measure is not None:
            validator.validate(base_measure, measure_model) 
        self.__base_measure = base_measure

    @property
    def conversion_factor(self) -> float:
        """ Коэффициент пересчёта к base_measure (целое положительное число) """
        return self.__conversion_factor
    
    @conversion_factor.setter
    def conversion_factor(self, conversion_factor: float):
        """ Устанавливает коэффициент пересчёта; валидируется тип (float) """
        validator.validate(conversion_factor, float)
        if conversion_factor <= 0:
            raise argument_exception("Некорректный аргумент!")
        self.__conversion_factor = conversion_factor

    """ Универсальный метод - фабричный. Упрощает переиспользование и использование распространенных единиц измерения """
    @staticmethod
    def create(name:str, base_measure: 'measure_model' = None, conversion_factor: float = 1.0):
        validator.validate(name, str)
        if name in measure_model._instances.keys():
            return measure_model._instances[name]
        inner_base = None
        if not base_measure is None: 
            validator.validate(base_measure, measure_model)
            inner_base = base_measure
        item = measure_model()
        item.name = name
        item.base_measure = inner_base
        item.conversion_factor = float(conversion_factor)
        measure_model._instances[name] = item
        return item

    """ Грамм """
    @staticmethod
    def create_gramm():
        return measure_model.create("грамм")
    
    """ Килограмм """
    @staticmethod
    def create_kilogramm():
        inner_gramm = measure_model.create_gramm()
        return measure_model.create("килограмм", inner_gramm, 1000)
    
    """ Штука """
    @staticmethod
    def create_piece():
        return measure_model.create("шт")
    
    """ Литр """
    @staticmethod
    def create_liter():
        return measure_model.create("литр")
    
    """ Миллилитр """
    @staticmethod
    def create_milliliter():
        inner_liter = measure_model.create_liter()
        return measure_model.create("миллилитер", inner_liter, 0.001)
    
    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto:measure_dto, cache:dict):
        validator.validate(dto, measure_dto)
        validator.validate(cache, dict)
        base  = cache[ dto.base_id ] if dto.base_id in cache else None
        item = measure_model.create(dto.name, dto.value, base)
        return item
    
    def to_dto(self) -> measure_dto:

        """
        Преобразует measure_model в measure_dto
        """
        
        dto = measure_dto()
        dto.id = self.unique_code
        dto.name = self.name
        dto.base_id = self.base_measure.unique_code if self.base_measure else None
        dto.value = self.conversion_factor
        return dto