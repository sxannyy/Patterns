from typing import Any, Dict
from Src.reposity import reposity
from Src.Core.validator import argument_exception, validator
from Src.Core.observe_service import observe_service
from Src.Core.event_type import event_type
from Src.Dto.reference_event_dto import reference_event_dto
from Src.Logics.reference_observer import reference_observer
from Src.start_service import start_service
from Src.settings_manager import settings_manager

class reference_service:
    """
    Универсальный сервис для операций со справочниками:
    - nomenclature (номенклатура)
    - measure (единицы измерения) 
    - nomenclature_group (группы номенклатуры)
    - storage (склады)
    """

    def __init__(self, repo: reposity, start_srv: start_service, settings_mgr: settings_manager):
        """
        Инициализация сервиса справочников
        """
        validator.validate(repo, reposity)
        validator.validate(start_srv, start_service)
        validator.validate(settings_mgr, settings_manager)

        self.__repo = repo
        self.__start_srv = start_srv
        self.__settings_mgr = settings_mgr

        # Регистрируем наблюдателя для пост-обработки операций
        self.__observer = reference_observer(self.__repo, self.__start_srv, self.__settings_mgr)
        observe_service.add(self.__observer)

    def __get_key(self, reference_type: str) -> str:
        """
        Возвращает ключ репозитория для указанного типа справочника
        
        Аргументы:
            reference_type (str): Тип справочника
            
        Возвращает:
            str: Ключ в репозитории
            
        Исключения:
            argument_exception: Если тип справочника не поддерживается
        """
        mapping = {
            "nomenclature": reposity.nomenclature_key(),
            "measure": reposity.measure_key(),
            "nomenclature_group": reposity.nomenclature_group_key(),
            "storage": reposity.storage_key()
        }
        
        if reference_type not in mapping:
            raise argument_exception(f"Неподдерживаемый тип справочника: {reference_type}")
            
        return mapping[reference_type]

    def get_one(self, reference_type: str, unique_code: str) -> Any:
        """
        Получает один элемент справочника по уникальному коду

        Аргументы:
            reference_type (str): Тип справочника
            unique_code (str): Уникальный код элемента

        Возвращает:
            Any: Элемент справочника или None если не найден

        Исключения:
            argument_exception: Если тип справочника не поддерживается
        """
        key = self.__get_key(reference_type)
        collection = self.__repo.data.get(key, {})

        # Сначала пытаемся найти по ключу напрямую
        item = collection.get(unique_code)
        if item is not None:
            return item

        # Если не нашли, ищем в values() по unique_code
        for value in collection.values():
            if hasattr(value, 'unique_code') and value.unique_code == unique_code:
                return value
            elif hasattr(value, 'id') and value.id == unique_code:
                return value

        return None

    def add(self, reference_type: str, item: Dict) -> Any:
        """
        Добавляет новый элемент в справочник
        """
        key = self.__get_key(reference_type)
        collection = self.__repo.data.setdefault(key, {})

        unique_code = item.get('unique_code', None) or item.get('id', None)
        if not unique_code:
            raise argument_exception("Элемент должен иметь уникальный код")

        # Проверяем существование элемента с таким кодом
        existing_item = self.get_one(reference_type, unique_code)
        if existing_item is not None:
            raise argument_exception("Элемент с таким уникальным кодом уже существует")

        collection[unique_code] = item

        # Уведомляем наблюдателей о добавлении
        event_dto = reference_event_dto()
        event_dto.action = "add"
        event_dto.reference_type = reference_type
        event_dto.item = item

        observe_service.create_event(event_type.add_new_reference(), event_dto)

        return item


    def update(self, reference_type: str, unique_code: str, changes: dict) -> Any:
        """
        Обновляет элемент справочника
        """
        key = self.__get_key(reference_type)
        collection = self.__repo.data.get(key, {})

        # Ищем элемент
        item = self.get_one(reference_type, unique_code)
        if item is None:
            raise argument_exception("Элемент не найден")

        old_item = item.__dict__.copy() if hasattr(item, '__dict__') else item.copy()

        # Применяем изменения
        for field, new_value in changes.items():
            if hasattr(item, field):
                setattr(item, field, new_value)
            elif isinstance(item, dict):
                item[field] = new_value

        # Уведомляем наблюдателей об изменении
        event_dto = reference_event_dto()
        event_dto.action = "update"
        event_dto.reference_type = reference_type
        event_dto.item = item
        event_dto.old_item = old_item
        event_dto.changes = changes

        observe_service.create_event(event_type.change_reference(), event_dto)

        # Сохраняем настройки и пересчитываем остатки
        self.__settings_mgr.save_settings()
        current_block = self.__start_srv.block_date
        self.__start_srv.block_date = current_block

        return item

    def delete(self, reference_type: str, unique_code: str) -> bool:
        """
        Удаляет элемент из справочника
        """
        key = self.__get_key(reference_type)
        collection = self.__repo.data.get(key, {})

        # Ищем элемент
        item = self.get_one(reference_type, unique_code)
        if item is None:
            raise argument_exception("Элемент не найден")

        # Находим ключ, по которому хранится элемент
        storage_key = None
        if unique_code in collection:
            storage_key = unique_code
        else:
            # Ищем ключ по значению
            for k, v in collection.items():
                if v == item:
                    storage_key = k
                    break

        if storage_key is None:
            raise argument_exception("Элемент не найден в коллекции")

        # Проверяем использование элемента перед удалением
        before_delete_dto = reference_event_dto()
        before_delete_dto.action = "delete"
        before_delete_dto.reference_type = reference_type
        before_delete_dto.unique_code = unique_code
        before_delete_dto.item = item

        observe_service.create_event(event_type.deleting_reference(), before_delete_dto)

        # Если никто не выбросил исключение, удаляем элемент
        collection.pop(storage_key, None)

        # Уведомляем наблюдателей об удалении
        after_delete_dto = reference_event_dto()
        after_delete_dto.action = "delete"
        after_delete_dto.reference_type = reference_type
        after_delete_dto.unique_code = unique_code
        after_delete_dto.item = item

        observe_service.create_event(event_type.deleted_reference(), after_delete_dto)

        # Сохраняем настройки и пересчитываем остатки
        self.__settings_mgr.save_settings()
        current_block = self.__start_srv.block_date
        self.__start_srv.block_date = current_block

        return True