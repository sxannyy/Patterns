from Src.Core.abstract_dto import abstract_dto
from datetime import datetime
from typing import List, Dict

from Src.Models.storage_model import storage_model

class osv_dto(abstract_dto):
    
    """
    DTO объект для передачи данных оборотно-сальдовой ведомости.
    Используется для сериализации/десериализации данных ОСВ.
    """

    __start_date: datetime = None
    __end_date: datetime = None
    __storage: storage_model = None
    __rows: List[Dict] = []

    @property
    def start_date(self) -> datetime:
        """Возвращает дату начала периода"""
        return self.__start_date
    
    @start_date.setter
    def start_date(self, value: datetime):
        """Устанавливает дату начала периода"""
        self.__start_date = value

    @property
    def end_date(self) -> datetime:
        """Возвращает дату окончания периода"""
        return self.__end_date
    
    @end_date.setter
    def end_date(self, value: datetime):
        self.__end_date = value

    @property
    def storage(self) -> storage_model:
        """Возвращает название склада"""
        return self.__storage
    
    @storage.setter
    def storage(self, value: storage_model):
        """Устанавливает название склада"""
        self.__storage = value

    @property
    def rows(self) -> List[Dict]:
        """Возвращает список строк отчета"""
        return self.__rows
    
    @rows.setter
    def rows(self, value: List[Dict]):
        """Устанавливает список строк отчета"""
        self.__rows = value