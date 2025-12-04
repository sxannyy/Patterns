from typing import Any
from Src.Core.abstract_logic import abstract_logic
from Src.Core.observe_service import observe_service
from Src.Core.event_type import event_type
from Src.Core.validator import argument_exception
from Src.reposity import reposity

class reference_observer(abstract_logic):
    """
    Наблюдатель для обработки операций со справочниками:
    - Проверяет зависимости при удалении
    - Обновляет связанные объекты при изменении
    - Инициирует пересчет остатков
    """

    def __init__(self, repo: reposity, start_service, settings_manager):
        """
        Инициализация наблюдателя
        
        Аргументы:
            repo (reposity): Репозиторий данных
            start_service: Сервис инициализации
            settings_manager: Менеджер настроек
        """
        super().__init__()
        self.__repo = repo
        observe_service.add(self)

    def __check_nomenclature_usage(self, nomenclature_code: str) -> list:
        """
        Проверяет использование номенклатуры в рецептах и транзакциях
        
        Аргументы:
            nomenclature_code (str): Код номенклатуры
            
        Возвращает:
            list: Список объектов, использующих номенклатуру
        """
        used_in = []
        
        # Проверяем рецепты
        recipes = self.__repo.data.get(reposity.recipe_key(), {})
        for recipe_code, recipe in recipes.items():
            if hasattr(recipe, 'ingredients'):
                for ingredient in recipe.ingredients:
                    nom = ingredient[0] if isinstance(ingredient, (list, tuple)) else ingredient
                    if hasattr(nom, 'unique_code') and nom.unique_code == nomenclature_code:
                        used_in.append(f"Рецепт: {recipe.name}")
                        break
        
        # Проверяем транзакции
        transactions = self.__repo.data.get(reposity.transaction_key(), {})
        for transaction_code, transaction in transactions.items():
            if (hasattr(transaction, 'nomenclature') and 
                hasattr(transaction.nomenclature, 'unique_code') and 
                transaction.nomenclature.unique_code == nomenclature_code):
                used_in.append(f"Транзакция: {transaction.name}")
        
        # Проверяем остатки
        balances = self.__repo.data.get(reposity.balance_key(), {})
        for balance_key, balance in balances.items():
            if (hasattr(balance, 'nomenclature') and 
                hasattr(balance.nomenclature, 'unique_code') and 
                balance.nomenclature.unique_code == nomenclature_code):
                used_in.append(f"Остаток: {balance.nomenclature.name}")
        
        return used_in

    def __check_measure_usage(self, measure_code: str) -> list:
        """
        Проверяет использование единицы измерения в номенклатуре и транзакциях
        """
        used_in = []
        
        # Проверяем номенклатуру
        nomenclatures = self.__repo.data.get(reposity.nomenclature_key(), {})
        for nom_code, nomenclature in nomenclatures.items():
            if (hasattr(nomenclature, 'measure') and 
                hasattr(nomenclature.measure, 'unique_code') and 
                nomenclature.measure.unique_code == measure_code):
                used_in.append(f"Номенклатура: {nomenclature.name}")
        
        # Проверяем транзакции
        transactions = self.__repo.data.get(reposity.transaction_key(), {})
        for transaction_code, transaction in transactions.items():
            if (hasattr(transaction, 'measure') and 
                hasattr(transaction.measure, 'unique_code') and 
                transaction.measure.unique_code == measure_code):
                used_in.append(f"Транзакция: {transaction.name}")
        
        return used_in

    def __check_group_usage(self, group_code: str) -> list:
        """
        Проверяет использование группы номенклатуры
        """
        used_in = []
        
        # Проверяем номенклатуру
        nomenclatures = self.__repo.data.get(reposity.nomenclature_key(), {})
        for nom_code, nomenclature in nomenclatures.items():
            if (hasattr(nomenclature, 'nomenclature_group') and 
                hasattr(nomenclature.nomenclature_group, 'unique_code') and 
                nomenclature.nomenclature_group.unique_code == group_code):
                used_in.append(f"Номенклатура: {nomenclature.name}")
        
        return used_in

    def __check_storage_usage(self, storage_code: str) -> list:
        """
        Проверяет использование склада в транзакциях и остатках
        """
        used_in = []
        
        # Проверяем транзакции
        transactions = self.__repo.data.get(reposity.transaction_key(), {})
        for transaction_code, transaction in transactions.items():
            if (hasattr(transaction, 'storage') and 
                hasattr(transaction.storage, 'unique_code') and 
                transaction.storage.unique_code == storage_code):
                used_in.append(f"Транзакция: {transaction.name}")
        
        # Проверяем остатки
        balances = self.__repo.data.get(reposity.balance_key(), {})
        for balance_key, balance in balances.items():
            if (hasattr(balance, 'storage') and 
                hasattr(balance.storage, 'unique_code') and 
                balance.storage.unique_code == storage_code):
                used_in.append(f"Остаток: {balance.storage.name}")
        
        return used_in

    def __update_references_in_recipes(self, reference_type: str, old_item: Any, new_item: Any):
        """
        Обновляет ссылки в рецептах при изменении справочника
        """
        recipes = self.__repo.data.get(reposity.recipe_key(), {})
        
        for recipe_code, recipe in recipes.items():
            if hasattr(recipe, 'ingredients'):
                updated = False
                new_ingredients = []
                
                for ingredient in recipe.ingredients:
                    if isinstance(ingredient, (list, tuple)) and len(ingredient) >= 2:
                        nom = ingredient[0]
                        quantity = ingredient[1]
                        
                        # Обновляем номенклатуру если изменилась
                        if (reference_type == "nomenclature" and 
                            hasattr(nom, 'unique_code') and 
                            nom.unique_code == getattr(old_item, 'unique_code', None)):
                            new_ingredients.append((new_item, quantity))
                            updated = True
                        else:
                            new_ingredients.append(ingredient)
                    else:
                        new_ingredients.append(ingredient)
                
                if updated:
                    recipe.ingredients = new_ingredients

    def handle(self, event: str, params: dict):
        """
        Обработка событий
        
        Аргументы:
            event (str): Тип события
            params (dict): Параметры события
        """
        super().handle(event, params)

        # Обработка события перед удалением
        if event == event_type.deleting_reference():
            reference_type = params.get("type")
            unique_code = params.get("unique_code")
            item = params.get("item")
            
            used_in = []
            
            # Проверяем использование в зависимости от типа справочника
            if reference_type == "nomenclature":
                used_in = self.__check_nomenclature_usage(unique_code)
            elif reference_type == "measure":
                used_in = self.__check_measure_usage(unique_code)
            elif reference_type == "nomenclature_group":
                used_in = self.__check_group_usage(unique_code)
            elif reference_type == "storage":
                used_in = self.__check_storage_usage(unique_code)
            
            # Если есть зависимости, блокируем удаление
            if used_in:
                usage_list = "\n- " + "\n- ".join(used_in)
                raise argument_exception(
                    f"Невозможно удалить {reference_type}. Используется в:\n{usage_list}"
                )

        # Обработка события изменения справочника
        elif event == event_type.change_reference():
            reference_type = params.get("type")
            item = params.get("item")
            old_item = params.get("old_item")
            changes = params.get("changes", {})
            
            # Обновляем ссылки в рецептах при изменении номенклатуры
            if reference_type == "nomenclature" and old_item:
                self.__update_references_in_recipes(reference_type, old_item, item)
            
            # Обновляем ссылки в транзакциях при изменении склада
            if reference_type == "storage" and old_item:
                transactions = self.__repo.data.get(reposity.transaction_key(), {})
                for transaction_code, transaction in transactions.items():
                    if (hasattr(transaction, 'storage') and 
                        hasattr(transaction.storage, 'unique_code') and 
                        transaction.storage.unique_code == getattr(old_item, 'unique_code', None)):
                        transaction.storage = item

        # Обработка события конвертации в JSON (логирование)
        elif event == event_type.convert_to_json():
            # Логируем операции для отладки
            action = params.get("action")
            reference_type = params.get("type")
            print(f"Операция {action} выполнена для {reference_type}")