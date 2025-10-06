from Src.Core.validator import validator
from Src.Core.abstract_model import abstract_model
from Src.Core.validator import argument_exception

"""
    Доменная модель «Единица измерения».

    Свойства:
        base_measure (measure_model|None): Базовая единица (например, штука).
        conversion_factor (int): Коэффициент пересчёта к базовой единице.
    Примеры:
        - 'упаковка' с conversion_factor=10 и base_measure='шт'.
"""

class measure_model(abstract_model):
    
    __base_measure: 'measure_model' = None
    __conversion_factor: float|int = 1.0
    _instances = {}

    def __init__(self, name:str = '', conversion_factor: float|int = 1.0, base_measure = None):
        super().__init__(name)
        if base_measure is not None:
            validator.validate(base_measure, measure_model)
        validator.validate(conversion_factor, float|int)
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
    def conversion_factor(self, conversion_factor):
        """ Устанавливает коэффициент пересчёта; валидируется тип (int) """
        validator.validate(conversion_factor, float|int)
        if conversion_factor <= 0:
            raise argument_exception("Некорректный аргумент!")
        self.__conversion_factor = conversion_factor

    """ Универсальный метод - фабричный """
    @staticmethod
    def create(name:str, base_measure: 'measure_model' = None, conversion_factor: float|int = 1.0):
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
