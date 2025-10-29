from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.abstract_model import abstract_model
from Src.Core.abstract_dto import abstract_dto
from Src.Core.common import common
from typing import Any, Dict

class reference_convertor(abstract_convertor):

    """
    Конвертер для работы со ссылочными типами (модели и DTO).
    Обрабатывает объекты, наследованные от abstract_model и abstract_dto.
    """

    def convert(self, obj: Any) -> Dict[str, Any]:

        """
        Преобразует ссылочные объекты в словарь.
        Аргументы:
            obj: Объект для преобразования
        Возвращает:
            Dict[str, Any]: Словарь с данными объекта
        """

        if not self.__can_convert(obj):
            return {'value': obj, 'type': 'unconvertible'}
        
        return obj.to_dto()

    def __can_convert(self, obj: Any) -> bool:

        """ Проверяет, является ли объект ссылочным типом """
        return (isinstance(obj, (abstract_model, abstract_dto)) or 
                (hasattr(obj, '__dict__') and not isinstance(obj, type)))

