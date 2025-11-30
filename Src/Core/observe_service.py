from Src.Core.abstract_logic import abstract_logic

""" 
Сервис для реализации паттерна Наблюдатель.
Позволяет добавлять, удалять и уведомлять о событиях.
"""
class observe_service:

    handlers = []

    """ 
    Добавляет объект в список наблюдателей.
    Аргументы:
        instance: Объект для добавления в наблюдение
    Условия:
        - Объект игнорируется если равен None
        - Объект должен быть унаследован от abstract_logic
        - Объект добавляется только если его еще нет в списке
    """
    @staticmethod
    def add(instance):
        if instance is None: return
        if not isinstance( instance, abstract_logic ): return

        if instance not in  observe_service.handlers:
            observe_service.handlers.append( instance )

    """ 
    Удаляет объект из списка наблюдателей.
    Аргументы:
        instance: Объект для удаления из наблюдения
    Условия:
        - Объект игнорируется если равен None
        - Объект должен быть унаследован от abstract_logic
        - Объект удаляется только если присутствует в списке
    """
    @staticmethod
    def delete(instance):
        if instance is None: return
        if not isinstance( instance, abstract_logic ): return

        if instance in  observe_service.handlers:
            observe_service.handlers.remove( instance )

    """ 
    Создает и рассылает событие всем зарегистрированным наблюдателям.
    Аргументы:
        event (str): Тип события для обработки
        params: Параметры события для передачи обработчикам
    Действие:
        - Каждый наблюдатель получает уведомление через метод handle()
    """
    @staticmethod
    def create_event(  event: str, params ):
        for instance in observe_service.handlers:        
            instance.handle(event, params)