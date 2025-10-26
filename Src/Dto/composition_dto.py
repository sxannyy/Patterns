from Src.Core.abstract_dto import abstract_dto

class composition_dto(abstract_dto):

    """
    DTO для представления состава/композиции.
    Используется для передачи данных о составе между слоями приложения.
    """
    
    # Приватные поля класса с значениями по умолчанию
    __nomenclature_id: str = ""      # ID номенклатуры
    __range_id: str = ""             # ID диапазона/ассортимента
    __value: int = 1                 # Значение/количество (по умолчанию 1)

    # Свойство для доступа к nomenclature_id
    @property
    def nomenclature_id(self) -> str:
        """Возвращает ID номенклатуры"""
        return self.__nomenclature_id

    @nomenclature_id.setter
    def nomenclature_id(self, value):
        """Устанавливает ID номенклатуры"""
        self.__nomenclature_id = value

    # Свойство для доступа к range_id
    @property
    def range_id(self) -> str:
        """Возвращает ID диапазона/ассортимента"""
        return self.__range_id

    @range_id.setter
    def range_id(self, value):
        """Устанавливает ID диапазона/ассортимента"""
        self.__range_id = value

    # Свойство для доступа к value
    @property
    def value(self) -> int:
        """Возвращает значение/количество"""
        return self.__value    
    
    @value.setter
    def value(self, value):
        """Устанавливает значение/количество"""
        self.__value = value