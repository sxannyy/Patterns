from Src.Core.abstract_convertor import abstract_convertor
from datetime import time
from typing import Any, Dict

class time_convertor(abstract_convertor):

    """
    Конвертер для работы c временем.
    Обрабатывает time объекты.
    """

    def convert(self, obj: Any) -> Dict[str, Any]:

        """
        Преобразует time объекты в словарь.
        Аргументы:
            obj: Объект для преобразования
        Возвращает:
            Dict[str, Any]: Словарь с данными time объекта
        """

        if not self.__can_convert(obj):
            return {'value': obj, 'type': 'other'}
        
        return self.__convert_time(obj)
    
    def __can_convert(self, obj: Any) -> bool:

        """ Проверяет, является ли объект time типом """

        return isinstance(obj, time)

    def __convert_time(self, dt_obj: Any) -> Dict[str, time]:
        
        if isinstance(dt_obj, time):
            return {
                'type': 'time',
                'hour': dt_obj.hour,
                'minute': dt_obj.minute, 
                'second': dt_obj.second,
                'iso_format': dt_obj.isoformat()
            }