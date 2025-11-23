from datetime import datetime
from typing import List
from Src.Core.abstract_model import abstract_model
from Src.Dto.filter_dto import filter_dto
from Src.Logics.prototype_report import prototype_report
from Src.Models.balance_model import balance_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Core.validator import operation_exception, validator
from Src.Models.osv_model import osv_model
from Src.Models.osv_unit_model import osv_unit_model
from Src.Models.storage_model import storage_model
from Src.Models.transaction_model import transaction_model

class osv_builder(abstract_model):

    __start_date: datetime
    __end_date: datetime
    __storage: storage_model
    __rows: List[osv_unit_model]

    def __init__(self, osv: osv_model):
        self.__start_date = osv.start_date
        self.__end_date = osv.end_date
        self.__storage = osv.storage
        self.__rows: List[osv_unit_model] = []

    @property
    def start_date(self) -> datetime:
        """Возвращает дату начала отчетного периода"""
        return self.__start_date

    @start_date.setter
    def start_date(self, start_date: datetime):
        """
        Устанавливает дату начала периода с валидацией типа данных.
        
        Аргументы:
            start_date (datetime): Дата начала отчетного периода
            
        Ошибки:
            Validation error: Если переданный параметр не является datetime
        """
        validator.validate(start_date, datetime)
        self.__start_date = start_date

    @property
    def end_date(self) -> datetime:
        """Возвращает дату окончания отчетного периода"""
        return self.__end_date
        
    @end_date.setter
    def end_date(self, end_date: datetime):
        """
        Устанавливает дату окончания периода с валидацией типа данных.
        
        Аргументы:
            end_date (datetime): Дата окончания отчетного периода
            
        Ошибки:
            Validation error: Если переданный параметр не является datetime
        """
        validator.validate(end_date, datetime)
        self.__end_date = end_date

    @property
    def storage(self) -> storage_model:
        """Возвращает объект склада, для которого формируется ведомость"""
        return self.__storage
        
    @storage.setter
    def storage(self, storage: storage_model):
        """
        Устанавливает склад для ведомости с валидацией типа данных.
        
        Аргументы:
            storage (storage_model): Объект склада
            
        Ошибки:
            Validation error: Если переданный параметр не является storage_model
        """
        validator.validate(storage, storage_model)
        self.__storage = storage

    @property
    def rows(self) -> List[osv_unit_model]:
        """Возвращает список строк оборотно-сальдовой ведомости"""
        return self.__rows
        
    @rows.setter
    def rows(self, rows: List[osv_unit_model]):
        """
        Устанавливает список строк ведомости с валидацией типа данных.
        
        Аргументы:
            rows (List[osv_unit_model]): Список строк отчета ОСВ
            
        Ошибки:
            Validation error: Если параметр не является списком или элементы не osv_unit_model
        """
        validator.validate(rows, list)
        for row in rows:
            validator.validate(row, osv_unit_model)
        self.__rows = rows

    def find_row(self, nomenclature):
        """
        Находит строку ведомости по номенклатуре.
        
        Аргументы:
            nomenclature: Номенклатура для поиска
            
        Возвращает:
            osv_unit_model: Найденная строка ведомости
            
        Ошибки:
            operation_exception: Если строка с указанной номенклатурой не найдена
        """
        # Итерируем по всем строкам ведомости
        for item in self.__rows:
            if item.nomenclature == nomenclature:
                return item
        # Если не найдено - генерируем исключение
        raise operation_exception("Элемент ОСВ не найден!")

    def generate_rows(
        self,
        transactions: dict[str, transaction_model],
        nomenclatures: dict[str, nomenclature_model],
        balance_cache: dict[str, balance_model] | None = None,
        block_date: datetime | None = None
    ):
        """
        Генерирует строки ведомости на основе транзакций и справочника номенклатур.

        Алгоритм:
        1. Фильтрация транзакций по складу
        2. Разделение транзакций на периоды:
           - часть, которая попадает в начальный остаток
           - часть, которая попадает в обороты за период
        3. Для каждой номенклатуры рассчитываются:
           - Остаток на начало периода (с учетом кэша, если задан block_date)
           - Обороты за период (приход и расход)
           - Остаток на конец периода

        Аргументы:
            transactions: Все транзакции (dict[unique_code -> transaction_model])
            nomenclatures: Все номенклатуры (dict[name/код -> nomenclature_model])
            balance_cache: Кэш остатков на дату block_date.
                Ключ: "<storage.unique_code>:<nomenclature.unique_code>"
            block_date: Дата блокировки кэша.
                Если None — кэш не используется.
        """

        # Валидация входных данных
        validator.validate(transactions, dict)
        validator.validate(nomenclatures, dict)

        if block_date is not None:
            validator.validate(block_date, datetime)
        if balance_cache is not None:
            validator.validate(balance_cache, dict)

        # Есть ли вообще кэш?
        use_cache = balance_cache is not None and block_date is not None

        # 1. Прототипы для работы с фильтрами
        transactions_prototype = prototype_report(transactions)

        # 2. Фильтруем транзакции по складу
        filter_storage = filter_dto().create(
            {
                "filter_name": "storage.name",
                "value": self.__storage.name,
                "type": "EQUALS",
            }
        )
        transactions_by_storage = transactions_prototype.filter(
            transactions_prototype,
            filter_storage,
        )

        # --- 3. Определяем эффективную дату начала оборотов ---
        # Если есть block_date, то обороты считаем с max(start_date, block_date)
        if use_cache:
            effective_start = max(self.__start_date, block_date)
            date_from_for_start = block_date
        else:
            # Без кэша — всё, как раньше: начиная "с начала времён"
            effective_start = self.__start_date
            date_from_for_start = datetime.min

        # Транзакции, которые попадут в начальный остаток:
        # - если есть кэш: [block_date; effective_start)
        # - если нет кэша: [datetime.min; start_date)
        filter_before_period = filter_dto().create(
            {
                "filter_name": "date",
                "value": (date_from_for_start, effective_start),
                "type": "IN_RANGE",
            }
        )
        transactions_before_period = transactions_by_storage.filter(
            transactions_by_storage,
            filter_before_period,
        )

        # Транзакции, которые попадут в обороты за период:
        # всегда [effective_start; end_date]
        filter_in_period = filter_dto().create(
            {
                "filter_name": "date",
                "value": (effective_start, self.__end_date),
                "type": "IN_RANGE",
            }
        )
        transactions_in_period = transactions_by_storage.filter(
            transactions_by_storage,
            filter_in_period,
        )

        # 4. Формируем строки ОСВ по каждой номенклатуре
        self.__rows = []

        for nomenclature in nomenclatures.values():
            # Фильтры по номенклатуре
            filter_nomenclature = filter_dto().create(
                {
                    "filter_name": "nomenclature",
                    "value": nomenclature,
                    "type": "EQUALS",
                }
            )

            nomenclature_before = transactions_before_period.filter(
                transactions_before_period,
                filter_nomenclature,
            )
            nomenclature_in_period = transactions_in_period.filter(
                transactions_in_period,
                filter_nomenclature,
            )

            # Строка ОСВ в базовой единице измерения номенклатуры
            base_measure = (
                nomenclature.measure.base_measure or nomenclature.measure
            )
            osv_row = osv_unit_model.create_default(
                nomenclature,
                base_measure,
            )

            # --- 4.1. Начальный остаток с учетом кэша и транзакций до effective_start ---
            start_balance = 0.0

            if use_cache:
                cache_key = f"{self.__storage.unique_code}:{nomenclature.unique_code}"
                balance_item = balance_cache.get(cache_key)

                if isinstance(balance_item, balance_model):
                    cached_balance = balance_item.end_balance

                    # На всякий случай приводим к мере строки, если они отличаются
                    if balance_item.measure != osv_row.measure:
                        if (
                            balance_item.measure.base_measure
                            and balance_item.measure.base_measure == osv_row.measure
                        ):
                            cached_balance *= balance_item.measure.conversion_factor
                        elif (
                            osv_row.measure.base_measure
                            and osv_row.measure.base_measure == balance_item.measure
                        ):
                            cached_balance /= osv_row.measure.conversion_factor

                    start_balance += cached_balance

            # Добавляем операции до effective_start
            for transaction in nomenclature_before.data:
                quantity = transaction.quantity

                # Приводим к базовой единице
                if (
                    transaction.measure.base_measure
                    and transaction.measure.base_measure == osv_row.measure
                ):
                    quantity *= transaction.measure.conversion_factor

                start_balance += quantity

            # --- 4.2. Обороты за период ---
            income = 0.0
            outcome = 0.0

            for transaction in nomenclature_in_period.data:
                quantity = transaction.quantity

                # Приводим к базовой единице
                if (
                    transaction.measure.base_measure
                    and transaction.measure.base_measure == osv_row.measure
                ):
                    quantity *= transaction.measure.conversion_factor

                if quantity > 0:
                    income += quantity
                else:
                    outcome += abs(quantity)

            # --- 4.3. Заполняем строку ОСВ ---
            osv_row.start_balance = start_balance
            osv_row.income = income
            osv_row.outcome = outcome
            osv_row.end_balance = start_balance + income - outcome

            self.__rows.append(osv_row)
