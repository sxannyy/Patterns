from Src.Core.validator import validator
from Src.Core.abstract_model import abstract_model

class measure_model(abstract_model):

    """
    Доменная модель «Единица измерения».

    Свойства:
        base_measure (measure_model|None): Базовая единица (например, штука).
        conversion_factor (int): Коэффициент пересчёта к базовой единице.
    Примеры:
        - 'упаковка' с conversion_factor=10 и base_measure='шт'.
    """

    __base_measure = None
    __conversion_factor: int

    def __init__(self, name, conversion_factor: int, base_measure = None):
        super().__init__(name)
        if base_measure is not None:
            validator.validate(base_measure, measure_model)
        validator.validate(conversion_factor, int)
        self.__base_measure: measure_model = base_measure
        self.__conversion_factor: int = conversion_factor

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
    def conversion_factor(self) -> int:
        """ Коэффициент пересчёта к base_measure (целое положительное число) """
        return self.__conversion_factor
    
    @conversion_factor.setter
    def conversion_factor(self, conversion_factor):
        """ Устанавливает коэффициент пересчёта; валидируется тип (int) """
        validator.validate(conversion_factor, int)
        self.__conversion_factor = conversion_factor
