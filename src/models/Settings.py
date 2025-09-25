from src.models.CompanyModel import CompanyModel

class Settings:
    def __init__(self):
        self.__company = CompanyModel()

    @property
    def company(self) -> str:
        return self.__company
    
    @company.setter
    def company(self, value: CompanyModel):
        if isinstance(value, CompanyModel):
            self.__company = value