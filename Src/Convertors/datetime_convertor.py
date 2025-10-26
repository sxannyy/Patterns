from Src.Core.abstract_convertor import abstract_convertor
from datetime import datetime, date, time
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

        if not self.can_convert(obj):
            return {'value': obj, 'type': 'other'}
        
        return self.__convert_datetime(obj)

    def can_convert(self, obj: Any) -> bool:

        """ Проверяет, является ли объект datetime типом """

        return isinstance(obj, (datetime, date, time))

    def __convert_datetime(self, dt_obj: Any) -> Dict[str, Any]:

        """ Преобразует datetime объект в словарь """
        if isinstance(dt_obj, datetime):
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
        elif isinstance(dt_obj, date):
            return {
                'type': 'date', 
                'year': dt_obj.year,
                'month': dt_obj.month,
                'day': dt_obj.day,
                'iso_format': dt_obj.isoformat()
            }
        elif isinstance(dt_obj, time):
            return {
                'type': 'time',
                'hour': dt_obj.hour,
                'minute': dt_obj.minute, 
                'second': dt_obj.second,
                'iso_format': dt_obj.isoformat()
            }