from typing import Any, Dict
from Src.Core.abstract_dto import abstract_dto

"""
DTO для передачи параметров события логирования.

Используется совместно с системой событий/наблюдателей для
передачи данных в logger и другие обработчики.

Содержит:
    - текст сообщения
    - словарь дополнительных данных
    - объект исключения (если есть)
"""

class log_event_dto(abstract_dto):
    """ 
    Объект передачи данных для логирования.

    Свойства:
        message (str): текст сообщения лога
        data (Dict[str, Any]): дополнительные данные, связанные с событием
        exception (Any): исключение или любая ошибка, которую нужно зафиксировать
    """

    __message: str = ""
    __data: Dict[str, Any] = None
    __exception: Any = None

    """ 
    Текст сообщения для логирования.
    Свойство:
        str: сообщение лога (по умолчанию пустая строка)
    """
    @property
    def message(self) -> str:
        return self.__message

    @message.setter
    def message(self, value: str):
        """ 
        Устанавливает текст сообщения.

        Аргументы:
            value (str): текст сообщения

        Примечания:
            Если передано None или пустое значение, будет установлена пустая строка.
        """
        self.__message = value or ""

    """ 
    Дополнительные данные, связанные с событием.
    Свойство:
        Dict[str, Any]: словарь данных (по умолчанию пустой словарь)
    """
    @property
    def data(self) -> Dict[str, Any]:
        return self.__data or {}

    @data.setter
    def data(self, value: Dict[str, Any]):
        """ 
        Устанавливает дополнительные данные для лога.

        Аргументы:
            value (Dict[str, Any]): словарь с данными

        Примечания:
            Если передано None, будет установлено пустое значение словаря.
        """
        self.__data = value or {}

    """ 
    Исключение или ошибка, связанная с событием.
    Свойство:
        Any: объект исключения или произвольная ошибка
    """
    @property
    def exception(self) -> Any:
        return self.__exception

    @exception.setter
    def exception(self, value: Any):
        """ 
        Устанавливает объект исключения.

        Аргументы:
            value (Any): исключение или иной объект ошибки

        Примечания:
            Специальная валидация не применяется,
            так как тип исключения может отличаться.
        """
        self.__exception = value