from Src.Models.settings_model import settings_model
from Src.Core.validator import argument_exception
from Src.Core.validator import operation_exception
from Src.Core.validator import validator
from Src.Models.company_model import company_model

import json, os

class settings_manager:
    __config_namefile:str = ""
    __settings:settings_model = None
    __load_result:dict

    def __init__(self, config_filename:str):
        self.__config_namefile = os.path.relpath(config_filename)
        self.default()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    @property
    def config_namefile(self) -> str:
        return self.__config_namefile
    
    @config_namefile.setter
    def config_namefile(self, value:str):
        validator.validate(value, str)
        abs_path = os.path.abspath(value)
        if os.path.exists(abs_path):
            self.__config_namefile = abs_path.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {abs_path}')

    def settings(self)-> settings_model:
        return self.__settings
    
    def company_settings(self) -> company_model:
        return self.__settings.company
    
    def convert_to_settings(self) -> bool:
        fields = ["name", "type_of_property", "inn", "bank_account", "correspondent_account", "bik"]
        if not all(field in self.__load_result for field in fields):
            return False
        for field in fields:
            setattr(self.__settings.company, field, self.__load_result[field])
        return True

    def load_settings(self) -> bool:
        if self.config_namefile.strip() == "":
            raise Exception("Не найден файл настроек!")
        try:
            with open(self.config_namefile,'r') as file:
                data = json.load(file)
                if "company" in data:
                    self.__load_result = data["company"]
                    return self.convert_to_settings()
                return False
        except:
            return False
    
    def default(self):
        self.__settings = settings_model()
        self.__settings.company = company_model()
        self.__settings.company.name = "Название компании"
        self.__settings.company.type_of_property= "ОООАА"
        self.__settings.company.inn=0
        self.__settings.company.bank_account=0
        self.__settings.company.correspondent_account=0
        self.__settings.company.bik=0