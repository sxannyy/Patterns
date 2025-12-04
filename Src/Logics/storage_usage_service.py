from typing import List
from Src.reposity import reposity

class storage_usage_service:
    """
    Сервис проверки использования склада
    """

    def __init__(self, repo: reposity):
        self.__repo = repo

    def get_usage(self, storage_code: str) -> List[str]:
        used_in: List[str] = []

        # Проверяем транзакции
        transactions = self.__repo.data.get(reposity.transaction_key(), {})
        for transaction_code, transaction in transactions.items():
            if (
                hasattr(transaction, "storage")
                and hasattr(transaction.storage, "unique_code")
                and transaction.storage.unique_code == storage_code
            ):
                used_in.append(f"Транзакция: {transaction.name}")

        # Проверяем остатки
        balances = self.__repo.data.get(reposity.balance_key(), {})
        for balance_key, balance in balances.items():
            if (
                hasattr(balance, "storage")
                and hasattr(balance.storage, "unique_code")
                and balance.storage.unique_code == storage_code
            ):
                used_in.append(f"Остаток: {balance.storage.name}")

        return used_in