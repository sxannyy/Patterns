from datetime import date, datetime, time
from Src.Convertors.date_convertor import date_convertor
from Src.Convertors.time_convertor import time_convertor
from Src.Convertors.basic_convertor import basic_convertor
from Src.Convertors.datetime_convertor import datetime_convertor
from Src.Convertors.reference_convertor import reference_convertor
from typing import Any, Dict, List

from Src.Core.abstract_model import abstract_model
from Src.Core.common import common

class convert_factory:

    """
    Фабрика для преобразования объектов любых типов в словари.
    Использует цепочку конвертеров: basic -> datetime -> reference.
    """

    def __init__(self):

        """
        Инициализирует цепочку конвертеров в порядке приоритета.
        """

        self.__converters = {
            # Простые типы (str, int, float, bool, None)
            str: basic_convertor(),
            int: basic_convertor(),
            float: basic_convertor(),
            bool: basic_convertor(),
            None: basic_convertor(),
            # Дата/время (datetime, date, time)  
            datetime: datetime_convertor(), 
            date: date_convertor(),
            time: time_convertor(),   
            # Модели, DTO, объекты
            abstract_model: reference_convertor()
        }

    def convert(self, obj: Any) -> Dict[str, Any]:

        """
        Преобразует любой объект в словарь используя подходящий конвертер.
        Аргументы:
            obj: Любой объект для преобразования
        Возвращает:
            Dict[str, Any]: Словарь с данными объекта
        """

        # Обрабатываем None отдельно
        if obj is None:
            return None
        
        if isinstance(obj, list):
            return self.convert_list(obj)
                
        if isinstance(obj, dict):
            return self.convert_dict(obj)
        
        if type(obj) in self.__converters.keys():
            converter = self.__converters[type(obj)]
            return converter.convert(obj)
            
        if type(obj).__bases__[0] not in self.__converters.keys():

            # Fallback: если ни один конвертер не подошел
            return {
                'value': str(obj),
                'type': 'unknown', 
                'converter': 'factory_fallback',
                'original_type': type(obj).__name__
            }
        
        converter = self.__converters[type(obj).__bases__[0]]
        result = converter.convert(obj)
        if isinstance(converter, reference_convertor):
            fields = common.get_fields(result)
            return {key: self.convert(getattr(result, key)) for key in fields}
        return result

    def convert_list(self, objects: List[Any]) -> List[Dict[str, Any]]:

        """
        Преобразует список объектов в список словарей.
        Аргументы:
            objects: Список объектов для преобразования
        Возвращает:
            List[Dict[str, Any]]: Список преобразованных объектов
        """

        return [self.convert(obj) for obj in objects]

    def convert_dict(self, obj_dict: Dict[Any, Any]) -> Dict[str, Any]:

        """
        Преобразует словарь объектов в словарь преобразованных объектов.
        Аргументы:
            obj_dict: Словарь объектов для преобразования
        Возвращает:
            Dict[str, Any]: Словарь с преобразованными объектами
        """

        return {str(key): self.convert(value) for key, value in obj_dict.items()}