from typing import List
from Src.reposity import reposity

class nomenclature_usage_service:
    """
    Сервис проверки использования номенклатуры в рецептах, транзакциях и остатках.
    """

    def __init__(self, repo: reposity):
        self.__repo = repo

    def get_usage(self, nomenclature_code: str) -> List[str]:
        used_in: List[str] = []

        # Проверяем рецепты
        recipes = self.__repo.data.get(reposity.recipe_key(), {})
        for recipe_code, recipe in recipes.items():
            if hasattr(recipe, "ingredients"):
                for ingredient in recipe.ingredients:
                    nom = (
                        ingredient[0]
                        if isinstance(ingredient, (list, tuple))
                        else ingredient
                    )
                    if (
                        hasattr(nom, "unique_code")
                        and nom.unique_code == nomenclature_code
                    ):
                        used_in.append(f"Рецепт: {recipe.name}")
                        break

        # Проверяем транзакции
        transactions = self.__repo.data.get(reposity.transaction_key(), {})
        for transaction_code, transaction in transactions.items():
            if (
                hasattr(transaction, "nomenclature")
                and hasattr(transaction.nomenclature, "unique_code")
                and transaction.nomenclature.unique_code == nomenclature_code
            ):
                used_in.append(f"Транзакция: {transaction.name}")

        # Проверяем остатки
        balances = self.__repo.data.get(reposity.balance_key(), {})
        for balance_key, balance in balances.items():
            if (
                hasattr(balance, "nomenclature")
                and hasattr(balance.nomenclature, "unique_code")
                and balance.nomenclature.unique_code == nomenclature_code
            ):
                used_in.append(f"Остаток: {balance.nomenclature.name}")

        return used_in