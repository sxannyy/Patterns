import abc
from Src.Core.validator import validator
from Src.Core.validator import operation_exception
from Src.Convertors.convert_factory import convert_factory

# Абстрактный класс для формирования ответов

class abstract_response(abc.ABC):

    def __init__(self):

        """ Инициализирует фабрику конвертеров """

        self._converter = convert_factory()

    # Cформировать нужный ответ
    @abc.abstractmethod
    def create(self, data: list) -> str:
        validator.validate(data, list)
        if len(data) == 0:
            raise operation_exception("Нет данных!")
        return ""