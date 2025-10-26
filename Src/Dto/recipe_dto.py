from Src.Core.abstract_dto import abstract_dto
from typing import List, Dict, Any

class recipe_dto(abstract_dto):
    """
    DTO модель для рецепта.
    Используется для передачи данных о рецепте между слоями приложения.
    Содержит информацию о названии, ингредиентах и шагах приготовления.
    """
    
    __name: str = ""
    __ingredients: List[Dict[str, Any]] = []
    __steps: List[str] = []

    @property
    def name(self) -> str:
        """Название рецепта"""
        return self.__name
    
    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def ingredients(self) -> List[Dict[str, Any]]:
        """Список ингредиентов в формате [{'nomenclature_id': '...', 'quantity': 100}, ...]"""
        return self.__ingredients
    
    @ingredients.setter
    def ingredients(self, value: List[Dict[str, Any]]):
        self.__ingredients = value

    @property
    def steps(self) -> List[str]:
        """Шаги приготовления"""
        return self.__steps
    
    @steps.setter
    def steps(self, value: List[str]):
        self.__steps = value