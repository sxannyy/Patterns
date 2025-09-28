from Src.Core.validator import validator
from Src.Core.abstract_model import abstract_model

class company_model(abstract_model):
    __type_of_property:str = ""
    __inn:int = 0
    __bank_account:int = 0
    __correspondent_account:int = 0
    __bik:int = 0

    # Вид собственности 5 симв
    # ИНН : 12 симв
    # Счет 11 симв
    # Корреспондентский счет 11 симв
    # БИК 9 симв
    
    # Вид собственности
    @property
    def type_of_property(self) -> str:
        return self.__type_of_property
    
    @type_of_property.setter
    def type_of_property(self, value:str):
        validator.validate(value, str, 5)
        self.__ownership = value.strip()
    
    # ИНН
    @property
    def inn(self) -> int:
        return self.__inn

    @inn.setter
    def inn(self, value:int):
        validator.validate(value, int, 12)
        self.__inn = value
    
    # Банковский счет
    @property
    def bank_account(self) -> int:
        return self.__bank_account
    
    @bank_account.setter
    def bank_account(self, value:int):
        validator.validate(value, int, 11)
        self.__bank_account = value
    
    # Корресподентский счет
    @property
    def correspondent_account(self) -> int:
        return self.__correspondent_account
    
    @correspondent_account.setter
    def correspondent_account(self, value:int):
        validator.validate(value, int, 11)
        self.__correspondent_account = value
    
    # БИК
    @property
    def bik(self) -> int:
        return self.__bik

    @bik.setter
    def bik(self, value:int):
        validator.validate(value, int, 9)
        self.__bik = value