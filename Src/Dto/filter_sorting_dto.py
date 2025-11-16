from typing import List
from Src.Core.validator import validator
from Src.Dto.filter_dto import filter_dto

class filter_sorting_dto():
    """
    DTO для передачи параметров фильтрации и сортировки.
    Объединяет критерии фильтрации и порядок сортировки в одном объекте.
    Используется для сложных запросов к данным с множественными фильтрами.
    """
    
    __filters: List[filter_dto]  # Список фильтров
    __sorting: List[str]         # Список полей для сортировки

    def __init__(self):
        """Инициализирует DTO с пустыми списками фильтров и сортировки"""
        self.__filters = []
        self.__sorting = []

    @property
    def filters(self) -> List[filter_dto]:
        """Возвращает список фильтров"""
        return self.__filters

    @filters.setter
    def filters(self, value: List[filter_dto]):
        """
        Устанавливает список фильтров
        
        Аргументы:
            value: Список объектов filter_dto
        Ошибки:
            ValueError: Если значение не является списком
        """
        validator.validate(value, list)
        self.__filters = value

    @property
    def sorting(self) -> List[str]:
        """Возвращает список полей для сортировки"""
        return self.__sorting

    @sorting.setter
    def sorting(self, value: List[str]):
        """
        Устанавливает список полей для сортировки
        
        Аргументы:
            value: Список названий полей для сортировки
        Ошибки:
            ValueError: Если значение не является списком
        """
        validator.validate(value, list)
        self.__sorting = value

    def create(self, data) -> "filter_sorting_dto":
        """
        Создает и инициализирует DTO из словаря с данными.
        
        Аргументы:
            data: Словарь с параметрами фильтрации и сортировки в формате:
                {
                    "filters": [
                        {
                            "filter_name": "название_поля",
                            "value": "значение_фильтра", 
                            "type": "тип_операции"
                        }
                    ],
                    "sorting": ["поле_сортировки1", "поле_сортировки2"]
                }
                
        Возвращает:
            filter_sorting_dto: Текущий экземпляр DTO с установленными значениями
            
        Ошибки:
            ValueError: Если переданные данные не являются словарем
            KeyError: Если в фильтрах указан неверный тип операции
        """
        validator.validate(data, dict)

        # Обрабатываем фильтры
        filters_data = data.get("filters", [])
        self.__filters = []
        for filter in filters_data:
            fd = filter_dto().create(filter)
            self.__filters.append(fd)

        # Обрабатываем сортировку
        self.__sorting = data.get("sorting", [])
        return self