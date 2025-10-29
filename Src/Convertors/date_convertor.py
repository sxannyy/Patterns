from Src.Core.abstract_convertor import abstract_convertor
from datetime import datetime, date, time
from typing import Any, Dict

class date_convertor(abstract_convertor):

    """
    Конвертер для работы с датами.
    Обрабатывает date объекты.
    """

    def convert(self, obj: Any) -> Dict[str, Any]:

        """
        Преобразует date объекты в словарь.
        Аргументы:
            obj: Объект для преобразования
        Возвращает:
            Dict[str, Any]: Словарь с данными date объекта
        """

        if not self.__can_convert(obj):
            return {'value': obj, 'type': 'other'}
        
        return self.__convert_date(obj)

    def __can_convert(self, obj: Any) -> bool:

        """ Проверяет, является ли объект date типом """

        return isinstance(obj, date)

    def __convert_date(self, dt_obj: Any) -> Dict[str, date]:

        if isinstance(dt_obj, date):
            return {
                'type': 'date', 
                'year': dt_obj.year,
                'month': dt_obj.month,
                'day': dt_obj.day,
                'iso_format': dt_obj.isoformat()
            }