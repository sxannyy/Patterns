from Src.Models.company_model import company_model
from Src.Core.validator import validator

class settings_model:

    """
    Контейнер настроек приложения. 

    Этот класс предназначен для хранения и управления настройками всего приложения.
    Он содержит настройки организации (информация о компании, используемой в приложении)
    и формат ответа (например, JSON, XML), используемый приложением.

    Свойства:
        company (company_model): Настройки организации.  Содержит информацию, относящуюся к компании,
                                        использующей приложение, такую как название, адрес и т.д.
        response_format (str): Формат ответа API, используемый приложением.

    """

    __company: company_model = None
    __response_format: str = ""

    @property
    def company(self) -> company_model:
        """ 
        Модель организации, полученная из конфигурации.

        Возвращает:
            company_model: Текущую модель организации.  Если модель не установлена, вернет None.
        """
        return self.__company

    @company.setter
    def company(self, value: company_model):
        """ 
        Задаёт модель организации.

        Аргументы:
            value (company_model): Модель организации для установки.

        Проверяет тип входного значения, используя validator, чтобы убедиться, что оно является
        экземпляром company_model.
        """
        validator.validate(value, company_model)
        self.__company = value

    @property
    def response_format(self) -> str:
        """
        Возвращает формат ответа API.

        Возвращает:
            str: Текущий формат ответа. Если формат не установлен, вернет пустую строку.
        """
        return self.__response_format

    @response_format.setter
    def response_format(self, value: str):
        """
        Устанавливает формат ответа API.

        Аргументы:
            value (str): Формат ответа для установки.

        Проверяет тип входного значения, используя validator, чтобы убедиться, что оно является строкой.
        """
        validator.validate(value, str)
        self.__response_format = value
