from Src.Core.abstract_dto import abstract_dto

class osv_unit_dto(abstract_dto):

    """
    DTO для представления строки оборотно-сальдовой ведомости.
    Используется для передачи данных о движении номенклатуры между слоями приложения.
    """
    
    # Приватные поля класса с значениями по умолчанию
    __nomenclature_id: str = ""          # ID номенклатуры
    __nomenclature_name: str = ""        # Название номенклатуры
    __measure_id: str = ""               # ID единицы измерения
    __measure_name: str = ""             # Название единицы измерения
    __start_balance: float = 0.0         # Начальный остаток
    __income: float = 0.0                # Приход за период
    __outcome: float = 0.0               # Расход за период
    __end_balance: float = 0.0           # Конечный остаток

    # Свойство для доступа к nomenclature_id
    @property
    def nomenclature_id(self) -> str:
        """Возвращает ID номенклатуры"""
        return self.__nomenclature_id

    @nomenclature_id.setter
    def nomenclature_id(self, value):
        """Устанавливает ID номенклатуры"""
        self.__nomenclature_id = value

    # Свойство для доступа к nomenclature_name
    @property
    def nomenclature_name(self) -> str:
        """Возвращает название номенклатуры"""
        return self.__nomenclature_name

    @nomenclature_name.setter
    def nomenclature_name(self, value):
        """Устанавливает название номенклатуры"""
        self.__nomenclature_name = value

    # Свойство для доступа к measure_id
    @property
    def measure_id(self) -> str:
        """Возвращает ID единицы измерения"""
        return self.__measure_id

    @measure_id.setter
    def measure_id(self, value):
        """Устанавливает ID единицы измерения"""
        self.__measure_id = value

    # Свойство для доступа к measure_name
    @property
    def measure_name(self) -> str:
        """Возвращает название единицы измерения"""
        return self.__measure_name

    @measure_name.setter
    def measure_name(self, value):
        """Устанавливает название единицы измерения"""
        self.__measure_name = value

    # Свойство для доступа к start_balance
    @property
    def start_balance(self) -> float:
        """Возвращает начальный остаток"""
        return self.__start_balance

    @start_balance.setter
    def start_balance(self, value):
        """Устанавливает начальный остаток"""
        self.__start_balance = value

    # Свойство для доступа к income
    @property
    def income(self) -> float:
        """Возвращает приход за период"""
        return self.__income

    @income.setter
    def income(self, value):
        """Устанавливает приход за период"""
        self.__income = value

    # Свойство для доступа к outcome
    @property
    def outcome(self) -> float:
        """Возвращает расход за период"""
        return self.__outcome

    @outcome.setter
    def outcome(self, value):
        """Устанавливает расход за период"""
        self.__outcome = value

    # Свойство для доступа к end_balance
    @property
    def end_balance(self) -> float:
        """Возвращает конечный остаток"""
        return self.__end_balance

    @end_balance.setter
    def end_balance(self, value):
        """Устанавливает конечный остаток"""
        self.__end_balance = value