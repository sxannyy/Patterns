from abc import ABC
import uuid
from Src.Core.validator import validator

# Исключение, когда класс не является абстрактным
class not_abstract_exception(Exception):
    pass

class abstract_model(ABC):

    """
    Базовая доменная модель с уникальным идентификатором и именем.

    Свойства:
        unique_code (str): Уникальный GUID-код модели.
        name (str): Отображаемое имя (не больше 50 симв).

    Особенности:
        - Переопределенно сравнение (__eq__) по unique_code для любых подклассов.
        - Генерация not_abstract_exception при сравнении с объектом иного базового класса.
    """

    __unique_code:str
    __name:str

    def __init__(self, name:str = "") -> None:
        super().__init__()
        self.__unique_code = uuid.uuid4().hex
        self.__name = name

    # Уникальный код
    @property
    def unique_code(self) -> str:
        """ Уникальный код доменной модели """
        return self.__unique_code
    
    @unique_code.setter
    def unique_code(self, value: str):
        """ Устанавливает уникальный код. Ожидается непустая строка """
        validator.validate(value, str)
        self.__unique_code = value.strip()

    # Наименование
    @property
    def name(self) -> str:
        """ Имя объекта """
        return self.__name
    
    @name.setter
    def name(self, value: str):
        """ Имя объекта, проверка на 50 символов и проверка на тип """
        validator.validate(value, str, 50)
        self.__name = value.strip()

    # Перегрузка штатного варианта сравнения
    def __eq__(self, value) -> bool:
        if not isinstance(value, abstract_model):
            raise not_abstract_exception("Ваш класс не является абстрактным!")
        return self.__unique_code == value.unique_code
