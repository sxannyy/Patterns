from Src.Models.company_model import company_model
from Src.Core.validator import validator

class settings_model:
    company: company_model = None

    @property
    def company(self) -> company_model:
        return self.__company
    
    @company.setter
    def company(self, value: company_model):
        validator.validate(value, company_model)
        self.__company = value