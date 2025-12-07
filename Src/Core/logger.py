import os
from datetime import datetime

from Src.Core.abstract_logic import abstract_logic
from Src.Core.event_type import event_type
from Src.Core.observe_service import observe_service
from Src.Dto.log_event_dto import log_event_dto
from Src.Models.settings_model import settings_model

"""
Класс для логирования событий приложения.
Поддерживает фильтрацию по минимальному уровню,
а также вывод в консоль и (опционально) запись в файл.

Работает как наблюдатель: регистрируется в observe_service
и реагирует на события логирования, приходящие из системы событий.
"""

class logger(abstract_logic):
    """ 
    Реализация логики логирования.

    Наследуется от abstract_logic и подписывается на события через observe_service.
    Обрабатывает события типов debug/info/warning/error и пишет их:
        - в консоль
        - в файл (если включено в настройках)

    Настройки:
        min_log_level (str): минимальный уровень логирования (DEBUG/INFO/WARNING/ERROR)
        log_to_file (bool): включить запись в файл
        log_file_path (str): путь к файлу логов
    """

    """ 
    Шкала уровней логирования.
    Используется для сравнения при фильтрации по минимальному уровню.
    """
    LEVELS = {
        "DEBUG": 1,
        "INFO": 2,
        "WARNING": 3,
        "ERROR": 4,
    }

    """ 
    Карта соответствия событий уровню логирования.

    Поддерживает два варианта ключей:
        1) значения, возвращаемые event_type.*_log()
        2) прямые строковые названия уровня ("DEBUG", "INFO", ...)
    """
    EVENT_LEVEL_MAP = {
        event_type.debug_log(): "DEBUG",
        event_type.info_log(): "INFO",
        event_type.warning_log(): "WARNING",
        event_type.error_log(): "ERROR",
        "DEBUG": "DEBUG",
        "INFO": "INFO",
        "WARNING": "WARNING",
        "ERROR": "ERROR",
    }

    def __init__(self, settings: settings_model):
        """ 
        Инициализация логгера.

        Регистрирует экземпляр в observe_service и читает настройки:
            - минимальный уровень логирования
            - необходимость записи в файл
            - путь к файлу логов

        Аргументы:
            settings (settings_model): модель настроек приложения

        Примечания:
            Метод использует безопасное чтение полей через getattr,
            чтобы избежать ошибок при отсутствии атрибутов в settings.
        """
        super().__init__()
        observe_service.add(self)

        # Защита от отсутствующих полей/пустых значений в настройках
        level_name = (getattr(settings, "min_log_level", "") or "INFO").upper()
        self.__min_level = self.LEVELS.get(level_name, self.LEVELS["INFO"])

        self.__log_to_file = bool(getattr(settings, "log_to_file", False))
        self.__log_file_path = getattr(settings, "log_file_path", "") if self.__log_to_file else ""

        if self.__log_to_file and self.__log_file_path:
            self.__ensure_log_path()
            self.__initialize_log_file()

    def __ensure_log_path(self):
        """ 
        Обеспечивает наличие директории для файла логов.

        Если в log_file_path указан путь с директорией,
        то директория будет создана при отсутствии.
        """
        # Создаем директорию, если указана
        directory = os.path.dirname(self.__log_file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def __initialize_log_file(self):
        """ 
        Инициализирует файл логов.

        Добавляет в конец файла разделитель с отметкой времени
        старта логирования текущего запуска приложения.
        """
        with open(self.__log_file_path, "a", encoding="utf-8") as file:
            file.write(f"\n=== Logging started at {datetime.now().isoformat()} ===\n")

    def handle(self, event: str, params):
        """ 
        Обрабатывает входящее событие логирования.

        Определяет уровень события, формирует итоговое сообщение
        и, при необходимости, передает его в общий метод записи.

        Аргументы:
            event (str): тип события
            params: объект параметров события (ожидается наличие полей:
                - message
                - data
                - exception)

        Примечания:
            Если событие не относится к логируемым, метод завершится без действий.
            Фильтрация выполняется по шкале LEVELS и значению __min_level.
        """
        super().handle(event, params)

        level_name = self.EVENT_LEVEL_MAP.get(event)
        if not level_name:
            return

        message = getattr(params, "message", "No message provided")
        data = getattr(params, "data", None) or {}
        exc = getattr(params, "exception", None)

        full_message = message
        if data:
            full_message += f" | data={data}"
        if exc:
            full_message += f" | exception={exc}"

        level_value = self.LEVELS[level_name]
        if level_value >= self.__min_level:
            self.__log(level_name, full_message)

    def __log(self, level: str, message: str):
        """ 
        Выполняет непосредственную запись лога.

        Формирует строку с timestamp и уровнем,
        затем:
            - пишет в файл (если включено)
            - выводит в консоль

        Аргументы:
            level (str): уровень логирования (DEBUG/INFO/WARNING/ERROR)
            message (str): итоговое сообщение лога
        """
        timestamp = datetime.now().isoformat()
        log_message = f"[{timestamp}] {level}: {message}"

        if self.__log_to_file and self.__log_file_path:
            with open(self.__log_file_path, "a", encoding="utf-8") as file:
                file.write(log_message + "\n")

        print(log_message)