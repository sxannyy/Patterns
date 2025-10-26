from Src.Core.abstract_dto import abstract_dto

'''
    Модель единицы измерения в DTO
    Пример структуры данных:
        {
            "name":"Грамм",
            "id":"adb7510f-687d-428f-a697-26e53d3f65b7",
            "base_id":null,
            "value":1
        }
'''

class measure_dto(abstract_dto):

    """
    Используется для передачи данных о единицах измерения между слоями приложения.
    """
    
    # Приватные поля класса с значениями по умолчанию
    __base_id: str = None    # ID базовой единицы измерения (может быть None)
    __value: int = 1         # Коэффициент преобразования к базовой единице (по умолчанию 1)

    # Свойство для доступа к base_id
    @property
    def base_id(self) -> str:
        """Возвращает ID базовой единицы измерения"""
        return self.__base_id    
    
    @base_id.setter
    def base_id(self, value):
        """Устанавливает ID базовой единицы измерения"""
        self.__base_id = value

    # Свойство для доступа к value
    @property
    def value(self) -> int:
        """Возвращает коэффициент преобразования к базовой единице"""
        return self.__value    
    
    @value.setter
    def value(self, value):
        """Устанавливает коэффициент преобразования к базовой единице"""
        self.__value = value