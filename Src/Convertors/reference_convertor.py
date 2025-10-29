from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.abstract_model import abstract_model
from Src.Core.abstract_dto import abstract_dto
from typing import Any

class reference_convertor(abstract_convertor):

    """
    Конвертер для работы c моделями и DTO.
    Обрабатывает объекты, наследованные от abstract_model и abstract_dto.
    """

    def convert(self, obj: Any) -> abstract_dto:

        """
        Преобразует объекты моделей в DTO.
        Аргументы:
            obj: Объект для преобразования
        Возвращает:
            Объект DTO
        """

        if not self.__can_convert(obj):
            return {'value': obj, 'type': 'unconvertible'}
        
        if isinstance(obj, abstract_dto):
            return obj
        
        return obj.to_dto()

    def __can_convert(self, obj: Any) -> bool:

        """ Проверяет, является ли объект моделью или DTO """
        return isinstance(obj, (abstract_model, abstract_dto))

