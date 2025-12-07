from typing import List
from Src.reposity import reposity

class nomenclature_group_usage_service:
    """
    Сервис проверки использования группы номенклатуры
    """

    def __init__(self, repo: reposity):
        self.__repo = repo

    def get_usage(self, group_code: str) -> List[str]:
        used_in: List[str] = []

        # Проверяем номенклатуру
        nomenclatures = self.__repo.data.get(reposity.nomenclature_key(), {})
        for nom_code, nomenclature in nomenclatures.items():
            if (
                hasattr(nomenclature, "nomenclature_group")
                and hasattr(nomenclature.nomenclature_group, "unique_code")
                and nomenclature.nomenclature_group.unique_code == group_code
            ):
                used_in.append(f"Номенклатура: {nomenclature.name}")

        return used_in