from Src.Models.settings_model import settings_model
from Src.Core.validator import argument_exception
from Src.Core.validator import validator
from Src.Models.company_model import company_model

import json, os

class settings_manager:

    """
    Загрузчик и держатель конфигурации приложения. Реализован как Singleton.

    Ответственность:
        - Хранит путь к файлу конфигурации.
        - Загружает JSON из файла конфигурации и мапит его в объекты settings_model и company_model.
        - Предоставляет доступ к текущим настройкам приложения через методы.
        - Обеспечивает хранение настроек в единственном экземпляре (Singleton).

    Ограничения:
        - В случае ошибок при загрузке настроек, оставляет настройки по умолчанию.
        - Предполагает, что файл конфигурации содержит секции настроек для company и других 
          глобальных атрибутов settings_model.

    """

    __config_namefile: str = ""  # Путь к файлу конфигурации.
    __settings: settings_model = None  # Объект settings_model, хранящий конфигурацию.
    __global_attributes: list = ["company", "response_format", "first_start"]  # Список глобальных атрибутов settings_model.
    __settings_dict: list = ["company"] # Список атрибутов settings_model, которые нужно конвертировать из словаря

    def __init__(self, config_filename: str):
        """
        Конструктор класса.  Инициализирует менеджер настроек с указанным именем файла конфигурации.
        Сохраняет относительный путь к файлу и загружает настройки по умолчанию.

        Аргументы:
            config_filename (str): Имя файла конфигурации.
        """
        self.__config_namefile = os.path.relpath(config_filename)
        self.default() # Загрузка настроек по умолчанию

    def __new__(cls, *args, **kwargs):
        """
        Реализация Singleton паттерна.  Гарантирует, что у класса будет только один экземпляр.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    @property
    def config_namefile(self) -> str:
        """
        Возвращает путь к файлу конфигурации.

        Возвращает:
            str: Путь к файлу конфигурации.
        """
        return self.__config_namefile

    @config_namefile.setter
    def config_namefile(self, value: str):
        """
        Устанавливает путь к файлу конфигурации.

        Аргументы:
            value (str): Новый путь к файлу конфигурации.

        Проверяет, что переданное значение является строкой, и что файл существует.
        В противном случае выбрасывает исключение argument_exception.
        """
        validator.validate(value, str)
        abs_path = os.path.abspath(value)
        if os.path.exists(abs_path):
            self.__config_namefile = abs_path.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {abs_path}')

    def settings(self) -> settings_model:
        """
        Возвращает текущие настройки приложения (объект settings_model).

        Возвращает:
            settings_model: Объект settings_model, содержащий текущие настройки.
        """
        return self.__settings

    def company_settings(self) -> company_model:
        """
        Удобный аксессор: возвращает settings.company.

        Возвращает:
            company_model: Объект company_model, содержащий настройки компании.
        """
        return self.__settings.company

    def is_first_start(self) -> bool:
        """
        Проверяет, является ли это первым запуском приложения.

        Возвращает:
            bool: True если первый запуск, иначе False
        """
        return getattr(self.__settings, 'first_start', True)

    def set_first_start_completed(self):
        """
        Устанавливает флаг первого запуска в False и сохраняет настройки.
        """
        self.__settings.first_start = False
        self.save_settings()

    def convert_to_settings(self, load_result: dict, key: str) -> bool:
        """
        Преобразует загруженный словарь в экземпляры доменных моделей (company_model).

        Аргументы:
            load_result (dict): Загруженный словарь настроек.
            key (str): Ключ, под которым находятся настройки компании в словаре.

        Возвращает:
            bool: True при успешном маппинге; False, если структура некорректна (не хватает полей).
        """

        load_result = load_result[key]

        fields = ["name", "type_of_property", "inn", "bank_account", "correspondent_account", "bik"]
        if not all(field in load_result for field in fields):
            return False

        self.__settings.company = company_model()

        for field in fields:
            setattr(self.__settings.company, field, load_result[field]) # Установка атрибутов company_model из словаря
        return True

    def load_settings(self) -> bool:
        """
        Загружает настройки из JSON-файла, обновляя внутреннее состояние.

        Возвращает:
            bool: True - если загрузка успешна и структура корректна, иначе False.

        Обрабатывает исключения при открытии и чтении файла. Проверяет, что в файле
        присутствуют все необходимые глобальные атрибуты.  Использует convert_to_settings
        для маппинга настроек компании в объект company_model.
        """

        if self.config_namefile.strip() == "":
            raise Exception("Не найден файл настроек!")
        try:
            with open(self.config_namefile,'r') as file:
                data = json.load(file)
                for key in self.__global_attributes:
                    if key not in data.keys():
                        return False

                self.__settings = settings_model()

                for key in self.__global_attributes:
                    if key in self.__settings_dict:
                        if not self.convert_to_settings(data, key):
                            return False # Ошибка конвертации настроек компании
                    else:
                        setattr(self.__settings, key, data[key])
            return True
        except Exception as e:
            print(f"Ошибка при загрузке настроек: {e}") # Logging ошибки
            return False

    def save_settings(self):
        """
        Сохраняет текущие настройки в файл конфигурации.
        """
        try:
            settings_dict = {}
            
            # Сохраняем настройки компании
            settings_dict["company"] = {
                "name": self.__settings.company.name,
                "type_of_property": self.__settings.company.type_of_property,
                "inn": self.__settings.company.inn,
                "bank_account": self.__settings.company.bank_account,
                "correspondent_account": self.__settings.company.correspondent_account,
                "bik": self.__settings.company.bik
            }
            
            # Сохраняем остальные глобальные атрибуты
            for attr in self.__global_attributes:
                if attr != "company" and hasattr(self.__settings, attr):
                    settings_dict[attr] = getattr(self.__settings, attr)
            
            with open(self.config_namefile, 'w', encoding='utf-8') as file:
                json.dump(settings_dict, file, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Ошибка при сохранении настроек: {e}")

    def default(self):
        """
        Устанавливает настройки по умолчанию.  Используется при инициализации и в случае ошибок загрузки.
        Создает объекты settings_model и company_model и заполняет их значениями по умолчанию.
        """
        self.__settings = settings_model()
        self.__settings.company = company_model()
        self.__settings.company.name = "Название компании"
        self.__settings.company.type_of_property = "ОООАА"
        self.__settings.company.inn = 0
        self.__settings.company.bank_account = 0
        self.__settings.company.correspondent_account = 0
        self.__settings.company.bik = 0
        self.__settings.response_format = "json"
        self.__settings.first_start = True