from Src.Core.abstract_model import abstract_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.measure_model import measure_model
from Src.Dto.osv_unit_dto import osv_unit_dto
from Src.Core.validator import validator

class osv_unit_model(abstract_model):
    """
    Модель строки оборотно-сальдовой ведомости.
    Представляет собой одну строку отчета ОСВ с данными по номенклатуре.
    Наследует от abstract_model (поля id, name, unique_code).
    """
    
    # Приватные поля модели
    __nomenclature: nomenclature_model      # Номенклатура
    __measure: measure_model                # Единица измерения
    __start_balance: float                  # Начальный остаток
    __income: float                         # Приход за период
    __outcome: float                        # Расход за период
    __end_balance: float                    # Конечный остаток

    @property
    def nomenclature(self) -> nomenclature_model:
        """Возвращает номенклатуру"""
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        """Устанавливает номенклатуру с валидацией типа"""
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    @property
    def measure(self) -> measure_model:
        """Возвращает единицу измерения"""
        return self.__measure
    
    @measure.setter
    def measure(self, value: measure_model):
        """Устанавливает единицу измерения с валидацией типа"""
        validator.validate(value, measure_model)
        self.__measure = value

    @property
    def start_balance(self) -> float:
        """Возвращает начальный остаток"""
        return self.__start_balance
    
    @start_balance.setter
    def start_balance(self, value: float):
        """Устанавливает начальный остаток с валидацией типа"""
        validator.validate(value, float)
        self.__start_balance = value

    @property
    def income(self) -> float:
        """Возвращает приход за период"""
        return self.__income
    
    @income.setter
    def income(self, value: float):
        """Устанавливает приход с валидацией типа"""
        validator.validate(value, float)
        self.__income = value

    @property
    def outcome(self) -> float:
        """Возвращает расход за период"""
        return self.__outcome
    
    @outcome.setter
    def outcome(self, value: float):
        """Устанавливает расход с валидацией типа"""
        validator.validate(value, float)
        self.__outcome = value

    @property
    def end_balance(self) -> float:
        """Возвращает конечный остаток"""
        return self.__end_balance
    
    @end_balance.setter
    def end_balance(self, value: float):
        """Устанавливает конечный остаток с валидацией типа"""
        validator.validate(value, float)
        self.__end_balance = value

    # Фабричный метод
    @staticmethod
    def create(nomenclature: nomenclature_model, measure: measure_model, 
               start_balance: float, income: float, outcome: float, end_balance: float) -> 'osv_unit_model':
        """
        Фабричный метод для создания строки ОСВ.
        Аргументы:
            nomenclature (nomenclature_model): Номенклатура
            unit (measure_unit_model): Единица измерения
            start_balance (float): Начальный остаток
            income (float): Приход за период
            outcome (float): Расход за период
            end_balance (float): Конечный остаток
        Возвращает:
            osv_unit_model: Созданная строка ОСВ
        """
        validator.validate(nomenclature, nomenclature_model)
        validator.validate(measure, measure_model)
        validator.validate(start_balance, float)
        validator.validate(income, float)
        validator.validate(outcome, float)
        validator.validate(end_balance, float)
        
        item = osv_unit_model()
        item.nomenclature = nomenclature
        item.measure = measure
        item.start_balance = start_balance
        item.income = income
        item.outcome = outcome
        item.end_balance = end_balance
        return item
    
    @staticmethod
    def create_default(nomenclature:nomenclature_model, measure: measure_model):
        item = osv_unit_model()
        item.measure = measure
        item.nomenclature = nomenclature
        item.start_balance = 0.0
        item.end_balance = 0.0
        item.income = 0.0
        item.outcome = 0.0
        return item


    def to_dto(self) -> osv_unit_dto:
        """
        Преобразует osv_unit_model в osv_unit_dto для передачи данных.
        """
        dto = osv_unit_dto()
        dto.id = self.unique_code
        dto.name = self.name if hasattr(self, 'name') else f"OSV_Unit_{self.unique_code}"
        dto.nomenclature_id = self.nomenclature.unique_code if self.nomenclature else None
        dto.nomenclature_name = self.nomenclature.name if self.nomenclature else ""
        dto.measure_id = self.measure.unique_code if self.measure else None
        dto.measure_name = self.measure.name if self.measure else ""
        dto.start_balance = self.start_balance
        dto.income = self.income
        dto.outcome = self.outcome
        dto.end_balance = self.end_balance
        return dto