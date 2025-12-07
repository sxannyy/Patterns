from datetime import datetime

from Src.Models.company_model import company_model
from Src.Core.validator import validator
from Src.Core.validator import validator, argument_exception
from Src.Core.observe_service import observe_service
from Src.Core.event_type import event_type
from Src.Dto.log_event_dto import log_event_dto

"""
Модель настроек приложения.

Класс выступает контейнером конфигурационных параметров системы.
Содержит бизнес-настройки (организация, формат ответа, даты),
а также настройки логирования.

Также умеет эмитить события логирования через observe_service
при изменении ключевых параметров.
"""

class settings_model:

    """
    Контейнер настроек приложения. 

    Этот класс предназначен для хранения и управления настройками всего приложения.
    Он содержит настройки организации (информация о компании, используемой в приложении),
    формат ответа (например, JSON, XML), используемый приложением,
    проверку на первый запуск системы и настроек,
    фиксированную дату блокировки.

    Свойства:
        company (company_model): Настройки организации. Содержит информацию,
                                 относящуюся к компании, использующей приложение.
        response_format (str): Формат ответа API, используемый приложением.
        first_start (bool): Проверка на первый запуск системы.
        block_date (str): Дата блокировки.
        min_log_level (str): Минимальный уровень логирования.
        log_to_file (bool): Нужно ли записывать логи в файл.
        log_file_path (str): Путь к файлу с логами.
    """

    __company: company_model = None
    __response_format: str = ""
    __first_start: bool = False
    __block_date: str = ""

    __min_log_level: str = "INFO"
    __log_to_file: bool = False
    __log_file_path: str = ""

    """ 
    Настройки организации.
    Свойство:
        company_model: Модель организации, полученная из конфигурации.
                       Если не установлена, возвращает None.
    """
    @property
    def company(self) -> company_model:
        """ 
        Модель организации, полученная из конфигурации.

        Возвращает:
            company_model: Текущую модель организации. Если модель не установлена, вернет None.
        """
        return self.__company

    @company.setter
    def company(self, value: company_model):
        """ 
        Задаёт модель организации.

        Аргументы:
            value (company_model): Модель организации для установки.

        Проверяет тип входного значения, используя validator, чтобы убедиться,
        что оно является экземпляром company_model.

        Исключения:
            Exception: Пробрасывает исключение в случае ошибки валидации/установки.
        """
        try:
            validator.validate(value, company_model)
            self.__company = value
            self.__log_info("Company settings set/updated.")
        except Exception as e:
            self.__log_error("Error setting company.", e)
            raise

    """ 
    Формат ответа API.
    Свойство:
        str: Текущий формат ответа (например, JSON, XML).
             Если не установлен, возвращает пустую строку.
    """
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

        Проверяет тип входного значения, используя validator, чтобы убедиться,
        что оно является строкой.

        Исключения:
            Exception: Пробрасывает исключение в случае ошибки валидации/установки.
        """
        try:
            validator.validate(value, str)
            self.__response_format = value
            self.__log_info(f"Response format set to: {value}")
        except Exception as e:
            self.__log_error("Error setting response_format.", e)
            raise

    """ 
    Флаг первого запуска.
    Свойство:
        bool: True если это первый запуск системы/настроек, иначе False.
    """
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

        Аргументы:
            value (bool): Значение флага первого запуска.

        Проверяет тип входного значения, используя validator.

        Исключения:
            Exception: Пробрасывает исключение в случае ошибки валидации/установки.
        """
        try:
            validator.validate(value, bool)
            self.__first_start = value
            self.__log_info(f"First start set to: {value}")
        except Exception as e:
            self.__log_error("Error setting first_start.", e)
            raise

    """ 
    Дата блокировки.
    Свойство:
        datetime | None: Дата блокировки. Возвращает None, если дата не задана.
    
    Примечания:
        Внутреннее хранение осуществляется строкой формата YYYY-MM-DD.
    """
    @property
    def block_date(self) -> datetime | None:
        """Текущая дата блокировки, либо None, если не задана."""
        if not self.__block_date:
            return None
        return datetime.strptime(self.__block_date, "%Y-%m-%d")

    @block_date.setter
    def block_date(self, value: datetime | str | None):
        """ 
        Устанавливает дату блокировки.

        Аргументы:
            value (datetime | str | None): 
                - datetime: будет преобразован в строку YYYY-MM-DD
                - str: ожидается формат YYYY-MM-DD
                - None: очистка даты блокировки

        Исключения:
            Exception: Пробрасывает исключение при неверном типе или формате даты.
        """
        try:
            if value is None:
                self.__block_date = ""
                self.__log_info("Block date cleared.")
                return

            if isinstance(value, datetime):
                self.__block_date = value.strftime("%Y-%m-%d")
                self.__log_info(f"Block date set to: {self.__block_date}")
                return

            validator.validate(value, str)
            # Проверяем формат
            datetime.strptime(value, "%Y-%m-%d")
            self.__block_date = value
            self.__log_info(f"Block date set to: {value}")

        except Exception as e:
            self.__log_error("Error setting block_date.", e)
            raise

    """ 
    Минимальный уровень логирования.
    Свойство:
        str: Один из уровней: DEBUG, INFO, WARNING, ERROR.
    """
    @property
    def min_log_level(self) -> str:
        return self.__min_log_level

    @min_log_level.setter
    def min_log_level(self, value: str):
        """ 
        Устанавливает минимальный уровень логирования.

        Аргументы:
            value (str): Название уровня.

        Проверяет:
            - тип значения
            - принадлежность к допустимым уровням

        Исключения:
            argument_exception: Если уровень не входит в список допустимых.
            Exception: Прочие ошибки валидации.
        """
        try:
            validator.validate(value, str)
            level = value.upper().strip()

            allowed = {"DEBUG", "INFO", "WARNING", "ERROR"}
            if level not in allowed:
                raise argument_exception(
                    f"min_log_level должен быть одним из {sorted(allowed)}"
                )

            self.__min_log_level = level
            self.__log_info(f"Min log level set to: {level}")

        except Exception as e:
            self.__log_error("Error setting min_log_level.", e)
            raise

    """ 
    Флаг записи логов в файл.
    Свойство:
        bool: True если запись в файл включена, иначе False.
    """
    @property
    def log_to_file(self) -> bool:
        return self.__log_to_file

    @log_to_file.setter
    def log_to_file(self, value: bool):
        """ 
        Включает или отключает запись логов в файл.

        Аргументы:
            value (bool): Флаг записи в файл.

        Исключения:
            Exception: Пробрасывает исключение при ошибке валидации.
        """
        try:
            validator.validate(value, bool)
            self.__log_to_file = value
            self.__log_info(f"Log to file set to: {value}")
        except Exception as e:
            self.__log_error("Error setting log_to_file.", e)
            raise

    """ 
    Путь к файлу логов.
    Свойство:
        str: Путь к файлу, в который будет вестись логирование (если включено).
    """
    @property
    def log_file_path(self) -> str:
        return self.__log_file_path

    @log_file_path.setter
    def log_file_path(self, value: str):
        """ 
        Устанавливает путь к файлу логов.

        Аргументы:
            value (str): Путь к файлу.

        Исключения:
            Exception: Пробрасывает исключение при ошибке валидации.
        """
        try:
            validator.validate(value, str)
            self.__log_file_path = value
            self.__log_info(f"Log file path set to: {value}")
        except Exception as e:
            self.__log_error("Error setting log_file_path.", e)
            raise

    """ 
    Создает и отправляет событие логирования через observe_service.

    Аргументы:
        event (str): Тип события логирования (event_type.*_log()).
        message (str): Текст сообщения.
        exc (Exception, optional): Исключение, связанное с событием.
        data (dict, optional): Дополнительные данные для контекста.

    Примечания:
        Для передачи параметров используется log_event_dto.
        Исключение сериализуется в строку, чтобы избежать проблем
        при дальнейшем логировании/выводе.
    """
    def __emit_log(self, event: str, message: str, exc: Exception = None, data: dict = None):
        dto = log_event_dto()
        dto.message = message
        dto.data = data or {}
        if exc is not None:
            dto.exception = str(exc)

        observe_service.create_event(event, dto)

    """ 
    Утилитарный метод для логирования информационных сообщений.
    
    Аргументы:
        message (str): Текст сообщения.
        data (dict, optional): Дополнительные данные.
    """
    def __log_info(self, message: str, data: dict = None):
        self.__emit_log(event_type.info_log(), message, data=data)

    """ 
    Утилитарный метод для логирования предупреждений.
    
    Аргументы:
        message (str): Текст сообщения.
        data (dict, optional): Дополнительные данные.
    """
    def __log_warning(self, message: str, data: dict = None):
        self.__emit_log(event_type.warning_log(), message, data=data)

    """ 
    Утилитарный метод для логирования ошибок.
    
    Аргументы:
        message (str): Текст сообщения.
        exc (Exception, optional): Исключение.
        data (dict, optional): Дополнительные данные.
    """
    def __log_error(self, message: str, exc: Exception = None, data: dict = None):
        self.__emit_log(event_type.error_log(), message, exc=exc, data=data)