from Src.Core.abstract_convertor import abstract_convertor
from datetime import datetime
from typing import Any, Dict

class datetime_convertor(abstract_convertor):

    """
    Конвертер для работы с датами и временем.
    Обрабатывает datetime, date, time объекты.
    """

    def convert(self, obj: Any) -> Dict[str, Any]:

        """
        Преобразует datetime объекты в словарь.
        Аргументы:
            obj: Объект для преобразования
        Возвращает:
            Dict[str, Any]: Словарь с данными datetime объекта
        """

        if not self.__can_convert(obj):
            return {'value': obj, 'type': 'other'}
        
        return self.__convert_datetime(obj)

    def __can_convert(self, obj: Any) -> bool:

        """ Проверяет, является ли объект datetime типом """

        return isinstance(obj, datetime)

    def __convert_datetime(self, dt_obj: Any) -> Dict[str, datetime]:

        """ Преобразует datetime объект в словарь """
        return {
            'type': 'datetime',
            'year': dt_obj.year,
            'month': dt_obj.month,
            'day': dt_obj.day,
            'hour': dt_obj.hour,
            'minute': dt_obj.minute,
            'second': dt_obj.second,
            'iso_format': dt_obj.isoformat()
        }