from typing import Any, Dict, List
from Src.Core.abstract_logic import abstract_logic
from Src.Core.observe_service import observe_service
from Src.Core.event_type import event_type
from Src.Core.validator import argument_exception
from Src.reposity import reposity
from Src.Dto.reference_event_dto import reference_event_dto
from Src.Logics.nomenclature_usage_service import nomenclature_usage_service
from Src.Logics.measure_usage_service import measure_usage_service
from Src.Logics.nomenclature_group_usage_service import nomenclature_group_usage_service
from Src.Logics.storage_usage_service import storage_usage_service

class reference_observer(abstract_logic):
    """
    Наблюдатель для обработки операций со справочниками:
    - Проверяет зависимости при удалении
    - Обновляет связанные объекты при изменении
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

        # Сервисы проверки использования справочников
        self.__nomenclature_usage_service = nomenclature_usage_service(repo)
        self.__measure_usage_service = measure_usage_service(repo)
        self.__group_usage_service = nomenclature_group_usage_service(repo)
        self.__storage_usage_service = storage_usage_service(repo)

        #  Тип справочника и функция, возвращающая список мест использования
        self.__usage_handlers: Dict[str, Any[[str], List[str]]] = {
            "nomenclature": self.__nomenclature_usage_service.get_usage,
            "measure": self.__measure_usage_service.get_usage,
            "nomenclature_group": self.__group_usage_service.get_usage,
            "storage": self.__storage_usage_service.get_usage,
        }

        self.__event_handlers: Dict[str, Any[[reference_event_dto], None]] = {
            event_type.deleting_reference(): self.__handle_deleting_reference,
            event_type.change_reference(): self.__handle_change_reference,
            event_type.convert_to_json(): self.__handle_convert_to_json,
        }

        observe_service.add(self)

    def __update_references_in_recipes(
        self, reference_type: str, old_item: Any, new_item: Any):
        """
        Обновляет ссылки в рецептах при изменении справочника
        """
        recipes = self.__repo.data.get(reposity.recipe_key(), {})

        for recipe_code, recipe in recipes.items():
            if hasattr(recipe, "ingredients"):
                updated = False
                new_ingredients = []

                for ingredient in recipe.ingredients:
                    if isinstance(ingredient, (list, tuple)) and len(ingredient) >= 2:
                        nom = ingredient[0]
                        quantity = ingredient[1]

                        # Обновляем номенклатуру если изменилась
                        if (
                            reference_type == "nomenclature"
                            and hasattr(nom, "unique_code")
                            and nom.unique_code
                            == getattr(old_item, "unique_code", None)
                        ):
                            new_ingredients.append((new_item, quantity))
                            updated = True
                        else:
                            new_ingredients.append(ingredient)
                    else:
                        new_ingredients.append(ingredient)

                if updated:
                    recipe.ingredients = new_ingredients

    def __handle_deleting_reference(self, params: reference_event_dto) -> None:
        """
        Обработка события перед удалением элемента справочника
        """
        reference_type = params.reference_type
        unique_code = params.unique_code

        used_in: List[str] = []

        usage_handler = self.__usage_handlers.get(reference_type)
        if usage_handler is not None and unique_code is not None:
            used_in = usage_handler(unique_code)

        # Если есть зависимости, блокируем удаление
        if used_in:
            usage_list = "\n- " + "\n- ".join(used_in)
            raise argument_exception(
                f"Невозможно удалить {reference_type}. Используется в:\n{usage_list}"
            )

    def __handle_change_reference(self, params: reference_event_dto) -> None:
        """
        Обработка события изменения справочника
        """
        reference_type = params.reference_type
        item = params.item
        old_item = params.old_item

        # Обновляем ссылки в рецептах при изменении номенклатуры
        if reference_type == "nomenclature" and old_item:
            self.__update_references_in_recipes(reference_type, old_item, item)

        # Обновляем ссылки в транзакциях при изменении склада
        if reference_type == "storage" and old_item:
            transactions = self.__repo.data.get(reposity.transaction_key(), {})
            for transaction_code, transaction in transactions.items():
                if (
                    hasattr(transaction, "storage")
                    and hasattr(transaction.storage, "unique_code")
                    and transaction.storage.unique_code
                    == getattr(old_item, "unique_code", None)
                ):
                    transaction.storage = item

    def __handle_convert_to_json(self, params: reference_event_dto) -> None:
        """
        Обработка события конвертации в JSON
        """
        return

    def handle(self, event: str, params: reference_event_dto):
        """
        Через __event_handlers делегирует обработку
        соответствующей функции по типу события.
        """
        super().handle(event, params)

        handler = self.__event_handlers.get(event)
        if handler is not None:
            handler(params)