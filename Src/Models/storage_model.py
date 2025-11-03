from Src.Core.validator import validator
from Src.Core.abstract_model import abstract_model
from Src.Dto.storage_dto import storage_dto

class storage_model(abstract_model):
    """
    Модель склада в предметной области.
    
    Представляет собой склад для хранения товарно-материальных ценностей.
    Наследует от abstract_model базовые поля: id, name, unique_code.
    """
    
    # Приватные поля модели
    __address: str = ""    # Адрес склада

    @property
    def address(self) -> str:
        """Возвращает адрес склада с удалением лишних пробелов"""
        return self.__address.strip()

    @address.setter
    def address(self, value: str):
        """
        Устанавливает адрес склада с валидацией типа данных и очисткой пробелов.
        
        Аргументы:
            value (str): Адрес склада
            
        Ошибки:
            Validation error: Если переданный параметр не является строкой
        """
        validator.validate(value, str)
        # Удаляем лишние пробелы в начале и конце строки
        self.__address = value.strip()

    def to_dto(self) -> storage_dto:
        """
        Преобразует модель домена storage_model в транспортный объект storage_dto.
        
        Возвращает:
            storage_dto: Транспортный объект для передачи данных между слоями приложения
        """
        dto = storage_dto()
        dto.id = self.unique_code    # Уникальный идентификатор склада
        dto.name = self.name         # Наименование склада
        dto.address = self.address   # Адрес склада
        
        return dto