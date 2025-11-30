from abc import ABC
from Src.Core.validator import validator, operation_exception
from Src.Core.event_type import event_type

"""
Абстрактный класс для обработки логики приложения.
Предоставляет базовую функциональность для обработки ошибок и событий.
"""

class abstract_logic(ABC):
    __error_text:str = ""

    """ 
    Текст ошибки, возникшей в процессе работы логики.
    Свойство:
        str: Текст ошибки в отформатированном виде (без пробелов по краям)
    """
    @property
    def error_text(self) -> str:
        return  self.__error_text.strip()
    
    @error_text.setter
    def error_text(self, message: str):
        """ 
        Устанавливает текст ошибки с валидацией типа данных.
        Аргументы:
            message (str): Текст сообщения об ошибке
        """
        validator.validate(message, str)
        self.__error_text = message.strip()

    """ 
    Флаг наличия ошибки в логике.
    Свойство:
        bool: True если есть текст ошибки, иначе False
    """
    @property
    def is_error(self) -> bool:
        return self.error_text != ""

    def _inner_set_exception(self, ex: Exception):
        """ 
        Внутренний метод для установки текста исключения.
        Аргументы:
            ex (Exception): Исключение для обработки
        """
        self.__error_text = f"Ошибка! Исключение {ex}"

    """ 
    Устанавливает текст ошибки на основе перехваченного исключения.
    Аргументы:
        ex (Exception): Исключение для обработки
    """
    def set_exception(self, ex: Exception):
        self.__error_text = f"Ошибка! Исключение {ex}"

    """ 
    Обрабатывает событие с проверкой его валидности.
    Аргументы:
        event (str): Тип события для обработки
        params: Параметры события
    Исключения:
        operation_exception: Если событие не найдено в списке допустимых событий
    """
    def handle(self,  event: str, params):
        validator.validate(event, str)
        events =  event_type.events()
        if event not in events:
            raise operation_exception(f"{events} - не является событием!")