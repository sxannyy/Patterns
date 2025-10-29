from Src.Core.abstract_convertor import abstract_convertor
from typing import Any

class basic_convertor(abstract_convertor):

    """
    Конвертер для преобразования простых типов данных (numeric, string) в словарь.
    Обрабатывает только: str, int, float, bool, None.
    Не обрабатывает списки, словари, объекты - только обычные типы.
    """
    
    def convert(self, obj: Any) -> str|int|float|bool|None:

        """
        Преобразует простые типы данных в словарь.
        Аргументы:
            obj: Объект для преобразования (простой тип)
        Ошибки:
            ValueError: Если объект не является простым типом
        """

        if not self.__can_convert(obj):
            raise ValueError(f"Basic_convertor не может обработать тип: {type(obj)}")
        
        return obj
    
    def __can_convert(self, obj: Any) -> bool:

        """
        Проверяет, может ли конвертер обработать данный объект.
        Basic convertor обрабатывает только простые типы.
        """

        return isinstance(obj, (str, int, float, bool, type(None)))