from Src.Models.company_model import company_model
from Src.Core.validator import validator

class settings_model:

    """
    Контейнер настроек приложения.

    Свойства:
        company (company_model): Настройки организации.
    """

    company: company_model = None

    @property
    def company(self) -> company_model:
        """ Модель организации, полученная из конфигурации """
        return self.__company
    
    @company.setter
    def company(self, value: company_model):
        """ Задаёт модель организации; проверяет тип через validator """
        validator.validate(value, company_model)
        self.__company = value