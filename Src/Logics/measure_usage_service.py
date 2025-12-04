from typing import List
from Src.reposity import reposity

class measure_usage_service:
    """
    Сервис проверки использования единицы измерения
    """

    def __init__(self, repo: reposity):
        self.__repo = repo

    def get_usage(self, measure_code: str) -> List[str]:
        used_in: List[str] = []

        # Проверяем номенклатуру
        nomenclatures = self.__repo.data.get(reposity.nomenclature_key(), {})
        for nom_code, nomenclature in nomenclatures.items():
            if (
                hasattr(nomenclature, "measure")
                and hasattr(nomenclature.measure, "unique_code")
                and nomenclature.measure.unique_code == measure_code
            ):
                used_in.append(f"Номенклатура: {nomenclature.name}")

        # Проверяем транзакции
        transactions = self.__repo.data.get(reposity.transaction_key(), {})
        for transaction_code, transaction in transactions.items():
            if (
                hasattr(transaction, "measure")
                and hasattr(transaction.measure, "unique_code")
                and transaction.measure.unique_code == measure_code
            ):
                used_in.append(f"Транзакция: {transaction.name}")

        return used_in