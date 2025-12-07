from typing import Any, Dict
from Src.Core.abstract_dto import abstract_dto

"""
DTO для передачи параметров событий справочников
между reference_service, observe_service и reference_observer.
"""

class reference_event_dto(abstract_dto):
    __action: str = ""
    __reference_type: str = ""
    __unique_code: Any = None
    __item: Any = None
    __old_item: Any = None
    __changes: Dict[str, Any] = {}

    @property
    def action(self) -> str:
        return self.__action

    @action.setter
    def action(self, value: str):
        self.__action = value

    @property
    def reference_type(self) -> str:
        return self.__reference_type

    @reference_type.setter
    def reference_type(self, value: str):
        self.__reference_type = value

    @property
    def unique_code(self) -> Any:
        return self.__unique_code

    @unique_code.setter
    def unique_code(self, value: Any):
        self.__unique_code = value

    @property
    def item(self) -> Any:
        return self.__item

    @item.setter
    def item(self, value: Any):
        self.__item = value

    @property
    def old_item(self) -> Any:
        return self.__old_item

    @old_item.setter
    def old_item(self, value: Any):
        self.__old_item = value

    @property
    def changes(self) -> Dict[str, Any]:
        return self.__changes

    @changes.setter
    def changes(self, value: Dict[str, Any]):
        self.__changes = value or {}