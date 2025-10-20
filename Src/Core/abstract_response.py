import abc
from Src.Core.validator import validator
from Src.Core.validator import operation_exception

# Aбстрактный класс для формирования ответов
class abstract_response(abc.ABC):

    # Cформировать нужный ответ
    @abc.abstractmethod
    def create(self, format: str, data: list) -> str:
        validator.validate(format, str)
        validator.validate(data, list)

        if len(data) == 0:
            raise operation_exception("Нет данных!")

        return f""