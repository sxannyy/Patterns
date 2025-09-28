from Src.Core.validator import validator
from Src.Core.abstract_model import abstract_model

class measure_model(abstract_model):
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
        return self.__base_measure
        
    @base_measure.setter
    def base_measure(self, base_measure):
        if base_measure is not None:
            validator.validate(base_measure, measure_model) 
        self.__base_measure = base_measure

    @property
    def conversion_factor(self) -> int:
        return self.__conversion_factor
    
    @conversion_factor.setter
    def conversion_factor(self, conversion_factor):
        validator.validate(conversion_factor, int)
        self.__conversion_factor = conversion_factor
