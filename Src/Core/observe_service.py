from Src.Core.abstract_logic import abstract_logic
from Src.Core.abstract_dto import abstract_dto

""" 
Сервис для реализации паттерна Наблюдатель.
Позволяет добавлять, удалять и уведомлять о событиях.
"""
class observe_service:

    handlers = []

    """ 
    Добавляет объект в список наблюдателей.
    """
    @staticmethod
    def add(instance):
        if instance is None:
            return
        if not isinstance(instance, abstract_logic):
            return

        if instance not in observe_service.handlers:
            observe_service.handlers.append(instance)

    """ 
    Удаляет объект из списка наблюдателей.
    """
    @staticmethod
    def delete(instance):
        if instance is None:
            return
        if not isinstance(instance, abstract_logic):
            return

        if instance in observe_service.handlers:
            observe_service.handlers.remove(instance)

    """ 
    Создает и рассылает событие всем зарегистрированным наблюдателям.
    Аргументы:
        event (str): Тип события для обработки
        params (abstract_dto): Параметры события
    """
    @staticmethod
    def create_event(event: str, params: abstract_dto):
        if params is None:
            return
        if not isinstance(params, abstract_dto):
            return

        for instance in observe_service.handlers:
            instance.handle(event, params)