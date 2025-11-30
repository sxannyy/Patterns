from Src.Core.abstract_logic import abstract_logic
from Src.Core.observe_service import observe_service
from Src.Core.event_type import event_type

"""
Сервис для вывода информации в консоль.
Реализует паттерн Наблюдатель для обработки событий приложения.
"""
class print_service(abstract_logic):
    
    def __init__(self):
        """ 
        Инициализирует сервис печати и регистрирует его как наблюдателя.
        Действие:
            - Автоматически добавляет экземпляр в observe_service при создании
        """
        super().__init__()
        observe_service.add(self)

    """ 
    Обрабатывает входящие события от системы наблюдения.
    Аргументы:
        event (str): Тип события для обработки
        params: Данные события для вывода
    Особенности:
        - Вызывает базовую обработку события из abstract_logic
        - При событии convert_to_json выводит параметры в консоль
    """
    def handle(self, event:str, params):
        super().handle(event, params)  
        if event == event_type.convert_to_json():
            print( f"params:{ params } ")