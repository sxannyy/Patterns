from src.models.CompanyModel import CompanyModel
from src.models.Settings import Settings

import json, os

class SettingsManager:
    __config_namefile:str = ""
    __settings:Settings = None
    __load_result:dict

    def __init__(self, config_filename:str):
        self.__config_namefile = os.path.relpath(config_filename)
        print(self.__config_namefile)
        self.default()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SettingsManager, cls).__new__(cls)
        return cls.instance

    @property
    def config_namefile(self) -> str:
        return self.__config_namefile
    
    @config_namefile.setter
    def config_namefile(self, value:str):
        value = value.strip()
        if value == "":
            return
        abs_path = os.path.abspath(value)
        if os.path.exists(abs_path):
            self.__config_namefile = abs_path

    def settings(self)-> Settings:
        return self.__settings
    
    def company_settings(self) -> CompanyModel:
        return self.__settings.company
    
    def convert_to_settings(self) -> bool:
        fields = ["name", "type_of_property", "inn", "bank_account", "correspondent_account", "bik"]
        for i in fields:
            if i not in self.__load_result.keys():
                return False
        self.__settings.company.name = self.__load_result['name']
        self.__settings.company.type_of_property = self.__load_result["type_of_property"]
        self.__settings.company.inn = self.__load_result['inn']
        self.__settings.company.bank_account = self.__load_result['bank_account']
        self.__settings.company.correspondent_account = self.__load_result['correspondent_account']
        self.__settings.company.bik = self.__load_result['bik']
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
        self.__settings = Settings()
        self.__settings.company = CompanyModel()
        self.__settings.company.name = "Название компании"
        self.__settings.company.type_of_property= "ОООАА"
        self.__settings.company.inn=0
        self.__settings.company.bank_account=0
        self.__settings.company.correspondent_account=0
        self.__settings.company.bik=0