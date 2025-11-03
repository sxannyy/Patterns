from Src.Core.abstract_dto import abstract_dto

class storage_dto(abstract_dto):
    """
    Транспортный объект (DTO) для передачи данных о складе между слоями приложения.
    
    Содержит основные атрибуты склада для сериализации и передачи данных.
    Наследует от abstract_dto базовые поля: id, name, unique_code.
    """
    
    # Приватные поля DTO
    __name: str = ""       # Наименование склада
    __address: str = ""    # Адрес склада

    @property
    def name(self) -> str:
        """Возвращает наименование склада"""
        return self.__name
    
    @name.setter
    def name(self, value: str):
        """
        Устанавливает наименование склада.
        
        Аргументы:
            value (str): Наименование склада
        """
        self.__name = value

    @property
    def address(self) -> str:
        """Возвращает адрес склада"""
        return self.__address
    
    @address.setter
    def address(self, value: str):
        """
        Устанавливает адрес склада.
        
        Аргументы:
            value (str): Адрес склада
        """
        self.__address = value