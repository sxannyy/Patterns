from abc import ABC, abstractmethod
from typing import Any, Dict

class abstract_convertor(ABC):

    """
    Абстрактный класс для преобразования объектов различных типов в словари.
    Каждая конкретная реализация отвечает за преобразование определенного типа данных.
    """
    
    @abstractmethod
    def convert(self, obj: Any) -> Dict[str, Any]:

        """
        Преобразует объект в словарь формата {ключ: значение}
        Аргументы:
            obj: Любой объект для преобразования
        Возвращает:
            Dict[str, Any]: Словарь с данными объекта
        """

        pass
    
    @abstractmethod
    def can_convert(self, obj: Any) -> bool:

        """
        Проверяет, может ли конвертер обработать данный тип объекта
        Аргументы:
            obj: Объект для проверки
        Возвращает:
            bool: True если конвертер может обработать данный тип
        """
        pass