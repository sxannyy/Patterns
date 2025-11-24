from datetime import datetime
from Src.Models.company_model import company_model
from Src.Core.validator import validator

class settings_model:

    """
    Контейнер настроек приложения. 

    Этот класс предназначен для хранения и управления настройками всего приложения.
    Он содержит настройки организации (информация о компании, используемой в приложении),
    формат ответа (например, JSON, XML), используемый приложением,
    проверку на первый запуск системы и настроек,
    фиксированную дату блокировки.

    Свойства:
        company (company_model): Настройки организации.  Содержит информацию, относящуюся к компании,
                                        использующей приложение, такую как название, адрес и т.д.
        response_format (str): Формат ответа API, используемый приложением.
        first_start (bool): Проверка на первый запуск системы.
        block_date (str): Дата блокировки.
    """

    __company: company_model = None
    __response_format: str = ""
    __first_start: bool = False
    __block_date: str = ""

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

    @property
    def first_start(self) -> bool:
        """
        Возвращает проверку настроек и первого запуска сервиса.
        """
        return self.__first_start

    @first_start.setter
    def first_start(self, value: bool):
        """
        Устанавливает проверку настроек и первого запуска сервиса.
        Проверяет тип входного значения, используя validator, чтобы убедиться, что оно является булевым.
        """
        validator.validate(value, bool)
        self.__first_start = value

    @property
    def block_date(self) -> datetime | None:
        """Текущая дата блокировки, либо None, если не задана."""
        if not self.__block_date:
            return None
        return datetime.strptime(self.__block_date, "%Y-%m-%d")

    @block_date.setter
    def block_date(self, value: datetime | str | None):
        """Устанавливает дату блокировки в формате YYYY-MM-DD."""
        if value is None:
            self.__block_date = ""
            return

        if isinstance(value, datetime):
            self.__block_date = value.strftime("%Y-%m-%d")
            return

        validator.validate(value, str)
        datetime.strptime(value, "%Y-%m-%d")
        self.__block_date = value