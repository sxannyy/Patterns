class CompanyModel():
    __name:str = ""
    __type_of_property:str = ""
    __inn:int = 0
    __bank_account:int = 0
    __correspondent_account:int = 0
    __bik:int = 0

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value:str):
        value = value.strip()
        if value != "":
            self.__name = value
    
    @property
    def type_of_property(self) -> str:
        return self.__type_of_property
    
    @type_of_property.setter
    def type_of_property(self, value:str):
        value = value.strip()
        if value != "" and len(value) == 5:
            self.__type_of_property = value
    
    @property
    def inn(self) -> int:
        return self.__inn

    @inn.setter
    def inn(self, value:int):
        if value > 0 and len(str(value)) == 12:
            self.__inn = value
    
    @property
    def bank_account(self) -> int:
        return self.__bank_account
    
    @bank_account.setter
    def bank_account(self, value:int):
        if value > 0 and len(str(value)) == 11:
            self.__bank_account = value
    
    @property
    def correspondent_account(self) -> int:
        return self.__correspondent_account
    
    @correspondent_account.setter
    def correspondent_account(self, value:int):
        if value > 0 and len(str(value)) == 11:
            self.__correspondent_account = value
    
    @property
    def bik(self) -> int:
        return self.__bik

    @bik.setter
    def bik(self, value:int):
        if value > 0 and len(str(value)) == 9:
            self.__bik = value