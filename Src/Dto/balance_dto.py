from datetime import datetime
from Src.Core.abstract_dto import abstract_dto

class balance_dto(abstract_dto):

    """
    DTO для представления остатков по номенклатуре.
    Используется для передачи данных об остатках между слоями приложения.
    """

    __nomenclature_id: str = ""             # ID номенклатуры
    __measure_id: str = ""                  # ID единицы измерения
    __storage_id: str = ""                  # ID склада
    __end_balance: float = 0.0              # Конечный остаток
    __block_date: datetime | None = None    # Фиксированная (закрытая) дата

    @property
    def nomenclature_id(self) -> str:
        """Возвращает ID номенклатуры"""
        return self.__nomenclature_id

    @nomenclature_id.setter
    def nomenclature_id(self, value):
        """Устанавливает ID номенклатуры"""
        self.__nomenclature_id = value

    @property
    def measure_id(self) -> str:
        """Возвращает ID единицы измерения"""
        return self.__measure_id

    @measure_id.setter
    def measure_id(self, value):
        """Устанавливает ID единицы измерения"""
        self.__measure_id = value

    @property
    def storage_id(self) -> str:
        """Возвращает ID склада"""
        return self.__storage_id

    @storage_id.setter
    def storage_id(self, value):
        """Устанавливает ID склада"""
        self.__storage_id = value

    @property
    def end_balance(self) -> float:
        """Возвращает конечный остаток"""
        return self.__end_balance

    @end_balance.setter
    def end_balance(self, value):
        """Устанавливает конечный остаток"""
        self.__end_balance = value

    @property
    def block_date(self) -> datetime | None:
        """Возвращает фиксированную (закрытую) дату"""
        return self.__block_date

    @block_date.setter
    def block_date(self, value):
        """Устанавливает фиксированную (закрытую) дату"""
        self.__block_date = value